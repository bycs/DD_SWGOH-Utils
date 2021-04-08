from django.contrib import admin

from .models import Directory


class DirectoryAdmin(admin.ModelAdmin):
    list_display = [
        "ally_code",
        "player_name",
        "telegram_username",
        "discord_username",
        "phone_number",
    ]
    list_filter = ["player_name"]
    search_fields = ["player_name"]


admin.site.register(Directory, DirectoryAdmin)
