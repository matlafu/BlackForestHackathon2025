import hassapi as hass

class HouseholdConsumptionReader(hass.Hass):
    def initialize(self):
        self.entity_id = "sensor.shellypro3em63_fce8c0dad39c_total_active_power"
        value = self.get_state(self.entity_id)
        try:
            self.latest_value = float(value)
        except (TypeError, ValueError):
            self.latest_value = 0.0
            self.log(f"Initial value for {self.entity_id} is unavailable, setting to 0.0 W")
        self.log(f"Current value of {self.entity_id}: {self.latest_value} W")
        self.listen_state(self.state_changed, self.entity_id)
        self.run_every(self.log_current_value, self.datetime(), 60)

    def state_changed(self, entity, attribute, old, new, kwargs):
        try:
            self.latest_value = float(new)
        except (TypeError, ValueError):
            self.latest_value = 0.0
            self.log(f"New value for {entity} is unavailable, setting to 0.0 W")
        self.log(f"{entity} changed from {old} W to {new} W")

    def log_current_value(self, kwargs):
        self.log(f"Current value of {self.entity_id}: {self.latest_value} W")

    def get_latest_value(self):
        return self.latest_value
