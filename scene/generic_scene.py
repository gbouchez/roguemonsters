import tcod
from input import InputType


class GenericScene:
    def __init__(self):
        self.previous_scene = None
        self.render_next = True

    def manage_input(self, game_input):
        if game_input is None:
            return None
        if game_input.type == InputType.KEY and game_input.value == tcod.KEY_ESCAPE:
            return {'action': 'cancel'}
        return None

    def render(self, console):
        pass

    def render_clean(self, console):
        pass
