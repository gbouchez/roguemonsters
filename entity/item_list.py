from entity.item_template import ShortSwordTemplate, PotionHealLightTemplate, LongSwordTemplate, FlailTemplate, \
    LeatherArmourTemplate, BucklerTemplate, ScaleMailTemplate, ChainmailTemplate, WoodenShieldTemplate, DaggerTemplate, \
    PotionHealMediumTemplate, PotionHealHeavyTemplate, PotionStrengthTemplate, ClubTemplate, MaceTemplate, \
    HammerTemplate, MorningstarTemplate, WarhammerTemplate, TwoHandedSwordTemplate
from entity.item_entity import ItemType

templates_by_type = {
    ItemType.POTION: [
        PotionHealLightTemplate,
        PotionHealMediumTemplate,
        PotionHealHeavyTemplate,
        PotionStrengthTemplate,
    ],
    ItemType.WEAPON: [
        ClubTemplate,
        MaceTemplate,
        HammerTemplate,
        MorningstarTemplate,
        FlailTemplate,
        WarhammerTemplate,
        DaggerTemplate,
        ShortSwordTemplate,
        LongSwordTemplate,
        TwoHandedSwordTemplate,
    ],
    ItemType.SHIELD: [
        WoodenShieldTemplate,
        BucklerTemplate,
    ],
    ItemType.BODY: [
        LeatherArmourTemplate,
        ScaleMailTemplate,
        ChainmailTemplate,
    ],
}
