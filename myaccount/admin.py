from django.contrib import admin
from .models import UserProfile

# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("uid", "nickname", "join_date", "mod_date")
    ordering = ("join_date", )