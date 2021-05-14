from django.shortcuts import render

import swgoh_sync.models.guilds
import swgoh_guilds.im.models


def im_index(request):
    return render(request, "im_index.html")


def data(request):
    guild_name = "Imperial Military"
    players = swgoh_guilds.im.models.Data.guild_players_data_manager.all()
    return render(
        request, "im_data.html", {"guild_name": guild_name, "players": players}
    )


def sync_guld_data(request):
    swgoh_sync.models.guilds.GuildsData.guilds_data_managers.sync_to_db(8187)
    swgoh_guilds.im.models.Data.guild_players_data_manager.sync_to_db(8187)
    return render(request, "im_index.html")
