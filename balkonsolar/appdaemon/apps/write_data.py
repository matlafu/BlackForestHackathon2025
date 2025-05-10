import hassapi as hass
import random
from datetime import timedelta

class RandomBulbColor(hass.Hass):
    def initialize(self):
        self.entity_id = "light.shellycolorbulb_409151581099"
        self.run_every(self.change_color, self.datetime() + timedelta(seconds=1), 10)

    def change_color(self, kwargs):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        # self.log(f"Setting {self.entity_id} to RGB ({r}, {g}, {b})")
        # if we activate this, the bulb will change color every 10 seconds
        # self.call_service("light/turn_on", entity_id=self.entity_id, rgb_color=[r, g, b])
