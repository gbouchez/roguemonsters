import tcod

from game_log import add_log_message, LogMessage
from input import InputManager
from map_generator import generate_map
from messages.messages import get_message
from player import Player
from render import RenderEngine
from save import load_game, save_game
from scene.map_scene import MapScene


class Game:
    def __init__(self):
        self.render_engine = RenderEngine()
        self.input_manager = InputManager()
        self.player = load_game()
        if self.player is None:
            self.player = Player()
            game_map = generate_map(1)
            game_map.take_over_monster(self.player)
        game_map = self.player.entity.game_map

        map_scene = MapScene(self.player, game_map)
        self.current_scene = map_scene

    def run(self):
        while not tcod.console_is_window_closed():
            self.render_engine.render_scene(self.current_scene)
            if self.current_scene.data is not None:
                input_return = self.current_scene.manage_input(None)
            else:
                game_input = self.input_manager.get_input()
                input_return = self.current_scene.manage_input(game_input)
            if input_return is None:
                continue
            if input_return['action']:
                if input_return['action'] == 'confirm':
                    input_return = self.current_scene.need_confirm
                if input_return['action'] == 'cancel' or input_return['action'] == 'cancel_with_action':
                    if self.current_scene.previous_scene is not None:
                        current = self.current_scene
                        self.current_scene = self.current_scene.previous_scene
                        current.previous_scene = None
                        if input_return['action'] == 'cancel_with_action' and isinstance(self.current_scene, MapScene):
                            self.current_scene.player_took_action = True
                        self.current_scene.render_next = True
                        del current
                    else:
                        if self.current_scene.need_confirm is not None:
                            return True
                        self.current_scene.need_confirm = input_return
                        add_log_message(
                            LogMessage(
                                get_message("quit_game.confirm"),
                                tcod.light_cyan
                            )
                        )
                        self.current_scene.render_next = True
                elif input_return['action'] == 'change_scene':
                    self.current_scene = input_return['scene']
                    self.current_scene.render_next = True

        if not self.player.entity.dead:
            save_game(self.player)

