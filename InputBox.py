import pygame
from Box import Box
from Timer import Timer


class InputBox(Box):

    def __init__(self, width, height, x, y, color, text="", text_size=30, center_text=False):
        super().__init__(width, height, x, y, color, text, text_size=text_size, center_text=center_text)
        self.active = False
        self.active_line = False
        self.line = self.FONT.render("|", True, "black")
        self.timer = Timer(650, True, True, self.toggle_line)
        self.delete = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and pygame.mouse.get_pressed()[0]:
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False

        if self.active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.delete = True
                elif event.key == pygame.K_RETURN:
                    self.active = False
                else:
                    self.text += event.unicode
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    self.delete = False
            if self.delete:
                self.text = self.text[:-1]

            self.txt_surface = self.FONT.render(self.text, True, "black")
            self.update_text_rect()

    def draw(self, screen, dest=None):
        if dest:
            pygame.draw.rect(screen, self.color, self.rect.move(dest[0], dest[1]))
            screen.blit(self.txt_surface, (self.text_rect.x + 5 + dest[0], self.text_rect.y + 5 + dest[1]))
        else:
            pygame.draw.rect(screen, self.color, self.rect)
            screen.blit(self.txt_surface, (self.text_rect.x + 5, self.text_rect.y + 5))

        self.timer.update()
        if self.active_line and self.active:
            if dest:
                screen.blit(self.line, (self.text_rect.x + 5 + self.txt_surface.get_width() + dest[0],
                                        self.text_rect.y + 2 + dest[1]))
            else:
                screen.blit(self.line, (self.text_rect.x + 5 + self.txt_surface.get_width(), self.text_rect.y + 2))

    def toggle_line(self):
        self.active_line = not self.active_line
