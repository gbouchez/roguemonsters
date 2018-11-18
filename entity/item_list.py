from entity.item_template import ShortSwordTemplate, PotionHealLightTemplate, LongSwordTemplate, FlailTemplate
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
}
