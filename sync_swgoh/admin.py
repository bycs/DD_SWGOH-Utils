from django.contrib import admin
from .models import BaseUnit, BaseAbility


@admin.register(BaseUnit, BaseAbility)
class BaseAdmin(admin.ModelAdmin):
    pass
