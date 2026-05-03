import requests
from game_logic import beings
from game_logic import gamelogic
import random
    
def getState(endless):
    # First GET
    if endless:
        enemies = []
        for i in range(1,6):
            enemies.append(beings.FOE_LIST[random.randint(0,len(beings.FOE_LIST)-1)](i))
            
        return enemies 
    else:
        r1 = requests.get("http://127.0.0.1:8000/")
        data = r1.json()
        seed = data["seed"]
        enemies = []
        for i, idx in enumerate(seed):
            enemies.append(beings.FOE_LIST[idx-1](i+1))

        return enemies