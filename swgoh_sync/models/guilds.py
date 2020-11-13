from django.db import models

from swgoh_sync.managers.guilds import GuildsDataManager


class GuildsData(models.Model):
    guild_id = models.PositiveIntegerField(
        db_index=True,
        primary_key=True,
        verbose_name='Guild ID',
    )
    guild_name = models.CharField(
        db_index=True,
        max_length=100,
        verbose_name='Guild Name',
    )
    gp_total = models.PositiveIntegerField(
        verbose_name='GP Total',
    )
    players_count = models.PositiveIntegerField(
        verbose_name='Players Count',
    )
    last_sync = models.DateTimeField(
        verbose_name='Last Sync',
    )
    json_data_and_units = models.JSONField(
        blank=True,
        editable=False,
        null=True,
        verbose_name='JSON with data and players',
    )

    guilds_data_managers = GuildsDataManager()

    def __str__(self):
        return self.guild_name

    class Meta:
        verbose_name = 'Guilds Data'
        verbose_name_plural = 'Guilds Data'
