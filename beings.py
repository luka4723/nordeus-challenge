import moves
import defs

class Being:
    def __init__(self,hp,atk,defense,magic):
        self.hp = hp
        self.atk = atk
        self.defense = defense
        self.magic = magic
        self.moves = []
        self.status_effects = []

class Hero(Being):
    def __init__(self):
        super().__init__(defs.HERO_HP, defs.HERO_ATK, defs.HERO_DEF, defs.HERO_MAGIC)
        self.moves = [moves.Slash(self), moves.ShieldUp(self), moves.BattleCry(self), moves.SecondWind(self)]
     

# Simulating higher levels each subsequent enemy
class Foe(Being):
    def __init__(self, order, hp, atk, defense, magic):
        super().__init__(hp, atk, defense, magic)
        self.order = order
        self.hp += defs.ORDER_HP * order
        self.atk += defs.ORDER_ATK * order
        self.defense += defs.ORDER_DEFENSE * order
        self.magic += defs.ORDER_MAGIC * order

class Witch(Foe):
    def __init__(self, order):
        super().__init__(order, defs.WITCH_HP, defs.WITCH_ATK, defs.WITCH_DEF, defs.WITCH_MAGIC)
        self.moves = [moves.ShadowBolt(self), moves.DrainLife(self), moves.Curse(self), moves.DarkPact(self)]
        
class Spider(Foe):
    def __init__(self, order):
        super().__init__(order, defs.SPIDER_HP, defs.SPIDER_ATK, defs.SPIDER_DEF, defs.SPIDER_MAGIC)
        self.moves = [moves.Bite(self), moves.WebThrow(self), moves.Pounce(self), moves.Skitter(self)]

class Dragon(Foe):
    def __init__(self, order):
        super().__init__(order, defs.DRAGON_HP, defs.DRAGON_ATK, defs.DRAGON_DEF, defs.DRAGON_MAGIC)
        self.moves = [moves.FlameBreath(self), moves.ClawSwipe(self), moves.Intimidate(self), moves.DragonScales(self)]

class Warrior(Foe):
    def __init__(self, order):
        super().__init__(order, defs.WARRIOR_HP, defs.WARRIOR_ATK, defs.WARRIOR_DEF, defs.WARRIOR_MAGIC)
        self.moves = [moves.RustyBlade(self), moves.DirtyKick(self), moves.Frenzy(self), moves.Headbutt(self)]

class Mage(Foe):
    def __init__(self, order):
        super().__init__(order, defs.MAGE_HP, defs.MAGE_ATK, defs.MAGE_DEF, defs.MAGE_MAGIC)
        self.moves = [moves.Firebolt(self), moves.ArcaneSurge(self), moves.ManaDrain(self), moves.HexShield(self)]
        
