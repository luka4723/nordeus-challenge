import arcade
from GUI import elements
from game_logic import defs

def make_label(text, font_size=16, bold=False, color=arcade.color.WHITE):
    return arcade.gui.UILabel(
        text=text, font_size=font_size, bold=bold,
        text_color=color, font_name="Kenney Mini"
    )

class DefeatView(arcade.View):
    def __init__(self, map, enemy_name):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.map = map
        self.enemy_name = enemy_name
        self.widget = None
        self.build_ui()

    def build_ui(self):
        self.manager.clear()

        layout = arcade.gui.UIBoxLayout(vertical=True, space_between=20)

        layout.add(make_label(
            "Defeat!", font_size=28, bold=True, color=arcade.color.GOLD
        ))
        layout.add(make_label(
            f"{self.enemy_name} was too strong.", font_size=18, color=arcade.color.WHITE
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
            from GUI import main_menu_view
            view.window.show_view(main_menu_view.MainMenuView())
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