# Generated by Django 3.2 on 2022-05-06 14:12

import colorfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_alter_project_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='color',
            field=colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=18, samples=None, verbose_name='Цвет'),
        ),
        migrations.AlterField(
            model_name='project',
            name='description',
            field=models.TextField(help_text='не более 500 символов', max_length=500, verbose_name='Описание'),
        ),
    ]
