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
    gp_all = models.PositiveIntegerField(
        verbose_name='GP Total',
    )

    def __str__(self):
        return self.player_name


class GuildCharacter(models.Model):
    id = models.AutoField(primary_key=True)
    ally_code = models.PositiveIntegerField(
        verbose_name='Ally Code',
        db_index=True,
    )
    unit_id = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='Unit ID',
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


class GuildShip(models.Model):
    id = models.AutoField(primary_key=True)
    ally_code = models.PositiveIntegerField(
        verbose_name='Ally Code',
        db_index=True,
    )
    unit_id = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='Unit ID',
    )
    rarity = models.PositiveSmallIntegerField(
        verbose_name='Rarity',
    )
    power = models.PositiveIntegerField(
        verbose_name='Power',
    )
