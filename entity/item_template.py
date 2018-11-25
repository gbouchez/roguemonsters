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
    accuracy = 0
    evasion = 0
    shield_rate = 0
    shield_block = 0
    armor_value = 0
    damage = 0
    equipable = True
    slot = None

    @classmethod
    def apply_template(cls, item):
        super(EquipmentTemplate, cls).apply_template(item)
        item.accuracy = cls.accuracy
        item.evasion = cls.evasion
        item.shield_rate = cls.shield_rate
        item.shield_block = cls.shield_block
        item.armor_value = cls.armor_value
        item.damage = cls.damage


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
    char = '('


class BodyTemplate(EquipmentTemplate):
    item_type = ItemType.BODY
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


class DaggerTemplate(WeaponTemplate):
    name = 'dagger'
    attack_speed = 70
    damage = 2
    description = 'A simple dagger.'
    weight = 4


class ShortSwordTemplate(WeaponTemplate):
    name = 'short sword'
    attack_speed = 90
    damage = 4
    description = 'A simple short sword.'
    weight = 8


class LongSwordTemplate(WeaponTemplate):
    name = 'long sword'
    attack_speed = 120
    damage = 8
    description = 'A simple long sword.'
    weight = 14


class FlailTemplate(WeaponTemplate):
    name = 'flail'
    attack_speed = 150
    damage = 12
    description = 'A simple flail.'
    weight = 20


class WoodenShieldTemplate(ShieldTemplate):
    name = 'wooden shield'
    description = 'A small wooden shield.'
    shield_block = 2
    weight = 5


class BucklerTemplate(ShieldTemplate):
    name = 'buckler'
    description = 'A small buckler.'
    shield_block = 3
    weight = 10


class LeatherArmourTemplate(BodyTemplate):
    name = 'leather armour'
    description = 'An armour made of leather.'
    armor_value = 2
    weight = 6


class ScaleMailTemplate(BodyTemplate):
    name = 'scale mail'
    description = 'A scale mail.'
    armor_value = 4
    weight = 9


class ChainmailTemplate(BodyTemplate):
    name = 'chainmail'
    description = 'A chainmail.'
    armor_value = 8
    weight = 16


class PotionHealLightTemplate(PotionTemplate):
    name = 'potion of light healing'

    @classmethod
    def use(cls, item):
        super(PotionHealLightTemplate, cls).use(item)
        heal_amount = randint(1, item.monster.get_constitution())
        heal_amount += randint(1, item.monster.get_constitution())
        heal_amount += randint(1, item.monster.get_constitution())
        heal_amount = max(5, int(heal_amount / 3))
        item.monster.heal(heal_amount)
