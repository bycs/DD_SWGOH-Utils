from django.db import models


class Unit(models.Model):
    unit_id = models.CharField(max_length=100)
    unit_name = models.CharField(max_length=100)
    max_power = models.PositiveIntegerField
    url_image = models.CharField(max_length=255)
    combat_type = models.PositiveSmallIntegerField

    def __str__(self):
        return self.unit_name


class Ability(models.Model):
    ability_id = models.CharField(max_length=100)
    ability_name = models.CharField(max_length=100)
    combat_type = models.PositiveSmallIntegerField
    char_id = models.CharField(max_length=100)
    ship_id = models.CharField(max_length=100)
    tier_max = models.PositiveSmallIntegerField
    is_zeta = models.BooleanField
    is_omega = models.BooleanField
    url_image = models.CharField(max_length=255)

    def __str__(self):
        return self.ability_name
