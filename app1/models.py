from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.fields import RandomCharField
# Create your models here.


class UserProfile(models.Model):
    AUTHORITY_CHOICE = (('admin','管理者'),
                        ('employee','照服員'),
                        ('resident','住民'),
                        ('family','家屬'),
                        ( 'vendor','廠商'),
                        )
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='userprofile')
    authority = models.CharField(max_length=20,choices=AUTHORITY_CHOICE,default='住民')
    Photo = models.ImageField(upload_to='users/%Y/%m/%d/',null=True,blank=True)


class Calendar(models):
    owner =   models.ForeignKey(User,on_delete=models.CASCADE,related_name='owner')
    title = models.CharField(max_length=64)
    conent = models.TextField()
    Photo = models.ImageField(upload_to='users/%Y/%m/%d/', null=True, blank=True)
    slug = RandomCharField(length=8, unique=True, unique_for_date='publish')
    publish = models.DateField(auto_created=True)
    spsor = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sponsor')
