from Box import Box


class Clock:
    def __init__(self, x, y, screen, days, hours):
        self.screen = screen

        self.days = days
        self.hours = hours

        self.minus_one = Box(80, 80, x, y, "light gray", "-1", True)

        self.days_box = Box(120, 80, x + 85, y, "light gray", "Days: " + str(days), True)
        self.hours_box = Box(120, 80, x + 210, y, "light gray", "Hours: " + str(hours), True)

        self.plus_one = Box(80, 80, x + 335, y, "light gray", "+1", True)
        self.plus_four = Box(80, 80, x + 420, y, "light gray", "+4", True)

    def draw(self):
        self.minus_one.draw(self.screen)
        self.days_box.draw(self.screen)
        self.hours_box.draw(self.screen)
        self.plus_one.draw(self.screen)
        self.plus_four.draw(self.screen)

    def handle_event(self):
        if self.minus_one.check_mouse_collision():
            self.change_time(-1)
        elif self.plus_one.check_mouse_collision():
            self.change_time(1)
        elif self.plus_four.check_mouse_collision():
            self.change_time(4)

    def change_time(self, value):
        if value > 0:
            if self.hours + value > 23:
                self.hours = (self.hours + value) % 24
                self.days += 1
            else:
                self.hours += value
        else:
            if self.hours + value < 0:
                self.hours = (self.hours + value) + 24
                self.days -= 1
            else:
                self.hours += value

        self.hours_box.set_text("Hours: " + str(self.hours))
        self.days_box.set_text("Days: " + str(self.days))
