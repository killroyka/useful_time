# Generated by Django 3.2 on 2022-05-21 15:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('records', '0009_auto_20220521_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='subrecord',
            name='longitude',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='продолжительность'),
        ),
    ]
