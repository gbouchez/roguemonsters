import tcod
from enum import Enum
from random import randint
from combat import attack
from entity.status_effects import StatusEffectRage, StatusEffectSoulbound, StatusEffectFatigue
from game_log import add_log_message, LogMessage, get_monster_message_prefix
from messages.messages import get_message


class AbilityTargeting(Enum):
    SELF = 1
    LOS = 2


class BattleAbility:
    name = ''
    hidden = False
    targeting = AbilityTargeting.SELF
    targeting_distance = 0

    @staticmethod
    def reset_turn(monster):
        pass

    @classmethod
    def use_ability(cls, monster, target):
        pass

    @staticmethod
    def meet_prerequisites(monster, target):
        pass

    @staticmethod
    def get_weight(monster, target):
        return 1

    @classmethod
    def get_name(cls):
        return cls.name


class BattleAbilitySoulSteal(BattleAbility):
    name = 'Soul steal'
    targeting = AbilityTargeting.LOS
    targeting_distance = 2

    @staticmethod
    def reset_turn(monster):
        monster.reset_turn(200)

    @classmethod
    def use_ability(cls, monster, target):
        cls.reset_turn(monster)
        if monster == target or target.has_status(StatusEffectSoulbound):
            add_log_message(
                LogMessage(
                    get_message('soulsteal.fail'),
                    tcod.white
                )
            )
            return
        success_roll = randint(1, monster.get_soul_power() + target.get_soul_power())
        success = success_roll <= monster.get_soul_power()
        if not success:
            add_log_message(
                LogMessage(
                    get_message('soulsteal.fail'),
                    tcod.white
                )
            )
            return
        monster.game_map.take_over_monster(monster.player, monster=target)
        cls.reset_turn(target)
        soulbound_turns = monster.get_soul_power() + target.get_soul_power()
        monster.status_effects.append(StatusEffectSoulbound(monster, soulbound_turns * randint(27, 33)))
        target.status_effects.append(StatusEffectSoulbound(target, soulbound_turns * randint(9, 11)))

    @staticmethod
    def meet_prerequisites(monster, target):
        return False

    @staticmethod
    def get_weight(monster, target):
        return 0


class BattleAbilityMoveToPlayer(BattleAbility):
    name = ''
    hidden = True

    @staticmethod
    def reset_turn(monster):
        monster.reset_turn(monster.land_speed)

    @classmethod
    def use_ability(cls, monster, target):
        monster.move_astar(target)
        monster.target = target
        cls.reset_turn(monster)

    @staticmethod
    def meet_prerequisites(monster, target):
        if monster.distance_to(target) >= 2:
            return True
        return False

    @staticmethod
    def get_weight(monster, target):
        return 1


class BattleAbilityAttackPlayer(BattleAbility):
    name = ''
    hidden = True

    @staticmethod
    def reset_turn(monster):
        monster.reset_turn(monster.get_attack_speed())

    @classmethod
    def use_ability(cls, monster, target):
        monster.target = target
        attack(monster, target)
        cls.reset_turn(monster)

    @staticmethod
    def meet_prerequisites(monster, target):
        if monster.distance_to(target) < 2 and target.get_hp() > 0:
            return True
        return False

    @staticmethod
    def get_weight(monster, target):
        return 1


class BattleAbilityPickItemUp(BattleAbility):
    name = ''
    hidden = True

    @staticmethod
    def reset_turn(monster):
        monster.reset_turn(100)

    @classmethod
    def use_ability(cls, monster, target):
        items = monster.game_map.get_items_at(monster.x, monster.y)
        if not items:
            add_log_message(
                LogMessage(
                    get_message(get_monster_message_prefix(monster) + 'pickup_item.none'),
                    tcod.dark_grey
                )
            )
        else:
            item = items.pop()
            monster.inventory.add_item(item)
            add_log_message(
                LogMessage(
                    get_message(get_monster_message_prefix(monster) + 'pickup_item')
                    .format(monster.get_name(), item.get_name()),
                    tcod.white
                )
            )
        cls.reset_turn(monster)

    @staticmethod
    def meet_prerequisites(monster, target):
        items = monster.game_map.get_items_at(monster.x, monster.y)
        if not items:
            return False
        return True

    @staticmethod
    def get_weight(monster, target):
        return 0.1


class BattleAbilityRage(BattleAbility):
    name = 'Rage'

    @staticmethod
    def reset_turn(monster):
        monster.reset_turn(150 - monster.get_constitution())

    @classmethod
    def use_ability(cls, monster, target):
        monster.status_effects.append(StatusEffectRage(monster, int(monster.get_constitution() / 2)))
        cls.reset_turn(monster)

    @staticmethod
    def meet_prerequisites(monster, target):
        if monster.has_status(StatusEffectRage) or monster.has_status(StatusEffectFatigue):
            return False
        if monster.distance_to(target) < 2:
            return True
        return False

    @staticmethod
    def get_weight(monster, target):
        return 2 - (monster.get_hp() / monster.get_max_hp()) * 2
