import appdaemon.plugins.hass.hassapi as hass

class FakeBatteryActions(hass.Hass):
    def initialize(self):
        self.run_in(self.fake_activate_and_set_charge, 10)

    def fake_activate_and_set_charge(self, kwargs):
        battery_controller = self.get_app("fake_battery_controller")
        if battery_controller is not None:
            self.log("[FAKE] Activating battery and setting charge to 1.5 kWh")
            battery_controller.activate_battery()
            battery_controller.set_battery_charge(1.5)
        else:
            self.log("[FAKE] fake_battery_controller app not found!")

class FakeRGBBulbActions(hass.Hass):
    def initialize(self):
        # Red, Yellow, Green
        self.colors = [(255, 0, 0), (255, 255, 0), (0, 255, 0)]
        self.color_index = 0
        self.run_in(self.fake_bulb_sequence, 10)

    def fake_bulb_sequence(self, kwargs):
        bulb_app = self.get_app("rgb_bulb")
        if bulb_app is not None:
            # self.log("[FAKE] Turning on RGB bulb")
            bulb_app.turn_on()
            self.run_in(self.fake_set_color, 2)
        else:
            self.log("[FAKE] rgb_bulb app not found!")

    def fake_set_color(self, kwargs):
        bulb_app = self.get_app("rgb_bulb")
        if bulb_app is not None:
            color = self.colors[self.color_index]
            # self.log(f"[FAKE] Setting RGB bulb color to {color}")
            bulb_app.set_color(*color)
            self.color_index = (self.color_index + 1) % len(self.colors)
            self.run_in(self.fake_set_color, 10)  # Change color every 10 seconds
        else:
            self.log("[FAKE] rgb_bulb app not found!")
