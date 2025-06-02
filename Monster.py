from Box import Box
from InputBox import InputBox


class Monster:
    def __init__(self, x, y):
        self.border = Box(345, 50, x, y, "light gray")
        self.name = InputBox(125, 40, x + 5, y + 5, "dark gray")
        self.int = InputBox(100, 40, x + 135, y + 5, "dark gray", "INT:")
        self.hp = InputBox(100, 40, x + 240, y + 5, "dark gray", "HP:")

    def draw(self, screen):
        self.border.draw(screen)
        self.name.draw(screen)
        self.int.draw(screen)
        self.hp.draw(screen)

    def handle_event(self, event):
        self.name.handle_event(event)
        self.int.handle_event(event)
        self.hp.handle_event(event)
