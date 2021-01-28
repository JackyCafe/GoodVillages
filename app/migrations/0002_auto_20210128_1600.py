# Generated by Django 3.0.8 on 2021-01-28 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamtask',
            name='finish_date',
            field=models.DateField(null=True, verbose_name='活動結束時間'),
        ),
        migrations.AlterField(
            model_name='myworktask',
            name='date',
            field=models.DateField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_type',
            field=models.CharField(choices=[('daily_task', '每日任務'), ('team_task', '團隊任務'), ('work_task', '工作任務')], default='daily_task', max_length=12, verbose_name='任務型別'),
        ),
    ]