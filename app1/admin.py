from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User

from app1.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserProfile._meta.fields]