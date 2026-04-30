import arcade
import arcade.gui
from pathlib import Path
import game_logic.client
from GUI import main_menu_view,moves_view,elements, battle_view

assets_path = Path(__file__).parent.parent.resolve() / Path("resources")
arcade.resources.add_resource_handle("res", assets_path)

def make_label(text, font_size=16, bold=False, color=arcade.color.WHITE):
    return arcade.gui.UILabel(
        text=text,
        font_size=font_size,
        bold=bold,
        text_color=color,
        font_name="Kenney Mini",
    )

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        arcade.load_font(":resources:/fonts/ttf/Kenney/Kenney_Mini.ttf")

        self.current_floor = 0

        monster_sheet = arcade.load_spritesheet(":res:monsters.png")
        hero_sheet = arcade.load_spritesheet(":res:rogues.png")
        texture_list = monster_sheet.get_texture_grid(size=(32, 32), columns=12, count=12 * 13)
        texture_list_heroes = hero_sheet.get_texture_grid(size=(32, 32), columns=7, count=7 * 7)

        self.hero, self.enemies = game_logic.client.getState()

        self.player_texture = texture_list_heroes[7]
        
        self.enemy_textures = []
        enemy_dict = {
            "Witch" : texture_list[64],
            "Dragon": texture_list[98],
            "Spider": texture_list[80],
            "Warrior": texture_list[7],
            "Mage": texture_list[6]
        }
        for enemy in self.enemies:
            self.enemy_textures.append(enemy_dict[f"{type(enemy).__name__}"])
        self.build_ui()

    def build_ui(self):
        self.manager.clear()
        self.enemy_slots = {}
        self.player_slot = None

        #LEFT PANEL
        left_panel = arcade.gui.UIBoxLayout(vertical=True, space_between=20)

        hero_header = arcade.gui.UIBoxLayout(vertical=True, space_between=6)
        hero_img = arcade.gui.UIImage(
            texture=self.player_texture, width=64, height=64
        )
        hero_header.add(hero_img)
        hero_header.add(make_label("HERO", font_size=16, bold=True, color=arcade.color.GOLD))
        left_panel.add(hero_header)

        btns = []
        for btn_text in ["Start Fight", "Moves", "Equipment","Save","Back"]:
            btn = elements.MyButton(text=btn_text, 
                              texture=arcade.load_texture(":resources:/gui_basic_assets/button/red_normal.png"),
                              texture_hovered=arcade.load_texture(":resources:/gui_basic_assets/button/red_hover.png"),
                              texture_pressed=arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png"),
                              width=200, height=60, text_size=20)
            btns.append(btn)
            left_panel.add(btn)
        
        @btns[0].event("on_click")
        def on_click_switch_button(event):
            self.window.show_view(battle_view.BattleView(
                                                        hero=self.hero,
                                                        enemy=self.enemies[self.current_floor],
                                                        hero_texture=self.player_texture,
                                                        enemy_texture=self.enemy_textures[self.current_floor],
                                                        return_view=self
                                                    ))
        @btns[1].event("on_click")
        def on_click_switch_button(event):
            self.window.show_view(moves_view.MovesView(self.hero,self))
        @btns[4].event("on_click")
        def on_click_switch_button(event):
            self.window.show_view(main_menu_view.MainMenuView())

        #MIDDLE PANEL
        center_panel = arcade.gui.UIBoxLayout(vertical=True, space_between=20)

        stats_title = make_label("STATS", font_size=20, color=arcade.color.LIGHT_GRAY)
        center_panel.add(stats_title)

        stats_data = [
            ("Level", f"{self.hero.lvl}"),
            ("XP", f"{self.hero.xp} / {100+(self.hero.lvl-1)*20}"),
            ("HP", f"{self.hero.hp} / {self.hero.max_hp}"),
            ("ATK", f"{self.hero.atk}"),
            ("DEF", f"{self.hero.defense}"),
            ("MAG", f"{self.hero.magic}"),
        ]

        stats_grid = arcade.gui.UIGridLayout(
            column_count=2, row_count=len(stats_data),
            horizontal_spacing=24, vertical_spacing=8
        )
        for i, (stat, val) in enumerate(stats_data):
            stats_grid.add(make_label(stat + ":", color=arcade.color.LIGHT_BLUE), column=0, row=i)
            stats_grid.add(make_label(val, bold=True), column=1, row=i)
        center_panel.add(stats_grid)

        eq_title = make_label("EQUIPMENT", font_size=20, color=arcade.color.LIGHT_GRAY)
        center_panel.add(eq_title)

        eq_slots = [
            ("Head", "──"),
            ("Torso", "──"),
            ("Arms", "──"),
            ("Legs", "──"),
            ("Weapon", "──"),
            ("Shield", "──"),
            ("Acc.", "──"),
        ]

        eq_grid = arcade.gui.UIGridLayout(
            column_count=2, row_count=len(eq_slots),
            horizontal_spacing=24, vertical_spacing=6
        )
        for i, (slot, val) in enumerate(eq_slots):
            eq_grid.add(make_label(slot + ":", color=arcade.color.LIGHT_BLUE), column=0, row=i)
            eq_grid.add(make_label(val, color=arcade.color.GRAY), column=1, row=i)
        center_panel.add(eq_grid)

        # RIGHT PANEL
        right_panel = arcade.gui.UIBoxLayout(vertical=True, space_between=12)
        right_panel.add(make_label("TOWER", font_size=20, color=arcade.color.GOLD))

        tower_content = arcade.gui.UIBoxLayout(vertical=False, space_between=8)

        player_col = arcade.gui.UIGridLayout(
            column_count=1, row_count=5, horizontal_spacing=0, vertical_spacing=6
        )
        for i in range(5):
            floor = 4 - i
            if floor == self.current_floor:
                img = arcade.gui.UIImage(
                    texture=self.player_texture, width=80, height=80
                )
                self.player_slot = img
                player_col.add(img, column=0, row=i)
            else:
                player_col.add(arcade.gui.UIWidget(width=80, height=80), column=0, row=i)

        enemy_col = arcade.gui.UIGridLayout(
            column_count=1, row_count=5, horizontal_spacing=0, vertical_spacing=6
        )
        for i in range(5):
            floor = 4 - i
            img = arcade.gui.UIImage(
                texture=self.enemy_textures[floor], width=80, height=80
            )
            self.enemy_slots[floor] = img
            enemy_col.add(img, column=0, row=i)

        tower_content.add(player_col)
        tower_content.add(enemy_col)
        right_panel.add(tower_content)

        # MAIN
        main_row = arcade.gui.UIBoxLayout(vertical=False, space_between=96)
        main_row.add(left_panel)
        main_row.add(center_panel)
        main_row.add(right_panel)

        anchor = self.manager.add(arcade.gui.UIAnchorLayout())
        anchor.add(anchor_x="center_x", anchor_y="center_y", child=main_row)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.manager.enable()
        self.build_ui()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()

        if self.current_floor in self.enemy_slots:
            r = self.enemy_slots[self.current_floor].rect
            arcade.draw_lbwh_rectangle_outline(
                r.left, r.bottom, r.width, r.height,
                color=arcade.color.DARK_RED, border_width=3
            )

        if self.player_slot:
            r = self.player_slot.rect
            arcade.draw_lbwh_rectangle_outline(
                r.left, r.bottom, r.width, r.height,
                color=arcade.color.DARK_BLUE, border_width=3
            )