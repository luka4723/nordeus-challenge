import arcade, arcade.gui
from GUI import elements, game_view
from game_logic import beings,defs

def make_label(text, font_size=14, bold=False, color=arcade.color.WHITE):
    return arcade.gui.UILabel(
        text=text, font_size=font_size, bold=bold,
        text_color=color, font_name="Kenney Mini"
    )

class SelectView(arcade.View):
    def __init__(self, return_view,map):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.return_view = return_view
        self.names = ["Knight", "Wizard","Rogue","Berserker","Granny"]
        self.current = 0
        self.icon = None
        self.widget = None
        self.current_map = map
        self.endless = False

    def build_ui(self):
        self.manager.clear()
        layout = arcade.gui.UIBoxLayout(vertical=True, space_between=16)

        # Name
        self.title_label = make_label(
            self.names[self.current].upper(),
            font_size=22, bold=True, color=arcade.color.GOLD
        )
        layout.add(self.title_label)

        # Scroll
        selector_row = arcade.gui.UIBoxLayout(vertical=False, space_between=12)

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
            view.current = (view.current - 1) % len(view.names)
            self.refresh()

        self.icon = arcade.gui.UIImage(
            texture=defs.BEING_SPRITES[self.names[self.current]],
            width=96, height=96
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
            view.current = (view.current + 1) % len(view.names)
            self.refresh()

        selector_row.add(btn_left)
        selector_row.add(self.icon.with_border(width=2, color=arcade.color.GOLD))
        selector_row.add(btn_right)
        layout.add(selector_row)

        endless_row = arcade.gui.UIBoxLayout(vertical=False, space_between=10)
        endless_label = make_label("Endless mode:", font_size=16, color=arcade.color.LIGHT_BLUE)
        
        empty_tex = arcade.Texture.create_empty("empty_checkbox", (30, 30))
        
        initial_tex = defs.X_ICON if self.endless else empty_tex
        
        btn_checkbox = elements.MyButton(
            text="",
            texture=initial_tex,
            texture_hovered=initial_tex,
            texture_pressed=initial_tex,
            width=30, height=30, text_size=1
        )
        
        @btn_checkbox.event("on_click")
        def on_checkbox_click(event, view=self, btn=btn_checkbox, empty=empty_tex):
            defs.SOUND.play(volume=0.08)
            view.endless = not view.endless  
            
            new_tex = defs.X_ICON if view.endless else empty
            btn.texture = new_tex
            btn.texture_hovered = new_tex
            btn.texture_pressed = new_tex
            
        endless_row.add(endless_label)
        
        endless_row.add(btn_checkbox.with_border(width=2, color=arcade.color.GOLD))
        layout.add(endless_row)
        
        # Btn
        btn_confirm = elements.MyButton(
            text="Continue",
            texture=defs.BTN_NORMAL_TEX,
            texture_hovered=defs.BTN_HOVERED_TEX,
            texture_pressed=defs.BTN_PRESSED_TEX,
            width=200, height=60, text_size=20
        )
        @btn_confirm.event("on_click")
        def on_confirm(event,view=self):
            defs.SOUND.play(volume=0.08)
            hero = getattr(beings, self.names[self.current])()
            self.window.show_view(game_view.GameView(map=self.current_map,hero = hero, 
                                                     play_tex=self.icon.texture,endless=self.endless))
        layout.add(btn_confirm)

        anchor = self.manager.add(arcade.gui.UIAnchorLayout())
        anchor.add(anchor_x="center_x", anchor_y="center_y", child=layout)
        self.widget = layout

    def refresh(self):
        self.title_label.text = self.names[self.current].upper()
        self.icon.texture = defs.BEING_SPRITES[self.names[self.current]]

    def on_show_view(self):
        self.manager.enable()
        self.build_ui()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(defs.MAP_IMGS[self.current_map],
                                 arcade.LBWH(0, 0, self.window.width, self.window.height))
        
        if self.widget and self.widget.rect.width > 0:
            r = self.widget.rect
            padding = 30
            arcade.draw_lrbt_rectangle_filled(
                r.left - padding, r.right + padding,
                r.bottom - padding, r.top + padding,
                (0, 0, 0, 180)
            )
            arcade.draw_lrbt_rectangle_outline(
                r.left - padding, r.right + padding,
                r.bottom - padding, r.top + padding,
                border_width=2, color=arcade.color.GOLD
            )
        self.manager.draw()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.return_view)