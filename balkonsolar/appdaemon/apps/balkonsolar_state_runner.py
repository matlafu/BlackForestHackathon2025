import appdaemon.plugins.hass.hassapi as hass
from balkonsolar.core.determine_balkonsolar_state import determine_balkonsolar_state
from balkonsolar.database_shenanigans.energy_db import EnergyDB

class BalkonsolarStateRunner(hass.Hass):
    """
    AppDaemon app that periodically runs the Balkonsolar state determination algorithm
    and stores the result in the energy database. This can be used for logging, monitoring,
    or triggering further automations based on the calculated state.
    """
    def initialize(self):
        """
        Called once when the app is initialized by AppDaemon.
        Sets up the database connection and schedules the algorithm to run every 15 minutes.
        """
        self.energy_db = EnergyDB()
        # Schedule the algorithm to run every 900 seconds (15 minutes)
        self.run_every(self.run_algorithm_and_store, self.datetime(), 900)

    def run_algorithm_and_store(self, kwargs):
        """
        Runs the Balkonsolar state determination algorithm, stores the result in the database,
        and logs the output with a timestamp.
        """
        result = determine_balkonsolar_state()
        timestamp = self.datetime().strftime("%Y-%m-%d %H:%M:%S")
        self.energy_db.store_algorithm_output(result, timestamp)
        self.log(f"Algorithm output {result} stored at {timestamp}")
