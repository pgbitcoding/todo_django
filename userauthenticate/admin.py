from django.contrib import admin
from .models import User
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email")
    search_fields = ("username",)

admin.site.register(User, UserAdmin)