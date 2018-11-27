import os
import shelve


def save_game(player):
    with shelve.open('save.dat', 'n') as data_file:
        data_file['player'] = player


def load_game():
    if not os.path.isfile('save.dat'):
        return None

    with shelve.open('save.dat', 'r') as data_file:
        player = data_file['player']

    return player


def delete_game():
    if not os.path.isfile('save.dat'):
        return

    os.remove('save.dat')
