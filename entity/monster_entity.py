import math
from math import floor

import tcod

from entity.generic_entity import GenericEntity
from entity.item_entity import ItemType
from entity.monster_ai import BasicAI
from game_log import add_log_message, LogMessage, get_monster_message_prefix
from inventory import Inventory
from messages.messages import get_message
from save import delete_game


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
        self.attack_speed = 100
        self.strength = 10
        self.dexterity = 3
        self.constitution = 3
        self.intelligence = 3
        self.monster_race = None
        self.monster_class = None
        self.level = 0
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
            'land_speed': {},
            'accuracy': {},
            'damage': {},
            'evasion': {},
            'shield_rate': {},
            'shield_block': {},
            'armor': {},
            'attack_speed': {},
        }
        self.inventory = Inventory(self)
        self.equip_slots = []

    def is_blocking(self):
        if self.dead:
            return False
        return super(MonsterEntity, self).is_blocking()

    def init_race(self, monster_race):
        self.monster_race = monster_race
        self.monster_race.apply_race(self)
        self.ai = BasicAI(self)

    def init_class(self, monster_class):
        self.monster_class = monster_class

    def gain_level(self, level):
        if level < 1:
            return
        for _ in range(level - 1):
            self.monster_race.gain_level(self)
            if self.monster_class:
                self.monster_class.gain_level(self)
        self.level += level

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
        return max(1, self.max_hp + (10 + self.get_constitution()) * 8)

    def get_hp(self):
        self.check_max_hp()
        return self.hp

    def get_equipment_accuracy_bonus(self):
        bonus = 0
        for slot in self.equip_slots:
            equip = self.inventory.get_equip(slot)
            if equip:
                bonus += equip.accuracy
        return bonus

    def get_equipment_damage_bonus(self):
        bonus = 0
        for slot in self.equip_slots:
            equip = self.inventory.get_equip(slot)
            if equip:
                bonus += equip.damage
        return bonus

    def get_equipment_evasion_bonus(self):
        bonus = 0
        for slot in self.equip_slots:
            equip = self.inventory.get_equip(slot)
            if equip:
                bonus += equip.evasion
        return bonus

    def get_equipment_shield_rate_bonus(self):
        bonus = 0
        for slot in self.equip_slots:
            equip = self.inventory.get_equip(slot)
            if equip:
                bonus += equip.shield_rate
        return bonus

    def get_equipment_shield_block_bonus(self):
        bonus = 0
        for slot in self.equip_slots:
            equip = self.inventory.get_equip(slot)
            if equip:
                bonus += equip.shield_block
        return bonus

    def get_equipment_armor_bonus(self):
        bonus = 0
        for slot in self.equip_slots:
            equip = self.inventory.get_equip(slot)
            if equip:
                bonus += equip.armor_value
        bonus += self.monster_race.get_natural_armor()
        return bonus

    def get_equipment_attack_speed_bonus(self):
        bonus = 0
        for slot in self.equip_slots:
            equip = self.inventory.get_equip(slot)
            if equip:
                bonus += equip.attack_speed
        return bonus

    def get_accuracy(self):
        accuracy = 100
        accuracy -= self.get_equipment_weight_malus()
        weapon_weight_malus = 0
        weapon = self.inventory.get_equip(ItemType.WEAPON)
        if weapon:
            weapon_weight_malus = max(0, weapon.template.weight - self.get_strength())
        accuracy += max(0, self.get_dexterity() - weapon_weight_malus)
        accuracy += self.get_equipment_accuracy_bonus()
        accuracy += self.get_total_bonus('accuracy')
        return max(0, accuracy)

    def get_damage(self):
        damage = 10
        weapon = self.inventory.get_equip(ItemType.WEAPON)
        if not weapon:
            weapon_damage = self.monster_race.get_natural_damage() * 2
        else:
            weapon_damage = weapon.damage
            if weapon.template.weight != 0:
                if self.get_strength() < weapon.template.weight:
                    weapon_damage /= 2
                    weapon_damage += weapon_damage * self.get_strength() / weapon.template.weight
                else:
                    weapon_damage += weapon_damage * min(1, (self.get_strength() - weapon.template.weight) / weapon.template.weight)
            else:
                weapon_damage *= 2

            damage += self.get_equipment_damage_bonus() - weapon.damage
        damage += weapon_damage
        damage += self.get_total_bonus('damage')

        return max(0, int(damage))

    def get_evasion(self):
        evasion = 15
        evasion -= self.get_equipment_weight_malus()
        evasion += self.get_dexterity()
        evasion += self.get_equipment_evasion_bonus()
        evasion += self.get_total_bonus('evasion')
        return max(0, evasion)

    def get_shield_rate(self):
        shield = self.inventory.get_equip(ItemType.SHIELD)
        if not shield:
            return 0
        rate = 10
        rate -= self.get_equipment_weight_malus()
        shield_weight_malus = max(0, shield.template.weight - self.get_strength())
        rate += max(0, self.get_dexterity() - shield_weight_malus)
        rate += self.get_equipment_shield_rate_bonus()
        rate += self.get_total_bonus('shield_rate')
        return max(0, rate)

    def get_shield_block(self):
        block = 0
        block += self.get_equipment_shield_block_bonus()
        block += self.get_total_bonus('shield_block')
        return block

    def get_armor_value(self):
        value = 10
        value += self.get_equipment_armor_bonus()
        value += self.get_total_bonus('armor')
        return max(0, value)

    def get_attack_speed(self):
        speed = self.attack_speed
        weapon = self.inventory.get_equip(ItemType.WEAPON)
        if weapon:
            speed += weapon.attack_speed
        speed = max(25, speed + self.get_equipment_weight_malus())
        speed += self.get_equipment_attack_speed_bonus()
        speed += self.get_total_bonus('attack_speed')
        return speed

    def get_equipment_weight_malus(self):
        malus = 0
        for slot in self.equip_slots:
            equip = self.inventory.get_equip(slot)
            if equip:
                stat_diff = equip.template.weight - self.get_strength()
                multiplier = 1
                while stat_diff > 0:
                    malus += min(4, stat_diff) * multiplier
                    stat_diff -= 4
        return malus

    def get_effective_level(self):
        level = self.monster_race.get_level()
        return level + self.level

    def get_level(self):
        return self.level

    def get_soul_power(self):
        # TODO better calc
        return self.get_effective_level() + self.get_intelligence()

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
        self.rest_turns += 10
        if self.rest_turns >= self.get_rest_wait():
            self.heal(floor(self.rest_turns / self.get_rest_wait()), False)
            self.rest_turns = self.rest_turns % self.get_rest_wait()

        for status in self.status_effects:
            status.pass_turn(self)
            if status.turns == 0:
                status.remove_effect()
                self.status_effects.remove(status)

    def get_rest_wait(self):
        return int(500 / self.get_constitution())

    def get_status(self, search_status):
        for status in self.status_effects:
            if isinstance(status, search_status):
                return status
        return None

    def add_status(self, status_type, turns):
        status = self.get_status(status_type)
        if status is not None:
            status.stack(self, turns)
        else:
            self.status_effects.append(status_type(self, turns))

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
            if self.player is not None:
                delete_game()

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

        return name

    def get_full_name(self):
        name = ''
        if self.player is not None:
            if self.dead:
                name += "your corpse "
            else:
                name += 'you, '
        else:
            if self.dead:
                name += "the corpse of "
            if self.name is not None:
                name += str.capitalize(self.name) + ', '
        name += self.monster_race.name_article + ' ' + self.monster_race.name
        if self.monster_class is not None:
            name += " " + self.monster_class.name
        body = self.inventory.get_equip(ItemType.BODY)
        if body:
            name += " in " + body.get_name()
        weapon = self.inventory.get_equip(ItemType.WEAPON)
        if weapon is not None:
            name += " wielding a " + weapon.get_name()
        return name

    def get_land_speed(self):
        return self.land_speed + self.get_total_bonus('land_speed')

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
        abilities = []
        if self.player is not None:
            abilities += self.player.get_abilities()
        abilities += self.monster_race.get_abilities()
        if self.monster_class is not None:
            abilities += self.monster_class.get_abilities()
        return abilities

    def get_ability_at_char(self, char):
        index = None
        if ord('a') <= ord(char) <= ord('z'):
            index = ord(char) - ord('a')
        elif ord('A') <= ord(char) <= ord('Z'):
            index = 26 + ord(char) - ord('A')
        display_abilities = list(filter(lambda ability: not ability.hidden, self.get_abilities()))
        if index is not None and len(display_abilities) > index:
            return display_abilities[index]
        return None

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
