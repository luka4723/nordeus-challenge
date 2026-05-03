import arcade
import arcade.gui
from game_logic import defs, equipment
from GUI import elements
import time

def move_name(name):
    result = [name[0]]
    for ch in name[1:]:
        if ch.isupper():
            result.append(" ")
        result.append(ch)
    return "".join(result)
    
def make_label(text, font_size=16, bold=False, color=arcade.color.WHITE):
    return arcade.gui.UILabel(
        text=text, font_size=font_size, bold=bold,
        text_color=color, font_name="Kenney Mini"
    )

SLOTS = [
    ("Head",   equipment.Head),
    ("Torso",  equipment.Torso),
    ("Arms",   equipment.Arms),
    ("Legs",   equipment.Legs),
    ("Weapon", equipment.Weapon),
    ("Shield", equipment.Shield),
    ("Acc",    equipment.Acc),
]

class EquipmentView(arcade.View):
    def __init__(self, hero, return_view, map):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.hero = hero
        self.return_view = return_view
        self.map = map
        self.widget = None
        self.center_btns = {}
        self.slot_buttons = {}
        self.scroll_index = {slot: 0 for slot, _ in SLOTS}
        self.hovered_move = None
        self.hover_start_time = 0
        self.hovered_button = None
        self.tooltip_delay = 0.75

        for slot_name, slot_type in SLOTS:
            active = self.get_active(slot_type)
            if active is not None:
                items = self.items_for_slot(slot_type)
                for j, item in enumerate(items):
                    if type(item) == type(active):
                        self.scroll_index[slot_name] = j + 1
                        break

        self.build_ui()

    def items_for_slot(self, slot_type):
        return [i for i in self.hero.available_equipment if isinstance(i, slot_type)]
    
    def items_for_slot_display(self, slot_type):
        return [type(i)(self.hero) for i in self.hero.available_equipment if isinstance(i, slot_type)]

    def get_active(self, slot_type):
        for item in self.hero.active_equipment:
            if isinstance(item, slot_type):
                return item
        return None

    def get_selected(self, slot_name, slot_type):
        idx = self.scroll_index[slot_name]
        if idx == 0:
            return None
        items = self.items_for_slot(slot_type)
        if idx <= len(items):
            return items[idx - 1]
        return None

    def update_ui(self):
        """Osvežava samo teksture i objekte na dugmićima, bez brisanja celog UI-a."""
        for slot_name, slot_type in SLOTS:
            slot_items = self.items_for_slot(slot_type)
            slot_items_display = self.items_for_slot_display(slot_type)
            total = len(slot_items) + 1
            idx = self.scroll_index[slot_name]

            for j, offset in enumerate([-1, 0, 1]):
                i = (idx + offset) % total

                if i == 0 or i - 1 >= len(slot_items):
                    tex = defs.X_ICON
                    display_item = None
                else:
                    tex = slot_items[i - 1].tex
                    display_item = slot_items_display[i - 1]

                btn = self.slot_buttons[slot_name][j]
                
                btn.texture = tex
                btn.texture_hovered = tex
                btn.texture_pressed = tex
                btn.move = type(display_item)(self.hero) if display_item is not None else None

    def build_ui(self):
        self.manager.clear()
        self.center_btns = {}
        self.slot_buttons = {}

        layout = arcade.gui.UIBoxLayout(vertical=True, space_between=12)
        layout.add(make_label("Equipment:", font_size=22, bold=True, color=arcade.color.GOLD))

        for slot_name, slot_type in SLOTS:
            row = arcade.gui.UIBoxLayout(vertical=False, space_between=8)
            row.add(make_label(f"{slot_name}:".ljust(7), font_size=16, color=arcade.color.LIGHT_BLUE))

            # left
            btn_left = elements.MyButton(
                text="", texture=defs.LEFT_TEX, texture_hovered=defs.LEFT_TEX,
                texture_pressed=defs.LEFT_TEX, width=24, height=24, text_size=1
            )
            @btn_left.event("on_click")
            def on_left(event, sn=slot_name, st=slot_type):
                defs.SOUND.play(volume=0.08)
                tot = len(self.items_for_slot(st)) + 1
                self.scroll_index[sn] = (self.scroll_index[sn] - 1) % tot
                self.update_ui()
            row.add(btn_left)

            self.slot_buttons[slot_name] = []
            for offset in [-1, 0, 1]:
                btn = elements.MyButton(
                    text="", texture=defs.X_ICON, texture_hovered=defs.X_ICON,
                    texture_pressed=defs.X_ICON, width=40, height=40, text_size=1, parent_win=self
                )
                
                self.slot_buttons[slot_name].append(btn)
                if offset == 0:
                    self.center_btns[slot_name] = btn

                row.add(btn)

            # right
            btn_right = elements.MyButton(
                text="", texture=defs.RIGHT_TEX, texture_hovered=defs.RIGHT_TEX,
                texture_pressed=defs.RIGHT_TEX, width=24, height=24, text_size=1
            )
            @btn_right.event("on_click")
            def on_right(event, sn=slot_name, st=slot_type):
                defs.SOUND.play(volume=0.08)
                tot = len(self.items_for_slot(st)) + 1
                self.scroll_index[sn] = (self.scroll_index[sn] + 1) % tot
                self.update_ui()
            row.add(btn_right)

            layout.add(row)

        # btn
        btn_done = elements.MyButton(
            text="Done", texture=defs.BTN_NORMAL_TEX, texture_hovered=defs.BTN_HOVERED_TEX,
            texture_pressed=defs.BTN_PRESSED_TEX, width=200, height=60, text_size=25
        )
        @btn_done.event("on_click")
        def on_done(event, view=self):
            defs.SOUND.play(volume=0.08)
            view.apply_equipment()
            view.window.show_view(view.return_view)
        layout.add(btn_done)

        self.widget = layout
        anchor = self.manager.add(arcade.gui.UIAnchorLayout())
        anchor.add(anchor_x="center_x", anchor_y="center_y", child=layout)
        
        self.update_ui()

    def apply_equipment(self):
        for item in self.hero.active_equipment:
            item.remove()
        self.hero.active_equipment = []

        for slot_name, slot_type in SLOTS:
            selected = self.get_selected(slot_name, slot_type)
            if selected is not None:
                selected.apply()
                self.hero.active_equipment.append(selected)

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
            padding = 20
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

        for slot_name, btn in self.center_btns.items():
            r = btn.rect
            arcade.draw_lbwh_rectangle_outline(
                r.left, r.bottom, r.width, r.height,
                color=arcade.color.GOLD, border_width=2
            )

        if self.hovered_move and (time.time() - self.hover_start_time) > self.tooltip_delay:
            scale = self.window.get_pixel_ratio()
            x = self.window._mouse_x / scale
            y = self.window._mouse_y / scale
            width = 180
            height = 25

            arcade.draw_lbwh_rectangle_filled(x, y, width, height, (20, 20, 30, 230))
            arcade.draw_lbwh_rectangle_outline(x, y, width, height, arcade.color.GOLD, 2)

            arcade.draw_text(
                move_name(type(self.hovered_move).__name__),
                x + 5, y + height,
                arcade.color.GOLD, 16, font_name="Kenney Mini"
            )
            arcade.draw_text(
                f"Increases {self.hovered_move.stat.upper()[:3]} by {self.hovered_move.val}",
                x + 5, y - 5 + height - 12,
                arcade.color.WHITE, 12,
                width=280, multiline=True, font_name="Kenney Mini"
            )