import textwrap

import tcod

from entity.battle_abilities import BattleAbilityMoveToPlayer, BattleAbilityAttackPlayer, BattleAbilityPickItemUp
from entity.item_entity import ItemEntity
from entity.monster_entity import MonsterEntity
from fov import initialize_fov, recompute_fov
from input import InputType
from game_log import get_message_pool
from scene.generic_scene import GenericScene
from scene.inventory_scene import InventoryScene
from variables import field_console_width, field_console_height, stat_console_height, log_console_height, \
    log_console_width, stat_console_width


class MapScene(GenericScene):
    def __init__(self, player, game_map):
        super().__init__()
        self.player = player
        self.game_map = game_map
        self.fov_recompute = True
        self.initialize_map(game_map)
        self.field_console = tcod.console_new(field_console_width, field_console_height)
        self.stat_console = tcod.console_new(stat_console_width, stat_console_height)
        self.log_console = tcod.console_new(log_console_width, log_console_height)
        tcod.console_set_default_foreground(self.field_console, tcod.white)
        tcod.console_set_default_foreground(self.stat_console, tcod.white)
        tcod.console_set_default_foreground(self.log_console, tcod.white)
        self.under_mouse = ''

    def initialize_map(self, game_map):
        self.game_map = game_map
        self.game_map.fov_map = initialize_fov(game_map)
        self.fov_recompute = True

    def manage_input(self, game_input):
        super_input = super().manage_input(game_input)
        if super_input is not None:
            return super_input

        if game_input is None:
            return None

        if game_input.type == InputType.MOUSE:
            mx, my = game_input.value.cx, game_input.value.cy
            mx = self.player.entity.x - int(field_console_width / 2) + mx
            my = self.player.entity.y - int(field_console_height / 2) + my
            self.under_mouse = self.game_map.get_names_at(mx, my)
            self.render_next = True
            return None
        self.under_mouse = ''

        if self.player.entity.dead:
            return None

        player_took_action = False

        if game_input.type == InputType.KEY:
            if game_input.value == tcod.KEY_UP \
                    or game_input.value == tcod.KEY_LEFT \
                    or game_input.value == tcod.KEY_DOWN \
                    or game_input.value == tcod.KEY_RIGHT \
                    or game_input.value == tcod.KEY_KP1 \
                    or game_input.value == tcod.KEY_KP2 \
                    or game_input.value == tcod.KEY_KP3 \
                    or game_input.value == tcod.KEY_KP4 \
                    or game_input.value == tcod.KEY_KP6 \
                    or game_input.value == tcod.KEY_KP7 \
                    or game_input.value == tcod.KEY_KP8 \
                    or game_input.value == tcod.KEY_KP9:
                coordinates = (0, 0)
                if game_input.value == tcod.KEY_UP or game_input.value == tcod.KEY_KP8:
                    coordinates = (0, -1)
                elif game_input.value == tcod.KEY_KP7:
                    coordinates = (-1, -1)
                elif game_input.value == tcod.KEY_LEFT or game_input.value == tcod.KEY_KP4:
                    coordinates = (-1, 0)
                elif game_input.value == tcod.KEY_KP1:
                    coordinates = (-1, 1)
                elif game_input.value == tcod.KEY_DOWN or game_input.value == tcod.KEY_KP2:
                    coordinates = (0, 1)
                elif game_input.value == tcod.KEY_KP3:
                    coordinates = (1, 1)
                elif game_input.value == tcod.KEY_RIGHT or game_input.value == tcod.KEY_KP6:
                    coordinates = (1, 0)
                elif game_input.value == tcod.KEY_KP9:
                    coordinates = (1, -1)
                attacked = self.game_map.move_monster(self.player.entity, coordinates)
                if attacked:
                    BattleAbilityAttackPlayer.reset_turn(self.player.entity)
                else:
                    BattleAbilityMoveToPlayer.reset_turn(self.player.entity)
                self.fov_recompute = True
                player_took_action = True
        elif game_input.type == InputType.CHAR:
            if game_input.value == 's':
                self.player.entity.reset_turn(100)
                player_took_action = True
            elif game_input.value == ',':
                BattleAbilityPickItemUp.use_ability(self.player.entity, self.player)
                player_took_action = True
            elif game_input.value == 'i':
                inventory_scene = InventoryScene(self.player, self)
                return {'action': 'change_scene', 'scene': inventory_scene}

        if player_took_action:
            self.player.entity.rest()
            self.render_next = True
            self.manage_all_entities()

        return None

    def render(self, console):
        if not self.render_next:
            return

        dx = -(self.player.entity.x - int(field_console_width / 2))
        dy = -(self.player.entity.y - int(field_console_height / 2))

        if self.fov_recompute:
            recompute_fov(self.game_map.fov_map, self.player.entity.x, self.player.entity.y, 10)

            for x in range(self.game_map.width):
                for y in range(self.game_map.height):
                    if x < self.player.entity.x - int(field_console_width / 2) \
                            or x > self.player.entity.x + int(field_console_width / 2) \
                            or y < self.player.entity.y - int(field_console_height / 2) \
                            or y > self.player.entity.y + int(field_console_height / 2):
                        continue
                    visible = tcod.map_is_in_fov(self.game_map.fov_map, x, y)

                    if visible:
                        tcod.console_set_char_background(
                            self.field_console,
                            x + dx,
                            y + dy,
                            self.game_map.field[x][y].background_color,
                            tcod.BKGND_SET
                        )
                        self.game_map.field[x][y].explored = True
                    elif self.game_map.field[x][y].explored:
                        tcod.console_set_char_background(
                            self.field_console,
                            x + dx,
                            y + dy,
                            self.game_map.field[x][y].background_color_dark,
                            tcod.BKGND_SET
                        )
                    else:
                        tcod.console_set_char_background(
                            self.field_console,
                            x + dx,
                            y + dy,
                            tcod.black,
                            tcod.BKGND_SET
                        )

        for x in range(field_console_width):
            for y in range(field_console_height):
                if x < (int(field_console_width / 2) - self.player.entity.x) \
                        or x > (self.game_map.width - 1 - self.player.entity.x + int(field_console_width / 2)) \
                        or y < (int(field_console_height / 2) - self.player.entity.y) \
                        or y > (self.game_map.height - 1 - self.player.entity.y + int(field_console_height / 2)):
                    tcod.console_set_char_background(self.field_console, x, y, tcod.black, tcod.BKGND_SET)

        for entity in self.game_map.entities:
            if entity.x < self.player.entity.x - int(field_console_width / 2) \
                    or entity.x > self.player.entity.x + int(field_console_width / 2) \
                    or entity.y < self.player.entity.y - int(field_console_height / 2) \
                    or entity.y > self.player.entity.y + int(field_console_height / 2):
                continue
            if not tcod.map_is_in_fov(self.game_map.fov_map, entity.x, entity.y):
                continue
            # Don't render a dead entity if there's already one on this tile
            if isinstance(entity, ItemEntity) and self.game_map.get_monster_at(entity.x, entity.y) is not None:
                continue
            # Don't render a dead entity if there's already one on this tile
            if isinstance(entity, MonsterEntity) \
                    and entity.dead \
                    and self.game_map.get_monster_at(entity.x, entity.y) is not None:
                continue
            tcod.console_set_default_foreground(self.field_console, entity.get_color())
            tcod.console_put_char(
                self.field_console,
                entity.x + dx,
                entity.y + dy,
                entity.get_char(),
                tcod.BKGND_NONE
            )

        tcod.console_blit(self.field_console, 0, 0, field_console_width, field_console_height, 0, 0, 0)
        self.render_stats()
        self.render_log()

    def render_log(self):
        y = 0
        for message in get_message_pool():
            tcod.console_set_default_foreground(self.log_console, message.color)
            tcod.console_print_ex(self.log_console, 0, y, tcod.BKGND_NONE, tcod.LEFT, message.text)
            y += 1

        tcod.console_blit(self.log_console, 0, 0, log_console_width, log_console_height, 0, 0, field_console_height)
        tcod.console_clear(self.log_console)

    def render_stats(self):
        tcod.console_set_default_background(self.stat_console, tcod.black)
        tcod.console_clear(self.stat_console)
        bar_width = int(float(self.player.entity.get_hp()) / self.player.entity.get_max_hp() * (stat_console_width - 6))
        tcod.console_set_default_background(self.stat_console, tcod.red)
        tcod.console_rect(self.stat_console, 5, 5, (stat_console_width - 6), 1, False, tcod.BKGND_SCREEN)
        tcod.console_set_default_background(self.stat_console, tcod.green)
        if bar_width > 0:
            tcod.console_rect(self.stat_console, 5, 5, bar_width, 1, False, tcod.BKGND_SCREEN)

        tcod.console_print_ex(self.stat_console, 1, 5, tcod.BKGND_NONE, tcod.LEFT, 'HP:')
        tcod.console_set_default_foreground(self.stat_console, tcod.black)
        tcod.console_print_ex(self.stat_console, 5, 5, tcod.BKGND_NONE, tcod.LEFT,
                                 '{0: 3}/{1: 3}'.format(
                                     self.player.entity.get_hp(),
                                     self.player.entity.get_max_hp(),
                                 ))
        tcod.console_set_default_foreground(self.stat_console, tcod.white)

        tcod.console_print_ex(self.stat_console, 1, 1, tcod.BKGND_NONE, tcod.LEFT,
                                 'Race:  {0}'.format(str.upper(self.player.entity.monster_race.name)))
        class_name = 'None'
        class_level = '-'
        if self.player.entity.monster_class is not None:
            class_name = str.upper(self.player.entity.monster_class.name)
            class_level = self.player.entity.class_level
        tcod.console_print_ex(self.stat_console, 1, 2, tcod.BKGND_NONE, tcod.LEFT,
                                 'Class: {0}'.format(class_name))
        tcod.console_print_ex(self.stat_console, 1, 3, tcod.BKGND_NONE, tcod.LEFT,
                                 'Level: {0}'.format(str(class_level)))
        tcod.console_print_ex(self.stat_console, 1, 6, tcod.BKGND_NONE, tcod.LEFT,
                                 'Land speed: {0: 2}'.format(
                                     self.player.entity.land_speed
                                 ))
        tcod.console_print_ex(self.stat_console, 1, 8, tcod.BKGND_NONE, tcod.LEFT,
                                 'STR {0:02} DEX {1:02} CON {2:02} INT {3:02}'.format(
                                     self.player.entity.get_strength(),
                                     self.player.entity.get_dexterity(),
                                     self.player.entity.get_constitution(),
                                     self.player.entity.get_intelligence(),
                                 ))
        tcod.console_print_ex(self.stat_console, 1, 10, tcod.BKGND_NONE, tcod.LEFT, 'Traits:')
        console_y = 11
        for trait in self.player.entity.traits:
            tcod.console_print_ex(self.stat_console, 1, console_y, tcod.BKGND_NONE, tcod.LEFT,
                                     ' {0}'.format(trait.name))
            console_y += 1

        under_mouse_lines = textwrap.wrap(self.under_mouse, stat_console_width)

        i_line = 0
        for line in under_mouse_lines:
            tcod.console_print_ex(self.stat_console, 1, field_console_height + i_line, tcod.BKGND_NONE,
                                     tcod.LEFT, line)
            i_line += 1

        tcod.console_blit(self.stat_console, 0, 0, stat_console_width, stat_console_height, 0, field_console_width,
                             0)

    def render_clean(self, console):
        if not self.render_next:
            return
        dx = -(self.player.entity.x - int(field_console_width / 2))
        dy = -(self.player.entity.y - int(field_console_height / 2))

        for entity in self.game_map.entities:
            if entity.x < self.player.entity.x - int(field_console_width / 2) \
                    or entity.x > self.player.entity.x + int(field_console_width / 2) \
                    or entity.y < self.player.entity.y - int(field_console_height / 2) \
                    or entity.y > self.player.entity.y + int(field_console_height / 2):
                continue
            tcod.console_put_char(self.field_console, entity.x + dx, entity.y + dy, ' ', tcod.BKGND_NONE)
        self.render_next = False

    def take_over_random_monster(self):
        self.player.entity = self.game_map.get_random_monster()
        self.player.entity.player = self.player

    def manage_all_entities(self):
        if self.player.entity.dead:
            return
        while True:
            for entity in self.game_map.entities:
                if not isinstance(entity, MonsterEntity):
                    continue
                entity.turn_to_action -= 1
                if entity.turn_to_action == 0:
                    if entity.player is not None:
                        return
                    if tcod.map_is_in_fov(self.game_map.fov_map, entity.x, entity.y):
                        entity.take_action(self.player)
                    else:
                        entity.rest_turn()
