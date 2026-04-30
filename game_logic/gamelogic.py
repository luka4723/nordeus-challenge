from game_logic import beings
from game_logic import defs
from game_logic import status_effects, moves
import random
import requests

class Encounter:
    def __init__(self, hero: beings.Hero, enemy: beings.Foe):
        self.hero = hero
        self.enemy = enemy
        self.result = None

    def heroMove(self, move : moves.Move):
        move.cast(self.enemy)
        if self.enemy.hp <= 0:
            self.hero.hp = self.hero.max_hp
            match self.enemy.order:
                case 1:
                    xp = defs.XP_LVL1
                case 2:
                    xp = defs.XP_LVL2
                case 3:
                    xp = defs.XP_LVL3
                case 4:
                    xp = defs.XP_LVL4
                case 5:
                    xp = defs.XP_LVL5
            
            self.hero.xp += xp
            # MOVED TO GAME VIEW
            # if self.hero.xp >= 100:
            #     self.hero.xp -= 100
            #     self.hero.lvl += 1
            #     levelUp(self.hero)

            order = random.randint(0,3)
            if type(self.enemy.moves[order]) in [type(m) for m in self.hero.available_moves]:
                print("Nothing learned, tough luck!\n")
            else:
                print(f"Wow, you learned a new move: {type(self.enemy.moves[order]).__name__}.\n")
                self.hero.available_moves.append(self.enemy.moves[order])
            self.result = True
            return True

    def foeMove(self):
        r2 = requests.get(f"http://127.0.0.1:8000/user/1", params={
                "enemy_hp": self.enemy.hp,
                "enemy_atk": self.enemy.atk,
                "enemy_def": self.enemy.defense,
                "enemy_mag": self.enemy.magic,
                "hero_hp": self.hero.hp,
                "hero_atk": self.hero.atk,
                "hero_def": self.hero.defense,
                "hero_mag": self.hero.magic 
            })
        move = r2.json()


        self.enemy.moves[move].cast(self.hero)
        if self.hero.hp <= 0 and self.result is None:
            self.result = False
        if self.result is None:
            return self.enemy.moves[move]

    def applyEffectsH(self):
        new_status = []
        for effect in self.hero.status_effects:
            if effect.duration>0:
                new_status.append(effect)
                effect.duration -= 1
                effect.apply()
            else:
                effect.remove()
        self.hero.status_effects = new_status

        if self.hero.hp<=0 and self.result is None:
            self.result = False

    def applyEffectsE(self):
        new_status = []
        for effect in self.enemy.status_effects:
            if effect.duration>0:
                new_status.append(effect)
                effect.duration -= 1
                effect.apply()
            else:
                effect.remove()
        self.enemy.status_effects = new_status

        if self.enemy.hp<=0 and self.result is None:
            self.result = True

def levelUp(hero : beings.Hero):
    print("You leveled up! Choose which stat to upgrade:")
    print(f"1. HP")
    print(f"2. ATK")
    print(f"3. DEF")
    print(f"4. MAG")

    stat = int(input("> "))
    print()
    match stat:
        case 1:
            hero.max_hp += defs.LVLUP_HP
            hero.hp = hero.max_hp
        case 2:
            hero.atk += defs.LVLUP_ATK
        case 3:
            hero.defense += defs.LVLUP_DEFENSE
        case 4:
            hero.magic += defs.LVLUP_MAGIC
