"""
Импорт и структуризация данных с  сайта swgoh.gg через API
с использованием библиотеки pandas
"""

import requests
import pandas as pd


def get_data_player(ally_code):
    """
    Получение информации по игроку

    :input ally_code (int):
    :return массив с данными о игроке (DataFrame):
    """
    link = f'https://swgoh.gg/api/player/{ally_code}/'
    data = pd.json_normalize(requests.get(link).json()['data'])
    data = pd.DataFrame(
        data=data,
        index=None,
        columns=['ally_code', 'name', 'character_galactic_power', 'ship_galactic_power', 'galactic_power']
    )
    data.set_axis(['ally_code', 'player_name', 'gp_chars', 'gp_ships', 'gp_all'], axis='columns', inplace=True)
    data.loc[:, 'ally_code'] = data.loc[:, 'ally_code'].astype('int32')
    data.loc[:, 'gp_chars':'gp_all'] = data.loc[:, 'gp_chars':'gp_all'].astype('int32')
    return data


def get_units_player(ally_code):
    """
    Получение списка персонажей по игроку

    :input ally_code (int):
    :return массив с персонажами (DataFrame):
    """
    link = f'https://swgoh.gg/api/player/{ally_code}/'
    units = pd.json_normalize(requests.get(link).json(), 'units', [['data', 'name'], ['data', 'ally_code']],
                              record_prefix='unit.', max_level=2,)
    units = pd.DataFrame(
        data=units,
        index=None,
        columns=[
            'data.ally_code', 'unit.data.base_id', 'unit.data.rarity', 'unit.data.gear_level', 'unit.data.relic_tier',
            'unit.data.power', 'unit.data.stats.1', 'unit.data.stats.28', 'unit.data.stats.5', 'unit.data.stats.6',
            'unit.data.stats.16', 'unit.data.stats.14', 'unit.data.stats.17', 'unit.data.stats.18',
            'unit.data.combat_type']
    )
    units.loc[:, 'unit.data.rarity':'unit.data.relic_tier'] = \
        units.loc[:, 'unit.data.rarity':'unit.data.relic_tier'].astype('int8')
    units.loc[:, 'unit.data.power':'unit.data.stats.28'] = \
        units.loc[:, 'unit.data.power':'unit.data.stats.28'].astype('int32')
    units.loc[:, 'unit.data.stats.5':'unit.data.stats.6'] = \
        units.loc[:, 'unit.data.stats.5':'unit.data.stats.6'].astype('int16')
    units.loc[:, 'unit.data.stats.16':'unit.data.stats.18'] = \
        units.loc[:, 'unit.data.stats.16':'unit.data.stats.18'].astype('float16')
    units.loc[:, 'unit.data.combat_type'] = units.loc[:, 'unit.data.combat_type'].astype('int8')
    units.set_axis(
        ['ally_code', 'unit_id', 'rarity', 'gear_level', 'relic_tier ', 'power',
         'health', 'protection', 'speed', 'physical_damage', 'critical_damage', 'critical_chance',
         'potency', 'tenacity', 'combat_type'],
        axis='columns',
        inplace=True
    )
    units = units.sort_values(by=['unit_id']).reset_index(drop=True)
    return units


def units_type_chars(units):
    """
    Отбор из юнитов только персонажей

    :input units (DataFrame):
    :return массив с персонажами (DataFrame):
    """
    characters = units[units['combat_type'] == 1]
    del characters['combat_type']
    return characters


def units_type_ships(units):
    """
    Отбор из юнитов только флот

    :input units (DataFrame):
    :return массив с флотом (DataFrame):
    """
    ships = units[units['combat_type'] == 2]
    ships = ships.loc[:, ['ally_code', 'unit_id', 'rarity', 'power']]
    return ships


def units_combat_type(units):
    """
    Разделение юнитов по классам (персонажи и флот)

    :input units (DataFrame):
    :return два массива: с персонажами и флотом (DataFrame x2):
    """
    characters = units_type_chars(units)
    ships = units_type_ships(units)
    return characters, ships


def get_ally_list(guild_id):
    """
    Получение списка игроков гильдии

    :input guild_id (int):
    :return строка с игроками гильдии (str):
    """
    link = f'https://swgoh.gg/api/guild/{guild_id}/'
    ally_list = pd.json_normalize(
        requests.get(link).json()['players']).loc[:, 'data.ally_code']
    ally_list = list(ally_list.astype('str'))
    ally_list = (', '.join(ally_list))
    return ally_list


def get_ally_count(guild_id):
    """
    Подсчет количества игроков в гильдии
    :input guild_id (str):
    :return количетсво игроков в гильдии (int):
    """
    ally_list = (get_ally_list(guild_id)).split(', ')
    count = len(ally_list)
    return count


def get_base_units(combat_type):
    """
    Получение списка юнитов: персонажи или флот
    :input 'characters' or 'ships':
    :return массив с базой юнитов (DataFrame):
    """
    link = f'https://swgoh.gg/api/{combat_type}/'
    units = pd.json_normalize(requests.get(link).json())
    units = pd.DataFrame(units, index=None, columns=['base_id', 'name', 'power', 'image', 'combat_type'])
    units.loc[:, 'power'] = units.loc[:, 'power'].astype('int32')
    units.loc[:, 'combat_type'] = units.loc[:, 'combat_type'].astype('int8')
    units.set_axis(['unit_id', 'unit_name', 'max_power', 'url_image', 'combat_type'], axis='columns', inplace=True)
    units = units.sort_values(by=['unit_id']).reset_index(drop=True)
    return units


def get_base_abilities():
    """
    :return массив со всеми способностями (DataFrame):
    """
    link_abilities = 'https://swgoh.gg/api/abilities/'
    abilities = pd.json_normalize(requests.get(link_abilities).json())
    abilities = pd.DataFrame(
        data=abilities,
        index=None,
        columns=['base_id', 'name', 'character_base_id', 'ship_base_id', 'tier_max',  'is_zeta', 'is_omega', 'image']
    )
    abilities.set_axis(
        ['ability_id', 'ability_name', 'char_id', 'ship_id', 'tier_max', 'is_zeta', 'is_omega', 'url_image'],
        axis='columns',
        inplace=True
    )
    abilities.loc[:, 'tier_max'] = abilities.loc[:, 'tier_max'].astype('int8')
    abilities['unit_id'] = abilities['char_id'].combine_first(abilities['ship_id'])
    abilities = abilities[['ability_id', 'ability_name', 'unit_id', 'tier_max', 'is_zeta', 'is_omega', 'url_image']]
    abilities = abilities.sort_values(by=['unit_id', 'ability_id']).reset_index(drop=True)
    return abilities


def get_base_units_and_abilities():
    """
    :return три массива со всеми персонажами, флотом и способностями (DataFrame x3):
    """
    chars = get_base_units('characters')
    ships = get_base_units('ships')
    units = pd.concat([chars, ships]).sort_values(by=['combat_type']).reset_index(drop=True)
    abilities = get_base_abilities()
    return units, abilities


def sync_for_ally_list(ally_list):
    """
    Получение строки со списком кодов игроков

    :input ally_list (str):
    :return три массива игроки, персонажи, флот (DataFrame x3):
    """
    ally_list = ally_list.split(', ')
    data = pd.DataFrame(data=None, index=None)
    units = pd.DataFrame(data=None, index=None)
    for player in ally_list:
        data = pd.concat([data, get_data_player(int(player))])
        units = pd.concat([units, get_units_player(int(player))])
    data = data.sort_values(by=['player_name']).reset_index(drop=True)
    units = units.sort_values(by=['ally_code']).reset_index(drop=True)
    chars, ships = units_combat_type(units)
    return data, chars, ships


def sync_for_guild_id(guild_id):
    """
    Получение всех данных по гильдии

    :input guild_id (int):
    :return три массива игроки, персонажи, флот (DataFrame x3):
    """
    ally_list = get_ally_list(guild_id)
    data, chars, ships = sync_for_ally_list(ally_list)
    return data, chars, ships
