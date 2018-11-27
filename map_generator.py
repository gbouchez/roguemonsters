from enum import Enum
from random import randint

from numpy.random.mtrand import choice

from map import Map, max_rooms, room_min_size, room_max_size, TileType

monsters_per_room_max_ratio = 1 / 16
items_per_room_max_ratio = 1 / 16


class RoomDecoration(Enum):
    WATER_SHALLOW_CENTER = 1
    WATER_DEEP_CENTER = 2


def decorate_room(game_map, rect):
    elements = [RoomDecoration.WATER_SHALLOW_CENTER, RoomDecoration.WATER_DEEP_CENTER]
    weights = [0.5, 0.5]
    decoration = choice(elements, p=weights)
    if decoration == RoomDecoration.WATER_SHALLOW_CENTER \
            or decoration == RoomDecoration.WATER_DEEP_CENTER:
        tile_type = TileType.WATER_SHALLOW
        if decoration == RoomDecoration.WATER_DEEP_CENTER:
            tile_type = TileType.WATER_DEEP
        x1 = randint(rect.x1 + 2, rect.x2 - 1)
        x2 = randint(x1, rect.x2 - 1)
        y1 = randint(rect.y1 + 2, rect.y2 - 1)
        y2 = randint(y1, rect.y2 - 1)
        for x in range(x1, x2):
            for y in range(y1, y2):
                game_map.field[x][y].__init__(x, y, tile_type)


def create_v_tunnel(game_map, y1, y2, x):
    first = True
    if y1 <= y2:
        todo = range(y1, y2 + 1)
    else:
        todo = range(y1, y2 - 1, -1)
    for y in todo:
        if game_map.field[x][y].tile_type != TileType.WALL and not first:
            return False
        game_map.field[x][y].__init__(x, y, TileType.FLOOR)
        first = False
    return True


def create_h_tunnel(game_map, x1, x2, y):
    first = True
    if x1 <= x2:
        todo = range(x1, x2 + 1)
    else:
        todo = range(x1, x2 - 1, -1)

    for x in todo:
        if game_map.field[x][y].tile_type != TileType.WALL and not first:
            return False
        game_map.field[x][y].__init__(x, y, TileType.FLOOR)
        first = False
    return True


def create_room(game_map, rect):
    for x in range(rect.x1 + 1, rect.x2):
        for y in range(rect.y1 + 1, rect.y2):
            game_map.field[x][y].__init__(x, y, TileType.FLOOR)
    if randint(0, 9) <= 8:
        decorate_room(game_map, rect)


def make_map(game_map, player=None):
    rooms = []
    num_rooms = 0
    player_placed = False

    for r in range(max_rooms):
        w = randint(room_min_size, room_max_size)
        h = randint(room_min_size, room_max_size)
        x = randint(0, game_map.width - w - 1)
        y = randint(0, game_map.height - h - 1)
        new_room = Rect(x, y, w, h)

        for other_room in rooms:
            if new_room.intersect(other_room):
                break
        else:
            create_room(game_map, new_room)
            number_monsters_to_generate = int(
                (randint(0, int((w - 1) * (h - 1) * monsters_per_room_max_ratio))
                 + randint(0, int((w - 1) * (h - 1) * monsters_per_room_max_ratio)))
                / 2)
            number_items_to_generate = int(
                (randint(0, int((w - 1) * (h - 1) * items_per_room_max_ratio))
                 + randint(0, int((w - 1) * (h - 1) * items_per_room_max_ratio)))
                / 2)

            for _ in range(number_monsters_to_generate):
                monster_x = randint(new_room.x1 + 1, new_room.x2 - 1)
                monster_y = randint(new_room.y1 + 1, new_room.y2 - 1)
                if game_map.can_walk_at(monster_x, monster_y):
                    if player_placed is False and player is not None:
                        game_map.add_monster(monster_x, monster_y, player.entity)
                        player_placed = True
                    else:
                        game_map.add_monster(monster_x, monster_y)

            for _ in range(number_items_to_generate):
                item_x = randint(new_room.x1 + 1, new_room.x2 - 1)
                item_y = randint(new_room.y1 + 1, new_room.y2 - 1)
                if game_map.can_walk_at(item_x, item_y, False):
                    game_map.add_random_item(item_x, item_y)

            if num_rooms != 0:
                prev = rooms[num_rooms - 1]
                possible_walls_begin = []
                possible_walls_end = []
                if prev.x2 <= new_room.x1 + 1:
                    possible_walls_begin.append('left')
                    possible_walls_end.append('right')
                elif prev.x1 + 1 >= new_room.x2:
                    possible_walls_begin.append('right')
                    possible_walls_end.append('left')
                if prev.y2 <= new_room.y1 + 1:
                    possible_walls_begin.append('top')
                    possible_walls_end.append('bottom')
                elif prev.y1 + 1 >= new_room.y2:
                    possible_walls_begin.append('bottom')
                    possible_walls_end.append('top')
                begin_wall = choice(possible_walls_begin)
                end_wall = choice(possible_walls_end)
                if begin_wall == 'left':
                    begin_x = new_room.x1
                    begin_y = randint(new_room.y1 + 1, new_room.y2 - 1)
                elif begin_wall == 'right':
                    begin_x = new_room.x2
                    begin_y = randint(new_room.y1 + 1, new_room.y2 - 1)
                elif begin_wall == 'top':
                    begin_y = new_room.y1
                    begin_x = randint(new_room.x1 + 1, new_room.x2 - 1)
                else:
                    begin_y = new_room.y2
                    begin_x = randint(new_room.x1 + 1, new_room.x2 - 1)
                if end_wall == 'left':
                    end_x = prev.x1
                    end_y = randint(prev.y1 + 1, prev.y2 - 1)
                elif end_wall == 'right':
                    end_x = prev.x2
                    end_y = randint(prev.y1 + 1, prev.y2 - 1)
                elif end_wall == 'top':
                    end_y = prev.y1
                    end_x = randint(prev.x1 + 1, prev.x2 - 1)
                else:
                    end_y = prev.y2
                    end_x = randint(prev.x1 + 1, prev.x2 - 1)

                if randint(0, 1) == 1:
                    continue_carving = create_h_tunnel(game_map, begin_x, end_x, begin_y)
                    if continue_carving:
                        create_v_tunnel(game_map, begin_y, end_y, end_x)
                else:
                    continue_carving = create_v_tunnel(game_map, begin_y, end_y, begin_x)
                    if continue_carving:
                        create_h_tunnel(game_map, begin_x, end_x, end_y)

            rooms.append(new_room)
            num_rooms += 1


def generate_map(depth, player=None):
    game_map = Map(depth, 80, 60)
    make_map(game_map, player)

    walkable_tiles = list(filter(lambda tile: tile.walkable, game_map.get_all_tiles()))

    stair_tiles = choice(walkable_tiles, 3, replace=False)
    for tile in stair_tiles:
        tile.stairs = True

    return game_map


class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return center_x, center_y

    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)
