from math import ceil

import tcod
from game_log import add_log_message, LogMessage, get_monster_message_prefix
from messages.messages import get_message


class StatusEffect:
    name = ''

    def __init__(self, monster, turns):
        self.monster = monster
        self.turns = turns

    def pass_turn(self, monster):
        self.turns -= 1

    def remove_effect(self):
        return


class StatusEffectSoulbound(StatusEffect):
    name = 'Soulbound'

    def __init__(self, monster, turns):
        super().__init__(monster, turns)

    def pass_turn(self, monster):
        self.turns -= 1

    def remove_effect(self):
        pass


class StatusEffectRage(StatusEffect):
    name = 'Rage'

    def __init__(self, monster, turns):
        self.elapsed_turns = 0
        super().__init__(monster, turns)
        monster.add_stat_bonus('strength', 'rage', 8)
        monster.add_stat_bonus('constitution', 'rage', 4)
        monster.add_stat_bonus('dexterity', 'rage', -4)
        monster.add_stat_bonus('intelligence', 'rage', -8)
        if tcod.map_is_in_fov(monster.game_map.fov_map, monster.x, monster.y):
            add_log_message(
                LogMessage(
                    get_message(get_monster_message_prefix(self.monster) + "rage.begin")
                    .format(str.capitalize(self.monster.get_name())),
                    tcod.blue
                )
            )

    def pass_turn(self, monster):
        self.turns -= 1
        self.elapsed_turns += 1

    def remove_effect(self):
        self.monster.remove_stat_bonus('strength', 'rage')
        self.monster.remove_stat_bonus('constitution', 'rage')
        self.monster.remove_stat_bonus('dexterity', 'rage')
        self.monster.remove_stat_bonus('intelligence', 'rage')
        if tcod.map_is_in_fov(self.monster.game_map.fov_map, self.monster.x, self.monster.y):
            add_log_message(
                LogMessage(
                    get_message(get_monster_message_prefix(self.monster) + "rage.end")
                    .format(str.capitalize(self.monster.get_name())),
                    tcod.desaturated_blue
                )
            )
        self.monster.status_effects.append(StatusEffectFatigue(self.monster, self.elapsed_turns * 2))


class StatusEffectSpiderWeb(StatusEffect):
    name = 'Spider web'

    def __init__(self, monster, turns):
        self.total_turns = turns
        super().__init__(monster, turns)
        monster.add_stat_bonus('dexterity', 'spider_web', -5)
        monster.add_stat_bonus('land_speed', 'spider_web', 50)
        if tcod.map_is_in_fov(monster.game_map.fov_map, monster.x, monster.y):
            add_log_message(
                LogMessage(
                    get_message(get_monster_message_prefix(self.monster) + "spider_web.begin")
                    .format(str.capitalize(self.monster.get_name())),
                    tcod.dark_orange
                )
            )

    def pass_turn(self, monster):
        self.turns -= 1
        multiplier = self.turns / self.total_turns

        monster.add_stat_bonus('dexterity', 'spider_web', ceil(-5 * multiplier))
        monster.add_stat_bonus('land_speed', 'spider_web', int(50 * multiplier))

    def remove_effect(self):
        self.monster.remove_stat_bonus('dexterity', 'spider_web')
        self.monster.remove_stat_bonus('land_speed', 'spider_web')
        if tcod.map_is_in_fov(self.monster.game_map.fov_map, self.monster.x, self.monster.y):
            add_log_message(
                LogMessage(
                    get_message(get_monster_message_prefix(self.monster) + "spider_web.end")
                    .format(str.capitalize(self.monster.get_name())),
                    tcod.desaturated_orange
                )
            )


class StatusEffectFatigue(StatusEffect):
    name = 'Fatigue'

    def __init__(self, monster, turns):
        super().__init__(monster, turns)
        monster.add_stat_bonus('strength', 'fatigue', -2)
        monster.add_stat_bonus('constitution', 'fatigue', -2)
        monster.add_stat_bonus('dexterity', 'fatigue', -2)
        if tcod.map_is_in_fov(monster.game_map.fov_map, monster.x, monster.y):
            add_log_message(
                LogMessage(
                    get_message(get_monster_message_prefix(self.monster) + "fatigue.begin")
                    .format(str.capitalize(self.monster.get_name())),
                    tcod.dark_orange
                )
            )

    def pass_turn(self, monster):
        self.turns -= 1

    def remove_effect(self):
        self.monster.remove_stat_bonus('strength', 'fatigue')
        self.monster.remove_stat_bonus('constitution', 'fatigue')
        self.monster.remove_stat_bonus('dexterity', 'fatigue')
        if tcod.map_is_in_fov(self.monster.game_map.fov_map, self.monster.x, self.monster.y):
            add_log_message(
                LogMessage(
                    get_message(get_monster_message_prefix(self.monster) + "fatigue.end")
                    .format(str.capitalize(self.monster.get_name())),
                    tcod.desaturated_orange
                )
            )
