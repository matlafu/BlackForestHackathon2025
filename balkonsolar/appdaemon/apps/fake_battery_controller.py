import appdaemon.plugins.hass.hassapi as hass

class FakeBatteryController(hass.Hass):
    def initialize(self):
        self.log("FakeBatteryController initialized! App name: fake_battery_controller")
        # Wait 30 seconds, then activate the fake battery controller
        self.run_in(self.activate_battery_controller, 15)

    def activate_battery_controller(self, kwargs):
        battery_controller = self.get_app("battery_controller")
        if battery_controller is None:
            self.log("battery_controller app not found!")
        else:
            self.log("[PLACEHOLDER] Activating battery (simulated external trigger)")
            battery_controller.activate_battery()
            battery_controller.set_battery_charge(1.5)  # Set to 1.5 kWh, for example
