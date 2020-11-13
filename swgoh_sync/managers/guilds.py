from django.db import models

from swgoh_sync.logics.guild_sync import get_guild_json, get_data_guild


class GuildsDataManager(models.Manager):
    def sync_to_db(self, guild_id):
        json_guild = get_guild_json(guild_id)
        data_guild = get_data_guild(json_guild)
        json_players = json_guild['players']
        data_guild = data_guild.to_dict('records')[0]
        guild_instances = [self.model(
            guild_id=data_guild['guild_id'],
            guild_name=data_guild['guild_name'],
            gp_total=data_guild['gp_total'],
            players_count=data_guild['players_count'],
            last_sync=data_guild['last_sync'],
            json_data_and_units=json_players,
        )]
        try:
            if self.get(guild_id=guild_id):
                self.bulk_update(guild_instances, [
                    'guild_name', 'gp_total', 'players_count',
                    'last_sync', 'json_data_and_units'
                ])
        except self.model.DoesNotExist:
            self.bulk_create(guild_instances)
