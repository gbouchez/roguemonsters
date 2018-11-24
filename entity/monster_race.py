from random import randint

from numpy.random.mtrand import choice

from entity.battle_abilities import BattleAbilityMoveToPlayer, BattleAbilityAttackPlayer, BattleAbilitySpiderWeb
from entity.battle_trait import get_random_possible_trait, TraitFastWalker
from entity.item_entity import ItemType


class MonsterRace:
    can_have_class = True
    name = ''
    name_article = 'a'
    char = '?'
    color = 255, 255, 255
    stat_per_level = 4
    weight_strength = 10
    weight_dexterity = 10
    weight_constitution = 10
    weight_intelligence = 10
    land_speed = 100
    traits_number = 3
    traits_list = []
    can_equip = True
    equip_slots = [
        ItemType.WEAPON,
        ItemType.SHIELD,
        ItemType.BODY,
    ]

    def get_level(self):
        total_stats = self.weight_strength + self.weight_dexterity + self.weight_constitution + self.weight_intelligence
        total_stats -= 40
        total_stats /= 4
        total_stats += ((-self.land_speed) + 100) / 10
        total_stats += (self.traits_number - 3) * 5

        return 1 + int(total_stats)

    def apply_race(self, monster):
        monster.strength = self.weight_strength - 2
        monster.dexterity = self.weight_dexterity - 2
        monster.constitution = self.weight_constitution - 2
        monster.intelligence = self.weight_intelligence - 2
        monster.land_speed = self.land_speed
        self.apply_random_stats(monster)
        self.apply_random_stats(monster)
        for _ in range(self.traits_number):
            self.gain_trait(monster)
        if self.can_equip:
            monster.equip_slots += self.equip_slots

    def apply_random_stats(self, monster):
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

    def get_abilities(self):
        return [
            BattleAbilityMoveToPlayer,
            BattleAbilityAttackPlayer,
        ]

    def gain_trait(self, monster):
        trait = get_random_possible_trait(monster, self.traits_list)

        if trait is not None:
            monster.add_trait(trait)


class MonsterRaceGoblin(MonsterRace):
    name = 'goblin'
    char = 'g'
    color = 160, 160, 30
    weight_strength = 10
    weight_dexterity = 8
    weight_constitution = 8
    weight_intelligence = 5
    traits_list = [
        TraitFastWalker,
    ]


class MonsterRaceOrc(MonsterRace):
    name = 'orc'
    name_article = 'an'
    char = 'o'
    color = 120, 160, 40
    weight_strength = 15
    weight_dexterity = 11
    weight_constitution = 15
    weight_intelligence = 9


class MonsterRaceKobold(MonsterRace):
    name = 'kobold'
    char = 'k'
    color = 0, 160, 0
    weight_strength = 8
    weight_dexterity = 15
    weight_constitution = 6
    weight_intelligence = 11
    traits_list = [
        TraitFastWalker,
    ]


class MonsterRaceHuman(MonsterRace):
    name = 'human'
    char = 'h'
    color = 150, 150, 150


class MonsterRaceGiantSpider(MonsterRace):
    name = 'giant spider'
    char = 's'
    color = 160, 160, 160
    can_have_class = False
    weight_strength = 13
    weight_dexterity = 17
    weight_constitution = 10
    weight_intelligence = 3
    land_speed = 70
    can_equip = False
    traits_list = [
        TraitFastWalker,
    ]

    def get_abilities(self):
        return super(MonsterRaceGiantSpider, self).get_abilities() + [
            BattleAbilitySpiderWeb,
        ]


class MonsterRaceGiantRat(MonsterRace):
    name = 'giant rat'
    char = 'r'
    color = 150, 150, 0
    can_have_class = False
    weight_strength = 6
    weight_dexterity = 10
    weight_constitution = 10
    weight_intelligence = 3
    land_speed = 90
    can_equip = False
    traits_list = [
        TraitFastWalker,
    ]


all_races = [
    # MonsterRaceGoblin(),
    # MonsterRaceKobold(),
    # MonsterRaceOrc(),
    MonsterRaceHuman(),

    MonsterRaceGiantSpider(),
    # MonsterRaceGiantRat(),
]
