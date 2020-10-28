from django.db import models

from sync_swgoh.models import GuildData, GuildCharacter, GuildShip


class IMData(GuildData):
    pass


class IMCharacter(GuildCharacter):
    ally_code = models.ForeignKey(
        'guild_im.IMData',
        on_delete=models.CASCADE,
    )


class IMShip(GuildShip):
    ally_code = models.ForeignKey(
        'guild_im.IMData',
        on_delete=models.CASCADE,
    )