import tcod
from enum import Enum
from entity.battle_abilities import AbilityTargeting
from input import InputType
from messages.messages import get_message
from modes import MapMode
from render import screen_width, screen_height
from scene.generic_scene import GenericScene


class AbilityMode(Enum):
    DESCRIPTION = 1
    USE = 2


class AbilityScene(GenericScene):
    def __init__(self, player, previous_scene=None):
        super().__init__()
        self.player = player
        self.previous_scene = previous_scene
        self.mode = AbilityMode.DESCRIPTION
        self.ability = None
        self.data = None
        self.console = tcod.console_new(screen_width, screen_height)
        tcod.console_set_default_foreground(self.console, tcod.white)
        tcod.console_set_default_background(self.console, tcod.black)

    def manage_input(self, game_input):
        if self.data is not None:
            self.previous_scene.mode = MapMode.FIELD
            self.previous_scene.render_next = True
            if self.data.get('action') == 'targeted':
                self.ability.use_ability(self.player.entity, self.data.get('target'))
                return {'action': 'cancel_with_action'}
            self.ability = None
            self.data = None

        super_input = super().manage_input(game_input)
        if super_input is not None:
            if super_input['action'] == 'cancel' and self.ability is not None:
                self.ability = None
                self.render_next = True
                return None
            return super_input

        if game_input is None:
            return None

        if game_input.type == InputType.CHAR:
            if game_input.value == '?':
                if self.mode == AbilityMode.DESCRIPTION:
                    self.mode = AbilityMode.USE
                else:
                    self.mode = AbilityMode.DESCRIPTION
            elif (ord('a') <= ord(game_input.value) <= ord('z')) \
                    or (ord('A') <= ord(game_input.value) <= ord('Z')):
                ability = self.player.entity.get_ability_at_char(game_input.value)
                if ability is not None:
                    if self.mode == AbilityMode.DESCRIPTION:
                        self.ability = ability
                    elif self.mode == AbilityMode.USE:
                        if ability.targeting == AbilityTargeting.SELF:
                            ability.use_ability(self.player.entity, self.player.entity)
                            self.previous_scene
                            return {'action': 'cancel_with_action'}
                        elif ability.targeting == AbilityTargeting.LOS:
                            self.ability = ability
                            self.previous_scene.mode = MapMode.TARGETING
                            self.previous_scene.previous_scene = self
                            self.previous_scene.target_mode = ability.targeting
                            self.previous_scene.target_distance = ability.targeting_distance
                            self.previous_scene.target_x = self.player.entity.x
                            self.previous_scene.target_y = self.player.entity.y
                            self.data = {'action': None}
                            return {'action': 'change_scene', 'scene': self.previous_scene}

        self.render_next = True
        return None

    def render(self, console):
        if not self.render_next:
            return
        tcod.console_clear(self.console)

        if self.mode != AbilityMode.DESCRIPTION or self.ability is None:
            self.render_list()

        tcod.console_blit(self.console, 0, 0, screen_width, screen_height, 0, 0, 0)

    def render_list(self):
        tcod.console_set_default_foreground(self.console, tcod.white)
        if self.mode == AbilityMode.DESCRIPTION:
            message = get_message('ability_menu.description')
        else:
            message = get_message('ability_menu.use')
        tcod.console_print_ex(
            self.console,
            1,
            1,
            tcod.BKGND_NONE,
            tcod.LEFT,
            message
        )

        index = 0
        for ability in self.player.entity.get_abilities():
            if ability.hidden:
                continue
            letter_index = ord('a') + index
            if letter_index > ord('z'):
                letter_index = ord('A') + index - 26

            message = '{0}) {1}'

            tcod.console_set_default_foreground(self.console, tcod.white)
            tcod.console_print_ex(
                self.console,
                2,
                3 + index,
                tcod.BKGND_NONE,
                tcod.LEFT,
                message.format(chr(letter_index), ability.get_name())
            )
            index += 1

        if self.mode == AbilityMode.DESCRIPTION:
            message = get_message('ability_menu.switch_mode.use')
        else:
            message = get_message('ability_menu.switch_mode.description')

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
