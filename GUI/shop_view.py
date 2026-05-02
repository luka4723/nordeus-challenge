import arcade
import arcade.gui
from game_logic import defs, equipment
from GUI import elements
import random

def make_label(text, font_size=16, bold=False, color=arcade.color.WHITE):
    return arcade.gui.UILabel(
        text=text, font_size=font_size, bold=bold,
        text_color=color, font_name="Kenney Mini"
    )

def move_name(name):
    result = [name[0]]
    for ch in name[1:]:
        if ch.isupper():
            result.append(" ")
        result.append(ch)
    return "".join(result)

class ShopView(arcade.View):
    def __init__(self, hero, items, map, return_view):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.hero = hero
        self.items = items
        self.map = map
        self.return_view = return_view
        self.widget = None
        self.selected = None  # (item, price)
        self.build_ui()

    def build_ui(self):
        self.manager.clear()

        layout = arcade.gui.UIBoxLayout(vertical=True, space_between=16)

        # up
        header = arcade.gui.UIBoxLayout(vertical=False, space_between=250)
        header.add(make_label("Shop", font_size=26, bold=True, color=arcade.color.GOLD))
        gold_row = arcade.gui.UIBoxLayout(vertical=False, space_between=6)
        gold_row.add(make_label(f"{self.hero.gold}", font_size=18, color=arcade.color.WHITE))
        gold_row.add(arcade.gui.UIImage(texture=defs.GOLD_ICON, width=24, height=24))
        header.add(gold_row)
        layout.add(header)

        main_row = arcade.gui.UIBoxLayout(vertical=False, space_between=32)

        # 3x3 grid
        grid = arcade.gui.UIGridLayout(
            column_count=3, row_count=3,
            horizontal_spacing=16, vertical_spacing=16
        )
        for idx, (item, price) in enumerate(self.items):
            is_selected = self.selected is not None and self.selected[0] is item
            border_color = arcade.color.GOLD if is_selected else arcade.color.DARK_GRAY

            btn = elements.MyButton(
                text="",
                texture=item.tex,
                texture_hovered=item.tex,
                texture_pressed=item.tex,
                width=64, height=64, text_size=1
            )
            btn.move = item

            @btn.event("on_click")
            def on_select(event, i=item, p=price):
                self.selected = (i, p)
                self.needs_rebuild = True

            grid.add(btn.with_border(width=2, color=border_color), column=idx % 3, row=idx // 3)

        main_row.add(grid)

        # grid
        preview_col = arcade.gui.UIBoxLayout(vertical=True, space_between=12)

        if self.selected:
            item, price = self.selected

            preview_col.add(arcade.gui.UIImage(
                texture=item.tex, width=128, height=128
            ).with_border(width=2, color=arcade.color.GOLD))

            preview_col.add(make_label(
                move_name(type(item).__name__),
                font_size=18, bold=True, color=arcade.color.GOLD
            ))
            preview_col.add(make_label(
                f"Increases {item.stat.upper()[:3]} by {item.val}",
                font_size=14, color=arcade.color.WHITE
            ))

            price_row = arcade.gui.UIBoxLayout(vertical=False, space_between=6)
            price_row.add(make_label(str(price), font_size=16, color=arcade.color.WHITE))
            price_row.add(arcade.gui.UIImage(texture=defs.GOLD_ICON, width=20, height=20))
            preview_col.add(price_row)

            can_afford = self.hero.gold >= price
            buy_btn = elements.MyButton(
                text="Buy",
                texture=defs.BTN_NORMAL_TEX if can_afford else defs.BTN_PRESSED_TEX,
                texture_hovered=defs.BTN_HOVERED_TEX if can_afford else defs.BTN_PRESSED_TEX,
                texture_pressed=defs.BTN_PRESSED_TEX,
                width=130, height=40, text_size=18
            )
            @buy_btn.event("on_click")
            def on_buy(event, i=item, p=price):
                if self.hero.gold >= p:
                    self.hero.gold -= p
                    self.hero.available_equipment.append(i)
                    self.items = [(it, pr) for it, pr in self.items if it is not i]
                    self.selected = None
                    self.needs_rebuild = True
            preview_col.add(buy_btn)
        else:
            preview_col.add(arcade.gui.UIWidget(
                width=128, height=128
            ).with_border(width=2, color=arcade.color.GOLD))

            preview_col.add(make_label(
                "Nothing", font_size=18, bold=True, color=arcade.color.GOLD
            ))
            preview_col.add(make_label(
                "It's dusty.", font_size=14, color=arcade.color.GRAY
            ))
            price_row = arcade.gui.UIBoxLayout(vertical=False, space_between=6)
            price_row.add(make_label("999", font_size=16, color=arcade.color.WHITE))
            price_row.add(arcade.gui.UIImage(texture=defs.GOLD_ICON, width=20, height=20))
            preview_col.add(price_row)

            buy_btn = elements.MyButton(
                text="Buy",
                texture=defs.BTN_PRESSED_TEX,
                texture_hovered=defs.BTN_PRESSED_TEX,
                texture_pressed=defs.BTN_PRESSED_TEX,
                width=130, height=40, text_size=18
            )
            preview_col.add(buy_btn)

        main_row.add(preview_col)
        layout.add(main_row)

        # btn
        btn_done = elements.MyButton(
            text="Done",
            texture=defs.BTN_NORMAL_TEX,
            texture_hovered=defs.BTN_HOVERED_TEX,
            texture_pressed=defs.BTN_PRESSED_TEX,
            width=200, height=60, text_size=20
        )
        @btn_done.event("on_click")
        def on_done(event, view=self):
            while len(self.items) < 9:
                eq = getattr(equipment, random.choice(list(defs.ITEMS.keys())).replace(" ", ""))(self.return_view.hero)
                
                while eq in self.return_view.hero.available_equipment and self.return_view.hero.available_equipment<len(defs.ITEMS.keys()):
                    eq = getattr(equipment, random.choice(list(defs.ITEMS.keys())).replace(" ", ""))(self.return_view.hero)
                p = random.randint(0,len(defs.PRICES)-1)
                self.items.append((eq,defs.PRICES[p]))
            self.return_view.shop_items = self.items    
            view.window.show_view(view.return_view)
        layout.add(btn_done)

        self.widget = layout
        anchor = self.manager.add(arcade.gui.UIAnchorLayout())
        anchor.add(anchor_x="center_x", anchor_y="center_y", child=layout)

    def on_update(self, delta_time):
        if getattr(self, 'needs_rebuild', False):
            self.needs_rebuild = False
            self.build_ui()

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