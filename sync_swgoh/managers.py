from django.db import models
from sync_swgoh.sync_swgoh import get_base_units, get_base_abilities, get_data_guild, \
    get_players_guild, get_units_guild, units_type_chars, units_type_ships


class BaseUnitManager(models.Manager):
    def sync_to_db(self):
        self.all().delete()
        units = get_base_units()
        units = units.to_dict('records')
        units_instances = [self.model(
            unit_id=unit['unit_id'],
            unit_name=unit['unit_name'],
            max_power=unit['max_power'],
            url_image=unit['url_image'],
            combat_type=unit['combat_type'],
        ) for unit in units]
        self.bulk_create(units_instances)


class BaseAbilityManager(models.Manager):
    def sync_to_db(self):
        self.all().delete()
        abilities = get_base_abilities()
        abilities = abilities.to_dict('records')
        abilities_instances = [self.model(
            ability_id=ability['ability_id'],
            ability_name=ability['ability_name'],
            unit_id=ability['unit_id'],
            tier_max=ability['tier_max'],
            is_zeta=ability['is_zeta'],
            is_omega=ability['is_omega'],
            url_image=ability['url_image'],
        ) for ability in abilities]
        self.bulk_create(abilities_instances)


"""
Всё что внизу нужно доделать
"""


class GuildsDataManager(models.Manager):
    def sync_to_db(self, guild_id):
        pass
        # Добавление / обновление информации о гильдии json + сохранение в БД
        data, json_players = get_data_guild(guild_id)
        data = data.to_dict('records')
        guild_instances = self.model(
            guild_id=data['guild_id'],
            guild_name=data['guild_name'],
            gp_total=data['gp_total'],
            players_count=data['players_count'],
            json_data_and_units=json_players,
        )
        self.bulk_create(guild_instances)  # нужно настроить bulk_update


class GuildPlayersDataManager(models.Manager):
    def sync_to_db(self, guild_id):
        pass
        self.all().delete()
        json = guild_id  # нужно взять json из БД по guild_id
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
        self.bulk_create(data_instances)


class GuildCharacterManager(models.Manager):
    def sync_to_db(self, guild_id):
        pass
        self.all().delete()
        json = guild_id  # нужно взять json из БД по guild_id
        units = get_units_guild(json)
        chars = units_type_chars(units)
        chars = chars.to_dict('records')
        chars_instances = [self.model(
            ally_code=player['ally_code'],
            unit_id=player['unit_id'],
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
        self.bulk_create(chars_instances)


class GuildShipManager(models.Manager):
    def sync_to_db(self, guild_id):
        pass
        self.all().delete()
        json = guild_id  # нужно взять json из БД по guild_id
        units = get_units_guild(json)
        ships = units_type_ships(units)
        ships = ships.to_dict('records')
        ships_instances = [self.model(
            ally_code=player['ally_code'],
            unit_id=player['unit_id'],
            rarity=player['rarity'],
            power=player['power'],
        ) for player in ships]
        self.bulk_create(ships_instances)
