# Nordeus full stack challenge 2026  
Turn based RPG game in python using arcade library and client/server architecture.
### How to run the game:  
  1. Run `pip install arcade requests uvicorn fastapi`  
  2. Run `uvicorn server:app --reload` in dedicated terminal
  3. Run main.py  

Note: I was using python version 3.14.3. In demo, hero is stronger than usual for time saving purposes.  

Note2: The game window is intended to be smaller than shown in the demo (windows scale setting affects the size). The cursos is mine and is not a part of the game.
### About the game  
Turn based combat against a gauntlet of enemies. Each enemy is stronger than the last. At the beginning the player can choose which hero to play as. 
Enemies drop items, moves, xp, and gold. All characters have pre-defined stats: HP, ATK, DEF, MAG. You can view enemy stats by hovering over their icon.

The items can be equipped in the Equipment menu. Each item has a type (Head, Torso, etc.) and the player can equip only one item per type. Items can be purchased in the shop.  

XP can be spent to level up a stat of the player's choice.

Upon defeating an enemy, you learn one of their moves at random. You can manage your moveset in the Moves menu. Hovering over a move (in battle or in Moves menu) shows 
what it does.  

You can select which map you want to be shown in the background - Desert, Catacombs or Forest

You can save the game and continue playing later.  

Endless mode allows playing until you lose.
