import hassapi as hass
import random
from datetime import timedelta

class RGBBulb(hass.Hass):
    """
    AppDaemon app that controls an RGB smart bulb.
    Periodically changes the bulb's color to a random value and provides methods to turn on, turn off, and set color.
    """
    def initialize(self):
        """
        Called once when the app is initialized by AppDaemon.
        Sets up the entity ID and schedules periodic color changes.
        """
        self.entity_id = "light.shellycolorbulb_409151581099"
        self.run_every(self.change_color, self.datetime() + timedelta(seconds=1), 10)

    def change_color(self, kwargs):
        """
        Changes the bulb's color to a random RGB value every 10 seconds.
        """
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        self.set_color(r, g, b)

    def turn_on(self):
        """
        Turns on the RGB bulb.
        """
        self.call_service("light/turn_on", entity_id=self.entity_id)
        self.log(f"Turned ON {self.entity_id}")

    def turn_off(self):
        """
        Turns off the RGB bulb.
        """
        self.call_service("light/turn_off", entity_id=self.entity_id)
        self.log(f"Turned OFF {self.entity_id}")

    def set_color(self, r, g, b):
        """
        Sets the RGB bulb to the specified color.
        Args:
            r: Red value (0-255)
            g: Green value (0-255)
            b: Blue value (0-255)
        """
        self.call_service("light/turn_on", entity_id=self.entity_id, rgb_color=[r, g, b])
        self.log(f"Set {self.entity_id} color to RGB ({r}, {g}, {b})")

    def get_state(self):
        """
        Returns the current state of the RGB bulb.
        """
        state = self.get_state(self.entity_id)
        self.log(f"State of {self.entity_id}: {state}")
        return state
