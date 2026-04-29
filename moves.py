import beings
import status_effects
import defs

class Move:
    def __init__(self, caster: beings.Being):
        self.caster = caster
    
    def cast(self,target: beings.Being = None):
        pass

    def __str__(self):
        return f"{type(self).__name__}"

class Slash(Move):    
    def cast(self, target):
        target.hp -= (self.caster.atk*defs.SLASH_DMG)/target.defense

class ShieldUp(Move):  
    def cast(self,target = None):
        self.caster.status_effects.append(status_effects.IncreaseDefense(self.caster,defs.SHIELDUP_DEF_INC,defs.SHIELDUP_LEN))

class BattleCry(Move):
    def cast(self,target = None):
        self.caster.status_effects.append(status_effects.IncreaseAtk(self.caster,defs.BATTLECRY_ATK_INC,defs.BATTLECRY_LEN))

class SecondWind(Move):
    def cast(self,target = None):
        self.caster.hp += defs.SECONDWIND_HEAL*self.caster.magic

class ShadowBolt(Move):
    def cast(self,target = None):
        target.hp -= defs.SHADOWBOLT_DMG*self.caster.magic

class DrainLife(Move):
    def cast(self,target = None):
        target.hp -= defs.DRAINLIFE_DMG*self.caster.magic
        self.caster.hp += defs.DRAINLIFE_DMG*self.caster.magic

class Curse(Move):
    def cast(self,target = None):
        target.status_effects.append(status_effects.DecreaseAtk(target,defs.CURSE_ATK_DEC,defs.CURSE_LEN))

class DarkPact(Move):
    def cast(self,target = None):
        self.caster.hp -= defs.DARKPACT_HEALTH_COST
        self.caster.status_effects.append(status_effects.IncreaseMagic(self.caster,defs.DARKPACT_MAGIC_INC,defs.DARKPACT_LEN))

class Bite(Move):
    def cast(self,target = None):
        target.hp -= (self.caster.atk*defs.BITE_DMG)/target.defense

class WebThrow(Move):
    def cast(self,target = None):
        target.hp -= (self.caster.atk*defs.WEBTHROW_DMG)/target.defense
        target.status_effects.append(status_effects.DecreaseDefense(target,defs.WEBTHROW_DEFENSE_DEC,defs.WEBTHROW_LEN))

class Pounce(Move):
    def cast(self,target = None):
        target.hp -= (self.caster.atk*defs.POUNCE_DMG)/target.defense

class Skitter(Move):
    def cast(self,target = None):
        self.caster.status_effects.append(status_effects.IncreaseDefense(self.caster,defs.SKITTER_DEF_INC,defs.SKITTER_LEN))

class FlameBreath(Move):
    def cast(self,target = None):
        target.hp -= self.caster.magic*defs.FLAMEBREATH_DMG

class ClawSwipe(Move):
    def cast(self,target = None):
        target.hp -= (self.caster.atk*defs.CLAWSWIPE_DMG)/target.defense

class Intimidate(Move):
    def cast(self,target = None):
        target.status_effects.append(status_effects.DecreaseAtk(target,defs.INTIMIDATE_ATK_DEC,defs.INTIMIDATE_LEN))

class DragonScales(Move):
    def cast(self,target = None):
        self.caster.status_effects.append(status_effects.IncreaseDefense(self.caster,defs.DRAGONSCALES_DEF_INC,defs.DRAGONSCALES_LEN))

class RustyBlade(Move):
    def cast(self,target = None):
        target.hp -= (self.caster.atk*defs.RUSTYBLADE_DMG)/target.defense

class DirtyKick(Move):
    def cast(self,target = None):
        target.hp -= (self.caster.atk*defs.DIRTYKICK_DMG)/target.defense
        target.status_effects.append(status_effects.DecreaseDefense(target,defs.DIRTYKICK_DEF_DEC,defs.DIRTYKICK_LEN))

class Frenzy(Move):
    def cast(self,target = None):
        self.caster.status_effects.append(status_effects.IncreaseAtk(self.caster,defs.FRENZY_ATK_INC,defs.FRENZY_LEN))

class Headbutt(Move):
    def cast(self,target = None):
        target.hp -= (self.caster.atk*defs.HEADBUTT_DMG)/target.defense

class Firebolt(Move):
    def cast(self,target = None):
        target.hp -= self.caster.magic*defs.FIREBOLT_DMG

class ArcaneSurge(Move):
    def cast(self,target = None):
        self.caster.status_effects.append(status_effects.IncreaseMagic(self.caster,defs.ARCANESURGE_MAGIC_INT,defs.ARCANESURGE_LEN))

class ManaDrain(Move):
    def cast(self,target = None):
        target.hp -= self.caster.magic*defs.MANADRAIN_DMG
        target.status_effects.append(status_effects.DecreaseMagic(target,defs.MANADRAIN_MAGIC_DEC,defs.MANADRAIN_LEN))

class HexShield(Move):
    def cast(self,target = None):
        self.caster.status_effects.append(status_effects.IncreaseDefense(self.caster,defs.HEXSHIELD_DEFENSE_INC,defs.HEXSHIELD_LEN))

