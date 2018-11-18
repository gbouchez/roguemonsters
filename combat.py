import math
from enum import Enum
from random import randint

import tcod

from game_log import add_log_message, LogMessage, get_monster_message_prefix
from messages.messages import get_message


def attack(attacker, target):
    message_key_prefix = get_monster_message_prefix(attacker)

    roll = make_attack_roll(attacker)
    dodge = target.get_dodge_components()
    dodge_value = sum(dodge.values())
    roll -= dodge_value
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

    armor = target.get_armor_components()
    armor_value = sum(armor.values())
    roll -= armor_value
    if roll <= 0:
        armor_reduction = randint(0, target.get_armor_reduction())
        damage -= armor_reduction
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
                get_message(message_key_prefix + "hit_armor")
                .format(str.capitalize(attacker.get_name()), target.get_name(), damage),
                tcod.white
            )
        )
        target.take_damage(damage)
        return
    add_log_message(
        LogMessage(
            get_message(message_key_prefix + "hit")
            .format(str.capitalize(attacker.get_name()), target.get_name(), damage),
            tcod.white
        )
    )
    target.take_damage(damage)



def make_attack_roll(monster):
    roll = randint(1, max(1, monster.get_accuracy()))
    return roll

def make_damage_roll(monster):
    roll = randint(1, monster.get_damage())
    roll += randint(1, monster.get_damage())
    roll += randint(1, monster.get_damage())
    return int(roll / 3)
