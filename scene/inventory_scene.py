from enum import Enum

import tcod

from input import InputType
from messages.messages import get_message
from render import screen_width, screen_height
from scene.generic_scene import GenericScene


class InventoryMode(Enum):
    USE = 1
    DESCRIPTION = 2
    DROP = 3


class InventoryScene(GenericScene):
    def __init__(self, player, previous_scene=None, mode=InventoryMode.DESCRIPTION):
        super().__init__()
        self.player = player
        self.previous_scene = previous_scene
        self.mode = mode
        self.item = None
        self.console = tcod.console_new(screen_width, screen_height)
        tcod.console_set_default_foreground(self.console, tcod.white)
        tcod.console_set_default_background(self.console, tcod.black)

    def manage_input(self, game_input):
        super_input = super().manage_input(game_input)
        if super_input is not None:
            if super_input['action'] == 'cancel' and self.item is not None:
                self.item = None
                self.render_next = True
                return None
            return super_input

        if game_input is None:
            return None

        if game_input.type == InputType.CHAR:
            if game_input.value == '?':
                if self.mode == InventoryMode.USE:
                    self.mode = InventoryMode.DESCRIPTION
                elif self.mode == InventoryMode.DESCRIPTION:
                    self.mode = InventoryMode.DROP
                else:
                    self.mode = InventoryMode.USE
            elif (ord('a') <= ord(game_input.value) <= ord('z')) \
                    or (ord('A') <= ord(game_input.value) <= ord('Z')):
                item = self.player.entity.inventory.get_item_at_char(game_input.value)
                if item is not None:
                    if self.mode == InventoryMode.DESCRIPTION:
                        self.item = item
                    elif self.mode == InventoryMode.USE and item.usable:
                        item.use()
                        self.player.entity.inventory.remove_item(item)
                        self.player.entity.reset_turn(100)
                        return {'action': 'cancel'}
                    elif self.mode == InventoryMode.DROP:
                        self.player.entity.inventory.drop_item(item)
                        self.player.entity.reset_turn(100)
                        return {'action': 'cancel'}

        self.render_next = True
        return None

    def render(self, console):
        if not self.render_next:
            return
        tcod.console_clear(self.console)

        if self.item is None:
            self.render_list()

        tcod.console_blit(self.console, 0, 0, screen_width, screen_height, 0, 0, 0)

    def render_list(self):
        tcod.console_set_default_foreground(self.console, tcod.white)
        if self.mode == InventoryMode.DESCRIPTION:
            message = get_message('inventory.description')
        elif self.mode == InventoryMode.DROP:
            message = get_message('inventory.drop')
        else:
            message = get_message('inventory.use')
        tcod.console_print_ex(
            self.console,
            1,
            1,
            tcod.BKGND_NONE,
            tcod.LEFT,
            message
        )

        index = 0
        for item in self.player.entity.inventory.items:
            letter_index = ord('a') + index
            if letter_index > ord('z'):
                letter_index = ord('A') + index - 26

            if item.usable or self.mode != InventoryMode.USE:
                color = item.get_color()
                message = '{0}) {1}'
            else:
                color = tcod.dark_grey
                message = '   {1}'

            tcod.console_set_default_foreground(self.console, color)
            tcod.console_print_ex(
                self.console,
                2,
                3 + index,
                tcod.BKGND_NONE,
                tcod.LEFT,
                message.format(chr(letter_index), item.get_name())
            )
            index += 1

        if self.mode == InventoryMode.DESCRIPTION:
            message = get_message('inventory.switch_mode.drop')
        elif self.mode == InventoryMode.DROP:
            message = get_message('inventory.switch_mode.use')
        else:
            message = get_message('inventory.switch_mode.description')

        tcod.console_set_default_foreground(self.console, tcod.desaturated_green)
        tcod.console_print_ex(
            self.console,
            1,
            55,
            tcod.BKGND_NONE,
            tcod.LEFT,
            message.format('?')
        )

    def render_clean(self, console):
        if not self.render_next:
            return
        tcod.console_clear(self.console)
        self.render_next = False
