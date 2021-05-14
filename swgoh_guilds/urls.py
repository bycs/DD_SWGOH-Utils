from django.urls import include, path


urlpatterns = [
    path("im/", include("swgoh_guilds.im.urls")),
]
