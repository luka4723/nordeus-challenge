import arcade
import arcade.gui
from pathlib import Path
import game_logic.client
from game_logic import defs, beings, equipment
from GUI import main_menu_view,moves_view,elements, battle_view, equipment_view, shop_view, end_view
import json, random, time

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
    def __init__(self, map, hero, play_tex,endless=None ,from_save=False):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.current_map = map
        self.widget = None
        self.start_time = time.time()
        self.paused_duration = 0

        self.map_preview = None
        self.lvl_label = None
        self.xp_label = None
        self.hp_label = None
        self.atk_label = None
        self.def_label = None
        self.mag_label = None
        self.player_slot_images = []
        self.stat_up_buttons = []
        
        self.empty_texture = arcade.Texture.create_empty("empty_slot", (80, 80))

        if from_save:
            with open(assets_path / "savefile.txt", "r") as f:
                save_dict = json.load(f)
                self.current_floor = save_dict["floor"]
                self.temp_floor = save_dict["temp_floor"]
                self.hero = beings.Hero.from_dict(save_dict["hero"])
                self.enemies = []
                for enemy_data in save_dict["enemies"]:
                    enemy = getattr(beings, enemy_data["type"])(enemy_data["order"])   
                    self.enemies.append(enemy)
                self.current_map = save_dict["map"]
                self.start_time = save_dict["start_time"]
                self.paused_duration = save_dict["paused_duration"] + (time.time() - save_dict["pause_start"])
                self.endless = save_dict["endless"]
                self.floor_count = save_dict["floor_count"]
        else:
            self.hero = hero
            self.endless = endless
            self.enemies = game_logic.client.getState(endless)
            self.current_floor = 0
            self.temp_floor = self.current_floor
            self.floor_count = 0

        self.player_texture = play_tex
        
        self.enemy_textures = []
        for enemy in self.enemies:
            self.enemy_textures.append(defs.BEING_SPRITES[f"{type(enemy).__name__}"])
        
        self.shop_items = [
            (getattr(equipment, name.replace(" ", ""))(self.hero), defs.PRICES[random.randint(0, len(defs.PRICES)-1)])
            for name in random.sample(list(defs.ITEMS.keys()), 9)
        ]   
        
        self.build_ui()

    def update_ui(self):
        self.lvl_label.text = f"{self.hero.lvl}"
        self.xp_label.text = f"{round(self.hero.xp)} / {100+(round(self.hero.lvl-1))*20}"
        self.hp_label.text = f"{round(self.hero.hp)} / {round(self.hero.max_hp)}"
        self.atk_label.text = f"{round(self.hero.atk,2)}"
        self.def_label.text = f"{round(self.hero.defense,2)}"
        self.mag_label.text = f"{round(self.hero.magic,2)}"

        self.levelup_available = self.hero.xp >= 100 + (self.hero.lvl - 1) * 20
    
        for btn in self.stat_up_buttons:
            btn.visible = self.levelup_available

        for floor, img_widget in self.player_slot_images:
            if floor == self.temp_floor:
                img_widget.texture = self.player_texture
                self.player_slot = img_widget
            else:
                img_widget.texture = self.empty_texture

    def build_ui(self):
        self.manager.clear()
        self.enemy_slots = {}
        self.player_slot = None

        if self.current_floor == 5:
            self.window.show_view(end_view.EndView(map=self.current_map,time= self.start_time + self.paused_duration))

        #LEFT 
        left_panel = arcade.gui.UIBoxLayout(vertical=True, space_between=20)

        hero_header = arcade.gui.UIBoxLayout(vertical=True, space_between=6)
        hero_img = arcade.gui.UIImage(
            texture=self.player_texture, width=64, height=64
        )
        hero_header.add(hero_img)
        hero_header.add(make_label(type(self.hero).__name__.upper(), font_size=16, bold=True, color=arcade.color.GOLD))
        left_panel.add(hero_header)

        btns = []
        for btn_text in ["Start Fight", "Moves", "Equipment", "Shop", "Save", "Back"]:
            btn = elements.MyButton(text=btn_text, 
                                    texture=defs.BTN_NORMAL_TEX,
                                    texture_hovered=defs.BTN_HOVERED_TEX,
                                    texture_pressed=defs.BTN_PRESSED_TEX,
                                    width=200, height=60, text_size=20)
            btns.append(btn)
            left_panel.add(btn)
        
        @btns[0].event("on_click")
        def on_click_battle(event):
            defs.SOUND.play(volume=0.08)
            self.window.show_view(battle_view.BattleView(
                                                        hero=self.hero,
                                                        enemy=self.enemies[self.temp_floor],
                                                        hero_texture=self.player_texture,
                                                        enemy_texture=self.enemy_textures[self.temp_floor],
                                                        return_view=self, map = self.current_map, endless=self.endless,floor=self.floor_count
                                                    ))
        @btns[1].event("on_click")
        def on_click_moves(event):
            defs.SOUND.play(volume=0.08)
            self.window.show_view(moves_view.MovesView(self.hero,self, map=self.current_map))

        @btns[2].event("on_click")
        def on_click_equipment(event):
            defs.SOUND.play(volume=0.08)
            self.window.show_view(equipment_view.EquipmentView(map=self.current_map,hero=self.hero,return_view=self))
        
        @btns[3].event("on_click")
        def on_click_shop(event):
            defs.SOUND.play(volume=0.08)
            self.window.show_view(shop_view.ShopView(map=self.current_map,hero=self.hero,return_view=self,items=self.shop_items))

        @btns[4].event("on_click")
        def on_click_save(event):
            defs.SOUND.play(volume=0.08)
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
                "temp_floor": self.temp_floor,
                "map" : self.current_map,
                "start_time": self.start_time,
                "paused_duration": self.paused_duration,
                "pause_start": time.time(),
                "endless": self.endless,
                "floor_count": self.floor_count,
            }
            with open(assets_path / "savefile.txt", "w") as f:
                json.dump(save_dict, f, indent=4)

        @btns[5].event("on_click")
        def on_click_back(event):
            defs.SOUND.play(volume=0.08)
            self.window.show_view(main_menu_view.MainMenuView())

        # MIDDLE
        center_panel = arcade.gui.UIBoxLayout(vertical=True, space_between=20)

        stats_title = make_label("STATS", font_size=20, color=arcade.color.GOLD)
        center_panel.add(stats_title)

        self.lvl_label = make_label(f"{self.hero.lvl}", bold=True)
        self.xp_label = make_label(f"{self.hero.xp} / {100+(self.hero.lvl-1)*20}", bold=True)
        self.hp_label = make_label(f"{round(self.hero.hp)} / {self.hero.max_hp}", bold=True)
        self.atk_label = make_label(f"{round(self.hero.atk,1)}", bold=True)
        self.def_label = make_label(f"{round(self.hero.defense,1)}", bold=True)
        self.mag_label = make_label(f"{round(self.hero.magic,1)}", bold=True)

        stats_data_labels = [
            ("Level", self.lvl_label),
            ("XP", self.xp_label),
            ("HP", self.hp_label),
            ("ATK", self.atk_label),
            ("DEF", self.def_label),
            ("MAG", self.mag_label),
        ]

        self.stat_up_buttons.clear()
        self.levelup_available = self.hero.xp >= 100 + (self.hero.lvl - 1) * 20

        stats_grid = arcade.gui.UIGridLayout(
            column_count=3, row_count=len(stats_data_labels), 
            horizontal_spacing=8, vertical_spacing=8
        )
        
        for i, (stat, label_widget) in enumerate(stats_data_labels):
            stats_grid.add(make_label(stat + ":", color=arcade.color.LIGHT_BLUE), column=0, row=i)
            stats_grid.add(label_widget, column=1, row=i)
            
            if self.levelup_available and stat in ("HP", "ATK", "DEF", "MAG"):
                btn = elements.MyButton(
                    text="",
                    texture=defs.UP_TEX, 
                    texture_hovered=defs.UP_TEX,
                    texture_pressed=defs.UP_TEX,
                    width=30, height=30, text_size=16
                )
                btn.visible = self.levelup_available
                @btn.event("on_click")
                def on_stat_up(event, a=stat):
                    defs.SOUND.play(volume=0.08)
                    if self.levelup_available:
                        self.upgrade_stat(a)
                self.stat_up_buttons.append(btn)
                stats_grid.add(btn, column=2, row=i)
            else:
                stats_grid.add(arcade.gui.UIWidget(width=30, height=30), column=2, row=i)
        
        center_panel.add(stats_grid)

        eq_title = make_label("EQUIPMENT", font_size=20, color=arcade.color.GOLD)
        center_panel.add(eq_title)

        SLOTS = [
            ("Head",   equipment.Head),
            ("Torso",  equipment.Torso),
            ("Arms",   equipment.Arms),
            ("Legs",   equipment.Legs),
            ("Weapon", equipment.Weapon),
            ("Shield", equipment.Shield),
            ("Acc",    equipment.Acc),
        ]

        eq_grid = arcade.gui.UIGridLayout(
            column_count=2, row_count=7,
            horizontal_spacing=24, vertical_spacing=6
        )
            
        for i, (slot, val) in enumerate(SLOTS):
            eq_grid.add(make_label(slot + ":", color=arcade.color.LIGHT_BLUE), column=0, row=i)
            has = False
            for eq in self.hero.active_equipment:
                if isinstance(eq, getattr(equipment, slot)):
                    has = eq
                    break
            if has:
                eq_grid.add(arcade.gui.UIImage(
                texture=has.tex, width=32, height=32
            ), column=1, row=i)
            else:
                eq_grid.add(arcade.gui.UIImage(
                texture=defs.X_ICON, width=32, height=32
            ), column=1, row=i)
        center_panel.add(eq_grid)

        # RIGHT
        right_panel = arcade.gui.UIBoxLayout(vertical=True, space_between=12)
        right_panel.add(make_label("TOWER", font_size=20, color=arcade.color.GOLD))

        tower_content = arcade.gui.UIBoxLayout(vertical=False, space_between=8)

        player_col = arcade.gui.UIGridLayout(
            column_count=1, row_count=5, horizontal_spacing=0, vertical_spacing=6
        )
        
        if self.endless:
            if self.current_floor ==3:
                self.current_floor-=1
                self.temp_floor-=1
                enemy = beings.FOE_LIST[random.randint(0,len(beings.FOE_LIST)-1)](self.floor_count+3)
                self.enemies.append(enemy)
                self.enemy_textures.append(defs.BEING_SPRITES[f"{type(enemy).__name__}"])
                self.enemy_textures = self.enemy_textures[-5:]
                self.enemies = self.enemies[-5:]

        self.player_slot_images = []
        for i in range(5):
            floor = 4 - i
            tex = self.player_texture if floor == self.temp_floor else self.empty_texture
            
            img = arcade.gui.UIImage(texture=tex, width=80, height=80)
            
            if floor == self.temp_floor:
                self.player_slot = img
                
            self.player_slot_images.append((floor, img))
            player_col.add(img, column=0, row=i)

        enemy_col = arcade.gui.UIGridLayout(
            column_count=1, row_count=5, horizontal_spacing=0, vertical_spacing=6
        )
        for i in range(5):
            floor = 4 - i
            btn = elements.MyButton(
                text="",
                texture=self.enemy_textures[floor],
                texture_hovered=self.enemy_textures[floor],
                texture_pressed=self.enemy_textures[floor],
                width=80, height=80, text_size=1
            )
            btn.floor = floor
            @btn.event("on_click")
            def on_enemy_click(event,b=btn):
                if b.floor <= self.current_floor:
                    self.temp_floor = b.floor
                    self.update_ui()
            self.enemy_slots[floor] = btn
            enemy_col.add(btn, column=0, row=i)

        tower_content.add(player_col)
        tower_content.add(enemy_col)
        right_panel.add(tower_content)
        
        # Map selector
        map_selector = arcade.gui.UIBoxLayout(vertical=False, space_between=8)

        btn_left = elements.MyButton(
            text="",
            texture=defs.LEFT_TEX,
            texture_hovered=defs.LEFT_TEX,
            texture_pressed=defs.LEFT_TEX,
            width=30, height=30, text_size=1
        )
        @btn_left.event("on_click")
        def on_left(event, view=self):
            defs.SOUND.play(volume=0.08)
            view.current_map = (view.current_map - 1) % len(defs.MAP_IMGS)
            self.refresh()

        self.map_preview = arcade.gui.UIImage(
            texture=defs.MAP_ICONS[self.current_map], width=64, height=64
        )

        btn_right = elements.MyButton(
            text="",
            texture=defs.RIGHT_TEX,
            texture_hovered=defs.RIGHT_TEX,
            texture_pressed=defs.RIGHT_TEX,
            width=30, height=30, text_size=1
        )
        @btn_right.event("on_click")
        def on_right(event, view=self):
            defs.SOUND.play(volume=0.08)
            view.current_map = (view.current_map + 1) % len(defs.MAP_IMGS)
            self.refresh()

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
        self.hero.lvl += 1        
        
        if stat == "HP":
            self.hero.max_hp += defs.LVLUP_HP
            self.hero.hp = self.hero.max_hp
        elif stat == "ATK":
            self.hero.atk += defs.LVLUP_ATK
        elif stat == "DEF":
            self.hero.defense += defs.LVLUP_DEFENSE
        elif stat == "MAG":
            self.hero.magic += defs.LVLUP_MAGIC        

        self.update_ui()

    def refresh(self):
        self.map_preview.texture = defs.MAP_ICONS[self.current_map]

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
        
        for floor, slot in self.enemy_slots.items():
            r = slot.rect
            if floor == self.current_floor:
                arcade.draw_lbwh_rectangle_outline(
                    r.left, r.bottom, r.width, r.height,
                    color=arcade.color.DARK_RED, border_width=3
                )
            elif floor < self.current_floor:
                arcade.draw_lbwh_rectangle_outline(
                    r.left, r.bottom, r.width, r.height,
                    color=arcade.color.DARK_GREEN, border_width=3
                )

        if self.player_slot:
            r = self.player_slot.rect
            arcade.draw_lbwh_rectangle_outline(
                r.left, r.bottom, r.width, r.height,
                color=arcade.color.DARK_BLUE, border_width=3
            )