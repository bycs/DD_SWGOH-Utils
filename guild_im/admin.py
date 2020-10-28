from django.contrib import admin
from .models import IMData, IMCharacter, IMShip


@admin.register(IMData, IMCharacter, IMShip)
class IMAdmin(admin.ModelAdmin):
    pass
