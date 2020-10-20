from datetime import datetime

from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django_extensions.db.fields import RandomCharField


# Create your models here.


class UserProfile(models.Model):
    AUTHORITY_CHOICE = (('admin', '管理者'),
                        ('employee', '照服員'),
                        ('resident', '住民'),
                        ('family', '家屬'),
                        ('vendor', '廠商'),
                        )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userprofile')
    username = models.CharField(max_length=10,verbose_name='姓名')
    authority = models.CharField(max_length=20, choices=AUTHORITY_CHOICE, default='resident')
    Photo = models.ImageField(upload_to='users/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return self.username


# 任務
class Task(models.Model):
    TASK_CHOICE = (('daily_task','每日任務')
                   ,('team_task','團隊任務')
                   ,('reward_task','懸賞任務')
                   ,('work_task','工作任務'))
    task_name = models.CharField(max_length=32,verbose_name='任務名稱' )
    task_content = RichTextField(verbose_name='任務內容')
    publish = models.DateField(default=timezone.now,verbose_name='任務發布時間')
    task_start = models.DateField(default=datetime.now,verbose_name='任務起始時間')
    task_end = models.DateField(default=datetime.now,verbose_name='任務結束時間')
    task_type = models.CharField(max_length=12,choices=TASK_CHOICE,default='daily_task',verbose_name='任務型別')
    point = models.IntegerField(verbose_name='點數')

    class Meta:
        ordering =['-publish']

    def __str__(self):
        return self.task_name


# 子任務
class SubTask(models.Model):
    task = models.ForeignKey(Task,on_delete=models.CASCADE,)
    sub_task_title = models.CharField()
    sub_task_content = models.CharField()



class PersonalTask(models.Model):
    user = models.ForeignKey()







# 行事曆
class Calendar(models.Model):
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='owner', verbose_name='擁有者')
    title = models.CharField(max_length=64,verbose_name='標題')
    content = RichTextField(verbose_name='說明')
    Photo = models.ImageField(upload_to='calendars/%Y/%m/%d/', null=True, blank=True,verbose_name='照片')
    slug = RandomCharField(length=8, unique=True, unique_for_date='publish')
    publish = models.DateField(auto_now=True,verbose_name='發布日期')
    sponsor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sponsor', verbose_name='發起者')
    participate = models.ManyToManyField(User, verbose_name='參與者')
    task = models.ManyToManyField(Task, verbose_name="任務")

    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return f'{self.title}'
