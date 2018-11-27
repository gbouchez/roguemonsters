import tcod
from input import InputType


class GenericScene:
    def __init__(self):
        self.previous_scene = None
        self.render_next = True
        self.data = None
        self.need_confirm = None

    def manage_input(self, game_input):
        if game_input is None:
            return None
        if self.need_confirm is not None:
            if game_input.type == InputType.CHAR:
                if game_input.value == 'Y':
                    return {'action': 'confirm'}
                elif game_input.value == 'N':
                    self.need_confirm = None
            return {'action': 'super'}
        # if game_input.type == InputType.KEY and game_input.value == tcod.KEY_ESCAPE:
        #     return {'action': 'cancel'}
        return None

    def render(self, console):
        pass

    def render_clean(self, console):
        pass
