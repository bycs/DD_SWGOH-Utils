from django.db import models

from swgoh_sync.models.guilds import GuildsData
from swgoh_sync.logics.actions import split_units_type_by_chars, split_units_type_by_ships
from swgoh_sync.logics.guild_sync import get_players_guild, get_units_guild


class GuildPlayersDataManager(models.Manager):
    def sync_to_db(self, guild_id):
        json = GuildsData.guilds_data_managers.get(guild_id=guild_id).json_data_and_units
        data = get_players_guild(json)
        data = data.to_dict('records')
        data_instances = [self.model(
            ally_code=player['ally_code'],
            player_name=player['player_name'],
            gp_chars=player['gp_chars'],
            gp_ships=player['gp_ships'],
            gp_total=player['gp_total'],
            last_updated=player['last_updated'],
            chars_average_rank=player['chars_average_rank'],
            ships_average_rank=player['ships_average_rank'],
        ) for player in data]
        self.all().delete()
        self.bulk_create(data_instances)


class GuildCharacterManager(models.Manager):
    def sync_to_db(self, guild_id):
        json = GuildsData.guilds_data_managers.get(guild_id=guild_id).json_data_and_units
        units = get_units_guild(json)
        chars = split_units_type_by_chars(units)
        chars = chars.to_dict('records')
        chars_instances = [self.model(
            ally_code_id=player['ally_code'],
            unit_id_id=player['unit_id'],
            rarity=player['rarity'],
            gear_level=player['gear_level'],
            relic_tier=player['relic_tier'],
            power=player['power'],
            health=player['health'],
            protection=player['protection'],
            speed=player['speed'],
            physical_damage=player['physical_damage'],
            critical_damage=player['critical_damage'],
            critical_chance=player['critical_chance'],
            potency=player['potency'],
            tenacity=player['tenacity'],
        ) for player in chars]
        self.all().delete()
        self.bulk_create(chars_instances)


class GuildShipManager(models.Manager):
    def sync_to_db(self, guild_id):
        json = GuildsData.guilds_data_managers.get(guild_id=guild_id).json_data_and_units
        units = get_units_guild(json)
        ships = split_units_type_by_ships(units)
        ships = ships.to_dict('records')
        ships_instances = [self.model(
            ally_code_id=player['ally_code'],
            unit_id_id=player['unit_id'],
            rarity=player['rarity'],
            power=player['power'],
        ) for player in ships]
        self.all().delete()
        self.bulk_create(ships_instances)
