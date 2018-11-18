class Inventory:
    def __init__(self, monster):
        self.items = []
        self.monster = monster

    def add_item(self, item):
        self.items.append(item)
        item.game_map.entities.remove(item)
        item.game_map = None
        item.monster = self.monster
