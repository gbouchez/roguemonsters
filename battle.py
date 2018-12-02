from math import floor
from random import randint

import tcod
from numpy import average
from numpy.random.mtrand import randint

from game_log import add_log_message, LogMessage, get_monster_message_prefix
from messages.messages import get_message


def attack(attacker, target):
    message_key_prefix = get_monster_message_prefix(attacker)

    roll = make_attack_roll(attacker)
    evasion = target.get_evasion()
    roll -= evasion
    if roll <= 0:
        add_log_message(
            LogMessage(
                get_message(message_key_prefix + "miss_dodge")
                .format(str.capitalize(attacker.get_name()), target.get_name()),
                tcod.grey
            )
        )
        return

    damage = make_damage_roll(attacker)
    if damage <= target.get_shield_block():
        shield = target.get_shield_rate()
        roll -= shield
        if roll <= 0:
            add_log_message(
                LogMessage(
                    get_message(message_key_prefix + "miss_block")
                    .format(str.capitalize(attacker.get_name()), target.get_name()),
                    tcod.grey
                )
            )
            return

    armor = target.get_armor_value()
    if armor >= 1:
        damage -= randint(0, armor)
    if damage <= 0:
        add_log_message(
            LogMessage(
                get_message(message_key_prefix + "miss_armor")
                .format(str.capitalize(attacker.get_name()), target.get_name()),
                tcod.grey
            )
        )
        return

    add_log_message(
        LogMessage(
            get_message(message_key_prefix + "hit")
            .format(str.capitalize(attacker.get_name()), target.get_name(), damage),
            tcod.white
        )
    )
    target.take_damage(damage, attacker)
    attacker.apply_attack_effect(target)


def make_attack_roll(monster):
    roll = randint(1, max(1, monster.get_accuracy()))
    return roll


def make_damage_roll(monster):
    return int(average(randint(1, monster.get_damage(), 10)))
