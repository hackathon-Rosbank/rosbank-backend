# Generated by Django 4.2 on 2024-10-14 10:59

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_employeeassesmentskill_assesment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeedevelopmentplan',
            name='performance_score',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='Процент развития'),
        ),
        migrations.AlterField(
            model_name='employeeengagement',
            name='employee',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='engagements', to='core.employee'),
        ),
        migrations.AlterField(
            model_name='employeeengagement',
            name='engagement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_engagements', to='core.engagement', verbose_name='Вовлеченность'),
        ),
        migrations.CreateModel(
            name='PositionGrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ate_added', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления грейда к должности')),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grade_position', to='core.grade', verbose_name='Грейд')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='position_grades', to='core.position', verbose_name='Должность')),
            ],
            options={
                'verbose_name': 'Грейд сотрудника',
                'verbose_name_plural': 'Грейды сотрудников',
                'ordering': ('position',),
            },
        ),
    ]
