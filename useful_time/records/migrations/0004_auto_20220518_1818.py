# Generated by Django 3.2 on 2022-05-18 15:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0003_auto_20220517_1259'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='record',
            name='endpoint',
        ),
        migrations.RemoveField(
            model_name='record',
            name='startpoint',
        ),
    ]