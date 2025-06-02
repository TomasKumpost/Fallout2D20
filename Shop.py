import pygame

from Item import Item
from ScrollPanel import ScrollPanel
from Box import Box
from ItemFinder import start


class Shop:
    def __init__(self, screen):
        self.trader_list = ScrollPanel(700, 600, 0, 0, "light gray", self.find_trader)
        self.player_list = ScrollPanel(700, 600, 900, 0, "light gray", self.find_player)

        self.clear_button = Box(125, 50, 750, 100, "red", "Clear", True)
        self.calculate_button = Box(125, 50, 750, 175, "light gray", "Calculate", True)

        self.trader_up_charge = Item(300, 75, 50, 625, "light gray", 0, text="Up charge %")
        self.trader_discount = Item(300, 75, 360, 625, "light gray", 0, text="Discount %")

        self.player_under_selling = Item(300, 75, 950, 625, "light gray", 0, text="Under selling %")
        self.player_up_charge = Item(300, 75, 1260, 625, "light gray", 0, text="Up charge %")

        self.trader_price = Box(200, 50, 50, 710, "light gray", "Caps: ")
        self.player_price = Box(200, 50, 950, 710, "light gray", "Caps: ")

        self.objects = (self.trader_list, self.trader_up_charge, self.trader_discount, self.trader_price,
                        self.player_list, self.player_up_charge, self.player_under_selling, self.player_price)
        self.screen = screen

    def draw(self):
        for obj in self.objects:
            obj.draw(self.screen)
        self.clear_button.draw(self.screen)
        self.calculate_button.draw(self.screen)

    def handle_event(self, event):
        for obj in self.objects:
            obj.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pressed()
            if mouse[0]:
                if self.clear_button.check_mouse_collision():
                    self.trader_list.clear_items()
                    self.player_list.clear_items()
                elif self.calculate_button.check_mouse_collision():
                    self.trader_price.set_text("Caps: " + str(int(self.calculate_trader())))
                    self.player_price.set_text("Caps: " + str(int(self.calculate_player())))

    def calculate_trader(self):
        return ((self.trader_list.final_amount() * (float(self.trader_up_charge.amount_box.text) / 100 + 1)) *
                (1 - float(self.trader_discount.amount_box.text) / 100))

    def calculate_player(self):
        return ((self.player_list.final_amount() * (1 - float(self.player_under_selling.amount_box.text) / 100)) *
                (float(self.player_up_charge.amount_box.text) / 100 + 1))

    def find_trader(self):
        items = start(self.screen)
        for name, cost in items:
            self.trader_list.add_item(name, cost)

    def find_player(self):
        items = start(self.screen)
        for name, cost in items:
            self.player_list.add_item(name, cost)
