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
    authority = models.CharField(max_length=20, choices=AUTHORITY_CHOICE, default='住民')
    Photo = models.ImageField(upload_to='users/%Y/%m/%d/', null=True, blank=True)

    def __str__(self):
        return self.user.username


# 任務
class Task(models.Model):
    task_name = models.CharField(max_length=32, verbose='任務名稱')
    task_content = models.TextField()
    publish = models.DateField(default=timezone.now)
    task_start = models.DateField(auto_now=True, )


# 行事曆
class Calendar(models):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner', verbose='擁有者')
    title = models.CharField(max_length=64)
    content = RichTextField()
    Photo = models.ImageField(upload_to='calendars/%Y/%m/%d/', null=True, blank=True)
    slug = RandomCharField(length=8, unique=True, unique_for_date='publish')
    publish = models.DateField(auto_now=True)
    sponsor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sponsor', verbose_name='發起者')
    participate = models.ManyToManyField(User, verbose_name='參與者')
    task = models.ManyToManyField(Task, verbose="任務")

    class Meta:
        order = ['-publish']



