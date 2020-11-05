"""
Запись данных из sync_swgoh в БД
"""
from sync_swgoh.models import BaseUnit, BaseAbility
from sync_swgoh.sync_swgoh import get_base_units_and_abilities


def sync_base_units_and_abilities():
    BaseUnit.objects.all().delete()
    BaseAbility.objects.all().delete()
    units, abilities = get_base_units_and_abilities()
    units = units.to_dict('records')
    abilities = abilities.to_dict('records')
    units_instances = [BaseUnit(
        unit_id=unit['unit_id'],
        unit_name=unit['unit_name'],
        max_power=unit['max_power'],
        url_image=unit['url_image'],
        combat_type=unit['combat_type'],
    ) for unit in units]
    abilities_instances = [BaseAbility(
        ability_id=ability['ability_id'],
        ability_name=ability['ability_name'],
        unit_id=ability['unit_id'],
        tier_max=ability['tier_max'],
        is_zeta=ability['is_zeta'],
        is_omega=ability['is_omega'],
        url_image=ability['url_image'],
    ) for ability in abilities]
    BaseUnit.objects.bulk_create(units_instances)
    BaseAbility.objects.bulk_create(abilities_instances)
