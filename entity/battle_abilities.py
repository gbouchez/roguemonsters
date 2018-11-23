from random import randint

import tcod

from combat import attack
from entity.status_effects import StatusEffectRage, StatusEffectSoulbound, StatusEffectFatigue
from game_log import add_log_message, LogMessage, get_monster_message_prefix
from messages.messages import get_message


class BattleAbility:
    name = ''
    hidden = False

    @staticmethod
    def reset_turn(monster):
        pass

    @classmethod
    def use_ability(cls, monster, player):
        pass

    @staticmethod
    def meet_prerequisites(monster, player):
        pass

    @staticmethod
    def get_weight(monster, player):
        return 1

    @classmethod
    def get_name(cls):
        return cls.name


class BattleAbilityTakeOverRandomMonster(BattleAbility):
    name = 'Monster takeover'

    @staticmethod
    def reset_turn(monster):
        monster.reset_turn(200)

    @classmethod
    def use_ability(cls, monster, player):
        monster.game_map.take_over_random_monster(player, in_fov=True)
        cls.reset_turn(monster)
        if player.entity == monster:
            add_log_message(
                LogMessage(
                    get_message('soulsteal.fail'),
                    tcod.white
                )
            )
            return
        cls.reset_turn(player.entity)
        soulbound_turns = monster.get_soul_power() + player.entity.get_soul_power()
        monster.status_effects.append(StatusEffectSoulbound(monster, soulbound_turns * randint(27, 33)))
        player.entity.status_effects.append(StatusEffectSoulbound(player.entity, soulbound_turns * randint(9, 11)))

    @staticmethod
    def meet_prerequisites(monster, player):
        return False

    @staticmethod
    def get_weight(monster, player):
        return 0


class BattleAbilityMoveToPlayer(BattleAbility):
    name = ''
    hidden = True

    @staticmethod
    def reset_turn(monster):
        monster.reset_turn(monster.land_speed)

    @classmethod
    def use_ability(cls, monster, player):
        monster.move_astar(player.entity)
        monster.target = player.entity
        cls.reset_turn(monster)

    @staticmethod
    def meet_prerequisites(monster, player):
        if monster.distance_to(player.entity) >= 2:
            return True
        return False

    @staticmethod
    def get_weight(monster, player):
        return 1


class BattleAbilityAttackPlayer(BattleAbility):
    name = ''
    hidden = True

    @staticmethod
    def reset_turn(monster):
        monster.reset_turn(monster.get_attack_speed())

    @classmethod
    def use_ability(cls, monster, player):
        monster.target = player.entity
        attack(monster, player.entity)
        cls.reset_turn(monster)

    @staticmethod
    def meet_prerequisites(monster, player):
        if monster.distance_to(player.entity) < 2 and player.entity.get_hp() > 0:
            return True
        return False

    @staticmethod
    def get_weight(monster, player):
        return 1


class BattleAbilityPickItemUp(BattleAbility):
    name = ''
    hidden = True

    @staticmethod
    def reset_turn(monster):
        monster.reset_turn(100)

    @classmethod
    def use_ability(cls, monster, player):
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
    def meet_prerequisites(monster, player):
        items = monster.game_map.get_items_at(monster.x, monster.y)
        if not items:
            return False
        return True

    @staticmethod
    def get_weight(monster, player):
        return 0.1


class BattleAbilityRage(BattleAbility):
    name = 'Rage'

    @staticmethod
    def reset_turn(monster):
        monster.reset_turn(150 - monster.get_constitution())

    @classmethod
    def use_ability(cls, monster, player):
        monster.status_effects.append(StatusEffectRage(monster, int(monster.get_constitution() / 2)))
        cls.reset_turn(monster)

    @staticmethod
    def meet_prerequisites(monster, player):
        if monster.has_status(StatusEffectRage) or monster.has_status(StatusEffectFatigue):
            return False
        if monster.distance_to(player.entity) < 2:
            return True
        return False

    @staticmethod
    def get_weight(monster, player):
        return 2 - (monster.get_hp() / monster.get_max_hp()) * 2
