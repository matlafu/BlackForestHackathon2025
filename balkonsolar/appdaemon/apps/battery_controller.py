import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="balkonsolar/.env")
import appdaemon.plugins.hass.hassapi as hass
from virtual_battery import VirtualBattery
from database_utils import DatabaseManager

class BatteryController(hass.Hass):
    """
    AppDaemon app that manages a virtual battery, simulates charging/discharging based on energy flows,
    and logs battery, solar, and grid data to the database. Supports activation, deactivation, and manual charge setting.
    """
    def initialize(self):
        """
        Called once when the app is initialized by AppDaemon.
        Sets up the PV and consumption apps, initializes the virtual battery and database, and schedules periodic management.
        """
        self.log("BatteryController initialized! App name: battery_controller")
        self.pv_app = self.get_app("pv_production_reader")
        self.consumption_app = self.get_app("household_consumption_reader")
        self.battery = VirtualBattery(capacity_kwh=2.560, initial_charge_kwh=0.0)

        # Initialize database with path from config or environment
        db_path = self.args.get("db_path") or os.getenv("DB_PATH")  # None will use the default path in DatabaseManager
        self.db_manager = DatabaseManager(db_path)
        self.log(f"Database initialized at {self.db_manager.db_path}")

        self.active = False
        self.current_action = "off"
        self.current_power = 0.0
        self.run_every(self.manage_battery, self.datetime(), 60)

    def manage_battery(self, kwargs):
        """
        Simulates battery charging/discharging based on PV production and grid consumption.
        Logs battery state and energy data to the database every minute.
        """
        pv_power = float(self.pv_app.get_latest_value())
        grid_power = float(self.consumption_app.get_latest_value())
        interval_hours = 1/60  # 1 minute interval
        state = self.battery.get_state()
        if not self.active:
            self.current_action = "off"
            self.current_power = 0.0
            # Log battery state even when off
            self.log(
                f"Battery state: OFF, charge: {state['current_charge_kwh']:.2f}/{state['capacity_kwh']} kWh ({state['percent_full']:.1f}%)"
            )
            return
        if grid_power < 0:
            surplus_energy = abs(grid_power) * interval_hours / 1000  # in kWh
            self.battery.charge(surplus_energy)
            self.current_action = "charging"
            self.current_power = abs(grid_power)
            self.log(f"Battery charged with {surplus_energy:.4f} kWh surplus.")
        elif grid_power > 0:
            deficit_energy = grid_power * interval_hours / 1000  # in kWh
            discharged = self.battery.discharge(deficit_energy)
            self.current_action = "discharging" if discharged > 0 else "idle"
            self.current_power = grid_power if discharged > 0 else 0.0
            self.log(f"Battery discharged by {discharged:.4f} kWh to cover deficit.")
        else:
            self.current_action = "idle"
            self.current_power = 0.0
        state = self.battery.get_state()
        # Auto turn-off if fully charged or discharged
        if state['current_charge_kwh'] >= state['capacity_kwh']:
            self.active = False
            self.log("Battery fully charged, turning off.")
        elif state['current_charge_kwh'] <= 0:
            self.active = False
            self.log("Battery fully discharged, turning off.")
        # Log the current charge to the database
        self.set_battery_charge(int(state['current_charge_kwh']))
        self.log(self._status_log(state))

        # Log solar, battery, and grid data to the database
        timestamp = self.datetime().strftime("%Y-%m-%d %H:%M:%S")
        self.db_manager.store_battery_status(self.battery.current_charge, timestamp)
        self.db_manager.store_solar_output(pv_power, timestamp)
        self.db_manager.store_grid_usage(grid_power, timestamp)
        self.log(f"Logged energy data to database at {timestamp}")

    def activate_battery(self):
        """
        Activates the virtual battery for simulation.
        """
        self.active = True
        self.log("Battery ACTIVATED.")

    def deactivate_battery(self):
        """
        Deactivates the virtual battery for simulation.
        """
        self.active = False
        self.log("Battery DEACTIVATED.")

    def get_battery_status(self):
        """
        Returns the current status of the virtual battery, including charge, capacity, percent full, and power.
        """
        state = self.battery.get_state()
        return {
            "active": self.active,
            "action": self.current_action,
            "current_charge_kwh": state["current_charge_kwh"],
            "capacity_kwh": state["capacity_kwh"],
            "percent_full": state["percent_full"],
            "current_power_w": self.current_power,
            "time_estimate_h": self._estimate_time(state)
        }

    def _estimate_time(self, state):
        """
        Estimates the time to full or empty based on current action and power.
        """
        if self.current_action == "charging" and self.current_power > 0:
            remaining_kwh = state["capacity_kwh"] - state["current_charge_kwh"]
            return remaining_kwh / (self.current_power / 1000)
        elif self.current_action == "discharging" and self.current_power > 0:
            return state["current_charge_kwh"] / (self.current_power / 1000)
        else:
            return None

    def _status_log(self, state):
        """
        Returns a formatted string summarizing the battery state for logging.
        """
        time_est = self._estimate_time(state)
        time_str = f", est. time to full/empty: {time_est:.2f} h" if time_est is not None else ""
        return (
            f"Battery state: {'ON' if self.active else 'OFF'}, "
            f"action: {self.current_action}, "
            f"charge: {state['current_charge_kwh']:.2f}/{state['capacity_kwh']} kWh ({state['percent_full']:.1f}%), "
            f"power: {self.current_power:.1f} W"
            f"{time_str}"
        )

    def set_battery_charge(self, kwh):
        """
        Sets the battery charge to a specific value in kWh and logs the change to the database.
        """
        # Get current state to access capacity
        state = self.battery.get_state()
        # Calculate new charge value (clamped between 0 and capacity)
        new_charge = max(0, min(state['capacity_kwh'], kwh))
        # Access the VirtualBattery internal attribute
        self.battery.current_charge = new_charge
        self.log(f"Battery charge manually set to {new_charge:.2f} kWh")

        # Log the manual change to the database
        timestamp = self.datetime().strftime("%Y-%m-%d %H:%M:%S")
        self.log(f"Logging battery charge {new_charge} kWh to database at {timestamp}")
        self.db_manager.store_battery_status(new_charge, timestamp)
