from numpy.random.mtrand import choice


class Trait:
    name = ''

    @staticmethod
    def apply_effect(monster):
        pass

    @staticmethod
    def meet_prerequisites(monster):
        pass


class TraitFastWalker(Trait):
    name = 'Fast walker'

    @staticmethod
    def apply_effect(monster):
        monster.land_speed -= 4

    @staticmethod
    def meet_prerequisites(monster):
        return monster.land_speed <= 200


all_traits = [
    TraitFastWalker,
]


def get_random_possible_trait(monster, trait_list=None):
    if trait_list is None:
        trait_list = all_traits
    trait_list = list(
        filter(
            lambda trait:
            trait.meet_prerequisites(monster)
            and trait not in monster.traits
            ,
            trait_list
        )
    )

    if not trait_list:
        return None
    return choice(trait_list)
