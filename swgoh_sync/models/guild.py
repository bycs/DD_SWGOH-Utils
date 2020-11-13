from django.db import models
from swgoh_sync.managers.guild import GuildCharacterManager, GuildPlayersDataManager, GuildShipManager


class GuildPlayersData(models.Model):
    ally_code = models.PositiveIntegerField(
        db_index=True,
        primary_key=True,
        verbose_name='Ally Code',
    )
    player_name = models.CharField(
        max_length=100,
        verbose_name='Player Name',
    )
    gp_chars = models.PositiveIntegerField(
        verbose_name='GP Characters',
    )
    gp_ships = models.PositiveIntegerField(
        verbose_name='GP Ships',
    )
    gp_total = models.PositiveIntegerField(
        verbose_name='GP Total',
    )
    last_updated = models.DateTimeField(
        verbose_name='Last Updated',
    )
    chars_average_rank = models.PositiveSmallIntegerField(
        verbose_name='Chars Arena',
    )
    ships_average_rank = models.PositiveSmallIntegerField(
        verbose_name='Ships Arena',
    )

    guild_players_data_manager = GuildPlayersDataManager()

    def __str__(self):
        return self.player_name

    class Meta:
        abstract = True
        verbose_name = 'Guild Players Data'
        verbose_name_plural = 'Guild Players Data'


class GuildCharacter(models.Model):
    id = models.AutoField(primary_key=True)
    ally_code = models.ForeignKey(
        '.GuildPlayersData',
        on_delete=models.CASCADE,
    )
    unit_id = models.ForeignKey(
        'swgoh_sync.BaseUnit',
        on_delete=models.CASCADE,
    )
    rarity = models.PositiveSmallIntegerField(
        verbose_name='Rarity',
    )
    gear_level = models.PositiveSmallIntegerField(
        verbose_name='Gear Level',
    )
    RELIC_TIER_CHOICES = [
        (1, 0),
        (2, 0),
        (3, 1),
        (4, 2),
        (5, 3),
        (6, 4),
        (7, 5),
        (8, 6),
        (9, 7),
    ]
    relic_tier = models.PositiveSmallIntegerField(
        choices=RELIC_TIER_CHOICES,
        verbose_name='Relic Tier',
    )
    power = models.PositiveIntegerField(
        verbose_name='Power',
    )
    health = models.PositiveIntegerField(
        verbose_name='Health',
    )
    protection = models.PositiveIntegerField(
        verbose_name='Protection',
    )
    speed = models.PositiveSmallIntegerField(
        verbose_name='Speed',
    )
    physical_damage = models.PositiveSmallIntegerField(
        verbose_name='Physical Damage',
    )
    critical_damage = models.FloatField(
        verbose_name='Critical Damage',
    )
    critical_chance = models.FloatField(
        verbose_name='Critical Chance',
    )
    potency = models.FloatField(
        verbose_name='Potency',
    )
    tenacity = models.FloatField(
        verbose_name='Tenacity',
    )

    guild_character_manager = GuildCharacterManager()

    class Meta:
        abstract = True
        verbose_name = 'Guild Character'
        verbose_name_plural = 'Guild Characters'


class GuildShip(models.Model):
    id = models.AutoField(primary_key=True)
    ally_code = models.ForeignKey(
        '.GuildPlayersData',
        on_delete=models.CASCADE,
    )
    unit_id = models.ForeignKey(
        'swgoh_sync.BaseUnit',
        on_delete=models.CASCADE,
    )
    rarity = models.PositiveSmallIntegerField(
        verbose_name='Rarity',
    )
    power = models.PositiveIntegerField(
        verbose_name='Power',
    )

    guild_ship_manager = GuildShipManager()

    class Meta:
        abstract = True
        verbose_name = 'Guild Ship'
        verbose_name_plural = 'Guild Ships'
