import requests
from game_logic import beings
from game_logic import gamelogic
import random
    
def getState():
    # First GET
    r1 = requests.get("http://127.0.0.1:8000/")
    data = r1.json()
    enemies: list[beings.Foe] = [beings.Foe.from_dict(m) for m in data["run_order"]]
    for enemy in enemies:
        print(enemy)

    hero = beings.Knight()
    return hero, enemies

    