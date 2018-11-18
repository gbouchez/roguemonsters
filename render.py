import tcod

screen_width = 80
screen_height = 60


class RenderEngine:
    def __init__(self):
        self.screen_width = 80
        self.screen_height = 60

        tcod.console_set_custom_font('arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
        self.root_console = tcod.console_init_root(self.screen_width, self.screen_height, title='Rogue Monsters')
        tcod.console_set_default_foreground(0, tcod.white)

    def render_scene(self, scene):
        scene.render(self.root_console)
        tcod.console_flush()
        scene.render_clean(self.root_console)
