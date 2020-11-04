from django.db import models


class BaseUnit(models.Model):
    unit_id = models.CharField(
        max_length=100,
        primary_key=True,
        db_index=True,
        verbose_name='Unit ID',
    )
    unit_name = models.CharField(
        max_length=100,
        verbose_name='Unit Name',
    )
    max_power = models.PositiveIntegerField(
        verbose_name='Max Power',
    )
    url_image = models.CharField(
        max_length=255,
        verbose_name='URL Image',
        editable=False,
    )
    COMBAT_TYPE_CHOICES = [
        (1, ''),
        (2, ''),
    ]
    combat_type = models.PositiveSmallIntegerField(
        verbose_name='Combat Type',
        choices=COMBAT_TYPE_CHOICES,
        editable=False,
    )

    class Meta:
        verbose_name = 'Unit'
        verbose_name_plural = 'Units'

    def __str__(self):
        return self.unit_name


class BaseAbility(models.Model):
    ability_id = models.CharField(
        max_length=100,
        primary_key=True,
        db_index=True,
        verbose_name='Ability ID',
    )
    ability_name = models.CharField(
        max_length=100,
        verbose_name='Ability Name',
    )
    unit_id = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='Unit ID',
    )
    tier_max = models.PositiveSmallIntegerField(
        verbose_name='Max Tier',
    )
    is_zeta = models.BooleanField(
        db_index=True,
        verbose_name='is Zeta',
    )
    is_omega = models.BooleanField(
        verbose_name='is Omega',
    )
    url_image = models.CharField(
        max_length=255,
        verbose_name='URL Image',
        editable=False,
    )

    class Meta:
        verbose_name = 'Ability'
        verbose_name_plural = 'Abilities'

    def __str__(self):
        return self.ability_name


class GuildData(models.Model):
    ally_code = models.PositiveIntegerField(
        primary_key=True,
        db_index=True,
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

    def __str__(self):
        return self.player_name

    class Meta:
        verbose_name = 'Guild Data'
        verbose_name_plural = 'Guild Data'
        abstract = True


class GuildCharacter(models.Model):
    id = models.AutoField(primary_key=True)
    ally_code = models.ForeignKey(
        'sync_swgoh.GuildData',
        on_delete=models.CASCADE,
    )
    unit_id = models.ForeignKey(
        'sync_swgoh.BaseUnit',
        on_delete=models.CASCADE,
    )
    rarity = models.PositiveSmallIntegerField(
        verbose_name='Rarity',
    )
    gear_level = models.PositiveSmallIntegerField(
        verbose_name='Gear Level',
    )
    relic_tier = models.PositiveSmallIntegerField(
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

    class Meta:
        verbose_name = 'Guild Character'
        verbose_name_plural = 'Guild Characters'
        abstract = True


class GuildShip(models.Model):
    id = models.AutoField(primary_key=True)
    ally_code = models.ForeignKey(
        'sync_swgoh.GuildData',
        on_delete=models.CASCADE,
    )
    unit_id = models.ForeignKey(
        'sync_swgoh.BaseUnit',
        on_delete=models.CASCADE,
    )
    rarity = models.PositiveSmallIntegerField(
        verbose_name='Rarity',
    )
    power = models.PositiveIntegerField(
        verbose_name='Power',
    )

    class Meta:
        verbose_name = 'Guild Ship'
        verbose_name_plural = 'Guild Ships'
        abstract = True
