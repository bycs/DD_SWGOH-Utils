class TemplateUnit(object):
    def __init__(self, unit_id, rarity, power):
        self.unit_id = unit_id
        self.rarity = rarity
        self.power = power


class TemplateUnitChar(TemplateUnit):
    def __init__(self, unit_id, rarity, gear_level, relic_tier, power):
        super().__init__(unit_id, rarity, power)
        self.gear_level = gear_level
        self.relic_tier = relic_tier


class TemplateUnitShip(TemplateUnit):
    pass
