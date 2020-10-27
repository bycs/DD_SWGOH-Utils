from django.db import models


class BaseUnit(models.Model):
    unit_id = models.CharField(
        max_length=100,
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
    combat_type = models.PositiveSmallIntegerField(
        verbose_name='Combat Type',
        editable=False,
    )

    def __str__(self):
        return self.unit_name


class BaseAbility(models.Model):
    ability_id = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='Ability ID',
    )
    ability_name = models.CharField(
        max_length=100,
        verbose_name='Ability Name',
    )
    unit_id = models.CharField(
        max_length=100,
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
