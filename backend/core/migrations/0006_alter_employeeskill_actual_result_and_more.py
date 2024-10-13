# Generated by Django 4.2 on 2024-10-13 15:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_employeeskill_actual_result_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeskill',
            name='actual_result',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='Фактическая оценка'),
        ),
        migrations.AlterField(
            model_name='employeeskill',
            name='planned_result',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='Плановая оценка'),
        ),
    ]
