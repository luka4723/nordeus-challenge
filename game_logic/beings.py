from game_logic import moves
from game_logic import defs
from game_logic import status_effects
from game_logic import equipment

class Being:
    def __init__(self,hp,atk,defense,magic):
        self.hp = hp
        self.atk = atk
        self.defense = defense
        self.magic = magic
        self.max_hp = self.hp
        self.moves: list[moves.Move] = []
        self.status_effects: list[status_effects.Effect] = []
    
    def to_dict(self):
        return {
            "type": type(self).__name__,
            # "hp": self.hp,
            # "atk": self.atk,
            # "defense": self.defense,
            # "magic": self.magic
        }
    
    def __str__(self):
        return f"{type(self).__name__}"

class Hero(Being):
    def __init__(self,hp,atk,defense,magic):
        super().__init__(hp,atk,defense,magic)
        self.xp = 0
        self.gold = 0
        self.lvl = 1
        self.moves = [moves.Slash(self), moves.ShieldUp(self), moves.BattleCry(self), moves.SecondWind(self)]
        self.available_moves = [moves.Slash(self), moves.ShieldUp(self), moves.BattleCry(self), moves.SecondWind(self)]
        self.available_equipment = []
        self.active_equipment = []

    def to_dict(self):
        return {
                "type": type(self).__name__,         
                "hp": self.hp,
                "max_hp": self.max_hp,
                "atk": self.atk,
                "defense": self.defense,
                "magic": self.magic,
                "lvl": self.lvl,
                "xp": self.xp,
                "gold": self.gold,
                "moves": [type(move).__name__ for move in self.moves],
                "available_moves": [type(move).__name__ for move in self.available_moves],
                "available_equipment": [type(eq).__name__ for eq in self.available_equipment],
                "active_equipment": [type(eq).__name__ for eq in self.active_equipment]
                }
    @staticmethod
    def from_dict(data):
        hero = globals()[data["type"]]()
        hero.hp = data["hp"]
        hero.max_hp = data["max_hp"]
        hero.atk = data["atk"]
        hero.defense = data["defense"]
        hero.magic = data["magic"]
        hero.lvl = data["lvl"]
        hero.xp = data["xp"]
        hero.gold = data["gold"]
        hero.moves = [
            getattr(moves, move)(hero)
            for move in data["moves"]
        ]
        hero.available_moves = [
            getattr(moves, move)(hero)
            for move in data["available_moves"]
        ]         
        hero.available_equipment = [
            getattr(equipment, eq)(hero)
            for eq in data["available_equipment"]
        ] 
        hero.active_equipment = [
            getattr(equipment, eq)(hero)
            for eq in data["active_equipment"]
        ] 
        hero.status_effects = []     
        return hero   

class Knight(Hero):
    def __init__(self):
        super().__init__(defs.KNIGHT_HP, defs.KNIGHT_ATK, defs.KNIGHT_DEF, defs.KNIGHT_MAGIC)
        self.moves = [moves.Slash(self), moves.ShieldUp(self), moves.BattleCry(self), moves.SecondWind(self)]
        self.available_moves = [moves.Slash(self), moves.ShieldUp(self), moves.BattleCry(self), moves.SecondWind(self)]

class Wizard(Hero):
    def __init__(self):
        super().__init__(defs.WIZARD_HP, defs.WIZARD_ATK, defs.WIZARD_DEF, defs.WIZARD_MAGIC)
        self.moves = [moves.Firebolt(self), moves.Hypnotize(self), moves.HexShield(self), moves.ShatteredFlask(self)]
        self.available_moves = [moves.Firebolt(self), moves.Hypnotize(self), moves.HexShield(self), moves.ShatteredFlask(self)]

class Rogue(Hero):
    def __init__(self):
        super().__init__(defs.ROGUE_HP, defs.ROGUE_ATK, defs.ROGUE_DEF, defs.ROGUE_MAGIC)
        self.moves = [moves.Shanking(self), moves.DirtThrow(self), moves.Bandages(self), moves.RustyBlade(self)]
        self.available_moves = [moves.Shanking(self), moves.DirtThrow(self), moves.Bandages(self), moves.RustyBlade(self)]

class Berserker(Hero):
    def __init__(self):
        super().__init__(defs.BERSERKER_HP, defs.BERSERKER_ATK, defs.BERSERKER_DEF, defs.BERSERKER_MAGIC)
        self.moves = [moves.Slash(self), moves.Frenzy(self), moves.RustyBlade(self), moves.SecondWind(self)]
        self.available_moves = [moves.Slash(self), moves.ShieldUp(self), moves.BattleCry(self), moves.SecondWind(self)]

class Granny(Hero):
    def __init__(self):
        super().__init__(defs.GRANNY_HP, defs.GRANNY_ATK, defs.GRANNY_DEF, defs.GRANNY_MAGIC)
        self.moves = [moves.RollingPin(self), moves.RollingPin(self), moves.RollingPin(self), moves.RollingPin(self)]
        self.available_moves = [moves.RollingPin(self), moves.RollingPin(self), moves.RollingPin(self), moves.RollingPin(self)]

# Simulating higher levels each subsequent enemy
class Foe(Being):
    def __init__(self, order, hp, atk, defense, magic):
        super().__init__(hp, atk, defense, magic)
        self.order = order
        self.hp += defs.ORDER_HP * order
        self.atk += defs.ORDER_ATK * order
        self.defense += defs.ORDER_DEFENSE * order
        self.magic += defs.ORDER_MAGIC * order
    
    def to_dict(self):
        new = super().to_dict()
        new["order"] = self.order
        return new

    @staticmethod
    def from_dict(data):

        types = {
            "Witch": Witch,
            "Spider": Spider,
            "Dragon": Dragon,
            "Warrior": Warrior,
            "Mage": Mage
        }

        cls = types[data["type"]]

        return cls(data["order"])

    # def __str__(self):
    #     return f"Type: {type(self).__name__}, Order: {self.order}"

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
        
FOE_LIST = [
    Witch,
    Spider,
    Dragon,
    Warrior,
    Mage
]