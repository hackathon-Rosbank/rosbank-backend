# Generated by Django 4.2 on 2024-10-04 14:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employeegrade",
            name="employee",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="grades",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="employeeposition",
            name="employee",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="positions",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="employeeskill",
            name="employee",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="skills",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="positioncompetency",
            name="position",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="competencies",
                to="core.position",
            ),
        ),
    ]
