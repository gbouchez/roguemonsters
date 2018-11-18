from enum import Enum

import tcod

key = tcod.Key()
mouse = tcod.Mouse()


class InputType(Enum):
    KEY = 1
    MOUSE = 2
    CHAR = 3


class Input:
    def __init__(self, type, value):
        self.type = type
        self.value = value


class InputManager:
    def __init__(self):
        pass

    def get_input(self):
        tcod.sys_wait_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse, False)
        if key.vk and key.vk != tcod.KEY_TEXT:
            return Input(type=InputType.KEY, value=key.vk)
        if key.vk and key.vk == tcod.KEY_TEXT:
            return Input(type=InputType.CHAR, value=key.text)
        if mouse:
            return Input(type=InputType.MOUSE, value=mouse)
        return None
