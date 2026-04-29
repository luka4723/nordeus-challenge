import uvicorn
from fastapi import FastAPI
import random
import beings


app = FastAPI()
next_id = 0
active_runs = {}

@app.get("/")
def home():
    global next_id
    next_id += 1
    monster_order = [1,2,3,4,5]
    random.shuffle(monster_order)
    print(monster_order)
    roster = [beings.Witch(monster_order[0]),
              beings.Spider(monster_order[1]),
              beings.Dragon(monster_order[2]),
              beings.Warrior(monster_order[3]),
              beings.Mage(monster_order[4])]
    roster.sort(key=lambda x: x.order)
    active_runs[f"{next_id}"] = roster
    return {
        "run_order": [m.to_dict() for m in roster],
        "id": next_id 
    }


@app.get("/user/{user_id}")
def get_user(user_id: int, enemy_hp: float, enemy_atk: float, enemy_def: float, enemy_mag: float, 
             hero_hp: float, hero_atk: float, hero_def: float, hero_mag: float):
    return random.randint(0,3)

if __name__ == '__main__':
    uvicorn.run(app)