# Generated by Django 4.2 on 2024-10-14 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0015_alter_employeeassesmentskill_employee"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employeeassesmentskill",
            name="employee",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="assesments_skills",
                to="core.employee",
            ),
        ),
    ]
