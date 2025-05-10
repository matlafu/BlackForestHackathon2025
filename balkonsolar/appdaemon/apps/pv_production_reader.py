import appdaemon.plugins.hass.hassapi as hass

class PVProductionReader(hass.Hass):
    def initialize(self):
        self.sensor = "sensor.8cbfea97f1ec_power"
        value = self.get_state(self.sensor)
        try:
            self.latest_value = float(value)
        except (TypeError, ValueError):
            self.latest_value = 0.0
            self.log(f"Initial value for {self.sensor} is unavailable, setting to 0.0 W")
        self.listen_state(self.state_changed, self.sensor)
        self.run_every(self.log_current_value, self.datetime(), 60)

    def state_changed(self, entity, attribute, old, new, kwargs):
        try:
            self.latest_value = float(new)
        except (TypeError, ValueError):
            self.latest_value = 0.0
            self.log(f"New value for {entity} is unavailable, setting to 0.0 W")
        self.log(f"{entity} changed from {old} W to {new} W")

    def log_current_value(self, kwargs):
        self.log(f"Current value of {self.sensor}: {self.latest_value} W")

    def get_latest_value(self):
        return self.latest_value
