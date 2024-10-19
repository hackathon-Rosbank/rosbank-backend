# Generated by Django 4.2 on 2024-10-17 12:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ManagerTeam",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="E-mail"
                    ),
                ),
                (
                    "first_name",
                    models.CharField(max_length=50, verbose_name="Имя"),
                ),
                (
                    "last_name",
                    models.CharField(max_length=50, verbose_name="Фамилия"),
                ),
                (
                    "password",
                    models.CharField(
                        max_length=100,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Пароль должен быть не менее 4-х символов",
                                regex="^.{4,}$",
                            )
                        ],
                        verbose_name="Пароль",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "Менеджер",
                "verbose_name_plural": "Менеджеры",
            },
        ),
    ]
