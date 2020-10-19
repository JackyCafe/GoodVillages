from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User

from app1.models import *


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserProfile._meta.fields]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Task._meta.fields]


@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Calendar._meta.fields]