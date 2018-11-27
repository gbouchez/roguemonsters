from enum import Enum

import tcod

key = tcod.Key()
mouse = tcod.Mouse()


class InputType(Enum):
    KEY = 1
    MOUSE = 2
    CHAR = 3


class Input:
    def __init__(self, type, value, key):
        self.type = type
        self.value = value
        self.key = key


class InputManager:
    def __init__(self):
        pass

    def get_input(self):
        tcod.sys_wait_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse, False)
        if key.vk and key.vk not in (tcod.KEY_TEXT, tcod.KEY_CHAR):
            return Input(InputType.KEY, key.vk, key)
        if key.vk and key.vk == tcod.KEY_TEXT:
            return Input(InputType.CHAR, key.text, key)
        if key.vk and key.vk == tcod.KEY_CHAR:
            return Input(InputType.CHAR, chr(key.c), key)
        if mouse:
            return Input(InputType.MOUSE, mouse, key)
        return None
