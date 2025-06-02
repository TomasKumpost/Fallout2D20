import pygame


class Box:
    def __init__(self, width, height, x, y, color, text="", center_text=False, text_size=30):
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.FONT = pygame.font.Font("Data/Fonts/Overseer.otf", text_size)
        self.txt_surface = self.FONT.render(text, True, "black")
        self.center_text = center_text
        if self.center_text:
            self.text_rect = self.txt_surface.get_rect().move(self.rect.center[0] -
                                                              self.txt_surface.get_rect().width / 2,
                                                              self.rect.center[1] -
                                                              self.txt_surface.get_rect().height / 2)
        else:
            self.text_rect = self.txt_surface.get_rect().move(self.rect.x + 5, self.rect.centery -
                                                              self.txt_surface.get_rect().height / 2)

    def draw(self, screen, dest=None):
        if dest:
            pygame.draw.rect(screen, self.color, self.rect.move(dest[0], dest[1]))
            screen.blit(self.txt_surface, self.text_rect.move(dest[0], dest[1]))
        else:
            pygame.draw.rect(screen, self.color, self.rect)
            screen.blit(self.txt_surface, self.text_rect)

    def update_pos(self, x=0, y=0):
        self.rect.move_ip(x, y)
        self.text_rect.move_ip(x, y)

    def set_pos(self, x, y):
        self.rect.update(x, y, self.rect.w, self.rect.h)
        self.update_text_rect()

    def set_text(self, text):
        self.txt_surface = self.FONT.render(text, True, "black")
        self.update_text_rect()
        self.text = text

    def update_text_rect(self):
        if self.center_text:
            self.text_rect = self.txt_surface.get_rect().move(self.rect.center[0] -
                                                              self.txt_surface.get_rect().width / 2,
                                                              self.rect.center[1] -
                                                              self.txt_surface.get_rect().height / 2)
        else:
            self.text_rect = self.txt_surface.get_rect().move(self.rect.x + 5, self.rect.centery -
                                                              self.txt_surface.get_rect().height / 2)

    def check_mouse_collision(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def update(self):
        pass

    def handle_event(self, event):
        pass

    def update_click(self):
        pass
