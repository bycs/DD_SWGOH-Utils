from django.contrib import admin

from swgoh_sync.models.base import BaseAbility, BaseUnit
from swgoh_sync.models.guilds import GuildsData


class BaseUnitAdmin(admin.ModelAdmin):
    list_display = ['unit_id', 'unit_name', 'max_power', 'combat_type']
    list_filter = ['unit_name']
    search_fields = ['unit_id', 'unit_name', 'combat_type']


class BaseAbilityAdmin(admin.ModelAdmin):
    list_display = ['ability_id', 'ability_name', 'unit_id', 'tier_max', 'is_omega', 'is_zeta']
    list_filter = ['unit_id']
    search_fields = ['ability_id', 'ability_name', 'unit_id', 'is_omega', 'is_zeta']


class GuildsDataAdmin(admin.ModelAdmin):
    list_display = ['guild_id', 'guild_name', 'players_count', 'gp_total', 'last_sync']
    list_filter = ['guild_name']
    search_fields = ['guild_id', 'guild_name']


admin.site.register(BaseUnit, BaseUnitAdmin)
admin.site.register(BaseAbility, BaseAbilityAdmin)
admin.site.register(GuildsData, GuildsDataAdmin)


class GuildPlayersDataAdmin(admin.ModelAdmin):
    list_display = [
        'ally_code', 'player_name', 'gp_chars', 'gp_ships', 'gp_total',
        'chars_average_rank', 'ships_average_rank', 'last_updated'
    ]
    list_filter = ['player_name']
    search_fields = ['ally_code', 'player_name']


class GuildCharacterAdmin(admin.ModelAdmin):
    list_display = ['ally_code', 'unit_id', 'rarity', 'gear_level', 'relic_tier', 'power']
    list_filter = ['ally_code', 'unit_id']
    search_fields = ['ally_code', 'unit_id']


class GuildShipAdmin(admin.ModelAdmin):
    list_display = ['ally_code', 'unit_id', 'rarity', 'power']
    list_filter = ['ally_code', 'unit_id']
    search_fields = ['ally_code', 'unit_id']
