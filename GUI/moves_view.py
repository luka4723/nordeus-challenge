import arcade
import arcade.gui
import game_logic.moves as moves
from GUI import elements
from game_logic import beings
import time

def move_name(move) -> str:
    name = type(move).__name__
    result = [name[0]]
    for ch in name[1:]:
        if ch.isupper():
            result.append(" ")
        result.append(ch)
    return "".join(result)

class MovesView(arcade.View):
    def __init__(self, hero: beings.Hero, return_view, map):
        super().__init__()
        self.hero = hero
        #print(self.hero.moves)
        self.return_view = return_view
        self.manager = arcade.gui.UIManager()
        self.selected_pool_move = None   
        self.selected_active = None  
        self.hovered_move = None
        self.hover_start_time = 0
        self.hovered_button = None
        self.tooltip_delay = 0.75
        self.widget = None
        self.build_ui()
        self.current_map = map
        self.maps = [
            arcade.load_texture(":res:desert_menu.png"),
            arcade.load_texture(":res:forest_menu.png"),
            arcade.load_texture(":res:dungeon_menu.png"),
        ]
    def build_ui(self):
        self.manager.clear()
        self.hovered_move = None     
        self.hovered_button = None

        root = arcade.gui.UIBoxLayout(vertical=True, space_between=16)

        # label
        root.add(arcade.gui.UILabel(
            text="Equipped Moves",
            font_size=22, bold=False,
            text_color=arcade.color.GOLD,
            font_name="Kenney Mini",
        ))

        # Active Moves
        active_row = arcade.gui.UIBoxLayout(vertical=False, space_between=12)
        for i in range(4):
            move = self.hero.moves[i]
            is_selected = (self.selected_active == i)
            if is_selected:
                btn = elements.MyButton(
                    text=move_name(move),
                    texture=arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png"),
                    texture_hovered=arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png"),
                    texture_pressed=arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png"),
                    width=170, height=50, text_size=17, parent_win=self
                )
            else:
                btn = elements.MyButton(text=move_name(move), 
                            texture=arcade.load_texture(":resources:/gui_basic_assets/button/red_normal.png"),
                            texture_hovered=arcade.load_texture(":resources:/gui_basic_assets/button/red_hover.png"),
                            texture_pressed=arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png"),
                            width=170, height=50, text_size=17, parent_win=self)
            btn.move = move

            idx = i 
            @btn.event("on_click")
            def on_click_switch_button(event, i=idx):
                if self.selected_pool_move is not None:
                    if self.selected_pool_move not in self.hero.moves:
                        self.hero.moves[i] = type(self.selected_pool_move)(self.hero)
                    self.selected_pool_move = None
                    self.selected_active = None
                else:
                    if self.selected_active == i:
                        self.selected_active = None
                    else:
                        self.selected_active = i
                self.build_ui()

            active_row.add(btn)

        root.add(active_row)

        # Label
        root.add(arcade.gui.UILabel(
            text="Available Moves",
            font_size=22, bold=False,
            text_color=arcade.color.GOLD,
            font_name="Kenney Mini",
        ))

        # Available moves
        pool_grid = arcade.gui.UIGridLayout(
            column_count=4,
            row_count=(len(self.hero.available_moves) + 3) // 4,
            horizontal_spacing=10,
            vertical_spacing=10,
        )

        for i, move in enumerate(self.hero.available_moves):
            is_selected = (move is self.selected_pool_move)

            if is_selected:
                btn = elements.MyButton(
                    text=move_name(move),
                    texture=arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png"),
                    texture_hovered=arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png"),
                    texture_pressed=arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png"),
                    width=170, height=50, text_size=17, parent_win=self
                )
            else:
                btn = elements.MyButton(text=move_name(move), 
                            texture=arcade.load_texture(":resources:/gui_basic_assets/button/red_normal.png"),
                            texture_hovered=arcade.load_texture(":resources:/gui_basic_assets/button/red_hover.png"),
                            texture_pressed=arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png"),
                            width=170, height=50, text_size=17, parent_win=self)
            
            btn.move = move
                
            @btn.event("on_click")
            def on_click_switch_button(event, m=move):
                if self.selected_active is not None:
                    if m not in self.hero.moves:
                        self.hero.moves[self.selected_active] = type(m)(self.hero)
                    self.selected_active = None
                    self.selected_pool_move = None
                else:
                    if self.selected_pool_move == m:
                        self.selected_pool_move = None
                    else:
                        self.selected_pool_move = m
                self.build_ui()

            pool_grid.add(btn, column=i % 4, row=i // 4)

        root.add(pool_grid)

        # Button
        back_btn = elements.MyButton(text="Back", 
                            texture=arcade.load_texture(":resources:/gui_basic_assets/button/red_normal.png"),
                            texture_hovered=arcade.load_texture(":resources:/gui_basic_assets/button/red_hover.png"),
                            texture_pressed=arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png"),
                             width=200, height=60, text_size=20)

        @back_btn.event("on_click")
        def on_click_switch_button(event):
            self.window.show_view(self.return_view)

        root.add(back_btn)
        self.widget = root

        anchor = self.manager.add(arcade.gui.UIAnchorLayout())
        anchor.add(anchor_x="center_x", anchor_y="center_y", child=root)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(self.maps[self.current_map],
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

        print(self.hovered_move)
        print(time.time())
        print(self.hover_start_time)
        print()
        print()
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

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.return_view)