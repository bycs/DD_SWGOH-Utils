from django.db import models

from swgoh_sync.models.guild import GuildCharacter, GuildPlayersData, GuildShip


class Data(GuildPlayersData):
    pass


class Character(GuildCharacter):
    ally_code = models.ForeignKey(
        'im.Data',
        on_delete=models.CASCADE,
    )


class Ship(GuildShip):
    ally_code = models.ForeignKey(
        'im.Data',
        on_delete=models.CASCADE,
    )
