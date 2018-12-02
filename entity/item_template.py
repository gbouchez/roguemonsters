from random import randint

from entity.item_entity import ItemType
from entity.status_effects import StatusEffectStrengthPotion
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

    @classmethod
    def get_level(cls):
        return 1

    @classmethod
    def get_p_at_level(cls, level):
        return 10


class EquipmentTemplate(ItemTemplate):
    accuracy = 0
    damage = 0
    evasion = 0
    shield_rate = 0
    shield_block = 0
    armor_value = 0
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
    item_type = ItemType.WEAPON
    hands = 1
    char = ')'

    @classmethod
    def get_level(cls):
        return 1 + max(0, (cls.damage - 13) // 3)

    @classmethod
    def get_p_at_level(cls, level):
        return min(10, max(0, 13 + level * 3 - cls.damage))


class ShieldTemplate(EquipmentTemplate):
    item_type = ItemType.SHIELD
    char = '('

    @classmethod
    def get_level(cls):
        return 1 + max(0, (cls.shield_block - 9) // 2)

    @classmethod
    def get_p_at_level(cls, level):
        return min(10, max(0, 9 + level * 2 - cls.shield_block))


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


class ClubTemplate(WeaponTemplate):
    name = 'club'
    description = 'A simple wooden club.'
    damage = 5
    weight = 4


class MaceTemplate(WeaponTemplate):
    name = 'mace'
    description = 'A simple mace.'
    damage = 9
    weight = 7


class HammerTemplate(WeaponTemplate):
    name = 'hammer'
    description = 'A simple hammer.'
    damage = 13
    weight = 10


class MorningstarTemplate(WeaponTemplate):
    name = 'morningstar'
    description = 'A morningstar.'
    damage = 17
    weight = 13


class FlailTemplate(WeaponTemplate):
    name = 'flail'
    damage = 21
    weight = 16
    description = 'A simple flail.'


class WarhammerTemplate(WeaponTemplate):
    name = 'warhammer'
    damage = 34
    weight = 39
    hands = 2
    description = 'A powerful warhammer.'


class DaggerTemplate(WeaponTemplate):
    name = 'dagger'
    damage = 4
    weight = 3
    description = 'A simple dagger.'


class ShortSwordTemplate(WeaponTemplate):
    name = 'short sword'
    damage = 7
    weight = 5
    description = 'A simple short sword.'


class LongSwordTemplate(WeaponTemplate):
    name = 'long sword'
    damage = 10
    weight = 7
    description = 'A simple long sword.'


class TwoHandedSwordTemplate(WeaponTemplate):
    name = 'two-handed sword'
    damage = 20
    weight = 21
    hands = 2
    description = 'A two-handed long sword.'


class WoodenShieldTemplate(ShieldTemplate):
    name = 'wooden shield'
    description = 'A small wooden shield.'
    shield_block = 5
    weight = 5


class BucklerTemplate(ShieldTemplate):
    name = 'buckler'
    description = 'A small buckler.'
    shield_block = 10
    weight = 10


class LeatherArmourTemplate(BodyTemplate):
    name = 'leather armour'
    description = 'An armour made of leather.'
    armor_value = 3
    weight = 6


class ScaleMailTemplate(BodyTemplate):
    name = 'scale mail'
    description = 'A scale mail.'
    armor_value = 6
    weight = 12


class ChainmailTemplate(BodyTemplate):
    name = 'chainmail'
    description = 'A chainmail.'
    armor_value = 10
    weight = 20


class PotionHealLightTemplate(PotionTemplate):
    name = 'potion of light healing'

    @classmethod
    def use(cls, item):
        super(PotionHealLightTemplate, cls).use(item)
        item.monster.heal(item.monster.get_constitution())


class PotionHealMediumTemplate(PotionTemplate):
    name = 'potion of medium healing'

    @classmethod
    def use(cls, item):
        super(PotionHealMediumTemplate, cls).use(item)
        item.monster.heal(item.monster.get_constitution() * 3)


class PotionHealHeavyTemplate(PotionTemplate):
    name = 'potion of heavy healing'

    @classmethod
    def use(cls, item):
        super(PotionHealHeavyTemplate, cls).use(item)
        item.monster.heal(item.monster.get_constitution() * 8)


class PotionStrengthTemplate(PotionTemplate):
    name = 'potion of strength'

    @classmethod
    def use(cls, item):
        super(PotionStrengthTemplate, cls).use(item)
        item.monster.add_status(StatusEffectStrengthPotion, 20)
