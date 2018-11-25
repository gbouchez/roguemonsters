from entity.item_template import ShortSwordTemplate, PotionHealLightTemplate, LongSwordTemplate, FlailTemplate, \
    LeatherArmourTemplate, BucklerTemplate, ScaleMailTemplate, ChainmailTemplate, WoodenShieldTemplate, DaggerTemplate
from entity.item_entity import ItemType

templates_by_type = {
    ItemType.POTION: [
        PotionHealLightTemplate,
    ],
    ItemType.WEAPON: [
        DaggerTemplate,
        ShortSwordTemplate,
        LongSwordTemplate,
        FlailTemplate,
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
