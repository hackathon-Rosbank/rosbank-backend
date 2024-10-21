from rest_framework import serializers
from users.models import Employee
from core.models import (
    DevelopmentPlan, EmployeeDevelopmentPlan, EmployeeEngagement,
    KeyPeople, EmployeeKeyPeople, TrainingApplication, EmployeeTrainingApplication,
    BusFactor, EmployeeBusFactor, Grade, EmployeeGrade, KeySkill, EmployeeKeySkill,
    Team, EmployeeTeam, Position, EmployeePosition, Competency, PositionCompetency,
    TeamPosition, EmployeeCompetency, Skill, EmployeeSkill, SkillForCompetency,
    ExpectedSkill, EmployeeExpectedSkill, CompetencyForExpectedSkill
)
from django.urls import reverse
from rest_framework.validators import UniqueTogetherValidator


class WorkersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'id', 'employee_id', 'first_name', 'patronymic', 'position'
        )


class SkillSerializer(serializers.ModelSerializer):
    """ Сериализатор для навыков сотрудника. """

    skill = serializers.CharField(source='skill.skill_name')

    class Meta:
        model = EmployeeSkill
        fields = (
            'skill', 'skill_level'
        )


class CompetencySerializer(serializers.ModelSerializer):
    """ Сериализатор для компетенций сотрудника. """

    competency = serializers.CharField(source='competency.competency_name')

    class Meta:
        model = EmployeeCompetency
        fields = (
            'competency', 'competency_level'
        )


class EmployeeSerializer(serializers.ModelSerializer):
    """ Основной сериализатор для сотрудников. """

    worker = serializers.SerializerMethodField()
    skills = SkillSerializer(many=True)
    competencies = CompetencySerializer(source='employee_competencies', many=True)
    position = serializers.CharField(source='positions.first.position.position_name', allow_null=True)
    grade = serializers.CharField(source='grades.grade.grade_name', )

    key_people = serializers.SerializerMethodField()
    bus_factor = serializers.SerializerMethodField()
    education = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = (
            'id', 'position', 'worker', 'grade', 'key_people',
            'bus_factor', 'education', 'skills','competencies'
        )

    def get_worker(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    # Проверка наличия записи в EmployeeKeyPeople
    def get_key_people(self, obj):
        return EmployeeKeyPeople.objects.filter(employee=obj).exists()

    # Проверка наличия записи в EmployeeBusFactor
    def get_bus_factor(self, obj):
        return EmployeeBusFactor.objects.filter(employee=obj).exists()

    # Проверка наличия записи в EmployeeTrainingApplication (образование)
    def get_education(self, obj):
        return EmployeeTrainingApplication.objects.filter(employee=obj).exists()


class DevelopmentPlanSerializer(serializers.ModelSerializer):
    """ ."""

    class Meta:
        model = DevelopmentPlan
        fields = (
            'month', 'year', 'key_skill',
        )


class IndividualDevelopmentPlanRequestSerializer(serializers.Serializer):
    employeeIds = serializers.ListField(
        child=serializers.CharField()
    )
    startPeriod = serializers.DictField(
        child=serializers.CharField(),
        required=True
    )
    endPeriod = serializers.DictField(
        child=serializers.CharField(),
        required=True
    )

class IndividualDevelopmentPlanResponseSerializer(serializers.Serializer):
    dashboard = serializers.ListField(
        child=serializers.DictField()
    )
    completionForToday = serializers.CharField()
    
