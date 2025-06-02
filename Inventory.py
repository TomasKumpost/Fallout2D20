from xml.etree import ElementTree

from Box import Box
from InputBox import InputBox
from ScrollPanel import ScrollPanelItem
from ItemFinderInventory import start


class Inventory:
    def __init__(self, screen):
        self.screen = screen
        self.gear_header = Box(700, 40, 10, 10, "#00ff00", "Gear", True)
        self.gear = ScrollPanelItem(700, 830, 10, 50, "#e6ffe6", self.find_gear)
        self.ammo_header = Box(700, 40, 720, 10, "#ffa31a", "Ammo", True)
        self.ammo = ScrollPanelItem(700, 400, 720, 50, "#ffebcc", self.find_ammo)

        self.encumbrance_header = Box(350, 40, self.ammo.rect.x, self.ammo.rect.bottomleft[1] + 10,
                                      "#80e5ff", "Encumbrance", True)
        self.max_carry = Box(300, 40, self.ammo.rect.x, self.encumbrance_header.rect.bottomleft[1],
                             "#b3f0ff", "Max Carry Weight", True)
        self.max_carry_value = Box(50, 40, self.ammo.rect.x + 300, self.max_carry.rect.y,
                                   "#e6faff", "0", True)
        self.current_carry = Box(300, 40, self.ammo.rect.x, self.max_carry.rect.bottomleft[1],
                                 "#b3f0ff", "Current Carry Weight", True)
        self.current_carry_value = Box(50, 40, self.max_carry.rect.x + 300, self.current_carry.rect.y,
                                       "#e6faff", "0", True)
        self.free_carry = Box(300, 40, self.ammo.rect.x, self.current_carry.rect.bottomleft[1],
                              "#b3f0ff", "Free Carry Weight", True)
        self.free_carry_value = Box(50, 40, self.free_carry.rect.x + 300, self.free_carry.rect.y,
                                    "#e6faff", "0", True)

        self.caps_header = Box(350, 40, self.encumbrance_header.rect.topright[0] + 10, self.encumbrance_header.rect.y,
                               "#fff266", "Caps", True)
        self.caps_value = InputBox(350, 40, self.caps_header.rect.x, self.caps_header.rect.bottomleft[1],
                                   "#fff9b3", "0", center_text=True)

        self.parse_items()

        self.current_carry_value.set_text(str(int(sum(self.gear.get_total_weight()) +
                                                  sum(self.ammo.get_total_weight()))))
        self.free_carry_value.set_text(str(int(self.max_carry_value.text) - int(self.current_carry_value.text)))
        self.draw_list = [self.gear_header, self.gear, self.ammo_header, self.ammo, self.encumbrance_header,
                          self.max_carry, self.max_carry_value, self.current_carry, self.current_carry_value,
                          self.free_carry, self.free_carry_value, self.caps_header, self.caps_value]

    def draw(self):
        self.current_carry_value.set_text(str(int(sum(self.gear.get_total_weight()) +
                                                  sum(self.ammo.get_total_weight()))))
        self.free_carry_value.set_text(str(int(self.max_carry_value.text) - int(self.current_carry_value.text)))

        for box in self.draw_list:
            box.draw(self.screen)

    def handle_event(self, event):
        self.gear.handle_event(event)
        self.ammo.handle_event(event)
        self.caps_value.handle_event(event)

    def find_gear(self):
        items = start(self.screen)
        for name, weight in items:
            self.gear.add_item(name, weight)

    def find_ammo(self):
        items = start(self.screen)
        for name, weight in items:
            self.ammo.add_item(name, weight)

    def parse_items(self):
        tree = ElementTree.parse("Data/inventory.xml")
        inv = tree.getroot()

        for gear in inv[0]:
            self.gear.add_item(gear.attrib.get("name"), float(gear.attrib.get("weight")), int(gear.text))

        for ammo in inv[1]:
            self.ammo.add_item(ammo.attrib.get("name"), float(ammo.attrib.get("weight")), int(ammo.text))

        self.max_carry_value.set_text(inv[2].text)
        self.caps_value.set_text(inv[3].text)

    def save_data(self):
        tree = ElementTree.parse("Data/inventory.xml")
        inv = tree.getroot()

        for child in inv[0].findall("item"):
            inv[0].remove(child)

        for item in self.gear.save_date():
            el = ElementTree.Element("item", {"name": item[0], "weight": str(item[1])})
            el.text = str(item[2])
            inv[0].append(el)

        for child in inv[1].findall("item"):
            inv[1].remove(child)

        for item in self.ammo.save_date():
            el = ElementTree.Element("item", {"name": item[0], "weight": str(item[1])})
            el.text = str(item[2])
            inv[1].append(el)

        if self.caps_value.text != "":
            inv[3].text = self.caps_value.text
        else:
            inv[3].text = "0"

        tree.write("Data/inventory.xml")
