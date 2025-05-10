import hassapi as hass
import random
from datetime import timedelta

class RGBBulb(hass.Hass):
    def initialize(self):
        self.entity_id = "light.shellycolorbulb_409151581099"
        self.run_every(self.change_color, self.datetime() + timedelta(seconds=1), 10)

    def change_color(self, kwargs):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        self.set_color(r, g, b)

    def turn_on(self):
        self.call_service("light/turn_on", entity_id=self.entity_id)
        self.log(f"Turned ON {self.entity_id}")

    def turn_off(self):
        self.call_service("light/turn_off", entity_id=self.entity_id)
        self.log(f"Turned OFF {self.entity_id}")

    def set_color(self, r, g, b):
        self.call_service("light/turn_on", entity_id=self.entity_id, rgb_color=[r, g, b])
        self.log(f"Set {self.entity_id} color to RGB ({r}, {g}, {b})")

    def get_state(self):
        state = self.get_state(self.entity_id)
        self.log(f"State of {self.entity_id}: {state}")
        return state
