from game_logic import beings
from game_logic import status_effects
from game_logic import defs

class Move:
    def __init__(self, caster: beings.Being):
        self.caster = caster
        self.desc = "test"
    
    def cast(self,target: beings.Being = None):
        pass

    def __str__(self):
        return f"{type(self).__name__}"
    
    def __eq__(self,other):
        if not isinstance(other, Move):
            return False
        return type(self).__name__ == type(other).__name__

class Slash(Move):
    def __init__(self, caster):
        super().__init__(caster)    
        self.desc = f"Type: Physical\nDamage: {defs.SLASH_DMG}\n\nScales off your ATK, reduced by target's DEF"

    def cast(self, target):
        target.hp -= (self.caster.atk*defs.SLASH_DMG)/target.defense

class ShieldUp(Move):
    def __init__(self, caster):
        super().__init__(caster)    
        self.desc = f"Type: Status Effect\nStat: DEF\nInrease: {defs.SHIELDUP_DEF_INC}\nDuration: {defs.SHIELDUP_LEN}"
  
    def cast(self,target = None):
        self.caster.status_effects.append(status_effects.IncreaseDefense(self.caster,defs.SHIELDUP_DEF_INC,defs.SHIELDUP_LEN))

class BattleCry(Move):
    def __init__(self, caster):
        super().__init__(caster)    
        self.desc = f"Type: Status Effect\nStat: ATK\nInrease: {defs.BATTLECRY_ATK_INC}\nDuration: {defs.BATTLECRY_LEN}"
    def cast(self,target = None):
        self.caster.status_effects.append(status_effects.IncreaseAtk(self.caster,defs.BATTLECRY_ATK_INC,defs.BATTLECRY_LEN))

class SecondWind(Move):
    def __init__(self, caster):
        super().__init__(caster)    
        self.desc = f"Type: Magic\nHeal: {defs.SECONDWIND_HEAL}\n\nScales off MAG"

    def cast(self,target = None):
        self.caster.hp += defs.SECONDWIND_HEAL*self.caster.magic

class ShadowBolt(Move):
    def __init__(self, caster):
        super().__init__(caster)    
        self.desc = f"Type: Magic\nDamage: {defs.SHADOWBOLT_DMG}\n\nScales off MAG"

    def cast(self,target = None):
        target.hp -= defs.SHADOWBOLT_DMG*self.caster.magic

class DrainLife(Move):
    def __init__(self, caster):
        super().__init__(caster)    
        self.desc = f"Type: Magic\nDamage: {defs.DRAINLIFE_DMG}\nHeal: {defs.DRAINLIFE_DMG}\n\nScales off MAG"

    def cast(self,target = None):
        target.hp -= defs.DRAINLIFE_DMG*self.caster.magic
        self.caster.hp += defs.DRAINLIFE_DMG*self.caster.magic

class Curse(Move):
    def __init__(self, caster):
        super().__init__(caster)    
        self.desc = f"Type: Status Effect\nStat: ATK\nDecrease: {defs.CURSE_ATK_DEC}\nDuration: {defs.CURSE_LEN}"

    def cast(self,target = None):
        target.status_effects.append(status_effects.DecreaseAtk(target,defs.CURSE_ATK_DEC,defs.CURSE_LEN))

class DarkPact(Move):
    def __init__(self, caster):
        super().__init__(caster)    
        self.desc = f"Type: Status Effect\nStat: MAG\nIncrease: {defs.DARKPACT_MAGIC_INC}\nDuration: {defs.DARKPACT_LEN}\nCost (HP): {defs.DARKPACT_HEALTH_COST}"

    def cast(self,target = None):
        self.caster.hp -= defs.DARKPACT_HEALTH_COST
        self.caster.status_effects.append(status_effects.IncreaseMagic(self.caster,defs.DARKPACT_MAGIC_INC,defs.DARKPACT_LEN))

class Bite(Move):
    def __init__(self, caster):
        super().__init__(caster)    
        self.desc = f"Type: Physical\nDamage: {defs.BITE_DMG}\n\nScales off your ATK, reduced by target's DEF"

    def cast(self,target = None):
        target.hp -= (self.caster.atk*defs.BITE_DMG)/target.defense

class WebThrow(Move):
    def __init__(self, caster):
        super().__init__(caster)    
        self.desc = f"Type: Physical/Status Effect\nDamage: {defs.WEBTHROW_DMG}\nStat: DEF\nDecrease: {defs.WEBTHROW_DEFENSE_DEC}\nDuration: {defs.WEBTHROW_LEN}"
 
    def cast(self,target = None):
        target.hp -= (self.caster.atk*defs.WEBTHROW_DMG)/target.defense
        target.status_effects.append(status_effects.DecreaseDefense(target,defs.WEBTHROW_DEFENSE_DEC,defs.WEBTHROW_LEN))

class Pounce(Move):
    def __init__(self, caster):
        super().__init__(caster)    
        self.desc = f"Type: Physical\nDamage: {defs.POUNCE_DMG}\n\nScales off your ATK stat, reduced by target's DEF"

    def cast(self,target = None):
        target.hp -= (self.caster.atk*defs.POUNCE_DMG)/target.defense

class Skitter(Move):
    def __init__(self, caster):
        super().__init__(caster)    
        self.desc = f"Type: Status Effect\nStat: DEF\nIncrease: {defs.SKITTER_DEF_INC}\nDuration: {defs.SKITTER_LEN}"

    def cast(self,target = None):
        self.caster.status_effects.append(status_effects.IncreaseDefense(self.caster,defs.SKITTER_DEF_INC,defs.SKITTER_LEN))

class FlameBreath(Move):
    def __init__(self, caster):
        super().__init__(caster)    
        self.desc = f"Type: Magic\nDamage: {defs.FLAMEBREATH_DMG}\n\nScales off MAG"

    def cast(self,target = None):
        target.hp -= self.caster.magic*defs.FLAMEBREATH_DMG

class ClawSwipe(Move):
    def __init__(self, caster):
        super().__init__(caster)    
        self.desc = f"Type: Physical\nDamage: {defs.CLAWSWIPE_DMG}\n\nScales off your ATK stat, reduced by target's DEF"

    def cast(self,target = None):
        target.hp -= (self.caster.atk*defs.CLAWSWIPE_DMG)/target.defense

class Intimidate(Move):
    def __init__(self, caster):
        super().__init__(caster)    
        self.desc = f"Type: Status Effect\nStat: ATK\nDecrease: {defs.INTIMIDATE_ATK_DEC}\nDuration: {defs.INTIMIDATE_LEN}"

    def cast(self,target = None):
        target.status_effects.append(status_effects.DecreaseAtk(target,defs.INTIMIDATE_ATK_DEC,defs.INTIMIDATE_LEN))

class DragonScales(Move):
    def __init__(self, caster):
        super().__init__(caster)    
        self.desc = f"Type: Status Effect\nStat: DEF\nIncrease: {defs.DRAGONSCALES_DEF_INC}\nDuration: {defs.DRAGONSCALES_LEN}"

    def cast(self,target = None):
        self.caster.status_effects.append(status_effects.IncreaseDefense(self.caster,defs.DRAGONSCALES_DEF_INC,defs.DRAGONSCALES_LEN))

class RustyBlade(Move):
    def __init__(self, caster):
        super().__init__(caster)    
        self.desc = f"Type: Physical\nDamage: {defs.RUSTYBLADE_DMG}\n\nScales off your ATK stat, reduced by target's DEF"

    def cast(self,target = None):
        target.hp -= (self.caster.atk*defs.RUSTYBLADE_DMG)/target.defense

class DirtyKick(Move):
    def __init__(self, caster):
        super().__init__(caster)    
        self.desc = f"Type: Physical/Status Effect\nDamage: {defs.DIRTYKICK_DMG}\nStat: DEF\nDecrease: {defs.DIRTYKICK_DEF_DEC}\nDuration: {defs.DIRTYKICK_LEN}"

    def cast(self,target = None):
        target.hp -= (self.caster.atk*defs.DIRTYKICK_DMG)/target.defense
        target.status_effects.append(status_effects.DecreaseDefense(target,defs.DIRTYKICK_DEF_DEC,defs.DIRTYKICK_LEN))

class Frenzy(Move):
    def __init__(self, caster):
        super().__init__(caster)    
        self.desc = f"Type: Status Effect\nStat: ATK\nIncrease: {defs.FRENZY_ATK_INC}\nDuration: {defs.FRENZY_LEN}"

    def cast(self,target = None):
        self.caster.status_effects.append(status_effects.IncreaseAtk(self.caster,defs.FRENZY_ATK_INC,defs.FRENZY_LEN))

class Headbutt(Move):
    def __init__(self, caster):
        super().__init__(caster)    
        self.desc = f"Type: Physical\nDamage: {defs.HEADBUTT_DMG}\n\nScales off your ATK stat, reduced by target's DEF"

    def cast(self,target = None):
        target.hp -= (self.caster.atk*defs.HEADBUTT_DMG)/target.defense

class Firebolt(Move):
    def __init__(self, caster):
        super().__init__(caster)    
        self.desc = f"Type: Magic\nDamage: {defs.SHADOWBOLT_DMG}\n\nScales off MAG"

    def cast(self,target = None):
        target.hp -= self.caster.magic*defs.FIREBOLT_DMG

class ArcaneSurge(Move):
    def __init__(self, caster):
        super().__init__(caster)    
        self.desc = f"Type: Status Effect\nStat: MAG\nIncrease: {defs.ARCANESURGE_MAGIC_INT}\nDuration: {defs.ARCANESURGE_LEN}"

    def cast(self,target = None):
        self.caster.status_effects.append(status_effects.IncreaseMagic(self.caster,defs.ARCANESURGE_MAGIC_INT,defs.ARCANESURGE_LEN))

class ManaDrain(Move):
    def __init__(self, caster):
        super().__init__(caster)    
        self.desc = f"Type: Physical/Status Effect\nDamage: {defs.MANADRAIN_DMG}\nStat: MAG\nDecrease: {defs.MANADRAIN_MAGIC_DEC}\nDuration: {defs.MANADRAIN_LEN}"

    def cast(self,target = None):
        target.hp -= self.caster.magic*defs.MANADRAIN_DMG
        target.status_effects.append(status_effects.DecreaseMagic(target,defs.MANADRAIN_MAGIC_DEC,defs.MANADRAIN_LEN))

class HexShield(Move):
    def __init__(self, caster):
        super().__init__(caster)    
        self.desc = f"Type: Status Effect\nStat: DEF\nIncrease: {defs.HEXSHIELD_DEFENSE_INC}\nDuration: {defs.HEXSHIELD_LEN}"

    def cast(self,target = None):
        self.caster.status_effects.append(status_effects.IncreaseDefense(self.caster,defs.HEXSHIELD_DEFENSE_INC,defs.HEXSHIELD_LEN))

