# Generated by Django 3.2 on 2022-05-07 14:19

import colorfield.fields
from django.db import migrations
import projects.validators


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20220506_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='color',
            field=colorfield.fields.ColorField(default='#FFFFFF', image_field=None, max_length=18, samples=None, validators=[projects.validators.validate_color], verbose_name='Цвет'),
        ),
    ]
