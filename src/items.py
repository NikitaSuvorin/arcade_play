import arcade


class Poison(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("assets/images/зелье.png", scale=0.3)
        self.center_x = x
        self.center_y = y


class NewSword(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__("assets/images/меч_1.png", scale=0.1)
        self.center_x = x
        self.center_y = y