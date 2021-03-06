# Generated by Django 3.2 on 2022-05-05 12:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='не более 100 символов', max_length=100, verbose_name='Название')),
                ('startpoint', models.DateTimeField()),
                ('endpoint', models.DateTimeField(blank=True, null=True)),
                ('project', models.ForeignKey(default='Безымянный промежуток', on_delete=django.db.models.deletion.CASCADE, related_name='records', to='projects.project', verbose_name='Проект')),
            ],
            options={
                'verbose_name': 'Запись',
                'verbose_name_plural': 'Записи',
            },
        ),
    ]
