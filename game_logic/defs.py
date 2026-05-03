import arcade
from pathlib import Path

KNIGHT_HP    = 200
KNIGHT_ATK   = 2.2
KNIGHT_DEF   = 1.4
KNIGHT_MAGIC = 0.8

WIZARD_HP    = 150
WIZARD_ATK   = 0.8
WIZARD_DEF   = 0.9
WIZARD_MAGIC = 2.2

ROGUE_HP    = 170
ROGUE_ATK   = 1.8
ROGUE_DEF   = 1.1
ROGUE_MAGIC = 0.8

BERSERKER_HP    = 190
BERSERKER_ATK   = 2.4
BERSERKER_DEF   = 0.9
BERSERKER_MAGIC = 0.7

GRANNY_HP    = 160
GRANNY_ATK   = 0.9
GRANNY_DEF   = 1.0
GRANNY_MAGIC = 2.0

# Witch
WITCH_HP    = 80
WITCH_ATK   = 1.0
WITCH_DEF   = 0.8
WITCH_MAGIC = 2.0

# Spider
SPIDER_HP    = 95
SPIDER_ATK   = 1.8
SPIDER_DEF   = 0.9
SPIDER_MAGIC = 0.3

# Dragon
DRAGON_HP    = 130
DRAGON_ATK   = 1.6
DRAGON_DEF   = 1.0
DRAGON_MAGIC = 1.2

# Warrior
WARRIOR_HP    = 110
WARRIOR_ATK   = 1.8
WARRIOR_DEF   = 1.2
WARRIOR_MAGIC = 0.5

MAGE_HP    = 75
MAGE_ATK   = 0.6
MAGE_DEF   = 0.8
MAGE_MAGIC = 1.8

ORDER_HP       = 20    
ORDER_ATK      = 0.12   
ORDER_DEFENSE  = 0.08   
ORDER_MAGIC    = 0.12  

LVLUP_HP       = 25
LVLUP_ATK      = 0.12
LVLUP_DEFENSE  = 0.10
LVLUP_MAGIC    = 0.12

SLASH_DMG         = 10

SHIELDUP_DEF_INC  = 0.5
SHIELDUP_LEN      = 2

BATTLECRY_ATK_INC = 0.4
BATTLECRY_LEN     = 2

SECONDWIND_HEAL   = 15

SHADOWBOLT_DMG    = 15

DRAINLIFE_DMG     = 8

CURSE_ATK_DEC     = 0.5
CURSE_LEN         = 3 

DARKPACT_HEALTH_COST = 20
DARKPACT_MAGIC_INC   = 0.6
DARKPACT_LEN         = 2

BITE_DMG             = 14
WEBTHROW_DMG         = 9
WEBTHROW_DEFENSE_DEC = 0.4
WEBTHROW_LEN         = 2
POUNCE_DMG           = 18   
SKITTER_DEF_INC      = 0.4
SKITTER_LEN          = 2

FLAMEBREATH_DMG      = 14  
CLAWSWIPE_DMG        = 16
INTIMIDATE_ATK_DEC   = 0.5
INTIMIDATE_LEN       = 2
DRAGONSCALES_DEF_INC = 0.5
DRAGONSCALES_LEN     = 2

RUSTYBLADE_DMG  = 15
DIRTYKICK_DMG   = 11
DIRTYKICK_DEF_DEC = 0.4
DIRTYKICK_LEN   = 2
FRENZY_ATK_INC  = 0.6
FRENZY_LEN      = 2
HEADBUTT_DMG    = 20

FIREBOLT_DMG         = 12
ARCANESURGE_MAGIC_INT = 0.5
ARCANESURGE_LEN      = 2
MANADRAIN_DMG        = 9
MANADRAIN_MAGIC_DEC  = 0.5
MANADRAIN_LEN        = 2
HEXSHIELD_DEFENSE_INC = 0.5
HEXSHIELD_LEN        = 2

BANDAGES_HEAL = 20

DIRTTHROW_ATK_DEC = 0.3
DIRTTHROW_DEF_INC = 0.2
DIRTTHROW_LEN     = 2

SHANKING_DMG       = 10
SHANKING_BLEED_DMG = 8 
SHANKING_LEN       = 2

SHATTEREDFLASK_DMG        = 10
SHATTEREDFLASK_POISON_DMG = 8
SHATTEREDFLASK_LEN        = 2

HYPNOTIZE_LEN = 1

XP     = [150, 70, 90, 110, 130]
GOLD   = [100, 100, 100, 100, 100]
PRICES = [60, 80, 100, 120, 140]

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