# Стандартные библиотеки
from calendar import month_name
from datetime import datetime, date
from typing import Optional, Tuple, List, Dict

# Сторонние библиотеки
from django.db.models import Avg, Sum, QuerySet
from django.db.models.functions import ExtractMonth, ExtractYear
from django.shortcuts import render, get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import (
    mixins,
    permissions,
    status,
    viewsets,
    exceptions,
    generics,
)
from rest_framework.decorators import action
from rest_framework.response import Response

# Модули текущего проекта
from core.models import (
    DevelopmentPlan,
    EmployeeDevelopmentPlan,
    EmployeeEngagement,
    KeyPeople,
    EmployeeKeyPeople,
    TrainingApplication,
    EmployeeTrainingApplication,
    BusFactor,
    EmployeeBusFactor,
    Grade,
    EmployeeGrade,
    KeySkill,
    EmployeeKeySkill,
    Team,
    EmployeeTeam,
    Position,
    EmployeePosition,
    Competency,
    PositionCompetency,
    TeamPosition,
    EmployeeCompetency,
    Skill,
    EmployeeSkill,
    SkillForCompetency,
    ManagerTeam,
    EmployeeExpectedSkill,
    CompetencyForExpectedSkill,
    Employee,
)
from api.serializers import (
    EmployeeSerializer,
    TimePeriodRequestSerializer,
    TeamMetricsResponseSerializer,
    SkillAssessmentRequestSerializer,
    TeamMetricsRequestSerializer,
    SkillDomenRequestSerializer,
    MetricResponseSerializer,
    CompetencyLevelRequestSerializer,
    EmployeeCompetencySerializer,
    TeamMetricResponseSerializer,
    TeamEmployeeDashboardSerializer,
    CompetencySerializer,
)


class DateConversionMixin:
    def convert_to_date(
        self, start_period: dict, end_period: dict
    ) -> Tuple[date, date]:
        """
        Преобразует периоды (начальный и конечный) в объекты даты.

        Параметры:
        - start_period (dict): Словарь с ключами 'year' (строка) и 'month' (название месяца на английском).
        - end_period (dict): Словарь с ключами 'year' (строка) и 'month' (название месяца на английском).

        Возвращает:
        - Tuple[date, date]: Кортеж с двумя объектами `date` — начальной и конечной датами.
        """
        start_date = datetime.strptime(
            f"{start_period['year']}-{start_period['month']}-15", "%Y-%B-%d"
        ).date()
        end_date = datetime.strptime(
            f"{end_period['year']}-{end_period['month']}-15", "%Y-%B-%d"
        ).date()
        return start_date, end_date


class EmployeesViewSet(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    Обрабатывает запросы для получения списка сотрудников и отдельного сотрудника.
    """

    serializer_class = EmployeeSerializer

    def get_queryset(self) -> QuerySet[Employee]:
        """
        Получает набор сотрудников, относящихся к конкретной команде и менеджеру.
        """
        team_slug = self.kwargs.get('team_slug')
        team = get_object_or_404(Team, slug=team_slug)
        manager = get_object_or_404(ManagerTeam, id=2)

        return Employee.objects.filter(
            teams__team=team, teams__manager=manager
        )


class MetricViewSet(
    DateConversionMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    """
    Обрабатывает запросы для создания метрик по заданным временным периодам.
    """

    serializer_class = TimePeriodRequestSerializer

    def create(self, request, metric_type: str, employee_id: int) -> Response:
        """
        Создает метрики для сотрудника на основе временного периода.

        Параметры:
        - request: объект запроса.
        - metric_type: тип метрики.
        - employee_id: идентификатор сотрудника.

        Возвращает:
        - Response: данные метрик и статус 200 (OK).
        """
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return self.error_response(serializer.errors)

        start_date, end_date = self.convert_to_date(
            serializer.validated_data['startPeriod'],
            serializer.validated_data['endPeriod'],
        )

        model = self.get_metric_model(metric_type)
        if model is None:
            return self.error_response({"error": "Invalid metric type."})

        dashboard, last_performance = self.get_employee_metrics(
            employee_id, model, start_date, end_date
        )
        response_data = {
            "dashboard": dashboard,
            "completionForToday": last_performance,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def get_employee_metrics(
        self, employee_id: int, model: str, start_date: date, end_date: date
    ) -> Tuple[List[dict], str]:
        """
        Получает метрики сотрудника за заданный период.

        Параметры:
        - employee_id: идентификатор сотрудника.
        - model: модель метрики.
        - start_date: дата начала периода.
        - end_date: дата окончания периода.

        Возвращает:
        - dashboard: список метрик по месяцам.
        - last_performance: последняя метрика производительности.
        """
        employee_metrics = model.objects.filter(
            employee__id=employee_id, add_date__range=[start_date, end_date]
        )

        if not employee_metrics.exists():
            return [], "0.00"

        metrics_by_month = self.group_metrics_by_month(employee_metrics)
        dashboard = [
            {
                "period": {"month": month_name[month], "year": year},
                "performance": str(performance),
            }
            for (year, month), performance in metrics_by_month.items()
        ]

        last_performance = (
            dashboard[-1]['performance'] if dashboard else "0.00"
        )
        return dashboard, last_performance

    def group_metrics_by_month(
        self, employee_metrics: QuerySet
    ) -> Dict[Tuple[int, int], float]:
        """
        Группирует метрики по месяцу и вычисляет среднее значение performance_score.

        Параметры:
        - employee_metrics: метрики сотрудника.

        Возвращает:
        - metrics_by_month_dict: словарь с ключом (year, month) и значением среднего performance_score.
        """
        metrics_by_month = (
            employee_metrics.annotate(
                year=ExtractYear('add_date'), month=ExtractMonth('add_date')
            )
            .values('year', 'month')
            .annotate(average_performance=Avg('performance_score'))
            .order_by('year', 'month')
        )

        metrics_by_month_dict = {
            (metric['year'], metric['month']): round(
                metric['average_performance'], 2
            )
            for metric in metrics_by_month
        }

        return metrics_by_month_dict

    def get_metric_model(self, metric_type: str):
        """
        Получает модель метрики по типу.
        """
        return {
            'development_plan': EmployeeDevelopmentPlan,
            'involvement': EmployeeEngagement,
        }.get(metric_type)

    def method_not_allowed_response(self) -> Response:
        """
        Возвращает ответ с ошибкой 405 (Method Not Allowed).
        """
        return Response(
            {"error": "Method not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def error_response(self, errors: dict) -> Response:
        """
        Возвращает ответ с ошибками валидации.
        """
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class TeamCountEmployeeViewSet(
    DateConversionMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    """
    Обрабатывает запросы для получения данных о команде по количеству сотрудников.
    """

    serializer_class = TimePeriodRequestSerializer

    def create(self, request, team_slug: str) -> Response:
        """
        Обрабатывает создание запроса для получения данных команды.

        Параметры:
        - request: объект запроса.
        - team_slug: уникальный слаг команды.

        Возвращает:
        - Response: данные о команде и статус 200 (OK) или сообщение об ошибке.
        """
        if request.method != 'POST':
            return self.method_not_allowed_response()

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            start_date, end_date = self.convert_to_date(
                serializer.validated_data['startPeriod'],
                serializer.validated_data['endPeriod'],
            )
            return self.get_team_employee_data(team_slug, start_date, end_date)

        return self.error_response(serializer.errors)

    def get_team_employee_data(
        self, team_slug: str, start_date: str, end_date: str
    ) -> Response:
        """
        Получает данные о команде, включая количество сотрудников,
        факторы риска и ключевых людей.

        Параметры:
        - team_slug: уникальный слаг команды.
        - start_date: дата начала периода.
        - end_date: дата окончания периода.

        Возвращает:
        - Response: данные о команде и статус 200 (OK) или сообщение об ошибке.
        """
        team = get_object_or_404(EmployeeTeam, team__slug=team_slug)
        employees = team.employee.all()

        number_of_employees = employees.count()
        number_of_bus_factors = EmployeeBusFactor.objects.filter(
            employee__in=employees, add_date__range=[start_date, end_date]
        ).count()
        number_of_key_people = EmployeeKeyPeople.objects.filter(
            employee__in=employees, add_date__range=[start_date, end_date]
        ).count()

        dashboard_data = {
            "period": {
                "month": month_name[start_date.month],
                "year": str(start_date.year),
            },
            "numberOfEmployee": str(number_of_employees),
            "numberOfBusFactor": str(number_of_bus_factors),
            "numberOfKeyPeople": str(number_of_key_people),
        }

        response_serializer = TeamEmployeeDashboardSerializer(
            data=dashboard_data
        )
        if response_serializer.is_valid():
            return Response(
                {"dashboard": [response_serializer.data]},
                status=status.HTTP_200_OK,
            )

        return self.error_response(response_serializer.errors)


class TeamMetricViewSet(
    DateConversionMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    """
    Обрабатывает запросы для получения метрик по команде за заданный временной период.
    """

    serializer_class = TimePeriodRequestSerializer

    def create(self, request, team_slug: str, metric_type: str) -> Response:
        """
        Создает метрики для команды на основе временного периода.

        Параметры:
        - request: объект запроса.
        - team_slug: уникальный слаг команды.
        - metric_type: тип метрики.

        Возвращает:
        - Response: данные метрик и статус 200 (OK) или сообщение об ошибке.
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return self.error_response(serializer.errors)

        start_date, end_date = self.convert_to_date(
            serializer.validated_data['startPeriod'],
            serializer.validated_data['endPeriod'],
        )

        team = get_object_or_404(EmployeeTeam, team__slug=team_slug)
        employees = team.employee.all()
        model = self.get_metric_model(metric_type)

        if model is None:
            return self.error_response({"error": "Invalid metric type."})

        metrics_by_month = self.get_metrics_by_month(
            employees, model, start_date, end_date
        )

        dashboard_data = [
            {
                "period": {"year": year, "month": month_name[month]},
                "performance": str(round(performance / len(employees), 2)),
            }
            for (year, month), performance in metrics_by_month.items()
        ]

        completion_for_today = (
            dashboard_data[-1]['performance'] if dashboard_data else "0.00"
        )
        response_data = {
            "dashboard": dashboard_data,
            "completionForToday": completion_for_today,
        }

        response_serializer = TeamMetricResponseSerializer(data=response_data)
        if response_serializer.is_valid():
            return Response(
                response_serializer.data, status=status.HTTP_200_OK
            )

        return self.error_response(response_serializer.errors)

    def get_metric_model(self, metric_type: str):
        """
        Получает модель метрики на основе типа.
        """
        return {
            'development_plan': EmployeeDevelopmentPlan,
            'involvement': EmployeeEngagement,
        }.get(metric_type)

    def get_metrics_by_month(
        self, employees, model, start_date: str, end_date: str
    ) -> Dict[tuple, float]:
        """
        Получает метрики сотрудников по месяцам.
        """
        metrics_by_month = (
            model.objects.filter(
                employee__in=employees, add_date__range=[start_date, end_date]
            )
            .annotate(
                year=ExtractYear('add_date'), month=ExtractMonth('add_date')
            )
            .values('year', 'month')
            .annotate(total_performance=Sum('performance_score'))
            .order_by('year', 'month')
        )

        metrics_by_month_dict = {
            (metric['year'], metric['month']): metric['total_performance']
            for metric in metrics_by_month
        }
        return metrics_by_month_dict


class TeamIndividualCompetenciesViewSet(
    DateConversionMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    """
    Обрабатывает запросы для получения компетенций сотрудников по домену навыков.
    """

    serializer_class = SkillDomenRequestSerializer

    def create(
        self, request, team_slug: str, employee_id: Optional[int] = None
    ) -> Response:
        """
        Создает запрос на получение компетенций для команды и/или сотрудника.

        Параметры:
        - request: объект запроса.
        - team_slug: уникальный слаг команды.
        - employee_id: (необязательный) ID сотрудника.

        Возвращает:
        - Response: компетенции сотрудников и статус 200 (OK) или сообщение об ошибке.
        """
        if request.method != 'POST':
            return self.method_not_allowed_response()

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            skill_domen = serializer.validated_data['skillDomen']
            team = get_object_or_404(EmployeeTeam, team__slug=team_slug)

            competencies = self.get_competencies(
                team, employee_id, skill_domen
            )

            response_serializer = CompetencySerializer(
                competencies, many=True, context={'skill_domen': skill_domen}
            )
            return Response(
                {"data": response_serializer.data}, status=status.HTTP_200_OK
            )

        return self.error_response(serializer.errors)

    def get_competencies(
        self, team: EmployeeTeam, employee_id: Optional[int], skill_domen: str
    ) -> QuerySet[EmployeeCompetency]:
        """
        Получает компетенции сотрудников по команде и домену навыков.
        """
        filter_kwargs = {
            'employee__teams': team,
            'competency__competency_type': skill_domen,
        }
        if employee_id is not None:
            filter_kwargs['employee__id'] = employee_id

        return EmployeeCompetency.objects.filter(**filter_kwargs)


class CompetencyLevelViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Обрабатывает запросы для получения уровней компетенций сотрудников.
    """

    serializer_class = CompetencyLevelRequestSerializer

    def create(
        self, request, team_slug: str, employee_id: Optional[int] = None
    ) -> Response:
        """
        Создает запрос на получение уровней компетенций для сотрудников в команде.

        Параметры:
        - request: объект запроса.
        - team_slug: уникальный слаг команды.
        - employee_id: (необязательный) ID сотрудника.

        Возвращает:
        - Response: уровни компетенций сотрудников и статус 200 (OK) или сообщение об ошибке.
        """
        if request.method != 'POST':
            return self.method_not_allowed_response()

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return self.error_response(serializer.errors)

        competency_id = serializer.validated_data['competencyId']
        team = get_object_or_404(EmployeeTeam, team__slug=team_slug)

        employees = self.get_employees(team, employee_id)

        employee_competencies = EmployeeCompetency.objects.filter(
            employee__in=employees,
            competency__id=competency_id,
        )

        serializer = EmployeeCompetencySerializer(
            employee_competencies, many=True
        )
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def get_employees(self, team, employee_id):
        return (
            team.employee.filter(id=employee_id)
            if employee_id
            else team.employee.all()
        )

    def method_not_allowed_response(self):
        return Response(
            {"error": "Method not allowed."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def error_response(self, errors):
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


#################################


class SkillAssessmentViewSet(viewsets.ViewSet):
    """
    ViewSet для получения оценки навыков команды и индивидуальных навыков.
    """

    def create(self, request, *args, **kwargs):
        if 'team-skill-assessment' in request.path:
            return self.team_skill_assessment(request)
        elif 'individual-skill-assessment' in request.path:
            return self.individual_skill_assessment(request)
        else:
            return Response(
                {"detail": "Invalid URL"}, status=status.HTTP_404_NOT_FOUND
            )

    def team_skill_assessment(self, request):
        """
        Получение оценки навыков команды.
        """
        serializer = SkillAssessmentRequestSerializer(data=request.data)
        if serializer.is_valid():
            employee_ids = serializer.validated_data['employeeIds']
            skill_domen = serializer.validated_data['skillDomen']
            start_period = serializer.validated_data['startPeriod']
            end_period = serializer.validated_data['endPeriod']

            skills_data = []
            for skill in Skill.objects.filter(domen=skill_domen):
                skill_assessments = EmployeeSkill.objects.filter(
                    employee__in=employee_ids,
                    skill=skill,
                    period__month__gte=start_period['month'],
                    period__year__gte=start_period['year'],
                    period__month__lte=end_period['month'],
                    period__year__lte=end_period['year'],
                )

                avg_assessment = skill_assessments.aggregate(
                    average=Avg('assesment')
                )['average']
                if avg_assessment:
                    skills_data.append(
                        {
                            'skillId': skill.id,
                            'skillName': skill.name,
                            'assesment': avg_assessment,
                        }
                    )

            response_data = [
                {"period": start_period, "skillsData": skills_data}
            ]
            return Response({"data": response_data}, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    def individual_skill_assessment(self, request):
        """
        Получение оценки навыков сотрудника.
        """
        serializer = SkillAssessmentRequestSerializer(data=request.data)
        if serializer.is_valid():
            employee_id = serializer.validated_data['employeeIds'][0]
            skill_domen = serializer.validated_data['skillDomen']
            start_period = serializer.validated_data['startPeriod']
            end_period = serializer.validated_data['endPeriod']

            skills_data = []
            for skill in Skill.objects.filter(domen=skill_domen):

                skill_assessments = EmployeeSkill.objects.filter(
                    employee_id=employee_id,
                    skill=skill,
                    period__month__gte=start_period['month'],
                    period__year__gte=start_period['year'],
                    period__month__lte=end_period['month'],
                    period__year__lte=end_period['year'],
                )

                avg_assessment = skill_assessments.aggregate(
                    average=Avg('assesment')
                )['average']
                if avg_assessment:
                    skills_data.append(
                        {
                            'skillId': skill.id,
                            'skillName': skill.name,
                            'assesment': avg_assessment,
                        }
                    )

            response_data = [
                {"period": start_period, "skillsData": skills_data}
            ]
            return Response({"data": response_data}, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
