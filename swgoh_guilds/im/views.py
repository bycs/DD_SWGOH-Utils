from django.shortcuts import render

from swgoh_sync.models import guilds
from swgoh_guilds.im import models


def im_index(request):
    return render(request, "im_index.html")


def data(request):
    guild_name = "Imperial Military"
    players = models.Data.guild_players_data_manager.all()
    return render(
        request, "im_data.html", {"guild_name": guild_name, "players": players}
    )


def sync_guld_data(request):
    guilds.GuildsData.guilds_data_managers.sync_to_db(8187)
    models.Data.guild_players_data_manager.sync_to_db(8187)
    return render(request, "im_index.html")
