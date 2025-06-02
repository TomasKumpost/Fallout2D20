from xml.etree import ElementTree

import pygame

from Box import Box
from Clock import Clock
from Monster import Monster
from PlayerBox import PlayerBox


class Counter:
    def __init__(self, screen):
        self.screen = screen

        self.player_boxes = self.prepare_player_boxes()
        self.monsters = self.prepare_monsters(self.player_boxes)

        self.FONT = pygame.font.Font("Data/Fonts/Overseer.otf", 30)
        self.txt_surface1 = self.FONT.render("Purified water = 4 Steps", True, "black")
        self.txt_surface2 = self.FONT.render("Dirty Water and Alcohol = 1 Step (and Milk and Blood Pack)", True,
                                             "black")
        self.txt_surface3 = self.FONT.render("Other Clean Water = 2 Steps", True, "black")
        self.text_x = self.player_boxes[-1].border.rect.bottomleft[0]
        self.text_y = self.player_boxes[-1].border.rect.bottomleft[1] + 10

        self.plus_one_button = Box(250, 80,
                                   self.player_boxes[-1].border.rect.bottomright[0] + 10,
                                   self.player_boxes[-1].border.rect.bottomright[1] + 10,
                                   "light gray", "+1 to all", True, 70)

        days, hours = self.prepare_clock()
        self.clock = Clock(self.plus_one_button.rect.topright[0] + 10,
                           self.plus_one_button.rect.topright[1], self.screen, days, hours)

    def draw(self):
        for player_box in self.player_boxes:
            player_box.draw(self.screen)
        for monster in self.monsters:
            monster.draw(self.screen)

        self.screen.blit(self.txt_surface1, (self.text_x, self.text_y))
        self.screen.blit(self.txt_surface2, (self.text_x, self.text_y + 35))
        self.screen.blit(self.txt_surface3, (self.text_x, self.text_y + 70))
        self.plus_one_button.draw(self.screen)
        self.clock.draw()

    def handle_event(self, event):
        for player_box in self.player_boxes:
            player_box.handle_event(event)
        for monster in self.monsters:
            monster.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pressed()
            if mouse[0] and self.plus_one_button.check_mouse_collision():
                for player_box in self.player_boxes:
                    if not player_box.border.click:
                        player_box.add_one_to_all()
            if mouse[0]:
                self.clock.handle_event()

    def save_data(self):
        tree = ElementTree.parse("Data/players.xml")
        players = tree.getroot()

        for player, node in zip(self.player_boxes, players):
            statuses = player.get_statuses()
            node.set("name", statuses[0])
            for status_value_old, status_value_new in zip(node, statuses[1:]):
                if status_value_new == "":
                    status_value_old.text = "0"
                else:
                    status_value_old.text = status_value_new

        tree.write("Data/players.xml")

        tree = ElementTree.parse("Data/time.xml")
        time = tree.getroot()
        time[0].text = str(self.clock.days)
        time[1].text = str(self.clock.hours)
        tree.write("Data/time.xml")

    @staticmethod
    def prepare_player_boxes():
        border_width = 700
        border_height = 250

        tree = ElementTree.parse("Data/players.xml")
        players = tree.getroot()
        player_boxes = []
        pos_x = 10
        pos_y = 10

        for player in players:
            player_boxes.append(PlayerBox(pos_x, pos_y, player.get("name"),
                                          int(player.find("hunger").text), int(player.find("thirst").text),
                                          int(player.find("sleep").text), int(player.find("initiative").text),
                                          int(player.find("fatigue").text), border_width, border_height))
            pos_x += 10 + border_width
            if pos_x >= 20 + 2 * border_width:
                pos_y += 10 + border_height
                pos_x = 10

        return player_boxes

    @staticmethod
    def prepare_clock():
        tree = ElementTree.parse("Data/time.xml")
        time = tree.getroot()
        return int(time[0].text), int(time[1].text)

    @staticmethod
    def prepare_monsters(player_boxes):
        x, y = player_boxes[-1].border.rect.topright
        return [Monster(x + 10 + (index % 2 * 355), y + (int(index / 2) * 60)) for index in range(8)]
