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
        monster.add_stat_bonus('land_speed', 'trait_fast_walker', -10)

    @staticmethod
    def meet_prerequisites(monster):
        return True


class TraitGoodEyesight(Trait):
    name = 'Good eyesight'

    @staticmethod
    def apply_effect(monster):
        monster.add_stat_bonus('accuracy', 'trait_good_eyesight', 4)

    @staticmethod
    def meet_prerequisites(monster):
        return True


all_traits = [
    TraitFastWalker,
    TraitGoodEyesight,
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
