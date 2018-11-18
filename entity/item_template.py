from entity.item_entity import ItemType


class ItemTemplate:
    item_type = None
    char = '?'
    name = ''
    color = 255, 255, 255


class EquipmentTemplate(ItemTemplate):
    attack = 0
    accuracy = 0
    armor_rate = 0
    armor_reduction = 0

    @classmethod
    def apply_template(cls, equipment):
        equipment.attack = cls.attack
        equipment.accuracy = cls.accuracy
        equipment.armor_rate = cls.armor_rate
        equipment.armor_reduction = cls.armor_reduction


class WeaponTemplate(EquipmentTemplate):
    attack_speed = 100
    item_type = ItemType.WEAPON
    char = ')'
    pass


class ShortSwordTemplate(WeaponTemplate):
    name = 'short sword'
    attack_speed = 90
    attack = 3
    accuracy = 0
    description = 'A simple short sword.'
