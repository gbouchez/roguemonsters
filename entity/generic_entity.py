import tcod


class GenericEntity:
    def __init__(self):
        self.x = None
        self.y = None
        self.name = None
        self.char = '?'
        self.color = tcod.white
        self.blocks = False

    def get_char(self):
        return self.char

    def get_color(self):
        return self.color

    def is_blocking(self):
        return self.blocks

    def get_name(self):
        return self.name
