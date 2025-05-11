class VirtualBattery:
    """
    Singleton class that simulates the behavior of a physical battery for use in energy management applications.
    Provides methods for charging, discharging, and querying the battery state.
    """
    _instance = None

    def __new__(cls, **kwargs):
        if cls._instance is None:
            cls._instance = super(VirtualBattery, cls).__new__(cls)
        return cls._instance

    def __init__(self, capacity_kwh=2.560, initial_charge_kwh=0.0, charge_efficiency=0.95, discharge_efficiency=0.95):
        """
        Initialize the virtual battery with given parameters.
        Args:
            capacity_kwh: Total capacity of the battery in kWh.
            initial_charge_kwh: Initial charge in kWh.
            charge_efficiency: Efficiency factor for charging (0 < efficiency ≤ 1).
            discharge_efficiency: Efficiency factor for discharging (0 < efficiency ≤ 1).
        """
        # Only initialize once
        if not hasattr(self, "_initialized"):
            self.capacity = capacity_kwh  # in kWh
            self.current_charge = initial_charge_kwh  # in kWh
            self.charge_efficiency = charge_efficiency
            self.discharge_efficiency = discharge_efficiency
            self.discharge_enabled = False
            self._initialized = True

    def charge(self, amount_kwh):
        """
        Charge the battery by the specified amount (in kWh), considering charge efficiency and not exceeding capacity.
        """
        effective_amount = amount_kwh * self.charge_efficiency
        self.current_charge = min(self.capacity, self.current_charge + effective_amount)

    def discharge(self, amount_kwh):
        """
        Discharge the battery by the specified amount (in kWh), considering discharge efficiency and not going below zero.
        Returns the actual discharged energy.
        """
        if not self.discharge_enabled:
            return 0.0
        # Only allow down to 0
        effective_amount = amount_kwh / self.discharge_efficiency
        discharged = min(self.current_charge, effective_amount)
        self.current_charge -= discharged
        return discharged * self.discharge_efficiency

    def get_state(self):
        """
        Returns a dictionary with the current charge, capacity, and percent full.
        """
        return {
            "current_charge_kwh": self.current_charge,
            "capacity_kwh": self.capacity,
            "percent_full": 100 * self.current_charge / self.capacity
        }

    def set_discharge_enabled(self, enabled: bool):
        """
        Enables or disables the ability to discharge the battery.
        Args:
            enabled: True to allow discharging, False to disable.
        """
        self.discharge_enabled = enabled
