# Generated by Django 4.2 on 2024-10-13 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_skill_skill_name_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='employeeteam',
            name='unique_employee_team',
        ),
    ]
