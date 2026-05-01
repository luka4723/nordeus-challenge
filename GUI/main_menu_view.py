import arcade
from pathlib import Path
import arcade.gui
import GUI.elements as ui
import GUI.game_view as game_view
import random

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
                                         texture=arcade.load_texture(":resources:/gui_basic_assets/button/red_normal.png"),
                                         texture_hovered=arcade.load_texture(":resources:/gui_basic_assets/button/red_hover.png"),
                                         texture_pressed=arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png"),
                                         width=200,
                                         height=60,
                                         text_size=26)
        
        if self.cont_avl:
            continue_button = ui.MyButton(text="Continue",
                                            texture=arcade.load_texture(":resources:/gui_basic_assets/button/red_normal.png"),
                                            texture_hovered=arcade.load_texture(":resources:/gui_basic_assets/button/red_hover.png"),
                                            texture_pressed=arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png"),
                                            width=200,
                                            height=60,
                                            text_size=26)
        else:
            continue_button = ui.MyButton(text="Continue",
                                            texture=arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png"),
                                            texture_hovered=arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png"),
                                            texture_pressed=arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png"),
                                            width=200,
                                            height=60,
                                            text_size=26)

        quit_button = ui.MyButton(text="Quit",
                                         texture=arcade.load_texture(":resources:/gui_basic_assets/button/red_normal.png"),
                                         texture_hovered=arcade.load_texture(":resources:/gui_basic_assets/button/red_hover.png"),
                                         texture_pressed=arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png"),
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
        def on_click_switch_button(event):
            self.window.show_view(game_view.GameView(self.current_map))

        @continue_button.event("on_click")
        def on_click_switch_button(event):
            if self.cont_avl:
                self.window.show_view(game_view.GameView(self.current_map,from_save=True))

        @quit_button.event("on_click")
        def on_click_switch_button(event):
            arcade.exit()

        self.current_map = random.randint(0,2)
        self.maps = [
            arcade.load_texture(":res:desert_menu.png"),
            arcade.load_texture(":res:forest_menu.png"),
            arcade.load_texture(":res:dungeon_menu.png"),
        ]

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
        arcade.draw_texture_rect(self.maps[self.current_map],
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