import appdaemon.plugins.hass.hassapi as hass
from balkonsolar.core.determine_balkonsolar_state import determine_balkonsolar_state
from balkonsolar.database_shenanigans.energy_db import EnergyDB

class BalkonsolarStateRunner(hass.Hass):
    def initialize(self):
        self.energy_db = EnergyDB()
        self.run_every(self.run_algorithm_and_store, self.datetime(), 300)  # every 5 minutes

    def run_algorithm_and_store(self, kwargs):
        result = determine_balkonsolar_state()
        timestamp = self.datetime().strftime("%Y-%m-%d %H:%M:%S")
        self.energy_db.store_algorithm_output(result, timestamp)
        self.log(f"Algorithm output {result} stored at {timestamp}")
