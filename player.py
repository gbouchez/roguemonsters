from entity.battle_abilities import BattleAbilitySoulSteal


class Player:
    def __init__(self):
        self.entity = None

    def get_x(self):
        return self.entity.x

    def get_y(self):
        return self.entity.y

    def get_abilities(self):
        return [
            BattleAbilitySoulSteal
        ]
