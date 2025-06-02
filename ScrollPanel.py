import pygame
from Box import Box
from Item import Item, InventoryItem


class ScrollPanel(Box):
    def __init__(self, width, height, x, y, color, fun=None):
        super().__init__(width, height, x, y, color)

        self.fun = fun
        self.dest = (-x, -y)
        self.items = []
        self.spacer = 10
        self.screen = pygame.surface.Surface((width, height))
        self.screen_rect = pygame.rect.Rect(0, 0, width, height)

        self.plus_button = Box(80, 80, self.rect.centerx - 40, self.rect.y + self.spacer,
                               "gray", "+", True, 75)

    def draw(self, screen, dest=None):
        pygame.draw.rect(self.screen, self.color, self.screen_rect)
        for item in self.items:
            item.draw(self.screen, self.dest)
        self.plus_button.draw(self.screen, self.dest)
        screen.blit(self.screen, self.rect)

    def add_item(self, name, cost):
        item_x = self.rect.centerx - 250
        if self.items.__len__() > 0:
            item_y = self.items[-1].rect.y + 80 + self.spacer
        else:
            item_y = self.spacer

        self.items.append(Item(500, 80, item_x, item_y, "gray", 1, cost, name))

        self.plus_button.update_pos(y=80 + self.spacer)

    def remove_item(self, remove_index):
        self.items.pop(remove_index)
        for item in self.items[remove_index:]:
            item.update_pos(y=-80 - self.spacer)
        self.plus_button.update_pos(y=-80 - self.spacer)

    def clear_items(self):
        self.items.clear()
        self.plus_button.set_pos(self.rect.centerx - 40, self.rect.y + self.spacer)

    def handle_event(self, event):
        if self.check_mouse_collision():
            for item in self.items:
                item.handle_event(event)

            if event.type == pygame.MOUSEWHEEL and not any([item.amount_box.check_mouse_collision() for item in self.items]):
                self.update_scroll(event.y)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pressed()
                if mouse[0]:
                    if self.plus_button.check_mouse_collision():
                        if self.fun:
                            self.fun()
                if mouse[2]:
                    if len(self.items) > 0:
                        remove_index = [i for i in range(len(self.items)) if self.items[i].check_mouse_collision()]
                        if remove_index:
                            self.remove_item(remove_index[0])

    def update_scroll(self, y=0):
        if y > 0 and self.items.__len__() > 0 and self.items[0].rect.y >= self.rect.y + self.spacer:
            pass
        else:
            if self.items.__len__() > 0:
                for item in self.items:
                    item.update_pos(y=y * 20)
                self.plus_button.update_pos(y=y * 20)

    def final_amount(self):
        final_amount = 0
        for item in self.items:
            final_amount += item.get_total_cost()
        return final_amount


class ScrollPanelItem(ScrollPanel):
    def __init__(self, width, height, x, y, color, fun=None):
        super().__init__(width, height, x, y, color, fun)

    def add_item(self, name, weight, amount=1):
        item_x = self.rect.centerx - 325
        if self.items.__len__() > 0:
            item_y = self.items[-1].rect.y + 80 + self.spacer
        else:
            item_y = self.spacer + self.rect.y

        self.items.append(InventoryItem(650, 80, item_x, item_y, "light gray", amount, weight, text=name))

        self.plus_button.update_pos(y=80 + self.spacer)

    def save_date(self):
        return [(item.text, item.weight, item.amount) for item in self.items]

    def get_total_weight(self):
        if self.items.__len__() > 0:
            return [item.weight * item.amount for item in self.items]
        else:
            return [0]
