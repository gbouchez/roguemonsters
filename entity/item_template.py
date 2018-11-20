from random import randint

from entity.item_entity import ItemType
from game_log import add_log_message, LogMessage, get_monster_message_prefix
from messages.messages import get_message


class ItemTemplate:
    item_type = None
    char = '?'
    name = ''
    color = 255, 255, 255
    usable = False
    equipable = False
    weight = 0

    @classmethod
    def apply_template(cls, item):
        item.usable = cls.usable
        item.equipable = cls.equipable

    @classmethod
    def use(cls, item):
        pass


class EquipmentTemplate(ItemTemplate):
    damage = 0
    accuracy = 0
    armor_rate = 0
    armor_reduction = 0
    shield_rate = 0
    shield_block = 0
    equipable = True
    slot = None

    @classmethod
    def apply_template(cls, item):
        super(EquipmentTemplate, cls).apply_template(item)
        item.damage = cls.damage
        item.accuracy = cls.accuracy
        item.armor_rate = cls.armor_rate
        item.armor_reduction = cls.armor_reduction
        item.shield_rate = cls.shield_rate
        item.shield_block = cls.shield_block


class WeaponTemplate(EquipmentTemplate):
    attack_speed = 100
    damage = 1
    item_type = ItemType.WEAPON
    char = ')'

    @classmethod
    def apply_template(cls, item):
        super(WeaponTemplate, cls).apply_template(item)
        item.attack_speed = cls.attack_speed


class ShieldTemplate(EquipmentTemplate):
    item_type = ItemType.SHIELD
    shield_rate = 10
    shield_block = 2
    char = '('


class BodyTemplate(EquipmentTemplate):
    item_type = ItemType.BODY
    armor_rate = 40
    armor_reduction = 1
    char = '='


class PotionTemplate(ItemTemplate):
    usable = True
    item_type = ItemType.POTION
    char = '!'

    @classmethod
    def use(cls, item):
        add_log_message(
            LogMessage(
                get_message(get_monster_message_prefix(item.monster) + 'item.potion.use')
                .format(str.capitalize(item.monster.get_name()), item.get_name())
            )
        )


class ShortSwordTemplate(WeaponTemplate):
    name = 'short sword'
    attack_speed = 90
    damage = 3
    description = 'A simple short sword.'
    weight = 10


class LongSwordTemplate(WeaponTemplate):
    name = 'long sword'
    attack_speed = 120
    damage = 6
    description = 'A simple long sword.'
    weight = 20


class FlailTemplate(WeaponTemplate):
    name = 'flail'
    attack_speed = 150
    damage = 9
    description = 'A simple flail.'
    weight = 30


class WoodenShieldTemplate(ShieldTemplate):
    name = 'wooden shield'
    description = 'A small wooden shield.'
    shield_rate = 10
    shield_block = 2
    weight = 5


class BucklerTemplate(ShieldTemplate):
    name = 'buckler'
    description = 'A small buckler.'
    shield_rate = 10
    shield_block = 3
    weight = 10


class LeatherArmourTemplate(BodyTemplate):
    name = 'leather armour'
    description = 'An armour made of leather.'
    armor_rate = 40
    armor_reduction = 4
    weight = 8


class ScaleMailTemplate(BodyTemplate):
    name = 'scale mail'
    description = 'A scale mail.'
    armor_rate = 45
    armor_reduction = 6
    weight = 12


class ChainmailTemplate(BodyTemplate):
    name = 'chainmail'
    description = 'A chainmail.'
    armor_rate = 50
    armor_reduction = 8
    weight = 16


class PotionHealLightTemplate(PotionTemplate):
    name = 'potion of light healing'

    @classmethod
    def use(cls, item):
        super(PotionHealLightTemplate, cls).use(item)
        heal_amount = randint(1, item.monster.get_constitution())
        heal_amount += randint(1, item.monster.get_constitution())
        heal_amount += randint(1, item.monster.get_constitution())
        heal_amount = int(heal_amount / 3)
        item.monster.heal(heal_amount)
