import pygame

from Box import Box


class Button(Box):
    def __init__(self, width, height, x, y, color, click_color, text="", center_text=False, text_size=30):
        super().__init__(width, height, x, y, color, text, center_text, text_size)
        self.click = False
        self.click_color = click_color

    def draw(self, screen, dest=None):
        if self.click:
            pygame.draw.rect(screen, self.click_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.txt_surface, self.text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and pygame.mouse.get_pressed()[0]:
                self.click = not self.click


class ItemButton(Button):
    def __init__(self, width, height, x, y, color, click_color, cost, text="", center_text=False, text_size=30):
        super().__init__(width, height, x, y, color, click_color, text, center_text, text_size)
        self.cost = cost
        self.cost_surface = self.FONT.render("Caps: " + str(cost), True, "black")
        self.active = True

    def set_active(self, statement=True):
        self.active = statement

    def draw(self, screen, dest=None):
        if self.active:
            if self.click:
                pygame.draw.rect(screen, self.click_color, self.rect)
            else:
                pygame.draw.rect(screen, self.color, self.rect)
            screen.blit(self.txt_surface, (self.text_rect.x, self.text_rect.y - 10))
            screen.blit(self.cost_surface, (self.text_rect.centerx - self.cost_surface.get_width()/2,
                                            self.text_rect.y + 15))

class InventoryButton(Button):
    def __init__(self, width, height, x, y, color, click_color, weight, text="", center_text=False, text_size=30):
        super().__init__(width, height, x, y, color, click_color, text, center_text, text_size)
        self.weight_val = weight
        self.weight = self.FONT.render("Weight: " + str(weight), True, "black")
        self.active = True

    def set_active(self, statement=True):
        self.active = statement

    def draw(self, screen, dest=None):
        if self.active:
            if self.click:
                pygame.draw.rect(screen, self.click_color, self.rect)
            else:
                pygame.draw.rect(screen, self.color, self.rect)
            screen.blit(self.txt_surface, (self.text_rect.x, self.text_rect.y - 10))
            screen.blit(self.weight, (self.text_rect.centerx - self.weight.get_width()/2,
                                      self.text_rect.y + 15))

