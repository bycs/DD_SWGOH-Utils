from bs4 import BeautifulSoup
import requests


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
    for value in value_average_rank:
        value_list.append(value.get_text())
    if len(value_list) > 5:
        chars_arena_rank = value_list[2]
        ships_arena_rank = value_list[5]
    else:
        value_current_rank = soup.find_all("div", {"class": "current-rank-value"})
        value_list = []
        for value in value_current_rank:
            value_list.append(value.get_text())
        chars_arena_rank = value_list[0]
        ships_arena_rank = value_list[1]
    return chars_arena_rank, ships_arena_rank


def split_units_type_by_chars(units):
    """
    Отбор из юнитов только персонажей

    :input units (DataFrame):
    :return массив с персонажами (DataFrame):
    """
    characters = units[units['combat_type'] == 1]
    del characters['combat_type']
    return characters.reset_index(drop=True)


def split_units_type_by_ships(units):
    """
    Отбор из юнитов только флот

    :input units (DataFrame):
    :return массив с флотом (DataFrame):
    """
    ships = units[units['combat_type'] == 2]
    ships = ships.loc[:, ['ally_code', 'unit_id', 'rarity', 'power']]
    return ships.reset_index(drop=True)


def split_units_combat_type(units):
    """
    Разделение юнитов по классам (персонажи и флот)

    :input units (DataFrame):
    :return два массива: с персонажами и флотом (DataFrame x2):
    """
    characters = split_units_type_by_chars(units)
    ships = split_units_type_by_ships(units)
    return characters, ships
