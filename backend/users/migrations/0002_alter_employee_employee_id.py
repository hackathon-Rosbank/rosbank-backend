# Generated by Django 4.2 on 2024-10-04 14:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="employee_id",
            field=models.CharField(
                default=uuid.uuid4, editable=False, max_length=100, unique=True
            ),
        ),
    ]
