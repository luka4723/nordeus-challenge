import requests
from game_logic import beings
from game_logic import gamelogic
import random
    
def getState():
    # First GET
    r1 = requests.get("http://127.0.0.1:8000/")
    data = r1.json()
    seed = data["seed"]
    enemies = []
    for i, idx in enumerate(seed):
        enemies.append(beings.FOE_LIST[idx-1](i))

    return enemies