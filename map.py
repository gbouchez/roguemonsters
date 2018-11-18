import tcod

from enum import Enum
from random import choice

from combat import attack
from entity.entity_generator import generate_fighting_entity, generate_item_entity
from entity.item_entity import ItemEntity
from entity.monster_entity import MonsterEntity

room_max_size = 12
room_min_size = 6
max_rooms = 30


class TileType(Enum):
    WALL = 1
    FLOOR = 2
    WATER_SHALLOW = 3
    WATER_DEEP = 4


class Tile:
    def __init__(self, tile_type=TileType.WALL):
        self.tile_type = tile_type
        self.explored = False

        if tile_type == TileType.WALL:
            walkable = False
            transparent = False
            background_color = 30, 30, 30
            background_color_dark = 10, 10, 10
        elif tile_type == TileType.FLOOR:
            walkable = True
            transparent = True
            background_color = 100, 100, 100
            background_color_dark = 65, 65, 65
        elif tile_type == TileType.WATER_DEEP:
            walkable = False
            transparent = True
            background_color = 0, 0, 120
            background_color_dark = 0, 0, 80
        elif tile_type == TileType.WATER_SHALLOW:
            walkable = True
            transparent = True
            background_color = 60, 60, 120
            background_color_dark = 40, 40, 80
        else:
            walkable = False
            transparent = False
            background_color = tcod.black
            background_color_dark = tcod.black

        self.walkable = walkable
        self.transparent = transparent
        self.background_color = background_color
        self.background_color_dark = background_color_dark


class Map:
    def __init__(self, depth=1, width=300, height=200):
        self.width = width
        self.height = height
        self.entities = []
        self.depth = depth
        self.field = [[Tile() for y in range(self.height)] for x in range(self.width)]
        self.fov_map = None

    def move_monster(self, monster, coordinates):
        dx, dy = coordinates
        if self.can_walk_at(monster.x + dx, monster.y + dy):
            monster.x += dx
            monster.y += dy
        elif monster.player is not None:
            destination_monster = self.get_monster_at(monster.x + dx, monster.y + dy)
            if destination_monster is not None:
                attack(monster, destination_monster)
                return True
        return False

    def add_random_monster(self, x, y):
        if not self.can_walk_at(x, y):
            return
        entity = generate_fighting_entity(self, self.depth)
        entity.x = x
        entity.y = y
        self.entities.append(entity)

    def add_random_item(self, x, y):
        if not self.can_walk_at(x, y, False):
            return
        entity = generate_item_entity(self, self.depth)
        entity.x = x
        entity.y = y
        self.entities.append(entity)

    def get_random_monster(self):
        return choice(list(filter(lambda entity: isinstance(entity, MonsterEntity), self.entities)))

    def get_monster_at(self, destination_x, destination_y):
        for entity in self.entities:
            if isinstance(entity,
                          MonsterEntity) and entity.x == destination_x and entity.y == destination_y and entity.is_blocking():
                return entity

        return None

    def get_items_at(self, destination_x, destination_y):
        entities = []
        for entity in self.entities:
            if isinstance(entity, ItemEntity) \
                    and entity.x == destination_x and entity.y == destination_y:
                entities.append(entity)

        return entities

    def can_walk_at(self, x, y, check_monster=True):
        if self.field[x][y].walkable and (not check_monster or self.get_monster_at(x, y) is None):
            return True
        return False

    def get_names_at(self, x, y):
        names = [entity.get_name() for entity in self.entities
                 if entity.x == x and entity.y == y and tcod.map_is_in_fov(self.fov_map, entity.x, entity.y)]
        names = ', '.join(names)

        return names.capitalize()
