from django.contrib.auth.models import User
from django.db import models


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