from datetime import datetime, timezone
import pandas as pd
import requests

from .actions import get_arena_average_rank
from .player_sync import get_data_player, get_units_player


def get_guild_json(guild_id):
    """
    Получение json по гильдии

    :input guild_id (int):
    :return json:
    """
    url = f"https://swgoh.gg/api/guild/{guild_id}/"
    json_guild = requests.get(url).json()
    return json_guild


def get_ally_list(guild_id):
    """
    Получение списка кодов игроков гильдии

    :input guild_id (int):
    :return список с игроками гильдии (list(int)):
    """
    url = f"https://swgoh.gg/api/guild/{guild_id}/"
    ally_list = pd.json_normalize(requests.get(url).json()["players"]).loc[
        :, "data.ally_code"
    ]
    ally_list = list(ally_list)
    return ally_list


def get_ally_count(guild_id):
    """
    Подсчет количества игроков в гильдии

    :input guild_id (int):
    :return количетсво игроков в гильдии (int):
    """
    ally_list = get_ally_list(guild_id)
    count_players = len(ally_list)
    return count_players


def get_arena_average_rank_for_guild(df_guild_players_data):
    """
    Получение средних значений арен игрока

    :input data (DataFrame):
    :return (list(int) х2):
    """
    chars_arena = []
    ships_arena = []
    for ally in df_guild_players_data["ally_code"]:
        chars_arena_player, ships_arena_player = get_arena_average_rank(ally)
        chars_arena.append(chars_arena_player)
        ships_arena.append(ships_arena_player)
    return chars_arena, ships_arena


def get_data_guild(json_guild):
    """
    Получение информации о гильдии

    :input json_guild (json):
    :return  (DataFrame):
    """
    json_guild_data = json_guild["data"]
    guild_data = pd.DataFrame(
        data=pd.json_normalize(json_guild_data),
        index=None,
        columns=["id", "name", "galactic_power", "member_count"],
    )
    guild_data.set_axis(
        ["guild_id", "guild_name", "gp_total", "players_count"],
        axis="columns",
        inplace=True,
    )
    guild_data["last_sync"] = datetime.now().astimezone(tz=timezone.utc)
    return guild_data


def get_players_guild(json_guild_players):
    """
    Получение игроков гильдии

    :input json_guild_players (json):
    :return  (DataFrame):
    """
    data_players_guild = pd.DataFrame(data=None, index=None)
    for player in range(len(json_guild_players)):
        data_player = get_data_player(json_guild_players[player])
        data_players_guild = pd.concat([data_players_guild, data_player])
    data_players_guild = data_players_guild.sort_values(by=["player_name"]).reset_index(
        drop=True
    )
    chars_arena, ships_arena = get_arena_average_rank_for_guild(data_players_guild)
    data_players_guild["chars_average_rank"] = chars_arena
    data_players_guild["ships_average_rank"] = ships_arena
    return data_players_guild


def get_units_guild(json_guild_players):
    """
    Получение юнитов гильдии

    :input json_guild_players (json):
    :return  (DataFrame):
    """
    units_guild = pd.DataFrame(data=None, index=None)
    for player in range(len(json_guild_players)):
        units_player = get_units_player(json_guild_players[player])
        units_guild = pd.concat([units_guild, units_player])
    units_guild = units_guild.sort_values(by=["ally_code"]).reset_index(drop=True)
    return units_guild
