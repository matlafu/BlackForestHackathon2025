import hassapi as hass
import requests

class PostToDashboard(hass.Hass):
    def initialize(self):
        self.entity_id = "sensor.shellypro3em63_fce8c0dad39c_total_active_energy"
        self.dashboard_url = "http://localhost:5000/api/update"  # Change to your dashboard API endpoint
        self.listen_state(self.state_changed, self.entity_id)

    def state_changed(self, entity, attribute, old, new, kwargs):
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
