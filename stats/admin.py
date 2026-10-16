from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(UserStat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('name', 'purchaseTotal')

    def name(self, obj):
        return obj.user.username

    name.short_description = "Username"