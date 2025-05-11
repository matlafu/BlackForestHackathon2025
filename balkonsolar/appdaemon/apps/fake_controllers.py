import appdaemon.plugins.hass.hassapi as hass

class FakeBatteryActions(hass.Hass):
    """
    AppDaemon app for simulating battery actions for testing purposes.
    Activates the battery and sets its charge to 1.5 kWh if not set.
    """
    def initialize(self):
        """
        Called once when the app is initialized by AppDaemon.
        Schedules the fake battery activation and charge setting after 10 seconds.
        """
        self.run_in(self.fake_activate_and_set_charge, 10)

    def fake_activate_and_set_charge(self, kwargs):
        """
        Activates the battery and sets its charge to 1.5 kWh if the current charge is not set.
        """
        battery_controller = self.get_app("battery_controller")
        if battery_controller is not None:
            self.log("[FAKE] Activating battery")
            battery_controller.activate_battery()
            current_charge = battery_controller.get_battery_status().get("current_charge_kwh")
            if current_charge is None:
                # if no current charge is available, set it to 1.5 kWh for proper testing
                battery_controller.set_battery_charge(1.5)
        else:
            self.log("[FAKE] battery_controller app not found!")

class FakeRGBBulbActions(hass.Hass):
    """
    AppDaemon app for simulating RGB bulb actions for testing purposes.
    Cycles through red, yellow, and green colors.
    """
    def initialize(self):
        """
        Called once when the app is initialized by AppDaemon.
        Initializes the color sequence and index.
        """
        # Red, Yellow, Green
        self.colors = [(255, 0, 0), (255, 255, 0), (0, 255, 0)]
        self.color_index = 0
        # self.run_in(self.fake_bulb_sequence, 10)

    def fake_bulb_sequence(self, kwargs):
        """
        Turns on the RGB bulb and starts the color cycling sequence.
        """
        bulb_app = self.get_app("rgb_bulb")
        if bulb_app is not None:
            # self.log("[FAKE] Turning on RGB bulb")
            bulb_app.turn_on()
            self.run_in(self.fake_set_color, 2)
        else:
            self.log("[FAKE] rgb_bulb app not found!")

    def fake_set_color(self, kwargs):
        """
        Sets the RGB bulb to the next color in the sequence and schedules the next change.
        """
        bulb_app = self.get_app("rgb_bulb")
        if bulb_app is not None:
            color = self.colors[self.color_index]
            # self.log(f"[FAKE] Setting RGB bulb color to {color}")
            bulb_app.set_color(*color)
            self.color_index = (self.color_index + 1) % len(self.colors)
            self.run_in(self.fake_set_color, 10)  # Change color every 10 seconds
        else:
            self.log("[FAKE] rgb_bulb app not found!")
