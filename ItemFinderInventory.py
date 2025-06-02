from xml.etree import ElementTree

from Box import Box
from Button import InventoryButton

import pygame
import sys

from InputBox import InputBox


def start(screen):
    clock = pygame.time.Clock()
    run = True
    filter_box = InputBox(1000, 75, 300, 8, "light gray", text_size=60)
    cust_y = 95
    cust_x = 300
    custom_item = [Box(150, 50, cust_x, cust_y, "light gray", "Custom item:"),
                   Box(70, 50, cust_x + 150, cust_y, "light gray", "name"),
                   InputBox(300, 50, cust_x + 220, cust_y, "dark gray"),
                   Box(80, 50, cust_x + 520, cust_y, "light gray", "weight"),
                   InputBox(50, 50, cust_x + 600, cust_y, "darkgray")]

    confirm_selection = Box(200, 75, 1350, 8, "#009900", "Confirm Selection")
    catalog = parse_items()
    setup(catalog, custom_item[0].rect.height + custom_item[0].rect.y)

    while run:
        screen.fill("white")
        clock.tick(30)

        draw(screen, catalog, filter_box, confirm_selection, custom_item)

        for event in pygame.event.get():
            filter_box.handle_event(event)
            for category, items in catalog:
                for item in items:
                    item.handle_event(event)

            for item in custom_item:
                item.handle_event(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return []
                if filter_box.active:
                    update_search(filter_box, catalog, custom_item)
            if event.type == pygame.MOUSEWHEEL:
                update_scroll(catalog, filter_box, confirm_selection, custom_item, event.y)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pressed()
                if mouse[0]:
                    if confirm_selection.check_mouse_collision():
                        return return_values(catalog, custom_item)

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
    return 1


def return_values(catalog, custom_item):
    return_list = []
    if custom_item[2].text != "":
        if custom_item[-1].text != "":
            return_list.append((custom_item[2].text, float(custom_item[-1].text)))
        else:
            return_list.append((custom_item[2].text, 0.1))

    for category, items in catalog:
        for item in items:
            if item.click:
                return_list.append((item.text, item.weight_val))
    return return_list


def draw(screen, catalog, filter_box, confirm_selection, custom_item):
    for item in custom_item:
        item.draw(screen)

    filter_box.draw(screen)
    confirm_selection.draw(screen)
    for category, items in catalog:
        screen.blit(category[0], category[1])
        pygame.draw.line(screen, "black", (category[1].x, category[1].y + category[1].height - 6),
                         (1584, category[1].y + category[1].height - 6), 3)
        for item in items:
            item.draw(screen)


def setup(catalog, start_y):
    vertical_spacer = 8
    horizontal_spacer = 16
    pos_y = start_y + vertical_spacer * 2
    for category, items in catalog:
        category[1].update((horizontal_spacer, pos_y), (category[1].width, category[1].height))
        pos_y += category[1].height + vertical_spacer

        local_x = horizontal_spacer
        for item in items:
            if item.active:
                item.set_pos(local_x, pos_y)
                local_x += 300 + horizontal_spacer

                if local_x >= (300 + horizontal_spacer) * 5:
                    local_x = horizontal_spacer
                    pos_y += vertical_spacer + 75
            else:
                item.set_pos(-1000, 0)

        if local_x > horizontal_spacer:
            pos_y += vertical_spacer + 75


def update_search(filter_box, catalog, custom_item):
    search = filter_box.text

    if search == "":
        for category, items in catalog:
            for item in items:
                item.set_active()
    else:
        for category, items in catalog:
            for item in items:
                if item.text.lower().find(search.lower()) != -1:
                    item.set_active()
                else:
                    item.set_active(False)

    setup(catalog, custom_item[0].rect.height + custom_item[0].rect.y)


def parse_items():
    font = pygame.font.Font("Data/Fonts/Overseer.otf", 70)

    tree = ElementTree.parse("Data/items.xml")
    catalog = tree.getroot()
    finished_catalog = []

    for category in catalog:
        category_name = font.render(category.tag.capitalize().replace("_", " "), True, "black")
        category_list = (category_name, category_name.get_rect())

        items = [InventoryButton(300, 75, 0, 0, "light gray", "dark gray", float(item[1]),
                                 item[0], True, 25)
                 for item in [(item.attrib.get("name"), item.attrib.get("weight")) for item in category]]

        finished_catalog.append((category_list, items))

    return finished_catalog


def update_scroll(catalog, filter_box, confirm_selection, custom_item, y=0):
    mod = 30

    if y > 0 and filter_box.rect.y >= 8:
        pass
    else:
        filter_box.update_pos(y=y * mod)
        confirm_selection.update_pos(y=y * mod)

        for item in custom_item:
            item.update_pos(y=y * mod)

        for category, items in catalog:
            category[1].move_ip(0, y * mod)
            for item in items:
                item.update_pos(y=y * mod)
