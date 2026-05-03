import arcade
import arcade.gui
import time

class MyButton(arcade.gui.UITextureButton):
    def __init__(self, text, text_size, parent_win=None, **kwargs):
        super().__init__(text="", **kwargs) 
        
        self._button_text = text
        arcade.load_font(":resources:/fonts/ttf/Kenney/Kenney_Mini.ttf")
        
        self.layout = arcade.gui.UIAnchorLayout(width=self.width, height=self.height)
        self.label = arcade.gui.UILabel(
            text=text,
            font_size=text_size,
            font_name="Kenney Mini",
            text_color=arcade.color.WHITE
        )
    
        self.layout.add(self.label, anchor_x="center", anchor_y="center")
        self.move = None
        self.parent_win = parent_win
        self.add(self.layout)

    @property
    def text(self):
        return self._button_text

    @text.setter
    def text(self, value):
        self._button_text = value
        self.label.text = value 

    def on_event(self, event):
        if isinstance(event, arcade.gui.events.UIMouseMovementEvent):     
            if self.parent_win:
                if self.hovered:
                    self.parent_win.hovered_move = self.move
                    if self.parent_win.hovered_button is not self:
                        self.parent_win.hover_start_time = time.time()
                    self.parent_win.hovered_button = self
                else:
                    if self.parent_win.hovered_move is self.move:
                        self.parent_win.hovered_move = None
                        self.parent_win.hover_start_time = 0
                        self.parent_win.hovered_button = None
        
        super().on_event(event)