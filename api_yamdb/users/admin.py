from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import RoleUser


# Register your models here.
@admin.register(RoleUser)
class RoleUserAdmin(UserAdmin):
    model = RoleUser
    list_display = ('username', 'email', 'role', 'bio', 'first_name')

