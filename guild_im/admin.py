from django.contrib import admin
from sync_swgoh.admin import GuildPlayersDataAdmin, GuildCharacterAdmin, GuildShipAdmin
from .models import IMData, IMCharacter, IMShip


class IMDataAdmin(GuildPlayersDataAdmin):
    pass


class IMCharacterAdmin(GuildCharacterAdmin):
    pass


class IMShipAdmin(GuildShipAdmin):
    pass


admin.site.register(IMData, IMDataAdmin)
admin.site.register(IMCharacter, IMCharacterAdmin)
admin.site.register(IMShip, IMShipAdmin)
