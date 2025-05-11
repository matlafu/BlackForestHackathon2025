# BalkonSolar

Optimizing Small-Scale Storage and Plug-In Solar for Grid Stability and Cost Savings

## Overview

BalkonSolar is a solution that helps prosumers (users with small-scale solar panels and batteries) optimize their energy consumption and feed-in behavior to support grid stability, reduce CO₂ emissions, and maximize financial benefits.

The system uses real-time data integration from weather forecasts, electricity prices, and grid demand to intelligently manage when to charge batteries, use solar energy directly, or feed energy back to the grid.

## System Architecture

```
┌─────────────────────────┐     ┌─────────────────────────┐
│ External Data Sources   │     │ Home Assistant          │
│ - Weather Forecasts     │     │ - Sensor Integration    │
│ - Electricity Prices    │◄───►│ - Device Control        │
│ - Grid Demand           │     │ - User Interface        │
└─────────────────────────┘     └─────────────────────────┘
            ▲                               ▲
            │                               │
            ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────┐
│ Core System             │     │ AppDaemon               │
│ - Optimization Logic    │◄───►│ - Apps for Control      │
│ - Decision Engine       │     │ - Automation Logic      │
│ - Database              │     │ - Virtual Devices       │
└─────────────────────────┘     └─────────────────────────┘
```

### Main Components:

1. **Core Module**: Contains the algorithm, database interface, and core business logic
2. **AppDaemon Integration**: Provides real-time control of devices via Home Assistant
3. **Data Management**: SQLite database storing historical data and optimization results
4. **API Clients**: Interfaces with external data sources

## Quickstart Guide

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-repo-directory>
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Set up your `.env` file:**
   ```bash
   cp balkonsolar/.env.example balkonsolar/.env
   # Edit balkonsolar/.env with your credentials and configuration
   ```

5. **Run AppDaemon for Home Assistant integration:**
   ```bash
   ./run_appdaemon.sh
   ```

   ```

## Usage Guide

### Basic Operation

1. **System Initialization**:
   - The system automatically collects data from configured sources
   - AppDaemon apps monitor your solar production and household consumption

2. **Optimization Process**:
   - The core algorithm runs hourly to determine optimal energy flow
   - Results are stored in the database and used by AppDaemon apps

3. **Device Control**:
   - Virtual battery controller manages charge/discharge cycles
   - RGB indicator shows system status (green=using solar, yellow=mixed, red=grid)

### Monitoring

- Access the Home Assistant dashboard to view:
  - Current solar production
  - Battery charge status
  - Energy flow direction
  - Prediction data

### Manual Control

- Override automatic operation via Home Assistant:
  - Set battery charge level manually
  - Force specific operation modes
  - Adjust optimization preferences

## Project Structure

```
balkonsolar/
├── api/                  # API clients for external services
├── appdaemon/            # AppDaemon configuration and apps
│   └── apps/             # Individual automation apps
├── core/                 # Core business logic
│   ├── algo.py           # Optimization algorithm
│   ├── database_interface.py # Database interactions
│   └── rules.py          # Decision rules engine
├── data/                 # Data storage and schemas
├── utils/                # Utility functions
└── README.md             # This documentation
```

## Development

- Run tests: `pytest`
- Format code: `black .`
- Lint code: `flake8`

## Home Assistant Integration

To enable voice commands and other integrations with Home Assistant, see the detailed setup instructions in the [Home Assistant section](docs/home-assistant.md).

For more details, see the technical documentation in `memory-bank/techContext.md`.

## License

MIT

## Miro for the project
https://miro.com/welcomeonboard/UHRWSFI5a3Job3cxSTVzanYvTG1YRWN3bkF2Z2VKcWRLeHFTWUlFTyt4TjNRQXVVYTIrQ0VhR0VXdDJIU0ZibFNnLzRHSEhieWhsVUxwd1dPWjFHVzY0akg0aVlwa2N3OVJUUzN2TU9CU1g0eXJENGFSaDdDanhBL2lUeU83TjJhWWluRVAxeXRuUUgwWDl3Mk1qRGVRPT0hdjE=?share_link_id=440103296435

## Relevant data
https://cloud.sbamueller.de/index.php/s/xazJLz2L6nQtLeB

## Home Assistant: Add Voice Command Webhook Automation

To enable voice commands (e.g., via Siri Shortcuts) to trigger Home Assistant actions and receive a custom response, add the following automation to your `automations.yaml`:

```yaml
- id: 'siri_webhook'
  alias: Handle Siri Command Webhook
  description: 'Handles incoming webhook commands from Siri'
  trigger:
    - platform: webhook
      webhook_id: siri_command
  action:
    - service: rest_command.call_appdaemon
      data_template:
        payload: "{{ trigger.json }}"  # Send the webhook data to AppDaemon for processing
    - wait_for_trigger:
        - platform: event
          event_type: appdaemon_response
          event_data:
            command_id: "{{ trigger.json.command_id }}"  # Match the response to the command
    - service: notify.notify
      data_template:
        message: "{{ trigger.event.data.message }}"  # Use the custom response message from AppDaemon
  mode: single
```

- Adjust the `webhook_id` and actions as needed for your setup.
- The `rest_command.call_appdaemon` should be defined in your `rest_command` configuration to forward the payload to your AppDaemon endpoint.
- This automation sends the webhook data to AppDaemon, waits for a response event (`appdaemon_response`), and then notifies the user with the custom response message from AppDaemon.

## Docker Deployment

(Docker is not working yet as the AppDaemon is not running on the same machine as the Home Assistant - this would be the next step)

You can also run BalkonSolar in a Docker container:

1. **Build the Docker image:**
   ```bash
   docker build -t balkonsolar .
   ```

2. **Prepare your configuration:**
   - Create a directory for configuration, data, and logs:
     ```bash
     mkdir -p ~/balkonsolar/{config,data,logs}
     cp balkonsolar/.env.example ~/balkonsolar/config/.env
     # Edit ~/balkonsolar/config/.env with your credentials
     ```

3. **Run the container:**
   ```bash
   docker run -d --name balkonsolar \
     -v ~/balkonsolar/config:/app/config \
     -v ~/balkonsolar/data:/app/data \
     -v ~/balkonsolar/logs:/app/logs \
     -p 5050:5050 \
     balkonsolar
   ```

4. **Access the AppDaemon dashboard:**
   - Open your browser and navigate to `http://localhost:5050`

5. **View logs:**
   ```bash
   docker logs balkonsolar
