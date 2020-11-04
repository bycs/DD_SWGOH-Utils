"""
Импорт и структуризация данных с  сайта swgoh.gg через API
с использованием библиотеки pandas
"""

import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup


def get_player_json(ally_code):
    """
    Получение json по игроку

    :input ally_code (int):
    :return json:
    """
    link = f'https://swgoh.gg/api/player/{ally_code}/'
    json = requests.get(link).json()
    return json


def get_data_player(json):
    """
    Получение информации по игроку из json

    :input json:
    :return массив с данными о игроке (DataFrame):
    """
    data = json['data']
    data['last_updated'] = datetime.fromisoformat(data['last_updated'])
    data = pd.json_normalize(data)
    data = pd.DataFrame(
        data=data,
        index=None,
        columns=[
            'ally_code', 'name', 'character_galactic_power', 'ship_galactic_power', 'galactic_power', 'last_updated']
    )
    data.set_axis(
        ['ally_code', 'player_name', 'gp_chars', 'gp_ships', 'gp_total', 'last_updated'],
        axis='columns',
        inplace=True
    )
    data.loc[:, 'ally_code'] = data.loc[:, 'ally_code'].astype('int32')
    data.loc[:, 'gp_chars':'gp_total'] = data.loc[:, 'gp_chars':'gp_total'].astype('int32')
    return data


def get_units_player(json):
    """
    Получение списка персонажей по игроку из json

    :input json:
    :return массив с персонажами (DataFrame):
    """
    units = pd.json_normalize(json, 'units', [['data', 'name'], ['data', 'ally_code']],
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
    return characters.reset_index(drop=True)


def units_type_ships(units):
    """
    Отбор из юнитов только флот

    :input units (DataFrame):
    :return массив с флотом (DataFrame):
    """
    ships = units[units['combat_type'] == 2]
    ships = ships.loc[:, ['ally_code', 'unit_id', 'rarity', 'power']]
    return ships.reset_index(drop=True)


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
    Получение списка кодов игроков гильдии

    :input guild_id (int):
    :return список с игроками гильдии (list(int)):
    """
    link = f'https://swgoh.gg/api/guild/{guild_id}/'
    ally_list = pd.json_normalize(
        requests.get(link).json()['players']).loc[:, 'data.ally_code']
    ally_list = list(ally_list)
    return ally_list


def get_ally_count(guild_id):
    """
    Подсчет количества игроков в гильдии

    :input guild_id (int):
    :return количетсво игроков в гильдии (int):
    """
    ally_list = get_ally_list(guild_id)
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


def get_arena_average_rank(ally_code):
    """
    Получение средних значений арен игрока

    :input ally_code (int):
    :return (int х2):
    """
    url = f'https://swgoh.gg/p/{ally_code}/'
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    value_average_rank = soup.find_all("div", {"class": "stat-item-value"})
    value_list = []
    for i in value_average_rank:
        value_list.append(i.get_text())
    if len(value_list) > 5:
        chars_arena_rank = value_list[2]
        ships_arena_rank = value_list[5]
    else:
        value_current_rank = soup.find_all("div", {"class": "current-rank-value"})
        value_list = []
        for i in value_current_rank:
            value_list.append(i.get_text())
        chars_arena_rank = value_list[0]
        ships_arena_rank = value_list[1]
    return chars_arena_rank, ships_arena_rank


def get_arena_average_rank_for_list(data):
    """
    Получение средних значений арен игрока

    :input data (DataFrame):
    :return (list(int) х2):
    """
    chars_arena = []
    ships_arena = []
    for ally in data['ally_code']:
        chars_arena_player, ships_arena_player = get_arena_average_rank(ally)
        chars_arena.append(chars_arena_player)
        ships_arena.append(ships_arena_player)
    return chars_arena, ships_arena


def sync_for_ally_list(ally_list):
    """
    Получение списка кодов игроков

    :input ally_list (list(int)):
    :return три массива игроки, персонажи, флот (DataFrame x3):
    """
    data = pd.DataFrame(data=None, index=None)
    units = pd.DataFrame(data=None, index=None)
    for player in ally_list:
        json = get_player_json(player)
        data = pd.concat([data, get_data_player(json)])
        units = pd.concat([units, get_units_player(json)])
    data = data.sort_values(by=['player_name']).reset_index(drop=True)
    chars_arena, ships_arena = get_arena_average_rank_for_list(data)
    data['chars_average_rank'] = chars_arena
    data['ships_average_rank'] = ships_arena
    units = units.sort_values(by=['ally_code']).reset_index(drop=True)
    chars, ships = units_combat_type(units)
    return data, chars, ships


def sync_for_guild_id(guild_id):
    """
    Получение всех данных по гильдии

    :input guild_id (int):
    :return три массива игроки, персонажи, флот (DataFrame x3):
    """
    link = f'https://swgoh.gg/api/guild/{guild_id}/'
    json = requests.get(link).json()['players']
    data = pd.DataFrame(data=None, index=None)
    units = pd.DataFrame(data=None, index=None)
    for player in range(len(json)):
        data_player = get_data_player(json[player])
        units_player = get_units_player(json[player])
        data = pd.concat([data, data_player])
        units = pd.concat([units, units_player])
    data = data.sort_values(by=['player_name']).reset_index(drop=True)
    chars_arena, ships_arena = get_arena_average_rank_for_list(data)
    data['chars_average_rank'] = chars_arena
    data['ships_average_rank'] = ships_arena
    units = units.sort_values(by=['ally_code']).reset_index(drop=True)
    chars, ships = units_combat_type(units)
    return data, chars, ships
