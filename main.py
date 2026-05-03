import arcade
from pathlib import Path
import arcade.gui
import GUI.elements as ui
import GUI.game_view as gv
import GUI.main_menu_view as mmv


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Norderus Challange"
window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.center_window()

if __name__ == '__main__':
    #current_win = gv.GameView(map=0)
    sound = arcade.Sound(":resources:/music/funkyrobot.mp3")
    sound.play(volume=0.04,loop=True)
    current_win = mmv.MainMenuView()
    window.show_view(current_win)
    arcade.run()