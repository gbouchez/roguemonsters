import tcod
from enum import Enum
from random import randint
from battle import attack
from entity.status_effects import StatusEffectRage, StatusEffectSoulbound, StatusEffectFatigue, StatusEffectSpiderWeb
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
    def use_ability(cls, monster):
        pass

    @staticmethod
    def meet_prerequisites(monster):
        pass

    @staticmethod
    def get_weight(monster):
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
    def use_ability(cls, monster):
        if monster.target is None:
            return
        cls.reset_turn(monster)
        if monster == monster.target or monster.target.get_status(StatusEffectSoulbound) is not None:
            add_log_message(
                LogMessage(
                    get_message('soulsteal.fail'),
                    tcod.white
                )
            )
            return
        success_roll = randint(1, monster.get_soul_power() + monster.target.get_soul_power())
        success = success_roll <= monster.get_soul_power()
        if not success:
            add_log_message(
                LogMessage(
                    get_message('soulsteal.fail'),
                    tcod.white
                )
            )
            return
        monster.game_map.take_over_monster(monster.player, monster=monster.target)
        cls.reset_turn(monster.target)
        soulbound_turns = monster.get_soul_power() + monster.target.get_soul_power()
        monster.add_status(StatusEffectSoulbound, soulbound_turns * randint(27, 33))
        monster.target.add_status(StatusEffectSoulbound, soulbound_turns * randint(9, 11))
        monster.target.target = None
        monster.target = None

    @staticmethod
    def meet_prerequisites(monster):
        return False

    @staticmethod
    def get_weight(monster):
        return 0


class BattleAbilityMoveToTarget(BattleAbility):
    name = ''
    hidden = True

    @staticmethod
    def reset_turn(monster):
        monster.reset_turn(monster.get_land_speed())

    @classmethod
    def use_ability(cls, monster):
        if not monster.target and abs(monster.target_x - monster.x) <= 1 or abs(monster.target_y - monster.y) <= 1:
            target_x = monster.target_x - 1 + randint(0, 2)
            target_y = monster.target_y - 1 + randint(0, 2)
            if monster.game_map.field[target_x][target_y].walkable:
                monster.target_x = target_x
                monster.target_y = target_y
        monster.move_astar(monster.target_x, monster.target_y, monster.target)
        cls.reset_turn(monster)

    @staticmethod
    def meet_prerequisites(monster):
        if monster.target and monster.distance_to(monster.target) < 2:
            return False
        if tcod.map_is_in_fov(monster.game_map.fov_map, monster.x, monster.y):
            return True
        if monster.target_x and monster.target_y:
            if abs(monster.target_x - monster.x) > 1 or abs(monster.target_y - monster.y) > 1:
                return True
        return False

    @staticmethod
    def get_weight(monster):
        return 1


class BattleAbilityAttackPlayer(BattleAbility):
    name = ''
    hidden = True

    @staticmethod
    def reset_turn(monster):
        monster.reset_turn(monster.get_attack_speed())

    @classmethod
    def use_ability(cls, monster):
        attack(monster, monster.target)
        cls.reset_turn(monster)

    @staticmethod
    def meet_prerequisites(monster):
        if not monster.target:
            return False
        if monster.distance_to(monster.target) < 2 and monster.target.get_hp() > 0:
            return True
        return False

    @staticmethod
    def get_weight(monster):
        return 1


class BattleAbilityPickItemUp(BattleAbility):
    name = ''
    hidden = True

    @staticmethod
    def reset_turn(monster):
        monster.reset_turn(100)

    @classmethod
    def use_ability(cls, monster):
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
    def meet_prerequisites(monster):
        items = monster.game_map.get_items_at(monster.x, monster.y)
        if not items:
            return False
        return True

    @staticmethod
    def get_weight(monster):
        return 0.1


class BattleAbilityRage(BattleAbility):
    name = 'Rage'

    @staticmethod
    def reset_turn(monster):
        monster.reset_turn(150 - monster.get_constitution())

    @classmethod
    def use_ability(cls, monster):
        monster.add_status(StatusEffectRage, monster.get_constitution())
        cls.reset_turn(monster)

    @staticmethod
    def meet_prerequisites(monster):
        if not monster.target:
            return False
        if monster.get_status(StatusEffectRage) is not None or monster.get_status(StatusEffectFatigue) is not None:
            return False
        return True

    @staticmethod
    def get_weight(monster):
        if not monster.target:
            return 0
        if monster.distance_to(monster.target) >= 2:
            return 0
        return 2 - (monster.get_hp() / monster.get_max_hp()) * 2


class BattleAbilitySpiderWeb(BattleAbility):
    name = 'Throw spider web'
    targeting = AbilityTargeting.LOS
    targeting_distance = 5

    @staticmethod
    def reset_turn(monster):
        monster.reset_turn(130 - monster.get_constitution())

    @classmethod
    def use_ability(cls, monster):
        monster.target.add_status(StatusEffectSpiderWeb, monster.get_constitution() * 3)
        cls.reset_turn(monster)

    @staticmethod
    def meet_prerequisites(monster):
        return monster.target is not None

    @staticmethod
    def get_weight(monster):
        if monster.distance_to(monster.target) >= 5:
            return 0
        return monster.get_land_speed() / monster.target.get_land_speed()
