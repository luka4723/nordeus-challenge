import arcade, requests
from pathlib import Path

import requests

r1 = requests.get("http://127.0.0.1:8000/c/2")
data = r1.json()

KNIGHT_HP    = data["KNIGHT_HP"]
KNIGHT_ATK   = data["KNIGHT_ATK"]
KNIGHT_DEF   = data["KNIGHT_DEF"]
KNIGHT_MAGIC = data["KNIGHT_MAGIC"]

WIZARD_HP    = data["WIZARD_HP"]
WIZARD_ATK   = data["WIZARD_ATK"]
WIZARD_DEF   = data["WIZARD_DEF"]
WIZARD_MAGIC = data["WIZARD_MAGIC"]

ROGUE_HP    = data["ROGUE_HP"]
ROGUE_ATK   = data["ROGUE_ATK"]
ROGUE_DEF   = data["ROGUE_DEF"]
ROGUE_MAGIC = data["ROGUE_MAGIC"]

BERSERKER_HP    = data["BERSERKER_HP"]
BERSERKER_ATK   = data["BERSERKER_ATK"]
BERSERKER_DEF   = data["BERSERKER_DEF"]
BERSERKER_MAGIC = data["BERSERKER_MAGIC"]

GRANNY_HP    = data["GRANNY_HP"]
GRANNY_ATK   = data["GRANNY_ATK"]
GRANNY_DEF   = data["GRANNY_DEF"]
GRANNY_MAGIC = data["GRANNY_MAGIC"]

WITCH_HP    = data["WITCH_HP"]
WITCH_ATK   = data["WITCH_ATK"]
WITCH_DEF   = data["WITCH_DEF"]
WITCH_MAGIC = data["WITCH_MAGIC"]

SPIDER_HP    = data["SPIDER_HP"]
SPIDER_ATK   = data["SPIDER_ATK"]
SPIDER_DEF   = data["SPIDER_DEF"]
SPIDER_MAGIC = data["SPIDER_MAGIC"]

DRAGON_HP    = data["DRAGON_HP"]
DRAGON_ATK   = data["DRAGON_ATK"]
DRAGON_DEF   = data["DRAGON_DEF"]
DRAGON_MAGIC = data["DRAGON_MAGIC"]

WARRIOR_HP    = data["WARRIOR_HP"]
WARRIOR_ATK   = data["WARRIOR_ATK"]
WARRIOR_DEF   = data["WARRIOR_DEF"]
WARRIOR_MAGIC = data["WARRIOR_MAGIC"]

MAGE_HP    = data["MAGE_HP"]
MAGE_ATK   = data["MAGE_ATK"]
MAGE_DEF   = data["MAGE_DEF"]
MAGE_MAGIC = data["MAGE_MAGIC"]

ORDER_HP      = data["ORDER_HP"]
ORDER_ATK     = data["ORDER_ATK"]
ORDER_DEFENSE = data["ORDER_DEFENSE"]
ORDER_MAGIC   = data["ORDER_MAGIC"]

LVLUP_HP      = data["LVLUP_HP"]
LVLUP_ATK     = data["LVLUP_ATK"]
LVLUP_DEFENSE = data["LVLUP_DEFENSE"]
LVLUP_MAGIC   = data["LVLUP_MAGIC"]

SLASH_DMG = data["SLASH_DMG"]

SHIELDUP_DEF_INC = data["SHIELDUP_DEF_INC"]
SHIELDUP_LEN     = data["SHIELDUP_LEN"]

BATTLECRY_ATK_INC = data["BATTLECRY_ATK_INC"]
BATTLECRY_LEN     = data["BATTLECRY_LEN"]

SECONDWIND_HEAL = data["SECONDWIND_HEAL"]

SHADOWBOLT_DMG = data["SHADOWBOLT_DMG"]

DRAINLIFE_DMG = data["DRAINLIFE_DMG"]

CURSE_ATK_DEC = data["CURSE_ATK_DEC"]
CURSE_LEN     = data["CURSE_LEN"]

DARKPACT_HEALTH_COST = data["DARKPACT_HEALTH_COST"]
DARKPACT_MAGIC_INC   = data["DARKPACT_MAGIC_INC"]
DARKPACT_LEN         = data["DARKPACT_LEN"]

BITE_DMG             = data["BITE_DMG"]
WEBTHROW_DMG         = data["WEBTHROW_DMG"]
WEBTHROW_DEFENSE_DEC = data["WEBTHROW_DEFENSE_DEC"]
WEBTHROW_LEN         = data["WEBTHROW_LEN"]
POUNCE_DMG           = data["POUNCE_DMG"]
SKITTER_DEF_INC      = data["SKITTER_DEF_INC"]
SKITTER_LEN          = data["SKITTER_LEN"]

FLAMEBREATH_DMG      = data["FLAMEBREATH_DMG"]
CLAWSWIPE_DMG        = data["CLAWSWIPE_DMG"]
INTIMIDATE_ATK_DEC   = data["INTIMIDATE_ATK_DEC"]
INTIMIDATE_LEN       = data["INTIMIDATE_LEN"]
DRAGONSCALES_DEF_INC = data["DRAGONSCALES_DEF_INC"]
DRAGONSCALES_LEN     = data["DRAGONSCALES_LEN"]

RUSTYBLADE_DMG   = data["RUSTYBLADE_DMG"]
DIRTYKICK_DMG    = data["DIRTYKICK_DMG"]
DIRTYKICK_DEF_DEC = data["DIRTYKICK_DEF_DEC"]
DIRTYKICK_LEN    = data["DIRTYKICK_LEN"]
FRENZY_ATK_INC   = data["FRENZY_ATK_INC"]
FRENZY_LEN       = data["FRENZY_LEN"]
HEADBUTT_DMG     = data["HEADBUTT_DMG"]

FIREBOLT_DMG          = data["FIREBOLT_DMG"]
ARCANESURGE_MAGIC_INT = data["ARCANESURGE_MAGIC_INT"]
ARCANESURGE_LEN       = data["ARCANESURGE_LEN"]
MANADRAIN_DMG         = data["MANADRAIN_DMG"]
MANADRAIN_MAGIC_DEC   = data["MANADRAIN_MAGIC_DEC"]
MANADRAIN_LEN         = data["MANADRAIN_LEN"]
HEXSHIELD_DEFENSE_INC = data["HEXSHIELD_DEFENSE_INC"]
HEXSHIELD_LEN         = data["HEXSHIELD_LEN"]

BANDAGES_HEAL = data["BANDAGES_HEAL"]

DIRTTHROW_ATK_DEC = data["DIRTTHROW_ATK_DEC"]
DIRTTHROW_DEF_INC = data["DIRTTHROW_DEF_INC"]
DIRTTHROW_LEN     = data["DIRTTHROW_LEN"]

SHANKING_DMG       = data["SHANKING_DMG"]
SHANKING_BLEED_DMG = data["SHANKING_BLEED_DMG"]
SHANKING_LEN       = data["SHANKING_LEN"]

SHATTEREDFLASK_DMG        = data["SHATTEREDFLASK_DMG"]
SHATTEREDFLASK_POISON_DMG = data["SHATTEREDFLASK_POISON_DMG"]
SHATTEREDFLASK_LEN        = data["SHATTEREDFLASK_LEN"]

HYPNOTIZE_LEN = data["HYPNOTIZE_LEN"]

BASE_XP     = data["BASE_XP"]
BASE_GOLD   = data["BASE_GOLD"]
XP_INC     = data["XP_INC"]
GOLD_INC   = data["GOLD_INC"]
PRICES = data["PRICES"]

assets_path = Path(__file__).parent.parent.resolve() / Path("resources")
arcade.resources.add_resource_handle("res", assets_path)
arcade.load_font(":resources:/fonts/ttf/Kenney/Kenney_Mini.ttf")

SOUND = arcade.Sound(":res:click.mp3")


BTN_NORMAL_TEX  = arcade.load_texture(":resources:/gui_basic_assets/button/red_normal.png")
BTN_HOVERED_TEX = arcade.load_texture(":resources:/gui_basic_assets/button/red_hover.png")
BTN_PRESSED_TEX = arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png")

UP_TEX    = arcade.load_texture(":res:up.png")
RIGHT_TEX = UP_TEX.rotate_90()
LEFT_TEX  = UP_TEX.rotate_270()

monster_sheet = arcade.load_spritesheet(":res:monsters.png")
item_sheet    = arcade.load_spritesheet(":res:items.png")
hero_sheet    = arcade.load_spritesheet(":res:rogues.png")
tile_sheet    = arcade.load_spritesheet(":res:tiles.png")
animal_sheet  = arcade.load_spritesheet(":res:animals.png")

MAP_ICONS = [
    animal_sheet.get_texture_grid(size=(32, 32), columns=9, count=9 * 16)[7*9+1],
    tile_sheet.get_texture_grid(size=(32, 32), columns=17, count=17 * 26)[25*17+1],
    tile_sheet.get_texture_grid(size=(32, 32), columns=17, count=17 * 26)[23*17]
]

GOLD_ICON = arcade.load_texture(":res:gold.png")
X_ICON    = arcade.load_texture(":res:none.png")
MAP_IMGS  = [
    arcade.load_texture(":res:desert_menu.png"),
    arcade.load_texture(":res:forest_menu.png"),
    arcade.load_texture(":res:dungeon_menu.png"),
]

texture_list        = monster_sheet.get_texture_grid(size=(32, 32), columns=12, count=12 * 13)
texture_list_heroes = hero_sheet.get_texture_grid(size=(32, 32), columns=7,  count=7 * 7)
texture_list_item   = item_sheet.get_texture_grid(size=(32, 32),  columns=11, count=11 * 26)

BEING_SPRITES = {
    "Knight":    texture_list_heroes[7].flip_left_right(),
    "Wizard":    texture_list_heroes[29].flip_left_right(),
    "Rogue":     texture_list_heroes[3].flip_left_right(),
    "Berserker": texture_list_heroes[22].flip_left_right(),
    "Granny":    texture_list_heroes[45].flip_left_right(),
    "Witch":     texture_list[64],
    "Dragon":    texture_list[98],
    "Spider":    texture_list[80],
    "Warrior":   texture_list[7],
    "Mage":      texture_list[6]
}

ITEMS = {
    "The Crucible":  [texture_list_item[9],   "atk",     0.3],
    "Viper Edge":    [texture_list_item[16],  "atk",     0.4],
    "Hallebarde":    [texture_list_item[35],  "atk",     0.4],
    "Crusher":       [texture_list_item[48],  "atk",     0.4],
    "Morning Star":  [texture_list_item[56],  "atk",     0.4],
    "Flail":         [texture_list_item[78],  "atk",     0.4],
    "Trident":       [texture_list_item[69],  "atk",     0.4],
    "Bow":           [texture_list_item[102], "atk",     0.4],
    "Orb Staff":     [texture_list_item[110], "magic",   0.4],
    "Arcane Branch": [texture_list_item[112], "magic",   0.4],
    "Walking Stick": [texture_list_item[119], "atk",     0.4],

    "Buckler":       [texture_list_item[126], "defense", 0.35],
    "Kite Shield":   [texture_list_item[127], "defense", 0.35],
    "Heater Shield": [texture_list_item[123], "defense", 0.35],

    "Plated Armor":  [texture_list_item[137], "defense", 0.30],
    "Arcane Robe":   [texture_list_item[134], "magic",   0.30],
    "Tunic":         [texture_list_item[132], "defense", 0.30],

    "Bracers":        [texture_list_item[146], "defense", 0.25],
    "Arcane Gloves":  [texture_list_item[145], "magic",   0.25],
    "Leather Gloves": [texture_list_item[144], "defense", 0.25],

    "Greaves":       [texture_list_item[157], "defense", 0.25],
    "Arcane Boots":  [texture_list_item[156], "magic",   0.25],
    "Leather Boots": [texture_list_item[155], "defense", 0.25],

    "Iron Helmet":   [texture_list_item[171], "defense", 0.25],
    "Arcane Hat":    [texture_list_item[167], "magic",   0.25],
    "Cowl":          [texture_list_item[168], "defense", 0.25],

    "Arcane Ring":   [texture_list_item[190], "magic",   0.30],
    "Scroll Of Wit": [texture_list_item[237], "magic",   0.30],
    "Amulet":        [texture_list_item[178], "defense", 0.30],
}

del texture_list, texture_list_heroes, hero_sheet, tile_sheet, animal_sheet, monster_sheet, item_sheet, texture_list_item