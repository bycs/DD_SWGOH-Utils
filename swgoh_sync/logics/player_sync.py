from datetime import datetime
import pandas as pd
import requests


def get_player_json(ally_code):
    """
    Получение json по игроку

    :input ally_code (int):
    :return json:
    """
    url = f'https://swgoh.gg/api/player/{ally_code}/'
    json_player = requests.get(url).json()
    return json_player


def get_data_player(json_player):
    """
    Получение информации по игроку из json

    :input json:
    :return массив с данными о игроке (DataFrame):
    """
    data = json_player['data']
    data['last_updated'] = datetime.fromisoformat(data['last_updated'])
    data = pd.json_normalize(data)
    data = pd.DataFrame(
        data=data,
        index=None,
        columns=[
            'ally_code', 'name', 'character_galactic_power',
            'ship_galactic_power', 'galactic_power', 'last_updated']
    )
    data.set_axis([
        'ally_code', 'player_name', 'gp_chars',
        'gp_ships', 'gp_total', 'last_updated'
    ],
        axis='columns',
        inplace=True
    )

    data['last_updated'] = data['last_updated'].astype('datetime64[ns, UTC]')
    data.loc[:, 'ally_code'] = data.loc[:, 'ally_code'].astype('int32')
    data.loc[:, 'gp_chars':'gp_total'] = data.loc[:, 'gp_chars':'gp_total'].astype('int32')
    return data


def get_units_player(json_player):
    """
    Получение списка персонажей по игроку из json

    :input json:
    :return массив с персонажами (DataFrame):
    """
    units = pd.json_normalize(
        json_player, 'units', [['data', 'name'], ['data', 'ally_code']],
        record_prefix='unit.',
        max_level=2,)
    units = pd.DataFrame(
        data=units,
        index=None,
        columns=[
            'data.ally_code', 'unit.data.base_id', 'unit.data.rarity',
            'unit.data.gear_level', 'unit.data.relic_tier', 'unit.data.power',
            'unit.data.stats.1', 'unit.data.stats.28', 'unit.data.stats.5',
            'unit.data.stats.6', 'unit.data.stats.16', 'unit.data.stats.14',
            'unit.data.stats.17', 'unit.data.stats.18', 'unit.data.combat_type']
    )
    units.loc[:, 'unit.data.rarity':'unit.data.relic_tier'] = \
        units.loc[:, 'unit.data.rarity':'unit.data.relic_tier'].astype('int8')
    units.loc[:, 'unit.data.power':'unit.data.stats.28'] = \
        units.loc[:, 'unit.data.power':'unit.data.stats.28'].astype('int32')
    units.loc[:, 'unit.data.stats.5':'unit.data.stats.6'] = \
        units.loc[:, 'unit.data.stats.5':'unit.data.stats.6'].astype('int16')
    units.loc[:, 'unit.data.stats.16':'unit.data.stats.18'] = \
        units.loc[:, 'unit.data.stats.16':'unit.data.stats.18'].astype('float16')
    units.loc[:, 'unit.data.combat_type'] = \
        units.loc[:, 'unit.data.combat_type'].astype('int8')
    units.set_axis(
        ['ally_code', 'unit_id', 'rarity', 'gear_level', 'relic_tier',
         'power', 'health', 'protection', 'speed', 'physical_damage',
         'critical_damage', 'critical_chance', 'potency', 'tenacity', 'combat_type'],
        axis='columns',
        inplace=True
    )
    units = units.sort_values(by=['unit_id']).reset_index(drop=True)
    return units
