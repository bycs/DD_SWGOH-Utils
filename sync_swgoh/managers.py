from django.db import models
from sync_swgoh.sync_swgoh import get_base_units, get_base_abilities


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
