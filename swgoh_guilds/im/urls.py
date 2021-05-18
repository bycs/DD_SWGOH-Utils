from django.urls import path

from swgoh_guilds.im import views

urlpatterns = [
    path("", views.im_index, name="im_index"),
    path("data/", views.data, name="im_data"),
    path("sync_guld_data/", views.sync_guld_data, name="im_sync_guld_data"),
]
