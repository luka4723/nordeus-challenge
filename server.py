import uvicorn
from fastapi import FastAPI
import random

app = FastAPI()
next_id = 0
active_runs = {}

@app.get("/")
def home():
    global next_id
    next_id += 1
    monster_order = [1,2,3,4,5]
    random.shuffle(monster_order)
    return {
        "seed": monster_order,
    }

@app.get("/endless")
def home():
    global next_id
    next_id += 1
    monster_order = [1,2,3,4,5]
    random.shuffle(monster_order)
    return {
        "seed": monster_order,
    }


@app.get("/c/1")
def get_user(enemy_hp: float, enemy_atk: float, enemy_def: float, enemy_mag: float,
             hero_hp: float, hero_atk: float, hero_def: float, hero_mag: float):
    num =random.randint(0,3)
    return {
        "ord" : num
    }

@app.get("/c/2")
def get_defs():
    return {
        "KNIGHT_HP": 200,
        "KNIGHT_ATK": 2.2,
        "KNIGHT_DEF": 1.4,
        "KNIGHT_MAGIC": 0.8,

        "WIZARD_HP": 150,
        "WIZARD_ATK": 0.8,
        "WIZARD_DEF": 0.9,
        "WIZARD_MAGIC": 2.2,

        "ROGUE_HP": 170,
        "ROGUE_ATK": 1.8,
        "ROGUE_DEF": 1.1,
        "ROGUE_MAGIC": 0.8,

        "BERSERKER_HP": 190,
        "BERSERKER_ATK": 2.4,
        "BERSERKER_DEF": 0.9,
        "BERSERKER_MAGIC": 0.7,

        "GRANNY_HP": 160,
        "GRANNY_ATK": 0.9,
        "GRANNY_DEF": 1.0,
        "GRANNY_MAGIC": 2.0,

        "WITCH_HP": 80,
        "WITCH_ATK": 1.0,
        "WITCH_DEF": 0.8,
        "WITCH_MAGIC": 2.0,

        "SPIDER_HP": 95,
        "SPIDER_ATK": 1.8,
        "SPIDER_DEF": 0.9,
        "SPIDER_MAGIC": 0.3,

        "DRAGON_HP": 130,
        "DRAGON_ATK": 1.6,
        "DRAGON_DEF": 1.0,
        "DRAGON_MAGIC": 1.2,

        "WARRIOR_HP": 110,
        "WARRIOR_ATK": 1.8,
        "WARRIOR_DEF": 1.2,
        "WARRIOR_MAGIC": 0.5,

        "MAGE_HP": 75,
        "MAGE_ATK": 0.6,
        "MAGE_DEF": 0.8,
        "MAGE_MAGIC": 1.8,

        "ORDER_HP": 20,
        "ORDER_ATK": 0.12,
        "ORDER_DEFENSE": 0.08,
        "ORDER_MAGIC": 0.12,

        "LVLUP_HP": 25,
        "LVLUP_ATK": 0.12,
        "LVLUP_DEFENSE": 0.10,
        "LVLUP_MAGIC": 0.12,

        "SLASH_DMG": 10,

        "SHIELDUP_DEF_INC": 0.5,
        "SHIELDUP_LEN": 2,

        "BATTLECRY_ATK_INC": 0.4,
        "BATTLECRY_LEN": 2,

        "SECONDWIND_HEAL": 15,

        "SHADOWBOLT_DMG": 15,

        "DRAINLIFE_DMG": 8,

        "CURSE_ATK_DEC": 0.5,
        "CURSE_LEN": 3,

        "DARKPACT_HEALTH_COST": 20,
        "DARKPACT_MAGIC_INC": 0.6,
        "DARKPACT_LEN": 2,

        "BITE_DMG": 14,
        "WEBTHROW_DMG": 9,
        "WEBTHROW_DEFENSE_DEC": 0.4,
        "WEBTHROW_LEN": 2,
        "POUNCE_DMG": 18,
        "SKITTER_DEF_INC": 0.4,
        "SKITTER_LEN": 2,

        "FLAMEBREATH_DMG": 14,
        "CLAWSWIPE_DMG": 16,
        "INTIMIDATE_ATK_DEC": 0.5,
        "INTIMIDATE_LEN": 2,
        "DRAGONSCALES_DEF_INC": 0.5,
        "DRAGONSCALES_LEN": 2,

        "RUSTYBLADE_DMG": 15,
        "DIRTYKICK_DMG": 11,
        "DIRTYKICK_DEF_DEC": 0.4,
        "DIRTYKICK_LEN": 2,
        "FRENZY_ATK_INC": 0.6,
        "FRENZY_LEN": 2,
        "HEADBUTT_DMG": 20,

        "FIREBOLT_DMG": 12,
        "ARCANESURGE_MAGIC_INT": 0.5,
        "ARCANESURGE_LEN": 2,
        "MANADRAIN_DMG": 9,
        "MANADRAIN_MAGIC_DEC": 0.5,
        "MANADRAIN_LEN": 2,
        "HEXSHIELD_DEFENSE_INC": 0.5,
        "HEXSHIELD_LEN": 2,

        "BANDAGES_HEAL": 20,

        "DIRTTHROW_ATK_DEC": 0.3,
        "DIRTTHROW_DEF_INC": 0.2,
        "DIRTTHROW_LEN": 2,

        "SHANKING_DMG": 10,
        "SHANKING_BLEED_DMG": 8,
        "SHANKING_LEN": 2,

        "SHATTEREDFLASK_DMG": 10,
        "SHATTEREDFLASK_POISON_DMG": 8,
        "SHATTEREDFLASK_LEN": 2,

        "HYPNOTIZE_LEN": 1,

        "BASE_XP": 25,
        "BASE_GOLD": 80,
        "XP_INC": 5,
        "GOLD_INC": 5,
        "PRICES": [60, 80, 100, 120, 140],
    }
    #XP inc gives bonus xp per order of the enemy (gold too)
    #prices are randomly assigned to items in shop. Array can be of any length
if __name__ == '__main__':
    uvicorn.run(app)