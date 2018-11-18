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
        map_scene.take_over_random_monster()
        self.current_scene = map_scene

    def run(self):
        while not tcod.console_is_window_closed():
            self.render_engine.render_scene(self.current_scene)
            game_input = self.input_manager.get_input()
            input_return = self.current_scene.manage_input(game_input)
            if input_return is None:
                continue
            if input_return['action']:
                if input_return['action'] == 'cancel':
                    if self.current_scene.previous_scene is not None:
                        current = self.current_scene
                        self.current_scene = self.current_scene.previous_scene
                        self.current_scene.render_next = True
                        del current
                    else:
                        return True
                elif input_return['action'] == 'change_scene':
                    self.current_scene = input_return['scene']
                    self.current_scene.render_next = True

