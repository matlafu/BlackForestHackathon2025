import hassapi as hass

class ReadShellyEnergy(hass.Hass):
    def initialize(self):
        entity_id = "sensor.shellypro3em63_fce8c0dad39c_total_active_energy"
        value = self.get_state(entity_id)
        self.log(f"Current value of {entity_id}: {value} kWh")
        self.listen_state(self.state_changed, entity_id)

    def state_changed(self, entity, attribute, old, new, kwargs):
        self.log(f"{entity} changed from {old} kWh to {new} kWh")
