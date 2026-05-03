from game_logic import beings
import arcade
import random

class Effect:
    def __init__(self, carrier: beings.Being, value, duration):
        self.duration = duration
        self.value = value
        self.carrier = carrier
        self.desc = "test"
        self.tex = None

    def apply(self):
        pass

    def remove(self):
        pass

class StatEffect(Effect):
    def __init__(self, carrier, value, duration):
        super().__init__(carrier, value, duration)
        self.flag = None
        self.apply()

class IncreaseDefense(StatEffect):
    def __init__(self, carrier, value, duration):
        super().__init__(carrier, value, duration)
        self.desc = f"Increased {type(self.carrier).__name__}'s DEF \nby {self.value} for {self.duration} moves"
        self.tex = arcade.load_texture(":res:defu.png")

    def apply(self):
        if self.flag is None:
            self.flag = True
            self.carrier.defense += self.value
    
    def remove(self):
        self.carrier.defense -= self.value
        self.flag = False

class IncreaseAtk(StatEffect):
    def __init__(self, carrier, value, duration):
        super().__init__(carrier, value, duration)
        self.desc = f"Increased {type(self.carrier).__name__}'s ATK \nby {self.value} for {self.duration} moves"
        self.tex = arcade.load_texture(":res:atku.png")

    def apply(self):
        if self.flag is None:
            self.flag = True
            self.carrier.atk += self.value
    
    def remove(self):
        self.carrier.atk -= self.value
        self.flag = False

class IncreaseMagic(StatEffect):
    def __init__(self, carrier, value, duration):
        super().__init__(carrier, value, duration)
        self.desc = f"Increased {type(self.carrier).__name__}'s MAG by \n{self.value} for {self.duration} moves"
        self.tex = arcade.load_texture(":res:magu.png")

    def apply(self):
        if self.flag is None:
            self.flag = True
            self.carrier.magic += self.value
    
    def remove(self):
        self.carrier.magic -= self.value
        self.flag = False

class DecreaseDefense(StatEffect):
    def __init__(self, carrier, value, duration):
        super().__init__(carrier, value, duration)
        self.desc = f"Decreased {type(self.carrier).__name__}'s DEF by \n{self.value} for {self.duration} moves"
        self.tex = arcade.load_texture(":res:defd.png")

    def apply(self):
        if self.flag is None:
            self.flag = True
            self.carrier.defense -= self.value
    
    def remove(self):
        self.carrier.defense += self.value
        self.flag = False

class DecreaseAtk(StatEffect):
    def __init__(self, carrier, value, duration):
        super().__init__(carrier, value, duration)
        self.desc = f"Decreased {type(self.carrier).__name__}'s ATK by \n{self.value} for {self.duration} moves"
        self.tex = arcade.load_texture(":res:atkd.png")

    def apply(self):
        if self.flag is None:
            self.flag = True
            self.carrier.atk -= self.value
    
    def remove(self):
        self.carrier.atk += self.value
        self.flag = False

class DecreaseMagic(StatEffect):
    def __init__(self, carrier, value, duration):
        super().__init__(carrier, value, duration)
        self.desc = f"Decreased {type(self.carrier).__name__}'s MAG by \n{self.value} for {self.duration} moves"
        self.tex = arcade.load_texture(":res:magd.png")

    def apply(self):
        if self.flag is None:
            self.flag = True
            self.carrier.magic -= self.value
    
    def remove(self):
        self.carrier.magic += self.value
        self.flag = False       

class TickEffect(Effect):
    def __init__(self, carrier, value, duration):
        super().__init__(carrier, value, duration)
        self.duration += 1

class Bleed(TickEffect):
    def __init__(self, carrier, value, duration):
        super().__init__(carrier, value, duration)
        self.desc = f"{type(self.carrier).__name__} bled for {self.value/self.carrier.defense} HP"
        self.tex = arcade.load_texture(":res:bleed.png")

    def apply(self):
        self.carrier.hp -= self.value/self.carrier.defense
      
class Poison(TickEffect):
    def __init__(self, carrier, value, duration):
        super().__init__(carrier, value, duration)
        self.desc = f"{type(self.carrier).__name__} is sick. Lost {self.value} HP"
        self.tex = arcade.load_texture(":res:poison.png")

    def apply(self):
        self.carrier.hp -= self.value

class Dizzy(TickEffect):
    def __init__(self, carrier, value, duration):
        super().__init__(carrier, value, duration)
        self.desc = f"{type(self.carrier).__name__} is dizzy for {self.duration+1} moves."
        self.tex = arcade.load_texture(":res:dizzy.png")

        