from enum import Enum
from entity.generic_entity import GenericEntity


class ItemType(Enum):
    POTION = 1
    WEAPON = 2
    SHIELD = 3
    BODY = 4


class ItemEntity(GenericEntity):
    def __init__(self, game_map=None, monster=None):
        super(ItemEntity, self).__init__()
        self.game_map = game_map
        self.monster = monster
        self.template = None
        self.usable = False
        self.equippable = False
        self.equipped = False

    def set_template(self, template):
        self.template = template
        self.template.apply_template(self)

    def get_char(self):
        return self.template.char

    def get_color(self):
        return self.template.color

    def get_name(self):
        return self.template.name

    def get_description(self):
        return self.template.description

    def use(self):
        return self.template.use(self)
