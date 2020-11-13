from django.contrib import admin
from swgoh_sync.admin import GuildCharacterAdmin, GuildPlayersDataAdmin, GuildShipAdmin
from .models import Data, Character, Ship


class DataAdmin(GuildPlayersDataAdmin):
    pass


class CharacterAdmin(GuildCharacterAdmin):
    pass


class ShipAdmin(GuildShipAdmin):
    pass


admin.site.register(Data, DataAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Ship, ShipAdmin)
