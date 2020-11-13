from django.db import models
from swgoh_sync.managers.base import BaseAbilityManager, BaseUnitManager


class BaseUnit(models.Model):
    unit_id = models.CharField(
        db_index=True,
        max_length=100,
        primary_key=True,
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
        editable=False,
        max_length=255,
        verbose_name='URL Image',
    )
    COMBAT_TYPE_CHOICES = [
        (1, 'Character'),
        (2, 'Ship'),
    ]
    combat_type = models.PositiveSmallIntegerField(
        blank=True,
        choices=COMBAT_TYPE_CHOICES,
        editable=False,
        verbose_name='Combat Type',
    )

    base_unit_manager = BaseUnitManager()

    class Meta:
        verbose_name = 'Unit'
        verbose_name_plural = 'Units'

    def __str__(self):
        return self.unit_name


class BaseAbility(models.Model):
    ability_id = models.CharField(
        db_index=True,
        max_length=100,
        primary_key=True,
        verbose_name='Ability ID',
    )
    ability_name = models.CharField(
        max_length=100,
        verbose_name='Ability Name',
    )
    unit_id = models.CharField(
        db_index=True,
        max_length=100,
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
        editable=False,
        max_length=255,
        verbose_name='URL Image',
    )

    base_ability_manager = BaseAbilityManager()

    class Meta:
        verbose_name = 'Ability'
        verbose_name_plural = 'Abilities'

    def __str__(self):
        return self.ability_name
