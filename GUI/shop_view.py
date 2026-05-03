import arcade
import arcade.gui
from game_logic import defs, equipment
from GUI import elements
import random

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
        self.selected = None  

        self.gold_label = None
        self.grid_buttons = [] 
        self.item_borders = [] 
        
        self.preview_img = None
        self.preview_title = None
        self.preview_desc = None
        self.price_label = None
        self.buy_btn = None

        self.empty_tex = arcade.make_soft_square_texture(128, (0, 0, 0, 0))

        self.build_ui()

    def update_ui(self):
        if self.gold_label:
            self.gold_label.text = f"{self.hero.gold}"

        for idx in range(9):
            btn = self.grid_buttons[idx]
            border = self.item_borders[idx]
            
            if idx < len(self.items):
                item, price = self.items[idx]
                btn.texture = item.tex
                btn.texture_hovered = item.tex
                btn.texture_pressed = item.tex
                btn.move = item 
                btn.visible = True
                border.visible = True
                
                is_selected = self.selected is not None and self.selected[0] is item
                border.border_color = arcade.color.GOLD if is_selected else (50, 50, 50)
            else:
                btn.visible = False
                border.visible = False

        if self.selected:
            item, price = self.selected
            self.preview_img.texture = item.tex
            self.preview_title.text = move_name(type(item).__name__)
            self.preview_desc.text = f"Increases {item.stat.upper()[:3]} by {item.val}"
            self.price_label.text = str(price)
            
            can_afford = self.hero.gold >= price
            self.buy_btn.texture = defs.BTN_NORMAL_TEX if can_afford else defs.BTN_PRESSED_TEX
            self.buy_btn.texture_hovered = defs.BTN_HOVERED_TEX if can_afford else defs.BTN_PRESSED_TEX
        else:
            self.preview_img.texture = self.empty_tex 
            self.preview_title.text = "Nothing"
            self.preview_desc.text = "It's dusty."
            self.price_label.text = "999"
            self.buy_btn.texture = defs.BTN_PRESSED_TEX 
            self.buy_btn.texture_hovered = defs.BTN_PRESSED_TEX

    def build_ui(self):
        self.manager.clear()
        layout = arcade.gui.UIBoxLayout(vertical=True, space_between=16)

        header = arcade.gui.UIBoxLayout(vertical=False, space_between=250)
        header.add(arcade.gui.UILabel(text="Shop", font_size=26, bold=True, text_color=arcade.color.GOLD, font_name="Kenney Mini"))
        
        gold_row = arcade.gui.UIBoxLayout(vertical=False, space_between=6)
        self.gold_label = arcade.gui.UILabel(text="", font_size=18, font_name="Kenney Mini", text_color=arcade.color.WHITE)
        gold_row.add(self.gold_label)
        gold_row.add(arcade.gui.UIImage(texture=defs.GOLD_ICON, width=24, height=24))
        header.add(gold_row)
        layout.add(header)

        main_row = arcade.gui.UIBoxLayout(vertical=False, space_between=32)

        grid = arcade.gui.UIGridLayout(column_count=3, row_count=3, horizontal_spacing=16, vertical_spacing=16)
        self.grid_buttons = []
        self.item_borders = []

        for i in range(9):
            btn = elements.MyButton(text="", texture=defs.BTN_NORMAL_TEX, width=64, height=64, text_size=1)
            border = btn.with_border(width=2, color=(50, 50, 50))
            btn.idx = i
            
            @btn.event("on_click")
            def on_select(event):
                idx = event.source.idx
                if idx < len(self.items):
                    self.selected = self.items[idx]
                    self.update_ui()

            self.grid_buttons.append(btn)
            self.item_borders.append(border)
            grid.add(border, column=i % 3, row=i // 3)
        
        main_row.add(grid)

        preview_col = arcade.gui.UIBoxLayout(vertical=True, space_between=12)
        
        self.preview_img = arcade.gui.UIImage(texture=self.empty_tex, width=128, height=128)
        preview_col.add(self.preview_img.with_border(width=2, color=arcade.color.GOLD))

        self.preview_title = arcade.gui.UILabel(text="Nothing", font_size=18, bold=True, text_color=arcade.color.GOLD, font_name="Kenney Mini")
        preview_col.add(self.preview_title)

        self.preview_desc = arcade.gui.UILabel(text="It's dusty.", font_size=14, text_color=arcade.color.WHITE, font_name="Kenney Mini")
        preview_col.add(self.preview_desc)

        price_row = arcade.gui.UIBoxLayout(vertical=False, space_between=6)
        self.price_label = arcade.gui.UILabel(text="999", font_size=16, text_color=arcade.color.WHITE, font_name="Kenney Mini")
        price_row.add(self.price_label)
        price_row.add(arcade.gui.UIImage(texture=defs.GOLD_ICON, width=20, height=20))
        preview_col.add(price_row)

        self.buy_btn = elements.MyButton(text="Buy", 
                                         texture=defs.BTN_NORMAL_TEX,
                                         texture_hovered=defs.BTN_HOVERED_TEX,
                                         texture_pressed=defs.BTN_PRESSED_TEX,
                                         width=130, height=40, text_size=18)
        @self.buy_btn.event("on_click")
        def on_buy(event):
            if self.selected:
                item, price = self.selected
                if self.hero.gold >= price:
                    defs.SOUND.play(volume=0.08)
                    self.hero.gold -= price
                    self.hero.available_equipment.append(item)
                    self.items = [it for it in self.items if it[0] is not item]
                    self.selected = None
                    self.update_ui()
        preview_col.add(self.buy_btn)

        main_row.add(preview_col)
        layout.add(main_row)

        btn_done = elements.MyButton(text="Done", 
                                     texture=defs.BTN_NORMAL_TEX,
                                     texture_hovered=defs.BTN_HOVERED_TEX,
                                     texture_pressed=defs.BTN_PRESSED_TEX,                                     
                                     width=200, height=60, text_size=20)
        @btn_done.event("on_click")
        def on_done(event): 
            defs.SOUND.play(volume=0.08)
            while len(self.items) < 9:
                item_key = random.choice(list(defs.ITEMS.keys())).replace(" ", "")
                eq = getattr(equipment, item_key)(self.return_view.hero)
                p_idx = random.randint(0, len(defs.PRICES) - 1)
                self.items.append((eq, defs.PRICES[p_idx]))
            self.return_view.shop_items = self.items
            self.window.show_view(self.return_view)
        layout.add(btn_done)

        self.widget = layout
        anchor = self.manager.add(arcade.gui.UIAnchorLayout())
        anchor.add(anchor_x="center_x", anchor_y="center_y", child=layout)
        
        self.update_ui()

    def on_show_view(self):
        self.manager.enable()

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(defs.MAP_IMGS[self.map],
                                 arcade.LBWH(0, 0, self.window.width, self.window.height))
        if self.widget:
            r = self.widget.rect
            padding = 20
            arcade.draw_lrbt_rectangle_filled(r.left - padding, r.right + padding,
                                              r.bottom - padding, r.top + padding, (0, 0, 0, 180))
            arcade.draw_lrbt_rectangle_outline(r.left - padding, r.right + padding,
                                               r.bottom - padding, r.top + padding, border_width=2, color=arcade.color.GOLD)
        self.manager.draw()