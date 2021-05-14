from django.urls import path

import swgoh_guilds.im.views

urlpatterns = [
    path("", swgoh_guilds.im.views.im_index),
    path("data/", swgoh_guilds.im.views.data),
    path("sync_guld_data/", swgoh_guilds.im.views.sync_guld_data),
]
