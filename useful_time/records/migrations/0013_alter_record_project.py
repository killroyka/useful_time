# Generated by Django 3.2 on 2022-05-25 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20220511_1936'),
        ('records', '0012_alter_record_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='records', to='projects.project', verbose_name='Проект'),
        ),
    ]
