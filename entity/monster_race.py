from random import randint

from entity.battle_abilities import BattleAbilityMoveToPlayer, BattleAbilityAttackPlayer
from entity.battle_trait import get_random_possible_trait, TraitFastWalker
from entity.item_entity import ItemType


class MonsterRace:
    can_have_class = True
    name = ''
    name_article = 'a'
    char = '?'
    color = 255, 255, 255
    base_strength = 9
    base_dexterity = 9
    base_constitution = 9
    base_intelligence = 9
    random_strength = 6
    random_dexterity = 6
    random_constitution = 6
    random_intelligence = 6
    land_speed = 100
    traits_number_min = 2
    traits_number_max = 4
    traits_list = []
    can_equip = True
    equip_slots = [
        ItemType.WEAPON,
        ItemType.SHIELD,
        ItemType.BODY,
    ]

    def get_level(self):
        total_stats = self.base_strength + self.base_dexterity + self.base_constitution + self.base_intelligence
        total_stats += (self.random_strength + 1) / 2
        total_stats += (self.random_dexterity + 1) / 2
        total_stats += (self.random_constitution + 1) / 2
        total_stats += (self.random_intelligence + 1) / 2
        total_stats -= 50
        total_stats /= 5
        total_stats += ((-self.land_speed) + 100) / 10

        return 1 + int(total_stats)

    def get_strength(self):
        return self.base_strength + randint(1, self.random_strength)

    def get_dexterity(self):
        return self.base_dexterity + randint(1, self.random_dexterity)

    def get_constitution(self):
        return self.base_constitution + randint(1, self.random_constitution)

    def get_intelligence(self):
        return self.base_intelligence + randint(1, self.random_intelligence)

    def apply_race(self, monster):
        monster.strength = self.get_strength()
        monster.dexterity = self.get_dexterity()
        monster.constitution = self.get_constitution()
        monster.intelligence = self.get_intelligence()
        monster.land_speed = self.land_speed
        number_of_traits = randint(self.traits_number_min, self.traits_number_max)
        for _ in range(number_of_traits):
            self.gain_trait(monster)
        if self.can_equip:
            monster.equip_slots += self.equip_slots

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
    base_strength = 7
    base_dexterity = 5
    base_constitution = 5
    base_intelligence = 3
    random_strength = 5
    random_dexterity = 5
    random_constitution = 5
    random_intelligence = 3
    traits_list = [
        TraitFastWalker,
    ]


class MonsterRaceOrc(MonsterRace):
    name = 'orc'
    name_article = 'an'
    char = 'o'
    color = 120, 160, 40
    base_strength = 11
    base_dexterity = 7
    base_constitution = 11
    base_intelligence = 5
    random_strength = 7
    random_dexterity = 7
    random_constitution = 7
    random_intelligence = 7


class MonsterRaceKobold(MonsterRace):
    name = 'kobold'
    char = 'k'
    color = 0, 160, 0
    base_strength = 4
    base_dexterity = 11
    base_constitution = 3
    base_intelligence = 5
    random_strength = 6
    random_dexterity = 7
    random_constitution = 5
    random_intelligence = 13
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
    base_strength = 11
    base_dexterity = 14
    base_constitution = 7
    base_intelligence = 0
    random_strength = 4
    random_dexterity = 6
    random_constitution = 5
    random_intelligence = 3
    land_speed = 70
    can_equip = False
    traits_list = [
        TraitFastWalker,
    ]


class MonsterRaceGiantRat(MonsterRace):
    name = 'giant rat'
    char = 'r'
    color = 150, 150, 0
    can_have_class = False
    base_strength = 3
    base_dexterity = 7
    base_constitution = 7
    base_intelligence = 0
    random_strength = 5
    random_dexterity = 5
    random_constitution = 5
    random_intelligence = 3
    land_speed = 90
    can_equip = False
    traits_list = [
        TraitFastWalker,
    ]


all_races = [
    MonsterRaceGoblin(),
    MonsterRaceKobold(),
    MonsterRaceOrc(),
    MonsterRaceHuman(),

    MonsterRaceGiantSpider(),
    MonsterRaceGiantRat(),
]
