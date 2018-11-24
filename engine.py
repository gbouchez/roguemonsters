import tcod

from input import InputManager
from map_generator import MapGenerator
from player import Player
from render import RenderEngine
from scene.map_scene import MapScene


class Game:
    def __init__(self):
        self.render_engine = RenderEngine()
        self.input_manager = InputManager()
        self.map_generator = MapGenerator()
        self.player = Player()
        first_map = self.map_generator.generate_map(1)
        map_scene = MapScene(self.player, first_map)
        first_map.take_over_random_monster(self.player)
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
                        return True
                elif input_return['action'] == 'change_scene':
                    self.current_scene = input_return['scene']
                    self.current_scene.render_next = True

