# Generated by Django 3.1.1 on 2020-10-19 03:52

import ckeditor.fields
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
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=32, verbose_name='任務名稱')),
                ('task_content', models.TextField()),
                ('publish', models.DateField(default=django.utils.timezone.now)),
                ('task_start', models.DateField(auto_now=True)),
                ('task_end', models.DateField(auto_now=True)),
                ('task_type', models.CharField(choices=[('daily_task', '每日任務'), ('team_task', '團隊任務'), ('reward_task', '懸賞任務'), ('work_task', '工作任務')], default='每日任務', max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=10, verbose_name='姓名')),
                ('authority', models.CharField(choices=[('admin', '管理者'), ('employee', '照服員'), ('resident', '住民'), ('family', '家屬'), ('vendor', '廠商')], default='住民', max_length=20)),
                ('Photo', models.ImageField(blank=True, null=True, upload_to='users/%Y/%m/%d/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Calendar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='標題')),
                ('content', ckeditor.fields.RichTextField(verbose_name='說明')),
                ('Photo', models.ImageField(blank=True, null=True, upload_to='calendars/%Y/%m/%d/', verbose_name='照片')),
                ('slug', django_extensions.db.fields.RandomCharField(blank=True, editable=False, length=8, unique=True, unique_for_date='publish')),
                ('publish', models.DateField(auto_now=True, verbose_name='發布日期')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='app1.userprofile', verbose_name='擁有者')),
                ('participate', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='參與者')),
                ('sponsor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sponsor', to=settings.AUTH_USER_MODEL, verbose_name='發起者')),
                ('task', models.ManyToManyField(to='app1.Task', verbose_name='任務')),
            ],
            options={
                'ordering': ['-publish'],
            },
        ),
    ]
