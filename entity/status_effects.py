import tcod
from game_log import add_log_message, LogMessage, get_monster_message_prefix
from messages.messages import get_message


class StatusEffect:
    name = ''

    def __init__(self, monster, turns):
        self.monster = monster
        self.turns = turns

    def pass_turn(self):
        self.turns -= 1

    def remove_effect(self):
        return


class StatusEffectRage(StatusEffect):
    name = 'Rage'

    def __init__(self, monster, turns):
        self.elapsed_turns = 0
        super().__init__(monster, turns)
        monster.add_stat_bonus('strength', 'rage', 4)
        monster.add_stat_bonus('constitution', 'rage', 4)
        if tcod.map_is_in_fov(monster.game_map.fov_map, monster.x, monster.y):
            add_log_message(
                LogMessage(
                    get_message(get_monster_message_prefix(self.monster) + "rage.begin")
                    .format(str.capitalize(self.monster.get_name())),
                    tcod.blue
                )
            )

    def pass_turn(self):
        self.turns -= 1
        self.elapsed_turns += 1

    def remove_effect(self):
        self.monster.remove_stat_bonus('strength', 'rage')
        self.monster.remove_stat_bonus('constitution', 'rage')
        if tcod.map_is_in_fov(self.monster.game_map.fov_map, self.monster.x, self.monster.y):
            add_log_message(
                LogMessage(
                    get_message(get_monster_message_prefix(self.monster) + "rage.end")
                    .format(str.capitalize(self.monster.get_name())),
                    tcod.desaturated_blue
                )
            )
