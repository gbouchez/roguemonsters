class Inventory:
    def __init__(self, monster):
        self.items = []
        self.monster = monster

    def add_item(self, item):
        self.items.append(item)
        item.game_map.entities.remove(item)
        item.game_map = None
        item.monster = self.monster

    def remove_item(self, item):
        self.items.remove(item)

    def get_item_at_char(self, char):
        index = None
        if ord('a') <= ord(char) <= ord('z'):
            index = ord(char) - ord('a')
        elif ord('A') <= ord(char) <= ord('Z'):
            index = 26 + ord(char) - ord('A')
        if index is not None and len(self.items) > index:
            return self.items[index]
        return None
