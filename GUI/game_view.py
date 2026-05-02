import arcade
import arcade.gui
from pathlib import Path
import game_logic.client
from game_logic import defs, beings
from GUI import main_menu_view,moves_view,elements, battle_view
import json

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
    def __init__(self, map, hero, play_tex,from_save=False):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.current_map = map
        self.widget = None


        if from_save:
            with open(assets_path / "savefile.txt", "r") as f:
                save_dict = json.load(f)
                self.current_floor = save_dict["floor"]
                self.hero = beings.Hero.from_dict(save_dict["hero"])
                self.enemies = []
                for enemy_data in save_dict["enemies"]:
                    enemy = getattr(beings,enemy_data["type"])(enemy_data["order"] )   
                    self.enemies.append(enemy)
                self.current_map = save_dict["map"]
        else:
            self.hero = hero
            self.enemies = game_logic.client.getState()
            self.current_floor = 0
        

        self.up_icon = arcade.load_texture(":res:up.png")
        self.right_icon = self.up_icon.rotate_90()
        self.left_icon = self.up_icon.rotate_270()
        self.player_texture = play_tex
        
        self.enemy_textures = []
        for enemy in self.enemies:
            self.enemy_textures.append(defs.BEING_SPRITES[f"{type(enemy).__name__}"])
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
        hero_header.add(make_label(type(self.hero).__name__.upper(), font_size=16, bold=True, color=arcade.color.GOLD))
        left_panel.add(hero_header)

        btns = []
        for btn_text in ["Start Fight", "Moves", "Equipment","Save","Back"]:
            btn = elements.MyButton(text=btn_text, 
                                    texture=defs.BTN_NORMAL_TEX,
                                    texture_hovered=defs.BTN_HOVERED_TEX,
                                    texture_pressed=defs.BTN_PRESSED_TEX,
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
                                                        return_view=self, map = self.current_map
                                                    ))
        @btns[1].event("on_click")
        def on_click_switch_button(event):
            self.window.show_view(moves_view.MovesView(self.hero,self, map=self.current_map))
        @btns[3].event("on_click")
        def on_click_switch_button(event):
            save_dict = {
                "hero": self.hero.to_dict(),
                "enemies": [
                                {
                                    "type": type(enemy).__name__,
                                    "order": enemy.order
                                }
                                for enemy in self.enemies
                            ],
                "floor": self.current_floor,
                "map" : self.current_map
            }
            with open(assets_path / "savefile.txt", "w") as f:
                json.dump(save_dict,f,indent=4)
            f.close

        @btns[4].event("on_click")
        def on_click_switch_button(event):
            self.window.show_view(main_menu_view.MainMenuView())

        #MIDDLE PANEL
        center_panel = arcade.gui.UIBoxLayout(vertical=True, space_between=20)

        stats_title = make_label("STATS", font_size=20, color=arcade.color.GOLD)
        center_panel.add(stats_title)

        stats_data = [
            ("Level", f"{self.hero.lvl}"),
            ("XP", f"{self.hero.xp} / {100+(self.hero.lvl-1)*20}"),
            ("HP", f"{round(self.hero.hp)} / {self.hero.max_hp}"),
            ("ATK", f"{self.hero.atk}"),
            ("DEF", f"{self.hero.defense}"),
            ("MAG", f"{self.hero.magic}"),
        ]

        self.levelup_available = self.hero.xp >= 100 + (self.hero.lvl - 1) * 20

        stats_grid = arcade.gui.UIGridLayout(
            column_count=3, row_count=len(stats_data), 
            horizontal_spacing=8, vertical_spacing=8
        )
        for i, (stat, val) in enumerate(stats_data):
            stats_grid.add(make_label(stat + ":", color=arcade.color.LIGHT_BLUE), column=0, row=i)
            stats_grid.add(make_label(val, bold=True), column=1, row=i)
            
            if self.levelup_available and stat in ("HP", "ATK", "DEF", "MAG"):
                btn = elements.MyButton(
                    text="",
                    texture=self.up_icon, 
                    texture_hovered=self.up_icon,
                    texture_pressed=self.up_icon,
                    width=30, height=30, text_size=16
                )
                @btn.event("on_click")
                def on_stat_up(event, a=stat):
                    self.upgrade_stat(a)
                stats_grid.add(btn, column=2, row=i)
            else:
                stats_grid.add(arcade.gui.UIWidget(width=30, height=30), column=2, row=i)
        center_panel.add(stats_grid)

        eq_title = make_label("EQUIPMENT", font_size=20, color=arcade.color.GOLD)
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
        
        # Map selector
        map_selector = arcade.gui.UIBoxLayout(vertical=False, space_between=8)

        btn_left = elements.MyButton(
            text="",
            texture=self.left_icon,
            texture_hovered=self.left_icon,
            texture_pressed=self.left_icon,
            width=30, height=30, text_size=1
        )
        @btn_left.event("on_click")
        def on_left(event, view=self):
            view.current_map = (view.current_map - 1) % len(defs.MAP_IMGS)
            view.build_ui()

        self.map_preview = arcade.gui.UIImage(
            texture=defs.MAP_ICONS[self.current_map], width=64, height=64
        )

        btn_right = elements.MyButton(
            text="",
            texture=self.right_icon,
            texture_hovered=self.right_icon,
            texture_pressed=self.right_icon,
            width=30, height=30, text_size=1
        )
        @btn_right.event("on_click")
        def on_right(event, view=self):
            view.current_map = (view.current_map + 1) % len(defs.MAP_IMGS)
            view.build_ui()

        map_selector.add(btn_left)
        map_selector.add(self.map_preview.with_border(width=2, color=arcade.color.GOLD))
        map_selector.add(btn_right)

        right_panel.add(map_selector)

        # MAIN
        main_row = arcade.gui.UIBoxLayout(vertical=False, space_between=96)
        main_row.add(left_panel)
        main_row.add(center_panel)
        main_row.add(right_panel)
        self.widget = main_row

        anchor = self.manager.add(arcade.gui.UIAnchorLayout())
        anchor.add(anchor_x="center_x", anchor_y="center_y", child=main_row)

    def upgrade_stat(self, stat):
        self.hero.xp -= 100+(self.hero.lvl-1)*20
        self.hero.lvl +=1        
        
        if stat == "HP":
            self.hero.max_hp += defs.LVLUP_HP
            self.hero.hp = self.hero.max_hp
        elif stat == "ATK":
            self.hero.atk += defs.LVLUP_ATK
        elif stat == "DEF":
            self.hero.defense += defs.LVLUP_DEFENSE
        elif stat == "MAG":
            self.hero.magic += defs.LVLUP_MAGIC
        
        self.build_ui()

    def on_show_view(self):
        self.manager.enable()
        self.build_ui()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(defs.MAP_IMGS[self.current_map],
                                 arcade.LBWH(0, 0, self.window.width, self.window.height))
        r = self.widget.rect
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