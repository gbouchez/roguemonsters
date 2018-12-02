from enum import Enum


class Inventory:
    def __init__(self, monster):
        self.items = []
        self.monster = monster

    def add_item(self, item):
        self.items.append(item)
        if item.game_map:
            item.game_map.entities.remove(item)
            item.game_map = None
        item.monster = self.monster

    def drop_item(self, item):
        item.game_map = self.monster.game_map
        item.x = self.monster.x
        item.y = self.monster.y
        item.monster = None
        item.game_map.entities.append(item)
        self.remove_item(item, False)

    def equip(self, item):
        if item not in self.items:
            # todo error ? something else ?
            return
        self.unequip(item.template.item_type)
        item.equipped = True

    def unequip(self, slot):
        for _ in list(filter(lambda entity: entity.template.item_type == slot, self.items)):
            _.equipped = False

    def remove_item(self, item, delete=True):
        if item.equipped:
            item.equipped = False
        self.items.remove(item)
        if delete:
            del item

    def get_equip(self, slot):
        equips = list(filter(lambda entity: entity.template.item_type == slot and entity.equipped, self.items))
        if equips:
            return equips.pop()
        return None

    def get_item_at_char(self, char):
        index = None
        if ord('a') <= ord(char) <= ord('z'):
            index = ord(char) - ord('a')
        elif ord('A') <= ord(char) <= ord('Z'):
            index = 26 + ord(char) - ord('A')
        if index is not None and len(self.items) > index:
            return self.items[index]
        return None
