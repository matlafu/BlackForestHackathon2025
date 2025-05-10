# Technical Context

## Technology Stack
### Backend
- **Language**: Python 3.11+
  - FastAPI for API development
  - Pydantic for data validation
  - SQLAlchemy for database ORM
  - APScheduler for task scheduling
  - Pandas for data analysis

### Frontend
- **Framework**: React with TypeScript
  - Material-UI for component library
  - Redux for state management
  - Chart.js for data visualization
  - React Query for API data fetching

### Data Storage
- **Time Series**: InfluxDB
- **Relational**: PostgreSQL
- **Cache**: Redis

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **API Gateway**: Nginx
- **Message Broker**: RabbitMQ

### Development Tools
- **Version Control**: Git
- **CI/CD**: GitHub Actions
- **Testing**: pytest, Jest
- **Documentation**: Sphinx, Storybook
- **Code Quality**: Black, ESLint, Prettier

## Development Setup
1. **Prerequisites**
   - Python 3.11+
   - Node.js 18+
   - Docker and Docker Compose
   - Git

2. **Local Development**
   - Clone repository
   - Set up virtual environment
   - Install dependencies
   - Configure environment variables
   - Run development servers

3. **Testing Environment**
   - Unit tests
   - Integration tests
   - End-to-end tests
   - Performance tests

4. **Local Development Setup for AppDaemon**
   - **Prerequisites:**
     - Python 3.11+
     - Docker and Docker Compose (optional, for local testing)
     - Home Assistant instance running on a Raspberry Pi (in a separate network, connected to the internet)
     - Home Assistant Cloud (Nabu Casa) subscription for secure remote access
     - AppDaemon installed (can be in a virtual environment or container)
   - **Setup Notes:**
     - Home Assistant is not running locally, but on a Raspberry Pi in a different network. Communication is established via Home Assistant Cloud (Nabu Casa), which provides secure remote access.
   - **Steps:**
     1. Ensure your Home Assistant instance is running on the Raspberry Pi and is connected to Home Assistant Cloud (Nabu Casa).
     2. Obtain your Home Assistant Cloud remote URL from the Home Assistant UI (Settings > Home Assistant Cloud > Remote Control).
     3. Install AppDaemon: `pip install appdaemon` (or use Docker)
     4. Configure AppDaemon to connect to Home Assistant Cloud by editing `appdaemon.yaml`:
        ```yaml
        appdaemon:
          latitude: YOUR_LAT
          longitude: YOUR_LONG
          elevation: YOUR_ELEVATION
          time_zone: YOUR_TIMEZONE
        hass:
          url: "https://<your-nabu-casa-remote-url>"
          token: "YOUR_LONG_LIVED_ACCESS_TOKEN"
        ```
        - Use the Nabu Casa remote URL (e.g., `https://<random-string>.ui.nabu.casa`) as the Home Assistant URL.
        - The long-lived access token must be generated in Home Assistant (Profile > Long-Lived Access Tokens).
     5. Run AppDaemon: `appdaemon -c /path/to/your/appdaemon/config`
     6. Develop and test your automation apps in the `apps/` directory. Changes are picked up automatically.
   - **References:**
     - [AppDaemon Docs](https://appdaemon.readthedocs.io/en/latest/)
     - [Home Assistant Cloud (Nabu Casa)](https://www.nabucasa.com/)
     - [Home Assistant Docs](https://www.home-assistant.io/docs/)

## Dependencies
### Backend Dependencies
- fastapi==0.104.1
- uvicorn==0.24.0
- sqlalchemy==2.0.23
- pydantic==2.5.2
- pandas==2.1.3
- influxdb-client==1.36.1
- redis==5.0.1
- pika==1.3.2
- pytest==7.4.3

### Frontend Dependencies
- react==18.2.0
- typescript==5.3.3
- @mui/material==5.15.1
- @reduxjs/toolkit==2.0.1
- chart.js==4.4.1
- @tanstack/react-query==5.8.7

## Hardware Used
- Shelly smart meter (measures current household energy usage)
- Smart Wi-Fi LED light (status indicator, integrated with Home Assistant)
- Shelly plugs (control devices via Home Assistant)
- Solar Panels with Zendure SolarFlow 800 inverter
- Zendure battery storage

## Technical Constraints
- **Hardware Requirements**: Minimal resource usage for Raspberry Pi compatibility
- **Network**: Support for local network operation
- **Security**: Secure device communication and data storage
- **Scalability**: Support for multiple devices and users
- **Compatibility**: Support for various battery and inverter types
- **Performance**: Real-time data processing and decision making
- **Reliability**: Fault tolerance and error recovery
- **Maintainability**: Clear documentation and code structure

Note: Needs to be updated with specific technical details.

# MVP Technical Implications

Refer to the Minimum Viable Product (MVP) section in productContext.md for the current project focus. The MVP requires:
- Integration with Home Assistant as the main hub for device and sensor data.
- Support for data sources: energy prices, weather forecasts, battery charge/capacity, current energy use, and production.
- Initial implementation of simple rule-based (if-then) logic for optimization, with plans for linear optimization in later stages.
- Hardware interaction for battery charging/discharging, device switching, and signaling.
- User interface to display recommendations, available charge, and algorithmic reasoning.

# AppDaemon ↔ Home Assistant Integration

AppDaemon apps can interact with Home Assistant via the HASS plugin. Key capabilities include:

## Reading Entity State
```python
state = self.get_state("sensor.living_room_temperature")
self.log(f"Living room temperature is {state}")
```

## Listening for State Changes
```python
def initialize(self):
    self.listen_state(self.my_callback, "light.living_room")

def my_callback(self, entity, attribute, old, new, kwargs):
    self.log(f"{entity} changed from {old} to {new}")
```

## Calling Services (e.g., turn on a light)
```python
self.call_service("light/turn_on", entity_id="light.living_room")
```

## Setting AppDaemon-only State
```python
self.set_state("sensor.my_virtual_sensor", state="on", attributes={"friendly_name": "My Virtual Sensor"})
```

See the AppDaemon API Reference for more details.

# AppDaemon Posting Data to Custom Dashboard API

AppDaemon apps can send data to external dashboards or services by making HTTP requests (e.g., POST) to a REST API endpoint. This allows for decoupled, real-time updates from Home Assistant to any custom dashboard or service.

## Example: Posting Sensor Data to a Dashboard API
```python
import requests

def state_changed(self, entity, attribute, old, new, kwargs):
    data = {
        "entity_id": entity,
        "old_value": old,
        "new_value": new,
        "timestamp": self.datetime().isoformat()
    }
    try:
        response = requests.post("http://localhost:5000/api/update", json=data)
        self.log(f"Posted to dashboard: {data} (status: {response.status_code})")
    except Exception as e:
        self.log(f"Error posting to dashboard: {e}", level="ERROR")
```

**Benefits:**
- Decouples automation logic from the dashboard UI
- Enables real-time updates to any web service or dashboard
- Flexible: can be used for logging, analytics, notifications, etc.
