import pygame
from Button import Button
from Box import Box
from InputBox import InputBox


class PlayerBox:
    def __init__(self, x, y, name, hunger, thirst, sleep, initiative, fatigue, border_width, border_height):
        self.border = Button(border_width, border_height, x, y, "light gray", "#666666")

        height = 40
        width_box = 100
        width_counter = 35
        spacer = 10

        self.name_box = Box(width_box * 3, height, x + spacer, y + spacer, "dark gray", "Name: " + name)
        self.name = name
        self.initiative_box = Box(width_box, height, self.name_box.rect.topright[0] + spacer * 2,
                                  self.name_box.rect.topright[1], "dark gray", "Initiative", True)
        self.initiative_counter = InputBox(width_counter, height, self.initiative_box.rect.topright[0] + spacer,
                                           self.initiative_box.rect.topright[1], "dark gray", str(initiative))
        self.fatigue_box = Box(width_box, height, self.initiative_counter.rect.topright[0] + spacer,
                               self.initiative_counter.rect.topright[1], "dark gray", "Fatigue", True)
        self.fatigue_counter = InputBox(width_counter, height, self.fatigue_box.rect.topright[0] + spacer,
                                        self.fatigue_box.rect.topright[1], "dark gray", str(fatigue))

        self.status_list = []
        box_names = ("Hunger", "Thirst", "Sleep")
        status_values = (hunger, thirst, sleep)
        for mod in range(3):
            pos_y = (self.name_box.rect.bottomleft[1] + spacer * 3) + ((spacer + height) * mod)

            box = Box(width_box, height, x + spacer, pos_y, "dark gray", box_names[mod], True)
            counter = [Button(30, height, (box.rect.topright[0] + spacer) + (30 + spacer) * i,
                              pos_y, "dark gray", "red") for i in range(8)]
            status = Box(width_box * 2.5, height, counter[-1].rect.topright[0] + spacer, pos_y, "dark gray", "Status:")

            self.status_list.append((box, counter, status))

        for x in range(3):
            self.set_status(self.status_list[x], status_values[x])

        self.list = (self.name_box, self.initiative_box, self.initiative_counter,
                     self.fatigue_box, self.fatigue_counter)

        self.update_status()

    def draw(self, screen):
        self.border.draw(screen)
        for item in self.list:
            item.draw(screen)

        for status in self.status_list:
            status[0].draw(screen)
            for counter in status[1]:
                counter.draw(screen)
            status[2].draw(screen)

    def handle_event(self, event):
        self.initiative_counter.handle_event(event)
        self.fatigue_counter.handle_event(event)
        mouse_2 = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pressed()
            for status in self.status_list:
                for step in status[1]:
                    if step.check_mouse_collision():
                        if mouse[0]:
                            self.set_status(status, status[1].index(step) + 1)
                            self.update_status()
                        if mouse[2]:
                            self.set_status(status, status[1].index(step))
                            self.update_status()
                            mouse_2 = False
                if mouse_2 and mouse[2] and self.name_box.check_mouse_collision():
                    self.border.click = not self.border.click

    def add_one_to_all(self):
        for status in self.status_list:
            for step in status[1]:
                if not step.click:
                    self.set_status(status, status[1].index(step) + 1)
                    break
        self.update_status()

    def get_statuses(self):
        return_list = [self.name]
        for status in self.status_list:
            return_list.append(str(len([x for x in status[1] if check_click(x)])))
        return_list.append(self.initiative_counter.text)
        return_list.append(self.fatigue_counter.text)
        return return_list


    @staticmethod
    def set_status(status, index):
        for clear_step in status[1]:
            clear_step.click = False
        for clear_step in status[1][:index]:
            clear_step.click = True

    def update_status(self):
        info = (((2, "Full"), (4, "Peckish"), (8, "Hungry"), (10, "Staving [f]")),
                ((2, "Hydrated"), (4, "Thirsty"), (5, "Very thirsty"), (10, "Dehydrated [f]")),
                ((2, "Rested"), (4, "Tired"), (6, "Weary [f]"), (10, "Exhausted [f]")))
        for mod in range(3):
            steps = len([x for x in self.status_list[mod][1] if check_click(x)])
            for effect in info[mod]:
                if steps < effect[0]:
                    self.status_list[mod][2].set_text("Status: " + effect[1])
                    break


def check_click(button):
    return button.click
