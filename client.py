import requests
import beings
import gamelogic
import random
    
if __name__ == '__main__':
    # First GET
    r1 = requests.get("http://127.0.0.1:8000/")
    data = r1.json()
    my_id = data["id"]
    #print(my_id)
    enemies: list[beings.Foe] = [beings.Foe.from_dict(m) for m in data["run_order"]]
    print("\nOrder of fights:")
    for enemy in enemies:
        print(enemy)
    print()

    hero = beings.Hero()
    i=0
    while i < len(enemies):
        encounter = gamelogic.Encounter(hero,enemies[i])
        while True:
            if encounter.heroMove():
                break
            encounter.applyEffectsH()

            if encounter.foeMove(my_id):
                break
            encounter.applyEffectsE()

        if encounter.result:
            print(f"Completed {i+1}/{len(enemies)}")
            ans = input("> Would you like to manage your moves? [Y/N]\n> ")
            if ans=="Y":
                gamelogic.manageMoves(hero)

            ans = input("> Replay the fight? [Y/N]\n> ") 
            if ans=="Y":
                enemies[i] = beings.Foe.from_dict(enemies[i].to_dict())
                continue
            i+=1
                           
        else:
            print("Thanks for playing")
            break



    