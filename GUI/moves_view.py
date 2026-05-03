import arcade
import arcade.gui
import game_logic.moves as moves
from GUI import elements
from game_logic import beings, defs
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
        self.return_view = return_view
        self.manager = arcade.gui.UIManager()
        self.selected_pool_move = None   
        self.selected_active = None  
        self.hovered_move = None
        self.hover_start_time = 0
        self.hovered_button = None
        self.tooltip_delay = 0.75
        self.widget = None
        self.current_map = map

        self.active_move_buttons = []
        self.pool_move_buttons = []

        self.build_ui()

    def update_ui(self):
        for i, btn in enumerate(self.active_move_buttons):
            move = self.hero.moves[i]
            new_name = move_name(move)
            
            if btn.text != new_name:
                btn.text = new_name
            
            btn.move = move 
            
            if self.selected_active == i:
                btn.texture = defs.BTN_PRESSED_TEX
            else:
                btn.texture = defs.BTN_NORMAL_TEX

        for btn in self.pool_move_buttons:
            if btn.move_obj is self.selected_pool_move:
                btn.texture = defs.BTN_PRESSED_TEX
            else:
                btn.texture = defs.BTN_NORMAL_TEX

    def build_ui(self):
        self.manager.clear()
        self.active_move_buttons.clear()
        self.pool_move_buttons.clear()

        root = arcade.gui.UIBoxLayout(vertical=True, space_between=16)

        root.add(arcade.gui.UILabel(
            text="Equipped Moves", font_size=22, text_color=arcade.color.GOLD, font_name="Kenney Mini"
        ))

        active_row = arcade.gui.UIBoxLayout(vertical=False, space_between=12)
        for i in range(4):
            move = self.hero.moves[i]
            btn = elements.MyButton(
                text=move_name(move), 
                texture=defs.BTN_NORMAL_TEX,
                texture_hovered=defs.BTN_HOVERED_TEX,
                texture_pressed=defs.BTN_PRESSED_TEX,
                width=170, height=50, text_size=17, parent_win=self
            )
            btn.move = move
            btn.idx = i
            
            @btn.event("on_click")
            def on_active_click(event):
                defs.SOUND.play(volume=0.08)
                b = event.source
                if self.selected_pool_move is not None:
                    if self.selected_pool_move not in self.hero.moves:
                        self.hero.moves[b.idx] = type(self.selected_pool_move)(self.hero)
                    self.selected_pool_move = None
                    self.selected_active = None
                else:
                    self.selected_active = b.idx if self.selected_active != b.idx else None
                self.update_ui()

            self.active_move_buttons.append(btn)
            active_row.add(btn)
        root.add(active_row)

        root.add(arcade.gui.UILabel(
            text="Available Moves", font_size=22, text_color=arcade.color.GOLD, font_name="Kenney Mini"
        ))

        pool_grid = arcade.gui.UIGridLayout(
            column_count=4,
            row_count=(len(self.hero.available_moves) + 3) // 4,
            horizontal_spacing=10, vertical_spacing=10,
        )

        for i, move in enumerate(self.hero.available_moves):
            btn = elements.MyButton(
                text=move_name(move), 
                texture=defs.BTN_NORMAL_TEX,
                texture_hovered=defs.BTN_HOVERED_TEX,
                texture_pressed=defs.BTN_PRESSED_TEX,
                width=170, height=50, text_size=17, parent_win=self
            )
            btn.move = move
            btn.move_obj = move 
            
            @btn.event("on_click")
            def on_pool_click(event):
                defs.SOUND.play(volume=0.08)
                b = event.source
                if self.selected_active is not None:
                    if b.move_obj not in self.hero.moves:
                        self.hero.moves[self.selected_active] = type(b.move_obj)(self.hero)
                    self.selected_active = None
                    self.selected_pool_move = None
                else:
                    self.selected_pool_move = b.move_obj if self.selected_pool_move != b.move_obj else None
                self.update_ui()

            self.pool_move_buttons.append(btn)
            pool_grid.add(btn, column=i % 4, row=i // 4)
        
        root.add(pool_grid)

        back_btn = elements.MyButton(text="Back", texture=defs.BTN_NORMAL_TEX, width=200, height=60, text_size=20)
        @back_btn.event("on_click")
        def on_back(event):
            defs.SOUND.play(volume=0.08)
            self.window.show_view(self.return_view)
        root.add(back_btn)

        self.widget = root
        anchor = self.manager.add(arcade.gui.UIAnchorLayout())
        anchor.add(anchor_x="center_x", anchor_y="center_y", child=root)
        
        self.update_ui()

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(defs.MAP_IMGS[self.current_map],
                                 arcade.LBWH(0, 0, self.window.width, self.window.height))
        
        r = self.widget.rect
        padding = 20
        arcade.draw_lrbt_rectangle_filled(r.left - padding, r.right + padding,
                                          r.bottom - padding, r.top + padding, (0, 0, 0, 160))
        arcade.draw_lrbt_rectangle_outline(r.left - padding, r.right + padding,
                                           r.bottom - padding, r.top + padding, border_width=2, color=arcade.color.GOLD)
        
        self.manager.draw()

        if self.hovered_move and (time.time() - self.hover_start_time) > self.tooltip_delay:
            scale = self.window.get_pixel_ratio()
            x = self.window._mouse_x / scale
            y = self.window._mouse_y / scale
            width = 300
            height = 100

            arcade.draw_lbwh_rectangle_filled(x, y, width, height, (20, 20, 30, 230))
            arcade.draw_lbwh_rectangle_outline(x, y, width, height, arcade.color.GOLD, 2)

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
                y - 5 + height - 12,
                arcade.color.WHITE,
                12,
                width=280,
                multiline=True,
                font_name="Kenney Mini"
            )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.return_view)