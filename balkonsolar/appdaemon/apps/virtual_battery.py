class VirtualBattery:
    def __init__(self, capacity_kwh=2.560, initial_charge_kwh=0.0, charge_efficiency=0.95, discharge_efficiency=0.95):
        self.capacity = capacity_kwh  # in kWh
        self.current_charge = initial_charge_kwh  # in kWh
        self.charge_efficiency = charge_efficiency
        self.discharge_efficiency = discharge_efficiency
        self.discharge_enabled = False

    def charge(self, amount_kwh):
        # Only allow up to capacity
        effective_amount = amount_kwh * self.charge_efficiency
        self.current_charge = min(self.capacity, self.current_charge + effective_amount)

    def discharge(self, amount_kwh):
        if not self.discharge_enabled:
            return 0.0
        # Only allow down to 0
        effective_amount = amount_kwh / self.discharge_efficiency
        discharged = min(self.current_charge, effective_amount)
        self.current_charge -= discharged
        return discharged * self.discharge_efficiency

    def get_state(self):
        return {
            "current_charge_kwh": self.current_charge,
            "capacity_kwh": self.capacity,
            "percent_full": 100 * self.current_charge / self.capacity
        }

    def set_discharge_enabled(self, enabled: bool):
        self.discharge_enabled = enabled
