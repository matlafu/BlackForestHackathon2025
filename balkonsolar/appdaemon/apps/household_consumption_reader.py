import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="balkonsolar/.env")
import appdaemon.plugins.hass.hassapi as hass
from database_utils import DatabaseManager

class HouseholdConsumptionReader(hass.Hass):
    def initialize(self):
        self.entity_id = "sensor.shellypro3em63_fce8c0dad39c_total_active_power"
        # Initialize database with path from config or environment
        db_path = self.args.get("db_path") or os.getenv("DB_PATH")  # None will use the default path in DatabaseManager
        self.db_manager = DatabaseManager(db_path)
        self.log(f"Database initialized at {self.db_manager.db_path}")

        value = self.get_state(self.entity_id)
        try:
            self.latest_value = float(value)
        except (TypeError, ValueError):
            self.latest_value = 0.0
            self.log(f"Initial value for {self.entity_id} is unavailable, setting to 0.0 W")
        self.log(f"Current value of {self.entity_id}: {self.latest_value} W")
        self.listen_state(self.state_changed, self.entity_id)
        self.run_every(self.log_consumption_power, self.datetime(), 60)

    def state_changed(self, entity, attribute, old, new, kwargs):
        try:
            self.latest_value = float(new)
        except (TypeError, ValueError):
            self.latest_value = 0.0
            self.log(f"New value for {entity} is unavailable, setting to 0.0 W")
        self.log(f"{entity} changed from {old} W to {new} W")

    def log_consumption_power(self, kwargs):
        consumption_power = self.latest_value
        timestamp = self.datetime().strftime("%Y-%m-%d %H:%M:%S")
        self.db_manager.store_grid_usage(consumption_power, timestamp)
        self.log(f"Logged household consumption {consumption_power} W to database at {timestamp}")

    def get_latest_value(self):
        return self.latest_value
