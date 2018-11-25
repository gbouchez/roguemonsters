from random import randint

from numpy.random.mtrand import choice

from entity.battle_abilities import BattleAbilityMoveToPlayer, BattleAbilityAttackPlayer, BattleAbilitySpiderWeb
from entity.battle_trait import get_random_possible_trait, TraitFastWalker, TraitGoodEyesight
from entity.item_entity import ItemType


class MonsterRace:
    can_have_class = True
    name = ''
    name_article = 'a'
    char = '?'
    color = 255, 255, 255
    stat_per_level = 4
    weight_strength = 12
    weight_dexterity = 12
    weight_constitution = 12
    weight_intelligence = 12
    land_speed = 100
    natural_damage = 1
    natural_armor = 0
    traits_number = 3
    traits_list = [
        TraitFastWalker,
        TraitGoodEyesight,
    ]
    custom_traits_list = []
    can_equip = True
    equip_slots = [
        ItemType.WEAPON,
        ItemType.SHIELD,
        ItemType.BODY,
    ]

    def get_level(self):
        total_stats = self.weight_strength + self.weight_dexterity + self.weight_constitution + self.weight_intelligence
        total_stats -= 48
        total_stats /= 4
        total_stats += ((-self.land_speed) + 100) / 10
        total_stats += (self.traits_number - 3) * 5

        if not self.can_equip:
            total_stats -= 3
            total_stats += self.natural_damage // 2
        else:
            total_stats += len(self.equip_slots) - 3
        total_stats += self.natural_armor

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
        trait = get_random_possible_trait(monster, self.get_possible_traits())

        if trait is not None:
            monster.add_trait(trait)

    def get_natural_damage(self):
        return self.natural_damage

    def get_natural_armor(self):
        return self.natural_armor

    def get_possible_traits(self):
        return self.traits_list + self.custom_traits_list


class MonsterRaceGoblin(MonsterRace):
    name = 'goblin'
    char = 'g'
    color = 160, 160, 30
    weight_strength = 10
    weight_dexterity = 8
    weight_constitution = 10
    weight_intelligence = 6


class MonsterRaceHobgoblin(MonsterRace):
    name = 'hobgoblin'
    char = 'g'
    color = 180, 140, 30
    weight_strength = 14
    weight_dexterity = 12
    weight_constitution = 12
    weight_intelligence = 8


class MonsterRaceOrc(MonsterRace):
    name = 'orc'
    name_article = 'an'
    char = 'o'
    color = 120, 160, 40
    weight_strength = 15
    weight_dexterity = 10
    weight_constitution = 15
    weight_intelligence = 7


class MonsterRaceOgre(MonsterRace):
    name = 'ogre'
    name_article = 'an'
    char = 'O'
    color = 160, 80, 40
    weight_strength = 24
    weight_dexterity = 6
    weight_constitution = 20
    weight_intelligence = 4


class MonsterRaceHalfOrc(MonsterRace):
    name = 'half-orc'
    name_article = 'a'
    char = 'o'
    color = 135, 155, 95
    weight_strength = 13
    weight_dexterity = 11
    weight_constitution = 13
    weight_intelligence = 10


class MonsterRaceKobold(MonsterRace):
    name = 'kobold'
    char = 'k'
    color = 0, 160, 0
    weight_strength = 8
    weight_dexterity = 15
    weight_constitution = 6
    weight_intelligence = 14


class MonsterRaceTengu(MonsterRace):
    name = 'tengu'
    char = 't'
    color = 0, 160, 160
    weight_strength = 10
    weight_dexterity = 15
    weight_constitution = 10
    weight_intelligence = 15
    land_speed = 120
    # todo flight speed


class MonsterRaceCentaur(MonsterRace):
    name = 'centaur'
    char = 'c'
    color = 160, 160, 20
    weight_strength = 14
    weight_dexterity = 16
    weight_constitution = 14
    weight_intelligence = 16
    land_speed = 80
    equip_slots = [
        ItemType.WEAPON,
        ItemType.SHIELD,
        ItemType.BODY,
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
    weight_strength = 14
    weight_dexterity = 18
    weight_constitution = 10
    weight_intelligence = 3
    land_speed = 80
    natural_damage = 3
    natural_armor = 2
    can_equip = False

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
    weight_constitution = 6
    weight_intelligence = 6
    land_speed = 60
    natural_damage = 1
    natural_armor = 1
    can_equip = False


all_races = [
    MonsterRaceGoblin(),
    MonsterRaceHobgoblin(),
    MonsterRaceKobold(),
    MonsterRaceOgre(),
    MonsterRaceOrc(),
    MonsterRaceHalfOrc(),
    MonsterRaceHuman(),
    MonsterRaceTengu(),
    MonsterRaceCentaur(),

    MonsterRaceGiantSpider(),
    MonsterRaceGiantRat(),
]
