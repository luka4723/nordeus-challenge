import beings

class Effect:
    def __init__(self, carrier: beings.Being, value, duration):
        self.duration = duration
        self.value = value
        self.carrier = carrier

    def apply(self):
        pass

    def remove(self):
        pass

class StatEffect:
    def __init__(self, carrier: beings.Being, value, duration):
        self.duration = duration
        self.value = value
        self.carrier = carrier
        self.old_value = None

    def apply(self):
        pass

    def remove(self):
        pass

class IncreaseDefense(StatEffect):
    def apply(self):
        if self.old_value is None:
            self.old_value = self.carrier.defense
        self.carrier.defense = self.value
    
    def remove(self):
        self.carrier.defense = self.old_value

class IncreaseAtk(StatEffect):
    def apply(self):
        if self.old_value is None:
            self.old_value = self.carrier.atk
        self.carrier.atk = self.value
    
    def remove(self):
        self.carrier.atk = self.old_value

class IncreaseMagic(StatEffect):
    def apply(self):
        if self.old_value is None:
            self.old_value = self.carrier.magic
        self.carrier.magic = self.value
    
    def remove(self):
        self.carrier.magic = self.old_value

class DecreaseDefense(StatEffect):
    def apply(self):
        if self.old_value is None:
            self.old_value = self.carrier.defense
        self.carrier.defense = self.value
    
    def remove(self):
        self.carrier.defense = self.old_value

class DecreaseAtk(StatEffect):
    def apply(self):
        if self.old_value is None:
            self.old_value = self.carrier.atk
        self.carrier.atk = self.value
    
    def remove(self):
        self.carrier.atk = self.old_value

class DecreaseMagic(StatEffect):
    def apply(self):
        if self.old_value is None:
            self.old_value = self.carrier.magic
        self.carrier.magic = self.value
    
    def remove(self):
        self.carrier.magic = self.old_value        