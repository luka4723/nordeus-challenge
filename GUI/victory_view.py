import arcade
import arcade.gui
from game_logic import defs
from GUI import elements

def make_label(text, font_size=16, bold=False, color=arcade.color.WHITE):
    return arcade.gui.UILabel(
        text=text, font_size=font_size, bold=bold,
        text_color=color, font_name="Kenney Mini"
    )

class VictoryView(arcade.View):
    def __init__(self, xp_gained, gold_gained, move_learned, equipment_found,
                 map, return_view, enemy_name):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.xp_gained = xp_gained
        self.gold_gained = gold_gained
        self.move_learned = move_learned
        self.equipment_found = equipment_found
        self.map = map
        self.return_view = return_view
        self.enemy_name = enemy_name
        self.widget = None
        self.build_ui()

    def build_ui(self):
        self.manager.clear()

        layout = arcade.gui.UIBoxLayout(vertical=True, space_between=20)

        layout.add(make_label(
            f"Victory! You have slain the {self.enemy_name}.",
            font_size=24, bold=True, color=arcade.color.GOLD
        ))

        rewards_row = arcade.gui.UIBoxLayout(vertical=False, space_between=60)

        left_col = arcade.gui.UIBoxLayout(vertical=True, space_between=10)

        #XP
        xp_row = arcade.gui.UIBoxLayout(vertical=False, space_between=6)
        xp_row.add(make_label(f"+{self.xp_gained}", font_size=18, color=arcade.color.WHITE))
        xp_row.add(make_label("XP", font_size=18, color=arcade.color.LIGHT_BLUE))
        left_col.add(xp_row)

        #GOld
        gold_row = arcade.gui.UIBoxLayout(vertical=False, space_between=8)
        gold_row.add(make_label(f"+{self.gold_gained}", font_size=18, color=arcade.color.WHITE))
        gold_row.add(arcade.gui.UIImage(texture=defs.GOLD_ICON, width=24, height=24))
        left_col.add(gold_row)

        #Move
        left_col.add(make_label("Move learned:", font_size=16, color=arcade.color.GOLD))
        if self.move_learned:
            left_col.add(make_label(self.move_learned, font_size=18, bold=True, color=arcade.color.LIGHT_BLUE))
        else:
            left_col.add(make_label("Nothing new.", font_size=16, color=arcade.color.WHITE))

        right_col = arcade.gui.UIBoxLayout(vertical=True, space_between=10)
        right_col.add(make_label("Equipment found:", font_size=16, color=arcade.color.GOLD))
        if self.equipment_found:
            eq_img = arcade.gui.UIImage(texture=self.equipment_found.tex,width=96, height=96)
            right_col.add(eq_img.with_border(width=2, color=arcade.color.GOLD))
        else:
            right_col.add(make_label("Nothing found.", font_size=16, color=arcade.color.GRAY))

        rewards_row.add(left_col)
        rewards_row.add(right_col)
        layout.add(rewards_row)

        # btn
        btn = elements.MyButton(
            text="Continue",
            texture=defs.BTN_NORMAL_TEX,
            texture_hovered=defs.BTN_HOVERED_TEX,
            texture_pressed=defs.BTN_PRESSED_TEX,
            width=200, height=60, text_size=20
        )
        @btn.event("on_click")
        def on_continue(event, view=self):
            defs.SOUND.play(volume=0.08)
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