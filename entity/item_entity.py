from enum import Enum

import tcod

from entity.generic_entity import GenericEntity


class ItemType(Enum):
    WEAPON = 1


class ItemEntity(GenericEntity):
    def __init__(self, game_map=None, monster=None):
        super(ItemEntity, self).__init__()
        self.game_map = game_map
        self.monster = monster
        self.template = None
        self.usable = False

    def get_char(self):
        return self.template.char

    def get_color(self):
        return self.template.color

    def get_name(self):
        return self.template.name

    def get_description(self):
        return self.template.description


class EquipmentEntity(ItemEntity):
    pass
