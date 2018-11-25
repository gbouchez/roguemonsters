from numpy.random.mtrand import choice

from entity.battle_abilities import BattleAbilityRage
from entity.battle_trait import get_random_possible_trait


class MonsterClass:
    name = ''
    stat_per_level = 4
    weight_strength = 10
    weight_dexterity = 10
    weight_constitution = 10
    weight_intelligence = 10

    def apply_class(self, monster, level):
        for _ in range(level):
            self.apply_level(monster, _ + 1)

    def apply_level(self, monster, level):
        self.gain_trait(monster, level)
        stats = ['strength', 'dexterity', 'constitution', 'constitution']
        weights = [self.weight_strength, self.weight_dexterity, self.weight_constitution, self.weight_intelligence]
        sum_weights = sum(weights)
        weights = list(map(lambda weight: weight / sum_weights, weights))
        for _ in range(self.stat_per_level):
            chosen_stat = choice(stats, p=weights)
            if chosen_stat == 'strength':
                monster.strength += 1
            elif chosen_stat == 'dexterity':
                monster.dexterity += 1
            elif chosen_stat == 'constitution':
                monster.constitution += 1
            elif chosen_stat == 'intelligence':
                monster.intelligence += 1

    def gain_trait(self, monster, level):
        # todo gain class traits
        trait = None

        if trait is not None:
            monster.add_trait(trait)

    def get_abilities(self):
        return []


class MonsterClassFighter(MonsterClass):
    name = 'fighter'
    weight_strength = 15
    weight_dexterity = 10
    weight_constitution = 14
    weight_intelligence = 6


class MonsterClassBarbarian(MonsterClass):
    name = 'barbarian'
    weight_strength = 18
    weight_dexterity = 8
    weight_constitution = 15
    weight_intelligence = 4

    def get_abilities(self):
        return [
            BattleAbilityRage,
        ]


class MonsterClassRogue(MonsterClass):
    name = 'rogue'
    weight_strength = 10
    weight_dexterity = 16
    weight_constitution = 10
    weight_intelligence = 12


all_classes = [
    MonsterClassFighter(),
    MonsterClassBarbarian(),
    MonsterClassRogue(),
]
