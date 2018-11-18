import math

import tcod

from entity.generic_entity import GenericEntity
from entity.monster_ai import BasicAI
from game_log import add_log_message, LogMessage, get_monster_message_prefix
from inventory import Inventory
from messages.messages import get_message


class MonsterEntity(GenericEntity):
    def __init__(self, game_map):
        super(MonsterEntity, self).__init__()
        self.game_map = game_map
        self.player = None
        self.target = None
        self.blocks = True
        self.turn_to_action = 100
        self.hp = 0
        self.max_hp = 0
        self.land_speed = 100
        self.strength = 10
        self.dexterity = 3
        self.constitution = 3
        self.intelligence = 3
        self.monster_race = None
        self.monster_class = None
        self.class_level = 0
        self.traits = []
        self.ai = None
        self.dead = False
        self.status_effects = []
        self.rest_turns = 0
        self.stat_bonuses = {
            'strength': {},
            'dexterity': {},
            'constitution': {},
            'intelligence': {},
        }
        self.inventory = Inventory(self)

    def is_blocking(self):
        if self.dead:
            return False
        return super(MonsterEntity, self).is_blocking()

    def init_race(self, monster_race):
        self.monster_race = monster_race
        self.monster_race.apply_race(self)
        self.ai = BasicAI(self)

    def init_class(self, monster_class, level):
        self.monster_class = monster_class
        self.class_level = level
        self.monster_class.apply_class(self, level)

    def add_trait(self, trait):
        self.traits.append(trait)
        trait.apply_effect(self)

    def init_fighter(self):
        self.hp = self.get_max_hp()
        self.reset_turn(100)
        return

    def check_max_hp(self):
        if self.hp > self.get_max_hp():
            self.hp = self.get_max_hp()

    def get_max_hp(self):
        return max(1, self.max_hp + self.get_constitution() * 2)

    def get_hp(self):
        self.check_max_hp()
        return self.hp

    def get_accuracy(self):
        return 100 + self.get_dexterity()

    def get_damage(self):
        return max(1, int(self.get_strength() / 2))

    def get_dodge_components(self):
        components = {
            'dexterity': self.get_dexterity(),
        }
        return components

    def get_armor_components(self):
        # todo armors
        components = {
            'unknown_armor': 40,
        }
        return components

    def get_armor_reduction(self):
        # todo armors
        return 5

    def get_effective_level(self):
        level = self.monster_race.get_level()
        if self.monster_class is not None:
            level += self.class_level
        return level

    def get_char(self):
        if self.player is not None:
            return '@'
        if self.dead:
            return '%'
        return self.monster_race.char

    def get_color(self):
        if self.player is not None:
            return tcod.white
        if self.dead:
            return tcod.dark_orange
        return self.monster_race.color

    def rest_turn(self):
        self.rest()
        self.reset_turn(100)

    def rest(self):
        self.rest_turns += 1
        if self.rest_turns >= self.get_rest_wait():
            self.heal(1, False)
            self.rest_turns -= self.get_rest_wait()

        for status in self.status_effects:
            status.pass_turn()
            if status.turns == 0:
                status.remove_effect()
                self.status_effects.remove(status)

    def heal(self, amount, with_message=True):
        self.hp += amount
        self.check_max_hp()
        if with_message:
            add_log_message(
                LogMessage(
                    get_message(get_monster_message_prefix(self) + 'healed')
                    .format(str.capitalize(self.get_name())),
                    tcod.desaturated_green if self.player is None else tcod.green
                )
            )

    def get_rest_amount(self):
        return max(1, int(self.constitution / 2))

    def get_rest_wait(self):
        return int(100 / self.get_rest_amount())

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            add_log_message(
                LogMessage(
                    get_message(get_monster_message_prefix(self) + "die")
                        .format(str.capitalize(self.get_name())),
                    tcod.orange if self.player is None else tcod.red
                )
            )
            self.dead = True

    def reset_turn(self, turns):
        self.turn_to_action = max(10, turns)

    def take_action(self, player):
        if self.dead:
            return
        self.ai.take_turn(player)
        if self.turn_to_action <= 0:
            self.reset_turn(100)
        self.rest()

    def get_name(self):
        if self.player is not None:
            return 'you'
        if self.name is not None:
            return str.capitalize(self.name)
        name = "the " + self.monster_race.name
        if self.monster_class is not None:
            name += " " + self.monster_class.name
        if self.dead:
            name += " corpse"
        return name

    def get_strength(self):
        return self.strength + self.get_total_bonus('strength')

    def get_dexterity(self):
        return self.dexterity + self.get_total_bonus('dexterity')

    def get_constitution(self):
        return self.constitution + self.get_total_bonus('constitution')

    def get_intelligence(self):
        return self.intelligence + self.get_total_bonus('intelligence')

    def get_total_bonus(self, stat):
        total = 0
        for source in self.stat_bonuses.get(stat):
            bonus = self.stat_bonuses.get(stat).get(source)
            total += bonus

        return total

    def add_stat_bonus(self, stat, source, value):
        self.stat_bonuses.get(stat)[source] = value

    def remove_stat_bonus(self, stat, source):
        del self.stat_bonuses.get(stat)[source]

    def get_abilities(self):
        abilities = self.monster_race.get_abilities()
        if self.monster_class is not None:
            abilities += self.monster_class.get_abilities()
        return abilities

    def move_towards(self, target_x, target_y):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if self.game_map.can_walk_at(self.x + dx, self.y + dy):
            self.game_map.move_monster(self, (dx, dy))

    def distance_to(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def move_astar(self, target):
        # Create a FOV map that has the dimensions of the map
        fov = tcod.map_new(self.game_map.width, self.game_map.height)

        # Scan the current map each turn and set all the walls as unwalkable
        for y1 in range(self.game_map.height):
            for x1 in range(self.game_map.width):
                tcod.map_set_properties(fov, x1, y1, self.game_map.field[x1][y1].transparent,
                                        self.game_map.field[x1][y1].walkable)

        # Scan all the objects to see if there are objects that must be navigated around
        # Check also that the object isn't self or the target (so that the start and the end points are free)
        # The AI class handles the situation if self is next to the target so it will not use this A* function anyway
        for entity in self.game_map.entities:
            if entity.is_blocking() and entity != self and entity != target:
                # Set the tile as a wall so it must be navigated around
                tcod.map_set_properties(fov, entity.x, entity.y, True, False)

        # Allocate a A* path
        # The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
        my_path = tcod.path_new_using_map(fov, 1)

        # Compute the path between self's coordinates and the target's coordinates
        tcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        # Check if the path exists, and in this case, also the path is shorter than 25 tiles
        # The path size matters if you want the monster to use alternative longer paths (for example through other rooms) if for example the player is in a corridor
        # It makes sense to keep path size relatively low to keep the monsters from running around the map if there's an alternative path really far away
        if not tcod.path_is_empty(my_path) and tcod.path_size(my_path) < 25:
            # Find the next coordinates in the computed full path
            x, y = tcod.path_walk(my_path, True)
            if x or y:
                # Set self's coordinates to the next path tile
                self.x = x
                self.y = y
        else:
            # Keep the old move function as a backup so that if there are no paths (for example another monster blocks a corridor)
            # it will still try to move towards the player (closer to the corridor opening)
            self.move_towards(target.x, target.y)

            # Delete the path to free memory
        tcod.path_delete(my_path)
