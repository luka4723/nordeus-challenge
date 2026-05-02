import arcade
import arcade.gui
from game_logic import beings, gamelogic, moves, status_effects, defs, equipment
from GUI import elements, main_menu_view, victory_view, defeat_view
import time, random

def format_str(val, width=6):
    return str(val).ljust(width)

def make_label(text, font_size=14, bold=False, color=arcade.color.WHITE):
    return arcade.gui.UILabel(
        text=text, font_size=font_size, bold=bold,
        text_color=color, font_name="Kenney Mini"
    )
def move_name(move):
    name = type(move).__name__
    result = [name[0]]
    for ch in name[1:]:
        if ch.isupper():
            result.append(" ")
        result.append(ch)
    return "".join(result)

class BattleView(arcade.View):
    def __init__(self, hero: beings.Hero, enemy: beings.Foe,
                 hero_texture, enemy_texture, return_view, map):
        super().__init__()
        self.hero = hero
        self.enemy = enemy
        self.hero_texture = hero_texture
        self.enemy_texture = enemy_texture
        self.return_view = return_view
        self.manager = arcade.gui.UIManager()
        self.log_lines = []
        self.log_panel = None
        self.battle_over = False
        self.enemy_maxhp = self.enemy.hp
        self.current_map = map
        self.maps = [
            arcade.load_texture(":res:map_desert.png"),
            arcade.load_texture(":res:map_forest.png"),
            arcade.load_texture(":res:map_dungeon.png"),
        ]
        self.hovered_move = None
        self.hover_start_time = 0
        self.hovered_button = None
        self.tooltip_delay = 0.75

        self.bottom_bar_height = 220 
        self.enemy_event_text = ""
        self.event_label = make_label("", font_size=14, bold=False, color=arcade.color.WHITE)
        self.game = gamelogic.Encounter(self.hero,self.enemy)

        self.hero_pos = (1280/2-64-200, 415)   
        self.enemy_pos = (1280/2+200, 415)
        self.char_size = 80

        self.build_ui()

    def build_ui(self):
        self.manager.clear()
        
        if self.battle_over:
            if self.game.result:
                for effect in self.hero.status_effects:
                    effect.remove()

                order = random.randint(0,3)
                move = None
                if type(self.enemy.moves[order]) in [type(m) for m in self.hero.available_moves]:
                    pass
                else:
                    self.hero.available_moves.append(self.enemy.moves[order])
                    move = self.enemy.moves[order]

                eq = None
                rand_eq = random.choice(list(defs.ITEMS.keys())).replace(" ", "")
                rand_eq = getattr(equipment, rand_eq)(self.hero)
                if rand_eq not in self.hero.available_equipment:
                    eq = rand_eq
                    self.hero.available_equipment.append(eq)
                self.window.show_view(victory_view.VictoryView(xp_gained=defs.XP[self.enemy.order-1],
                                                                   gold_gained=defs.GOLD[self.enemy.order-1],
                                                                   move_learned=move_name(move),
                                                                   equipment_found=eq,
                                                                   map=self.current_map,
                                                                   return_view=self.return_view,
                                                                   enemy_name=type(self.enemy).__name__))
                if self.return_view.current_floor == self.return_view.temp_floor:
                    self.return_view.current_floor +=1
                    self.return_view.temp_floor +=1
                    
            else:
                self.window.show_view(defeat_view.DefeatView(map=self.current_map,enemy_name=type(self.enemy).__name__))
        main_anchor = self.manager.add(arcade.gui.UIAnchorLayout())

        bottom_line = arcade.gui.UIBoxLayout(vertical=False, space_between=20)
        
        #Hero stats
        hero_stats_box = arcade.gui.UIBoxLayout(vertical=True, space_between=6)
        hero_stats_box.add(make_label(type(self.hero).__name__.upper(), font_size=22, bold=True, color=arcade.color.UA_BLUE))

        stats = [
            ("HP",  format_str(f"{max(0, int(self.hero.hp))} / {self.hero.max_hp}",width=7)),
            ("ATK", format_str(round(self.hero.atk,2))),
            ("DEF", format_str(round(self.hero.defense,2))),
            ("MAG", format_str(round(self.hero.magic,2))),
        ]
        
        g = arcade.gui.UIGridLayout(column_count=2, row_count=len(stats), horizontal_spacing=10, vertical_spacing=5)
        for i, (lbl, val) in enumerate(stats):
            hp_low = lbl == "HP" and self.hero.hp < self.hero.max_hp * 0.2
            g.add(make_label(lbl + ":", color=arcade.color.LIGHT_BLUE, font_size=18), column=0, row=i)
            g.add(make_label(val, color=arcade.color.RED if hp_low else arcade.color.WHITE,font_size=18), column=1, row=i)
        hero_stats_box.add(g)
        
        bottom_line.add(hero_stats_box)

        #Enemy stats
        enemy_stats_box = arcade.gui.UIBoxLayout(vertical=True, space_between=6)
        enemy_stats_box.add(make_label(str(self.enemy).upper(), font_size=22, bold=True, color=arcade.color.UA_RED))
        
        e_stats = [
            ("HP",  format_str(f"{max(0, int(self.enemy.hp))} / {self.enemy_maxhp}",width=7)),
            ("ATK", format_str(round(self.enemy.atk,2))),
            ("DEF", format_str(round(self.enemy.defense,2))),
            ("MAG", format_str(round(self.enemy.magic,2))),
        ]
        
        eg = arcade.gui.UIGridLayout(column_count=2, row_count=len(e_stats), horizontal_spacing=10, vertical_spacing=5)
        for i, (lbl, val) in enumerate(e_stats):
            hp_low = lbl == "HP" and self.enemy.hp < self.enemy_maxhp * 0.2
            eg.add(make_label(lbl + ":", color=arcade.color.LIGHT_BLUE, font_size=18), column=0, row=i)
            eg.add(make_label(val,font_size=18,color=arcade.color.RED if hp_low else arcade.color.WHITE), column=1, row=i)
        enemy_stats_box.add(eg)

        #adding later for the sake of order

        #Buttons
        if not self.battle_over:
            moves_grid = arcade.gui.UIGridLayout(column_count=2, row_count=2, horizontal_spacing=15, vertical_spacing=15)
            for i, move in enumerate(self.hero.moves):
                btn = elements.MyButton(
                    text=move_name(move),
                    texture=defs.BTN_NORMAL_TEX,
                    texture_hovered=defs.BTN_HOVERED_TEX,
                    texture_pressed=defs.BTN_PRESSED_TEX,
                    width=150, height=40, text_size=14, parent_win=self
                )
                btn.move = move
                @btn.event("on_click")
                def on_move_click(event, m=move):
                    if not self.battle_over:
                        self.do_player_turn(m)
                moves_grid.add(btn, column=i % 2, row=i // 2)
            bottom_line.add(moves_grid)

        self.log_panel = arcade.gui.UIWidget(width=500, height=180).with_background(color=(0,0,0))
        bottom_line.add(self.log_panel)
        bottom_line.add(enemy_stats_box)

        main_anchor.add(
            child=bottom_line, 
            anchor_x="center_x", anchor_y="bottom",
            align_y=20
        )

    def do_player_turn(self, move: moves.Move):
        self.event_label.text = f""
        self.enemy_event_text = f""
        
        hp_before_enemy = self.enemy.hp
        hp_before_hero = self.hero.hp
        status_num_hero_before = len(self.hero.status_effects)

        self.game.heroMove(move)
        self.log_lines.append(f"{type(self.hero).__name__} used {type(move).__name__}")

        dmg_to_enemy = hp_before_enemy - self.enemy.hp
        heal_to_hero = self.hero.hp - hp_before_hero
        
        if "Physical" in move.type or "Magic" in move.type:
            self.event_label.text += f"Enemy lost {int(dmg_to_enemy)} HP.\n"
        
        if "Heal" in move.type:
            self.event_label.text += f"You gained {int(heal_to_hero)} HP.\n"
            
        if "Status" in move.type:
            if status_num_hero_before < len(self.hero.moves):
                if self.hero.status_effects:
                    self.event_label.text += self.hero.status_effects[-1].desc +"\n"
            else:
                if self.enemy.status_effects:
                    self.event_label.text += self.enemy.status_effects[-1].desc +"\n"

        self.game.applyEffectsH()

        if self.game.result is None:
            status_num_enemy_before = len(self.enemy.status_effects)
            hp_before_foe_move = self.hero.hp
            
            if any(isinstance(effect, status_effects.Dizzy) for effect in self.enemy.status_effects):
                foe_move = self.enemy.moves[random.randint(0,3)]
                if self.hero.hp <= 0 and self.game.result is None:
                    self.game.result = False
            else:
                foe_move = self.game.foeMove()
            
            if foe_move:
                self.log_lines.append(f"{type(self.enemy).__name__} used {type(foe_move).__name__}")
                
                hero_dmg_taken = hp_before_foe_move - self.hero.hp
                enemy_heal = self.enemy.hp - hp_before_enemy

                if "Physical" in foe_move.type or "Magic" in foe_move.type:
                    self.enemy_event_text += f"You lost {int(hero_dmg_taken)} HP.\n"
                
                if "Heal" in foe_move.type:
                    self.enemy_event_text += f"Enemy gained {int(enemy_heal)} HP.\n"
                
                if "Status" in foe_move.type:
                    if status_num_enemy_before < len(self.enemy.moves):
                        if self.hero.status_effects:
                            self.enemy_event_text += self.hero.status_effects[-1].desc + "\n"
                    else:
                        if self.enemy.status_effects:
                            self.enemy_event_text += self.enemy.status_effects[-1].desc + "\n"

            self.game.applyEffectsE()

        if self.game.result is not None:
            self.battle_over = True

        if self.log_lines and self.log_lines[0] == " ":
            self.log_lines.pop(0)

        self.build_ui()

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.maps[self.current_map],
                                 arcade.LBWH(0, 0, self.window.width, self.window.height))
        icon_size = 32
        icon_y = self.bottom_bar_height + 8
        icon_padding = 4

        # Hero
        arcade.draw_texture_rect(
            self.hero_texture,
            arcade.LBWH(self.hero_pos[0], self.hero_pos[1], self.char_size, self.char_size)
        )

        # Enemy
        arcade.draw_texture_rect(
            self.enemy_texture,
            arcade.LBWH(self.enemy_pos[0], self.enemy_pos[1], self.char_size, self.char_size)
        )

        for i, effect in enumerate(self.hero.status_effects):
            icon_x = 10 + i * (icon_size + icon_padding)
            arcade.draw_texture_rect(
                effect.tex,
                arcade.LBWH(icon_x, icon_y, icon_size, icon_size)
            )

        for i, effect in enumerate(self.enemy.status_effects):
            icon_x = self.window.width - 10 - (i + 1) * (icon_size + icon_padding)
            arcade.draw_texture_rect(
                effect.tex,
                arcade.LBWH(icon_x, icon_y, icon_size, icon_size)
            )

        arcade.draw_lrbt_rectangle_filled(
            left=0, 
            right=self.window.width,
            bottom=0, 
            top=self.bottom_bar_height,
            color=(0, 0, 0, 160)
        )
        
        arcade.draw_line(
            start_x=0, start_y=self.bottom_bar_height, 
            end_x=self.window.width, end_y=self.bottom_bar_height, 
            color=arcade.color.GOLD, line_width=2
        )
        self.manager.draw()

        if self.log_panel:
            px = self.log_panel.rect.left
            py = self.log_panel.rect.top
            panel_width = self.log_panel.rect.width
            panel_height = self.log_panel.rect.height
            padding = 10

            #Hero Actions
            arcade.draw_text("Hero Actions:", px + padding, py - padding - 16,
                            arcade.color.UA_BLUE, 16, font_name="Kenney Mini")
            if self.event_label.text:
                for i, line in enumerate(self.event_label.text.strip().split("\n")):
                    arcade.draw_text(line, px + padding, py - padding - 36 - i * 18,
                                    arcade.color.WHITE, 12, font_name="Kenney Mini")

            #Enemy actions
            bottom_y = py - panel_height // 2
            arcade.draw_text("Enemy Actions:", px + padding, bottom_y - padding - 16,
                            arcade.color.UA_RED, 16, font_name="Kenney Mini")
            if self.enemy_event_text:
                for i, line in enumerate(self.enemy_event_text.strip().split("\n")):
                    arcade.draw_text(line, px + padding, bottom_y - padding - 36 - i * 18,
                                    arcade.color.WHITE, 12, font_name="Kenney Mini")

            # Log
            right_x = px + panel_width // 2
            arcade.draw_text("Move history:", right_x + padding, py - padding - 16,
                            arcade.color.LIGHT_GRAY, 16, font_name="Kenney Mini")
            for i, line in enumerate(self.log_lines[-5:]):
                arcade.draw_text(line, right_x + padding, py - padding - 36 - i * 18,
                                arcade.color.LIGHT_GRAY, 12, font_name="Kenney Mini")

            mid_x = px + panel_width // 2
            arcade.draw_line(mid_x, self.log_panel.rect.bottom + padding,
                            mid_x, py - padding,
                            arcade.color.DARK_GRAY, 1)

        if self.hovered_move and (time.time() - self.hover_start_time) > self.tooltip_delay:
            scale = self.window.get_pixel_ratio()

            x = self.window._mouse_x /scale
            y = self.window._mouse_y /scale

            width = 300
            height = 100

            arcade.draw_lbwh_rectangle_filled(
                x,
                y,
                width,
                height,
                (20, 20, 30, 230)
            )

            arcade.draw_lbwh_rectangle_outline(
                x,
                y,
                width,
                height,
                arcade.color.GOLD,
                2
            )

            arcade.draw_text(
                move_name(self.hovered_move),
                x + 5,
                y + height,
                arcade.color.GOLD,
                16,
                font_name="Kenney Mini"
            )

            arcade.draw_text(
                self.hovered_move.desc,
                x + 5,
                y -5 + height - 12,
                arcade.color.WHITE,
                12,
                width=280,
                multiline=True,
                font_name="Kenney Mini"
            )
