from entity.battle_abilities import BattleAbilityRage
from entity.battle_trait import get_random_possible_trait


class MonsterClass:
    name = ''

    def apply_class(self, monster, level):
        for _ in range(level):
            self.apply_level(monster, _ + 1)

    def apply_level(self, monster, level):
        self.gain_trait(monster, level)

    def gain_trait(self, monster, level):
        trait = get_random_possible_trait(monster)

        if trait is not None:
            monster.add_trait(trait)

    def get_abilities(self):
        return []


class MonsterClassFighter(MonsterClass):
    name = 'fighter'


class MonsterClassBarbarian(MonsterClass):
    name = 'barbarian'

    def get_abilities(self):
        return [
            BattleAbilityRage,
        ]


class MonsterClassRogue(MonsterClass):
    name = 'rogue'


all_classes = [
    MonsterClassFighter(),
    MonsterClassBarbarian(),
    MonsterClassRogue(),
]
