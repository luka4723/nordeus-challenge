import arcade
from pathlib import Path
import arcade.gui
import GUI.elements as ui
import GUI.game_view as game_view
import GUI.select_view as select_view
import random
import json
from game_logic import beings, defs

assets_path = Path(__file__).parent.parent.resolve() / Path("resources")
arcade.resources.add_resource_handle("res",assets_path)

class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()

        save_path = assets_path / "savefile.txt"
        self.cont_avl = save_path.exists()
        if not self.cont_avl:
            with open(assets_path / "savefile.txt", "w"):
                pass
        self.cont_avl = save_path.stat().st_size > 0

        enter_button = ui.MyButton(text="New Game",
                                         texture=defs.BTN_NORMAL_TEX,
                                         texture_hovered=defs.BTN_HOVERED_TEX,
                                         texture_pressed=defs.BTN_PRESSED_TEX,
                                         width=200,
                                         height=60,
                                         text_size=26)
        
        if self.cont_avl:
            continue_button = ui.MyButton(text="Continue",
                                            texture=defs.BTN_NORMAL_TEX,
                                            texture_hovered=defs.BTN_HOVERED_TEX,
                                            texture_pressed=defs.BTN_PRESSED_TEX,
                                            width=200,
                                            height=60,
                                            text_size=26)
        else:
            continue_button = ui.MyButton(text="Continue",
                                            texture=defs.BTN_PRESSED_TEX,
                                            texture_hovered=defs.BTN_PRESSED_TEX,
                                            texture_pressed=defs.BTN_PRESSED_TEX,
                                            width=200,
                                            height=60,
                                            text_size=26)

        quit_button = ui.MyButton(text="Quit",
                                         texture=defs.BTN_NORMAL_TEX,
                                         texture_hovered=defs.BTN_HOVERED_TEX,
                                         texture_pressed=defs.BTN_PRESSED_TEX,
                                         width=200,
                                         height=60,
                                         text_size=26
                                         )
        
        self.grid = arcade.gui.UIGridLayout(
            column_count=1, row_count=3, horizontal_spacing=20, vertical_spacing=20
        )
        self.grid.add(enter_button, column= 0, row=0)
        self.grid.add(continue_button, column= 0, row=1)
        self.grid.add(quit_button, column= 0, row=2)

        @enter_button.event("on_click")
        def on_click_new(event):
            self.window.show_view(select_view.SelectView(map=self.current_map,return_view=self))
            defs.SOUND.play(volume=0.08)

        @continue_button.event("on_click")
        def on_click_continue(event):
            if self.cont_avl:
                defs.SOUND.play(volume=0.08)
                with open(assets_path / "savefile.txt", "r") as f:
                    save_dict = json.load(f)
                    hero = beings.Hero.from_dict(save_dict["hero"])
                f.close()
                self.window.show_view(game_view.GameView(self.current_map,from_save=True,play_tex=defs.BEING_SPRITES[type(hero).__name__],hero=hero))

        @quit_button.event("on_click")
        def on_click_exit(event):
            defs.SOUND.play(volume=0.08)
            arcade.exit()
            self.window.close()

        self.current_map = random.randint(0,2)

        self.anchor = self.manager.add(arcade.gui.UIAnchorLayout())
        self.anchor.add(
            anchor_x="center_x",
            anchor_y="center_y",
            child=self.grid,
        )

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(defs.MAP_IMGS[self.current_map],
                                 arcade.LBWH(0, 0, self.window.width, self.window.height))
        r = self.grid.rect
        padding = 20
        arcade.draw_lrbt_rectangle_filled(
            r.left - padding, r.right + padding,
            r.bottom - padding, r.top + padding,
            (0, 0, 0, 160)
        )
        arcade.draw_lrbt_rectangle_outline(
            r.left - padding, r.right + padding,
            r.bottom - padding, r.top + padding,
            border_width=2, color=arcade.color.GOLD
        )

        self.manager.draw()
        
    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            arcade.exit()