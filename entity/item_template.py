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
    weight = 0
    equipable = True
    slot = None

    @classmethod
    def apply_template(cls, item):
        super(EquipmentTemplate, cls).apply_template(item)
        item.damage = cls.damage
        item.accuracy = cls.accuracy
        item.armor_rate = cls.armor_rate
        item.armor_reduction = cls.armor_reduction


class WeaponTemplate(EquipmentTemplate):
    attack_speed = 100
    item_type = ItemType.WEAPON
    char = ')'


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
    accuracy = 0
    description = 'A simple short sword.'
    weight = 8


class LongSwordTemplate(WeaponTemplate):
    name = 'long sword'
    attack_speed = 120
    damage = 6
    accuracy = -5
    description = 'A simple long sword.'
    weight = 20


class FlailTemplate(WeaponTemplate):
    name = 'flail'
    attack_speed = 90
    damage = 12
    accuracy = -10
    description = 'A simple flail.'
    weight = 30


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
