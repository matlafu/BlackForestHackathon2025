import appdaemon.plugins.hass.hassapi as hass
from database_utils import DatabaseManager

class PVProductionReader(hass.Hass):
    """
    AppDaemon app that reads PV (solar) production from a sensor,
    logs the value every minute, and stores it in the database for later analysis.
    """
    def initialize(self):
        """
        Called once when the app is initialized by AppDaemon.
        Sets up the sensor entity, initializes the database connection, and schedules periodic logging.
        """
        self.sensor = "sensor.8cbfea97f1ec_power"
        # Initialize database with path from config
        db_path = self.args.get("db_path", None)  # None will use the default path in DatabaseManager
        self.db_manager = DatabaseManager(db_path)
        self.log(f"Database initialized at {self.db_manager.db_path}")
        value = self.get_state(self.sensor)
        try:
            self.latest_value = float(value)
        except (TypeError, ValueError):
            self.latest_value = 0.0
            self.log(f"Initial value for {self.sensor} is unavailable, setting to 0.0 W")
        # Listen for state changes and log every minute
        self.listen_state(self.state_changed, self.sensor)
        self.run_every(self.log_pv_power, self.datetime(), 60)

    def log_pv_power(self, kwargs):
        """
        Periodically logs the current PV production value to the database with a timestamp.
        """
        pv_power = float(self.get_state(self.sensor))
        timestamp = self.datetime().strftime("%Y-%m-%d %H:%M:%S")
        self.db_manager.store_solar_output(pv_power, timestamp)
        self.log(f"Logged PV power {pv_power} W to database at {timestamp}")

    def state_changed(self, entity, attribute, old, new, kwargs):
        """
        Callback for when the sensor state changes. Updates the latest value and logs the change.
        """
        try:
            self.latest_value = float(new)
        except (TypeError, ValueError):
            self.latest_value = 0.0
            self.log(f"New value for {entity} is unavailable, setting to 0.0 W")
        self.log(f"{entity} changed from {old} W to {new} W")

    def get_latest_value(self):
        """
        Returns the most recent PV production value.
        """
        return self.latest_value
