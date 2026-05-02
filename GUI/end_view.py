import arcade
import arcade.gui
from game_logic import defs
from GUI import elements, main_menu_view
import time

def make_label(text, font_size=16, bold=False, color=arcade.color.WHITE):
    return arcade.gui.UILabel(
        text=text, font_size=font_size, bold=bold,
        text_color=color, font_name="Kenney Mini"
    )

class EndView(arcade.View):
    def __init__(self, map, time):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.map = map
        self.return_view = main_menu_view.MainMenuView()
        self.widget = None
        self.time = time
        self.build_ui()

    def build_ui(self):
        self.manager.clear()

        layout = arcade.gui.UIBoxLayout(vertical=True, space_between=30)

        layout.add(make_label(
            "Tower Completed!",
            font_size=32, bold=True, color=arcade.color.GOLD
        ))

        layout.add(make_label(
            "You have conquered all floors.",
            font_size=18, color=arcade.color.WHITE
        ))
        layout.add(make_label(
            f"Time: {round(time.time() - self.time)} sec",
            font_size=18, color=arcade.color.WHITE
        ))

        btn = elements.MyButton(
            text="Continue",
            texture=defs.BTN_NORMAL_TEX,
            texture_hovered=defs.BTN_HOVERED_TEX,
            texture_pressed=defs.BTN_PRESSED_TEX,
            width=200, height=60, text_size=20
        )
        @btn.event("on_click")
        def on_continue(event, view=self):
            view.window.show_view(view.return_view)
        layout.add(btn)

        self.widget = layout
        anchor = self.manager.add(arcade.gui.UIAnchorLayout())
        anchor.add(anchor_x="center_x", anchor_y="center_y", child=layout)

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            defs.MAP_IMGS[self.map],
            arcade.LBWH(0, 0, self.window.width, self.window.height)
        )
        if self.widget and self.widget.rect.left > 0:
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