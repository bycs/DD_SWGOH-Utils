import pandas as pd
import requests


def get_base_units_combat_type(combat_type):
    """
    Получение типа юнитов: персонажи или флот

    :input 'characters' or 'ships':
    :return массив с базой юнитов (DataFrame):
    """
    url = f'https://swgoh.gg/api/{combat_type}/'
    units = pd.json_normalize(requests.get(url).json())
    units = pd.DataFrame(
        data=units,
        index=None,
        columns=['base_id', 'name', 'power', 'image', 'combat_type'])
    units.loc[:, 'power'] = units.loc[:, 'power'].astype('int32')
    units.loc[:, 'combat_type'] = units.loc[:, 'combat_type'].astype('int8')
    units.set_axis([
        'unit_id', 'unit_name', 'max_power', 'url_image', 'combat_type'
    ],
        axis='columns', inplace=True)
    units = units.sort_values(by=['unit_id']).reset_index(drop=True)
    return units


def get_base_units():
    """
    :return массив со всеми юнитами (DataFrame):
    """
    chars = get_base_units_combat_type('characters')
    ships = get_base_units_combat_type('ships')
    units = pd.concat([chars, ships]).sort_values(
        by=['combat_type']).reset_index(drop=True)
    return units


def get_base_abilities():
    """
    :return массив со всеми способностями (DataFrame):
    """
    url_abilities = 'https://swgoh.gg/api/abilities/'
    abilities = pd.json_normalize(requests.get(url_abilities).json())
    abilities = pd.DataFrame(
        data=abilities,
        index=None,
        columns=['base_id', 'name', 'character_base_id', 'ship_base_id',
                 'tier_max',  'is_zeta', 'is_omega', 'image'
                 ])
    abilities.set_axis(
        ['ability_id', 'ability_name', 'char_id', 'ship_id',
         'tier_max', 'is_zeta', 'is_omega', 'url_image'],
        axis='columns',
        inplace=True
    )
    abilities.loc[:, 'tier_max'] = abilities.loc[:, 'tier_max'].astype('int8')
    abilities['unit_id'] = abilities['char_id'].combine_first(abilities['ship_id'])
    abilities = abilities[[
        'ability_id', 'ability_name', 'unit_id', 'tier_max',
        'is_zeta', 'is_omega', 'url_image'
    ]]
    abilities = abilities.drop_duplicates(subset=['ability_id'])
    abilities = abilities.sort_values(by=['unit_id', 'ability_id']).reset_index(drop=True)
    return abilities
