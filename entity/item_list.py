from entity.item_template import ShortSwordTemplate, PotionHealLightTemplate, LongSwordTemplate, FlailTemplate, \
    LeatherArmourTemplate, BucklerTemplate
from entity.item_entity import ItemType

templates_by_type = {
    ItemType.POTION: [
        PotionHealLightTemplate,
    ],
    ItemType.WEAPON: [
        ShortSwordTemplate,
        LongSwordTemplate,
        FlailTemplate,
    ],
    ItemType.SHIELD: [
        BucklerTemplate,
    ],
    ItemType.BODY: [
        LeatherArmourTemplate,
    ],
}
