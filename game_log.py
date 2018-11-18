import tcod

import textwrap

from variables import log_console_width, log_console_height

message_pool = []


class LogMessage:
    def __init__(self, text, color=tcod.white):
        self.text = text
        self.color = color


def add_log_message(message):
    new_msg_lines = textwrap.wrap(message.text, log_console_width)

    for line in new_msg_lines:
        if len(message_pool) == log_console_height:
            del message_pool[0]

        # Add the new line as a Message object, with the text and the color
        message_pool.append(LogMessage(line, message.color))


def get_message_pool():
    return message_pool


def get_monster_message_prefix(monster):
    if monster.player is None:
        return 'monster.'
    else:
        return 'you.'
