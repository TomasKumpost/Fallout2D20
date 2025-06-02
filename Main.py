import sys

import pygame

from Box import Box
from Counter import Counter
from Inventory import Inventory
from Shop import Shop

pygame.init()
# pyinstaller --noconsole -F  Main.py
section = 0
screen = pygame.display.set_mode((1600, 900))
pygame.display.set_caption("Fallout 2D20")
pygame.display.set_icon(pygame.image.load("Data/icon.png"))
clock = pygame.time.Clock()
run = True

inventory = Inventory(screen)
shop = Shop(screen)
counter = Counter(screen)

inventory_box = Box(300, 100, 650, 230, "light gray", "INVENTORY", True, 70)
shop_box = Box(300, 100, 650, 340, "light gray", "SHOP", True, 70)
counter_box = Box(300, 100, 650, 450, "light gray", "COUNTER", True, 70)

while run:
    screen.fill("white")
    clock.tick(30)

    if section == 0:
        inventory_box.draw(screen)
        shop_box.draw(screen)
        counter_box.draw(screen)
    elif section == 1:
        inventory.draw()
    elif section == 2:
        shop.draw()
    elif section == 3:
        counter.draw()

    for event in pygame.event.get():
        if section == 0:
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                if inventory_box.check_mouse_collision():
                    section = 1
                elif shop_box.check_mouse_collision():
                    section = 2
                elif counter_box.check_mouse_collision():
                    section = 3
        elif section == 1:
            inventory.handle_event(event)
        elif section == 2:
            shop.handle_event(event)
        elif section == 3:
            counter.handle_event(event)

        if event.type == pygame.QUIT:
            counter.save_data()
            inventory.save_data()
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and section != 0:
                section = 0

    pygame.display.update()
