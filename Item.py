import pygame

from Box import Box
from InputBox import InputBox


class Item(Box):
    def __init__(self, width, height, x, y, color, amount, cost=0, text="", text_size=30):
        super().__init__(width, height, x, y, color, text, text_size=text_size)

        self.amount = amount
        self.amount_box = InputBox(60, 50, self.rect.topright[0] - 70,
                                   self.rect.centery - 25, "dark gray", str(amount), text_size)
        self.cost = cost

    def draw(self, screen, dest=None):
        super().draw(screen, dest)
        self.amount_box.draw(screen, dest)

    def handle_event(self, event):
        self.amount_box.handle_event(event)

        if event.type == pygame.MOUSEWHEEL and self.amount_box.check_mouse_collision():
            try:
                if (event.y + (int(self.amount_box.text))) >= 0:
                    self.amount_box.text = (str(int(self.amount_box.text) + event.y))
                self.amount_box.txt_surface = self.amount_box.FONT.render(self.amount_box.text, True, "black")
            except ValueError:
                pass
        if not self.amount_box.active:
            try:
                self.amount = (int(self.amount_box.text))
            except ValueError:
                pass

    def get_total_cost(self):
        return int(self.amount_box.text) * self.cost

    def update_pos(self, x=0, y=0):
        self.rect.move_ip(x, y)
        self.text_rect.move_ip(x, y)
        self.amount_box.update_pos(x, y)


class InventoryItem(Item):
    def __init__(self, width, height, x, y, color, amount, weight, cost=0, text="", text_size=30):
        super().__init__(width, height, x, y, color, amount, cost, text, text_size)
        self.weight = weight
        self.amount_box = InputBox(60, 50, self.rect.topright[0] - 70,
                                   self.rect.centery - 25, "dark gray", str(amount), text_size)
        self.weight_box = Box(60, 50, self.amount_box.rect.x - 105, self.rect.centery - 25, "light gray",
                              "Weight:" + str(weight * amount), True)

    def draw(self, screen, dest=None):
        super().draw(screen, dest)
        self.weight_box.set_text("Weight:" + str(round(self.weight * float(self.amount), 1)))
        self.weight_box.draw(screen, dest)

    def update_pos(self, x=0, y=0):
        super().update_pos(x, y)
        self.weight_box.update_pos(x, y)

    def get_total_weight(self):
        return round(self.weight * float(self.amount), 1)
