from game_logic import defs

def move_name(name):
    result = [name[0]]
    for ch in name[1:]:
        if ch.isupper():
            result.append(" ")
        result.append(ch)
    return "".join(result)

class Equipment():
    def __init__(self, hero):
        i = move_name(type(self).__name__)
        self.hero = hero
        self.tex = defs.ITEMS[i][0]
        self.stat = defs.ITEMS[i][1]
        self.val = defs.ITEMS[i][2]
    
    def apply(self):
        pass

    def remove(self):
        pass

class Head(Equipment):
    def __init__(self, hero):
        super().__init__(hero)

class Torso(Equipment):
    def __init__(self, hero):
        super().__init__(hero)

class Arms(Equipment):
    def __init__(self, hero):
        super().__init__(hero)

class Legs(Equipment):
    def __init__(self, hero):
        super().__init__(hero)

class Weapon(Equipment):
    def __init__(self, hero):
        super().__init__(hero)

class Shield(Equipment):
    def __init__(self, hero):
        super().__init__(hero)

class Acc(Equipment):
    def __init__(self, hero):
        super().__init__(hero)




class TheCrucible(Weapon):
    def __init__(self, hero):
        super().__init__(hero)

class ViperEdge(Weapon):
    def __init__(self, hero):
        super().__init__(hero)

class Hallebarde(Weapon):
    def __init__(self, hero):
        super().__init__(hero)

class Crusher(Weapon):
    def __init__(self, hero):
        super().__init__(hero)

class MorningStar(Weapon):
    def __init__(self, hero):
        super().__init__(hero)

class Flail(Weapon):
    def __init__(self, hero):
        super().__init__(hero)

class Trident(Weapon):
    def __init__(self, hero):
        super().__init__(hero)

class Bow(Weapon):
    def __init__(self, hero):
        super().__init__(hero)

class OrbStaff(Weapon):
    def __init__(self, hero):
        super().__init__(hero)

class ArcaneBranch(Weapon):
    def __init__(self, hero):
        super().__init__(hero)

class WalkingStick(Weapon):
    def __init__(self, hero):
        super().__init__(hero)

class Buckler(Shield):
    def __init__(self, hero):
        super().__init__(hero)

class KiteShield(Shield):
    def __init__(self, hero):
        super().__init__(hero)

class HeaterShield(Shield):
    def __init__(self, hero):
        super().__init__(hero)

class PlatedArmor(Torso):
    def __init__(self, hero):
        super().__init__(hero)

class ArcaneRobe(Torso):
    def __init__(self, hero):
        super().__init__(hero)

class Tunic(Torso):
    def __init__(self, hero):
        super().__init__(hero)

class Bracers(Arms):
    def __init__(self, hero):
        super().__init__(hero)

class ArcaneGloves(Arms):
    def __init__(self, hero):
        super().__init__(hero)

class LeatherGloves(Arms):
    def __init__(self, hero):
        super().__init__(hero)

class Greaves(Legs):
    def __init__(self, hero):
        super().__init__(hero)

class ArcaneBoots(Legs):
    def __init__(self, hero):
        super().__init__(hero)

class LeatherBoots(Legs):
    def __init__(self, hero):
        super().__init__(hero)

class IronHelmet(Head):
    def __init__(self, hero):
        super().__init__(hero)

class ArcaneHat(Head):
    def __init__(self, hero):
        super().__init__(hero)

class Cowl(Head):
    def __init__(self, hero):
        super().__init__(hero)

class ArcaneRing(Acc):
    def __init__(self, hero):
        super().__init__(hero)

class ScrollOfWit(Acc):
    def __init__(self, hero):
        super().__init__(hero)

class Amulet(Acc):
    def __init__(self, hero):
        super().__init__(hero)

