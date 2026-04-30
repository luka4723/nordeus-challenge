from game_logic import beings
from game_logic import defs
from game_logic import status_effects
import random
import requests

class Encounter:
    def __init__(self, hero: beings.Hero, enemy: beings.Foe):
        self.hero = hero
        self.enemy = enemy
        self.result = False

        print(f"Starting encounter against {type(enemy).__name__}")
        print(f"{type(enemy).__name__}'s stats:")
        print(f"HP : {round(enemy.hp,2)}")
        print(f"ATK: {round(enemy.atk,2)}")
        print(f"DEF: {round(enemy.defense,2)}")
        print(f"MAG: {round(enemy.magic,2)}\n")

        print(hero.hp)

    def heroMove(self):
        move_ord = self.queryMove()
        self.hero.moves[move_ord].cast(self.enemy)
        print(f"You used {type(self.hero.moves[move_ord]).__name__} against the foe.")
        print(f"Foe's new health is {round(self.enemy.hp,2)}\n")
        if self.enemy.hp <= 0:
            print("You win!")
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
            if self.hero.xp >= 100:
                self.hero.xp -= 100
                self.hero.lvl += 1
                levelUp(self.hero)

            order = random.randint(0,3)
            if type(self.enemy.moves[order]) in [type(m) for m in self.hero.available_moves]:
                print("Nothing learned, tough luck!\n")
            else:
                print(f"Wow, you learned a new move: {type(self.enemy.moves[order]).__name__}.\n")
                self.hero.available_moves.append(self.enemy.moves[order])
            self.result = True
            return True

    def foeMove(self, my_id):
        r2 = requests.get(f"http://127.0.0.1:8000/user/{my_id}", params={
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
        print(f"Foe used {type(self.enemy.moves[move]).__name__} against you")
        print(f"Your new health is {round(self.hero.hp,2)}\n")
        if self.hero.hp <= 0:
            print("You Lose!")
            return True
    
    def queryMove(self):
        print("Your moves:")
        i = 1
        for move in self.hero.moves:
            print(f"{i}. {move}")
            i+=1
        num = int(input("> Choose a number from 1 to 4: "))
        return num-1

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

def manageMoves(hero : beings.Hero):
    i = 1
    print("Active moves:")
    print(f"1. {hero.moves[0]}")
    print(f"2. {hero.moves[1]}")
    print(f"3. {hero.moves[2]}")
    print(f"4. {hero.moves[3]}\n")
    
    print("Available moves:")
    for move in hero.available_moves:
        print(f"{i}. {move}")
        i+=1
    
    res = input("> Choose 4 moves: ").split()
    print(res)
    hero.moves = []
    for i in range(0, len(res)):
        hero.moves.append(hero.available_moves[int(res[i])-1])

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
