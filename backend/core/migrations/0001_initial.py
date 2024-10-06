# Generated by Django 4.2 on 2024-10-05 22:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BusFactor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bus_factor_name', models.CharField(max_length=255, verbose_name='Название Bus фактора')),
                ('employee_count', models.IntegerField(default=0, verbose_name='Количество сотрудников с этим Bus фактором')),
            ],
            options={
                'verbose_name': 'Bus Фактор',
                'verbose_name_plural': 'Bus Факторы',
                'ordering': ('bus_factor_name',),
            },
        ),
        migrations.CreateModel(
            name='Competency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competency_name', models.CharField(max_length=255, verbose_name='Название компетенции')),
                ('employee_count', models.IntegerField(default=0, verbose_name='Количество сотрудников с данной компетенцией')),
            ],
            options={
                'verbose_name': 'Компетенция',
                'verbose_name_plural': 'Компетенции',
                'ordering': ('competency_name',),
            },
        ),
        migrations.CreateModel(
            name='CompetencyForExpectedSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Компетенция для ожидаемого навыка',
                'verbose_name_plural': 'Компетенции для ожидаемых навыков',
            },
        ),
        migrations.CreateModel(
            name='DevelopmentPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_name', models.CharField(max_length=255, unique=True, verbose_name='Название плана')),
                ('employee_count', models.IntegerField(default=0, verbose_name='Кол-во сотрудников с планом развития')),
            ],
            options={
                'verbose_name': 'План развития',
                'verbose_name_plural': 'Планы развития',
                'ordering': ('plan_name',),
            },
        ),
        migrations.CreateModel(
            name='EmployeeBusFactor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateField(auto_now_add=True, db_index=True, verbose_name='Дата добавления bud-фактора сотрудника')),
            ],
            options={
                'verbose_name': 'Bus Фактор сотрудника',
                'verbose_name_plural': 'Bus Факторы сотрудников',
                'ordering': ('bus_factor',),
            },
        ),
        migrations.CreateModel(
            name='EmployeeCompetency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competency_level', models.CharField(max_length=255, verbose_name='Уровень компетенции сотрудника')),
            ],
            options={
                'verbose_name': 'Компетенция сотрудника',
                'verbose_name_plural': 'Компетенции сотрудников',
                'ordering': ('competency',),
            },
        ),
        migrations.CreateModel(
            name='EmployeeDevelopmentPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('development_progress', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Процент развития')),
                ('add_date', models.DateField(auto_now_add=True, db_index=True, verbose_name='Дата добавления сотрудника в план развития')),
            ],
            options={
                'verbose_name': 'План развития сотрудника',
                'verbose_name_plural': 'Планы развития сотрудников',
                'ordering': ('development_plan',),
            },
        ),
        migrations.CreateModel(
            name='EmployeeEngagement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('engagement_level', models.IntegerField(verbose_name='Уровень вовлеченности сотрудника')),
                ('add_date', models.DateField(auto_now_add=True, db_index=True, verbose_name='Дата вовлечения сотрудника')),
            ],
            options={
                'verbose_name': 'Вовлеченность сотрудника',
                'verbose_name_plural': 'Вовлеченность сотрудников',
                'ordering': ('engagement_level',),
            },
        ),
        migrations.CreateModel(
            name='EmployeeExpectedSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Ожидаемый навык сотрудника',
                'verbose_name_plural': 'Ожидаемые навыки сотрудниов',
                'ordering': ('expected_skill',),
            },
        ),
        migrations.CreateModel(
            name='EmployeeGrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Класс сотрудника',
                'verbose_name_plural': 'Классы сотрудников',
                'ordering': ('grade',),
            },
        ),
        migrations.CreateModel(
            name='EmployeeKeyPeople',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateField(auto_now_add=True, db_index=True, verbose_name='Дата добавления ключевого сотрудника')),
            ],
            options={
                'verbose_name': 'Key People сотрудника',
                'verbose_name_plural': 'Key People сотрудников',
                'ordering': ('key_people',),
            },
        ),
        migrations.CreateModel(
            name='EmployeeKeySkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_level', models.CharField(max_length=255, verbose_name='Уровень ключевого навыка сотрудника')),
                ('add_date', models.DateField(auto_now_add=True, db_index=True, verbose_name='Дата добавления ключевого навыка сотрудника')),
            ],
            options={
                'verbose_name': 'Ключевой навык сотрудника',
                'verbose_name_plural': 'Ключевые навыки сотрудников',
                'ordering': ('key_skill',),
            },
        ),
        migrations.CreateModel(
            name='EmployeePosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Должность сотрудника',
                'verbose_name_plural': 'Должности сотрудников',
                'ordering': ('position',),
            },
        ),
        migrations.CreateModel(
            name='EmployeeSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_level', models.CharField(max_length=255, verbose_name='Уровень навыка сотрудника')),
            ],
            options={
                'verbose_name': 'Навык сотрудника',
                'verbose_name_plural': 'Навыки сотрудников',
                'ordering': ('skill',),
            },
        ),
        migrations.CreateModel(
            name='EmployeeTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Команда сотрудника',
                'verbose_name_plural': 'Команды сотрудников',
                'ordering': ('team',),
            },
        ),
        migrations.CreateModel(
            name='EmployeeTrainingApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_date', models.DateField(auto_now_add=True, db_index=True, verbose_name='Дата добавления заявки на обучение')),
            ],
            options={
                'verbose_name': 'Заявка на обучение сотрудника',
                'verbose_name_plural': 'Заявки на обучение сотрудников',
                'ordering': ('training_application',),
            },
        ),
        migrations.CreateModel(
            name='Engagement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('engagement_name', models.CharField(max_length=255, verbose_name='Название вовлеченности')),
                ('employee_count', models.IntegerField(default=0, verbose_name='Количество вовлеченных сотрудников')),
            ],
            options={
                'verbose_name': 'Вовлеченность',
                'verbose_name_plural': 'Вовлеченности',
                'ordering': ('engagement_name',),
            },
        ),
        migrations.CreateModel(
            name='ExpectedSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expected_skill_name', models.CharField(max_length=255, verbose_name='Название ожидаемого навыка')),
                ('employee_count', models.IntegerField(default=0, verbose_name='Количество сотрудников с данным ожидаемым навыком')),
            ],
            options={
                'verbose_name': 'Ожидаемый навык',
                'verbose_name_plural': 'Ожидаемые навыки',
                'ordering': ('expected_skill_name',),
            },
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade_name', models.CharField(max_length=255, verbose_name='Название класса')),
            ],
            options={
                'verbose_name': 'Класс',
                'verbose_name_plural': 'Классы',
                'ordering': ('grade_name',),
            },
        ),
        migrations.CreateModel(
            name='KeyPeople',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_people_name', models.CharField(max_length=255, verbose_name='Название key people')),
                ('employee_count', models.IntegerField(default=0, verbose_name='Количество сотрудников Key People')),
            ],
            options={
                'verbose_name': 'Вовлеченность сотрудника',
                'verbose_name_plural': 'Вовлеченность сотрудников',
                'ordering': ('key_people_name',),
            },
        ),
        migrations.CreateModel(
            name='KeySkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(max_length=255, verbose_name='Название ключевого навыка')),
                ('employee_count', models.IntegerField(default=0, verbose_name='Количество сотрудников с данным ключевым навыком')),
            ],
            options={
                'verbose_name': 'Ключевой навык',
                'verbose_name_plural': 'Ключевые навыки',
                'ordering': ('skill_name',),
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_name', models.CharField(max_length=255, unique=True, verbose_name='Название должности')),
                ('grade_count', models.IntegerField(default=0, verbose_name='Количество грейдов, связанных с должностью')),
            ],
            options={
                'verbose_name': 'Должность',
                'verbose_name_plural': 'Должности',
                'ordering': ('position_name',),
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill_name', models.CharField(max_length=255, verbose_name='Название навыка')),
                ('employee_count', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Навык',
                'verbose_name_plural': 'Навыки',
                'ordering': ('skill_name',),
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=255, verbose_name='Название команды')),
            ],
            options={
                'verbose_name': 'Команда',
                'verbose_name_plural': 'Команды',
            },
        ),
        migrations.CreateModel(
            name='TrainingApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('training_name', models.CharField(max_length=255, verbose_name='Название обучения')),
                ('employee_count', models.IntegerField(default=0, verbose_name='Количество сотрудников на обучении')),
            ],
            options={
                'verbose_name': 'Заявка на обучение',
                'verbose_name_plural': 'Заявки на обучение',
                'ordering': ('training_name',),
            },
        ),
        migrations.CreateModel(
            name='TeamPosition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.position')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.team')),
            ],
            options={
                'verbose_name': 'Должность для команды',
                'verbose_name_plural': 'Должности для команд',
                'ordering': ('team',),
            },
        ),
        migrations.CreateModel(
            name='SkillForCompetency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.competency')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.skill')),
            ],
            options={
                'verbose_name': 'Навык для компетенции',
                'verbose_name_plural': 'Навыки для компетенций',
            },
        ),
        migrations.CreateModel(
            name='PositionCompetency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.competency')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competencies', to='core.position')),
            ],
            options={
                'verbose_name': 'Должность к компетенции',
                'verbose_name_plural': 'Должности к компетенциям',
            },
        ),
    ]
