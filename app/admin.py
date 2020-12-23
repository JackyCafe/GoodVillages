from django.contrib import admin
from django.contrib.auth.models import User
from app.models import *


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserProfile._meta.fields]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Task._meta.fields]


# @admin.register(Calendar)
# class CalendarAdmin(admin.ModelAdmin):
#     list_display = [field.name for field in Calendar._meta.fields]


@admin.register(TeamTask)
class TeamTaskAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TeamTask._meta.fields]


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Group._meta.fields]


@admin.register(MyTeamTask)
class MyTeamTaskAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MyTeamTask._meta.fields]

