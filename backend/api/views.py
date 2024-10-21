from django.shortcuts import render
from django_filters import rest_framework as filters
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework import (
    mixins,
    permissions,
    status,
    viewsets,
    exceptions,
    generics
)
from users.models import (
    ManagerTeam,
)
from core.models import (
    DevelopmentPlan, EmployeeDevelopmentPlan, EmployeeEngagement,
    KeyPeople, EmployeeKeyPeople, TrainingApplication, EmployeeTrainingApplication,
    BusFactor, EmployeeBusFactor, Grade, EmployeeGrade, KeySkill, EmployeeKeySkill,
    Team, EmployeeTeam, Position, EmployeePosition, Competency, PositionCompetency,
    TeamPosition, EmployeeCompetency, Skill, EmployeeSkill, SkillForCompetency,
    ExpectedSkill, EmployeeExpectedSkill, CompetencyForExpectedSkill, Employee
)
from .serializers import (
    EmployeeSerializer, DevelopmentPlanSerializer, IndividualDevelopmentPlanRequestSerializer,
    IndividualDevelopmentPlanResponseSerializer, MetricRequestSerializer, 
    SkillSerializer, SkillAverageRequestSerializer, SkillAverageResponseSerializer, TeamMetricsRequestSerializer
)
# from api.filters import (
#     EmployeeFilter
# )
from rest_framework.response import Response
from django.db.models import Avg

# class WorkersViewSet(viewsets.ModelViewSet):
#     queryset = Employee.objects.all()
#     serializer_class = EmployeeSerializer
#     # filter_backends = (filters.DjangoFilterBackend,)
#     # filterset_class = EmployeeFilter

class WorkersViewSet(viewsets.ModelViewSet): 
    serializer_class = EmployeeSerializer
    
    def get_queryset(self):
        team_slug = self.kwargs.get('team_slug')  # Получаем слаг команды
        user = self.request.user  # Получаем текущего пользователя
        
        team = Team.objects.get(slug=team_slug)  # Предполагается, что у команды есть связь с slug
        manager = ManagerTeam.objects.get(user=user)  # Предполагается, что у менеджера есть связь с пользователем

        # Возвращаем сотрудников, относящихся к команде текущего менеджера
        return Employee.objects.filter(
            employeeteam__team=team,
            employeeteam__manager=manager
        )



class DevelopmentPlanViewSet(viewsets.ModelViewSet):
    queryset = DevelopmentPlan.objects.all()
    serializer_class = DevelopmentPlanSerializer

from datetime import datetime
from calendar import month_name
class MetricViewSet(viewsets.ViewSet): 
    def create(self, request, metric_type):
        request_serializer = IndividualDevelopmentPlanRequestSerializer(data=request.data)

        if request_serializer.is_valid():
            employee_ids = request_serializer.validated_data['employeeIds']
            start_period = request_serializer.validated_data['startPeriod']
            end_period = request_serializer.validated_data['endPeriod']

            # Преобразование формата даты
            start_date, end_date = self.convert_to_date(start_period, end_period)

            dashboard = []
            total_performance = 0
            employee_count = 0

            # Определяем модель в зависимости от типа метрики
            model = None
            if metric_type == 'development_plan':
                model = EmployeeDevelopmentPlan
            elif metric_type == 'engagement':
                model = EmployeeEngagement
            elif metric_type == 'employees':
                return self.get_employee_data(employee_ids, start_date, end_date)  # Обрабатываем данные по сотрудникам
            else:
                return Response(
                    {"error": "Invalid metric type."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Обрабатываем данные по каждому сотруднику
            for employee_id in employee_ids:
                try:
                    # Получаем данные только за указанный период
                    employee_metrics = model.objects.filter(
                        employee__employee_id=employee_id,
                        add_date__range=[start_date, end_date]  # Фильтрация по промежутку времени
                    )
                    
                    if employee_metrics.exists():
                        # Группируем метрики по месяцам
                        metrics_by_month = {}
                        
                        for metric in employee_metrics:
                            month_year_key = (metric.add_date.year, metric.add_date.month)
                            performance = metric.performance_score

                            if month_year_key not in metrics_by_month:
                                metrics_by_month[month_year_key] = 0
                            metrics_by_month[month_year_key] += performance

                        # Формируем данные для ответа
                        for (year, month), performance in metrics_by_month.items():
                            dashboard.append({
                                "period": {
                                    "month": month_name[month],  # Импортируйте month_name из calendar
                                    "year": year
                                },
                                "performance": str(performance)
                            })

                        
                        
                except model.DoesNotExist:
                    continue

            # Получаем последнее значение производительности за указанный период
            completion_for_today = dashboard[-1]['performance'] if dashboard else "0.00"

            response_data = {
                "dashboard": dashboard,
                "completionForToday": completion_for_today
            }

            return Response(response_data, status=status.HTTP_200_OK)

        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def convert_to_date(self, start_period, end_period):
        start_date = datetime.strptime(f"{start_period['year']}-{start_period['month']}-09", "%Y-%B-%d").date()
        end_date = datetime.strptime(f"{end_period['year']}-{end_period['month']}-09", "%Y-%B-%d").date()
        return start_date, end_date

    def get_employee_data(self, employee_ids, start_period, end_period):
        dashboard = []

        for employee_id in employee_ids:
            try:
                employee = Employee.objects.get(employee_id=employee_id)
                number_of_employees = Employee.objects.count()
                number_of_bus_factors = BusFactor.objects.count()
                number_of_key_people = Employee.objects.filter(is_key_person=True).count()

                dashboard.append({
                    "period": {
                        "start": start_period,
                        "end": end_period
                    },
                    "countData": [
                        {
                            "numberOfEmployees": str(number_of_employees),
                            "numberOfBusFactors": str(number_of_bus_factors),
                            "numberOfKeyPeople": str(number_of_key_people)
                        }
                    ]
                })
            except Employee.DoesNotExist:
                continue

        return Response({"count": dashboard}, status=status.HTTP_200_OK)
#################################
class TeamMetricViewSet(viewsets.ViewSet):
    def create(self, request,):
        # Получаем данные из запроса
        request_serializer = TeamMetricsRequestSerializer(data=request.data)

        if request_serializer.is_valid():
            start_period = request_serializer.validated_data['startPeriod']
            end_period = request_serializer.validated_data['endPeriod']

            # Преобразование дат
            start_date, end_date = self.convert_to_date(start_period, end_period)

            # Получаем команду по слагу
            try:
                team = EmployeeTeam.objects.get(team__team_name='Кто если не мы')
                employees = team.employee.all()  # Все сотрудники в команде
            except Team.DoesNotExist:
                return Response({"error": "Team not found."}, status=status.HTTP_404_NOT_FOUND)

            # Сбор метрик
            dashboard = []
            total_performance = 0
            employee_count = employees.count()

            # Группируем метрики по месяцам
            metrics_by_month = {}
            
            for employee in employees:
                # Получаем метрики для каждого сотрудника
                employee_metrics = EmployeeDevelopmentPlan.objects.filter(
                    employee=employee,
                    add_date__range=[start_date, end_date]
                )

                if employee_metrics.exists():
                    for metric in employee_metrics:
                        month_year_key = (metric.add_date.year, metric.add_date.month)
                        performance_score = metric.performance_score  # или engagement_level

                        # Суммируем производительность
                        total_performance += performance_score

                        # Группируем метрики по месяцам
                        if month_year_key not in metrics_by_month:
                            metrics_by_month[month_year_key] = 0
                        metrics_by_month[month_year_key] += performance_score

            # Подсчет средней производительности
            # Формируем dashboard
            for (year, month), performance in metrics_by_month.items():
                dashboard.append({
                    "period": {
                        "month": month_name[month],
                        "year": year
                    },
                    "performance": str(performance / employee_count)  # Усредняем по количеству сотрудников
                })

            # Завершающая производительность
            completion_for_today = dashboard[-1]['performance'] if dashboard else "0.00"

            response_data = {
                "dashboard": dashboard,
                "completionForToday": completion_for_today
            }

            return Response(response_data, status=status.HTTP_200_OK)

        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def convert_to_date(self, start_period, end_period):
        # Преобразование даты в формат
        start_date = datetime.strptime(f"{start_period['year']}-{start_period['month']}-09", "%Y-%B-%d").date()
        end_date = datetime.strptime(f"{end_period['year']}-{end_period['month']}-09", "%Y-%B-%d").date()
        return start_date, end_date
#################################

class SkillViewSet(viewsets.ModelViewSet):
    """ . """
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

    def list(self, request):
        # Сериализация входящих данных
        serializer = SkillAverageRequestSerializer(data=request.data)
        if serializer.is_valid():
            employee_ids = serializer.validated_data['employeeIds']
            skill_type = serializer.validated_data['skillType']

            # Получаем навыки заданного типа (hard/soft) для указанных сотрудников
            skills_data = EmployeeSkill.objects.filter(
                employee__employee_id__in=employee_ids,
                skill__skill_type=skill_type
            ).values('skill__skill_name', 'skill_level')

            # Формируем список с навыками и средними оценками
            skills = [{"skillName": data['skill__skill_name'], "averageAssessment": data['skill_level']} for data in skills_data]

            response_serializer = SkillAverageResponseSerializer({"skills": skills})
            return Response(response_serializer.data, status=status.HTTP_200_OK)

        # В случае ошибки валидации возвращаем ошибку
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        # Сериализация входящих данных
        serializer = SkillAverageRequestSerializer(data=request.data)
        if serializer.is_valid():
            employee_ids = serializer.validated_data['employeeIds']
            skill_type = serializer.validated_data['skillType']

            # Получаем навыки заданного типа (hard/soft) для указанных сотрудников
            skills_data = EmployeeSkill.objects.filter(
                employee__employee_id__in=employee_ids,
                skill__skill_type=skill_type
            ).values('skill__skill_name').annotate(avg_assessment=Avg('skill_level'))

            # Формируем список с навыками и средними оценками
            skills = [{"skillName": data['skill__skill_name'], "averageAssessment": data['avg_assessment']} for data in skills_data]

            response_serializer = SkillAverageResponseSerializer({"skills": skills})
            return Response(response_serializer.data, status=status.HTTP_200_OK)

        # В случае ошибки валидации возвращаем ошибку
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
