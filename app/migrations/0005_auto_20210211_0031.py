# Generated by Django 3.0.8 on 2021-02-11 00:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_userprofile_open_point'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamtask',
            name='award',
            field=models.IntegerField(default=0, verbose_name='獎勵點數'),
        ),
        migrations.CreateModel(
            name='SubTeamTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=32, null=True, verbose_name='方案名稱')),
                ('task_content', models.TextField(null=True, verbose_name='方案內容')),
                ('point', models.IntegerField(default=0, verbose_name='方案支付點數')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task', to='app.TeamTask')),
            ],
        ),
    ]
