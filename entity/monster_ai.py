from numpy.random.mtrand import choice


class BasicAI:
    def __init__(self, monster):
        self.monster = monster

    def take_turn(self, player):
        abilities = filter(lambda ability: ability.meet_prerequisites(self.monster, player), self.monster.get_abilities())
        ability_choices = []
        ability_weights = []
        for ability in abilities:
            ability_choices.append(ability)
            ability_weights.append(ability.get_weight(self.monster, player))
        sum_weight = sum(ability_weights)
        if not ability_choices or sum_weight == 0:
            self.monster.rest_turn()
            return
        ability_weights = list(map(lambda weight: weight / sum_weight, ability_weights))

        chosen_ability = choice(ability_choices, p=ability_weights)

        chosen_ability.use_ability(self.monster, player)
