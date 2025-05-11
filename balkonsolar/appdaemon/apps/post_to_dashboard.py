import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="balkonsolar/.env")
import hassapi as hass
import requests

class PostToDashboard(hass.Hass):
    """
    AppDaemon app that listens for changes to a specific sensor and posts the data
    to a dashboard API endpoint for real-time monitoring or visualization.
    """
    def initialize(self):
        """
        Called once when the app is initialized by AppDaemon.
        Sets up the sensor entity and dashboard URL, and starts listening for state changes.
        """
        self.entity_id = "sensor.shellypro3em63_fce8c0dad39c_total_active_energy"
        self.dashboard_url = os.getenv("DASHBOARD_URL", "http://localhost:5000/api/update")  # Use env var if set
        self.listen_state(self.state_changed, self.entity_id)

    def state_changed(self, entity, attribute, old, new, kwargs):
        """
        Callback for when the sensor state changes.
        Posts the new data to the dashboard API endpoint and logs the result.
        """
        data = {
            "entity_id": entity,
            "old_value": old,
            "new_value": new,
            "timestamp": self.datetime().isoformat()
        }
        try:
            response = requests.post(self.dashboard_url, json=data)
            self.log(f"Posted to dashboard: {data} (status: {response.status_code})")
        except Exception as e:
            self.log(f"Error posting to dashboard: {e}", level="ERROR")
