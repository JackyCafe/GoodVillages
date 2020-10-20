# Generated by Django 3.1.1 on 2020-10-20 10:18

import ckeditor.fields
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', django_extensions.db.fields.RandomCharField(blank=True, editable=False, length=16, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=32, verbose_name='任務名稱')),
                ('task_content', ckeditor.fields.RichTextField(verbose_name='任務內容')),
                ('publish', models.DateField(default=django.utils.timezone.now, verbose_name='任務發布時間')),
                ('task_start', models.DateField(default=datetime.datetime.now, verbose_name='任務起始時間')),
                ('task_end', models.DateField(default=datetime.datetime.now, verbose_name='任務結束時間')),
                ('task_type', models.CharField(choices=[('daily_task', '每日任務'), ('team_task', '團隊任務'), ('reward_task', '懸賞任務'), ('work_task', '工作任務')], default='daily_task', max_length=12, verbose_name='任務型別')),
                ('point', models.IntegerField(verbose_name='點數')),
            ],
            options={
                'ordering': ['-publish'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=10, verbose_name='姓名')),
                ('authority', models.CharField(choices=[('admin', '管理者'), ('employee', '照服員'), ('resident', '住民'), ('family', '家屬'), ('vendor', '廠商')], default='resident', max_length=20)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='users/%Y/%m/%d/')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to='app1.group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TeamTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='群組', to='app1.group')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.task', verbose_name='任務')),
            ],
        ),
        migrations.CreateModel(
            name='SubTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_task_title', models.CharField(max_length=20)),
                ('sub_task_content', models.TextField()),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.task')),
            ],
        ),
        migrations.CreateModel(
            name='PersonalTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date1', models.DateField(default=datetime.datetime.now)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.task', verbose_name='任務')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.userprofile', verbose_name='人員')),
            ],
        ),
        migrations.CreateModel(
            name='PersonalSubTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date1', models.DateField(default=datetime.datetime.now)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.task', verbose_name='任務')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.userprofile', verbose_name='人員')),
            ],
        ),
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='標題')),
                ('content', ckeditor.fields.RichTextField(verbose_name='說明')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='calendars/%Y/%m/%d/', verbose_name='照片')),
                ('slug', django_extensions.db.fields.RandomCharField(blank=True, editable=False, length=8, unique=True, unique_for_date='publish')),
                ('publish', models.DateField(auto_now=True, verbose_name='發布日期')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='app1.userprofile', verbose_name='擁有者')),
                ('participate', models.ManyToManyField(to='app1.UserProfile', verbose_name='參與者')),
                ('sponsor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sponsor', to='app1.userprofile', verbose_name='發起者')),
                ('task', models.ManyToManyField(to='app1.Task', verbose_name='任務')),
            ],
            options={
                'ordering': ['-publish'],
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.userprofile', verbose_name='人員')),
            ],
        ),
    ]
