# Generated by Django 5.1.2 on 2024-11-23 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_rename_project_my_project_rename_task_my_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='my_project',
            name='name',
            field=models.CharField(max_length=25),
        ),
        migrations.AlterField(
            model_name='my_task',
            name='title',
            field=models.CharField(max_length=25),
        ),
    ]
