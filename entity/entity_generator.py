from numpy.random.mtrand import choice

from entity.item_entity import ItemType, ItemEntity
from entity.item_list import templates_by_type
from entity.monster_class import all_classes
from entity.monster_entity import MonsterEntity
from entity.monster_race import all_races


def get_random_level(level=1):
    random_levels = [
        level,
        level - 1,
        level + 1,
        level - 2,
        level + 2,
        level - 3,
        level + 3,
        level + 4,
    ]
    random_levels_weight = [
        1,
        1/4,
        1/3,
        1/6,
        1/5,
        1/8,
        1/7,
        1/9,
    ]

    sum_weights = sum(random_levels_weight)

    random_levels_weight = list(map(lambda weight: weight / sum_weights, random_levels_weight))

    return choice(random_levels, p=random_levels_weight)


def get_random_race_for_level(level=1):
    possible_races = []
    for race in all_races:
        if race.can_have_class and race.get_level() < level \
                or not race.can_have_class and race.get_level() == level:
            possible_races.append(race)

    return choice(possible_races)


def get_random_class_for_monster(monster):
    possible_classes = []
    for monster_class in all_classes:
            possible_classes.append(monster_class)

    return choice(possible_classes)


def generate_fighting_entity(game_map, level=1):
    level = get_random_level(level)
    race = get_random_race_for_level(level)
    monster = MonsterEntity(game_map)
    monster.init_race(race)
    if race.can_have_class and race.get_level() < level:
        monster_class = get_random_class_for_monster(monster)
        monster.init_class(monster_class, level - race.get_level())
    monster.init_fighter()

    return monster


def get_random_item_type(level):
    return ItemType.POTION


def generate_item_entity(game_map, level=1):
    item_type = get_random_item_type(level)
    templates = templates_by_type.get(item_type)
    template = choice(templates)
    item = ItemEntity(game_map=game_map)
    item.set_template(template)

    return item
