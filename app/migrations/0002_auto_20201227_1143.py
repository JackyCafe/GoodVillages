# Generated by Django 3.1.1 on 2020-12-27 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myworktask',
            name='end_time',
            field=models.DateField(null=True, verbose_name='任務結束時間'),
        ),
        migrations.AlterField(
            model_name='myworktask',
            name='start_time',
            field=models.DateField(null=True, verbose_name='任務開始時間'),
        ),
    ]
