# BalkonSolar

Optimizing Small-Scale Storage and Plug-In Solar for Grid Stability and Cost Savings

## Overview

BalkonSolar is a solution that helps prosumers (users with solar and storage) optimize their energy consumption and feed-in behavior to support grid stability, reduce CO₂ emissions, and maximize financial benefits.

## Features

- Real-time data integration from weather, electricity prices, and grid demand
- Smart optimization of battery charging/discharging
- User-friendly interface for monitoring and control
- Open-source implementation

## Project Structure

```
balkonsolar/
├── api/            # API clients for external services
├── core/           # Core business logic
├── data/           # Data models and database
├── utils/          # Utility functions
└── tests/          # Test suite
```

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   ```
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```
5. Run the application:
   ```
   python -m balkonsolar
   ```

## Development

- Run tests: `pytest`
- Format code: `black .`
- Lint code: `flake8`

## License

MIT

## AppDaemon Local Development Setup

To run AppDaemon and connect it to your Home Assistant instance (running on a Raspberry Pi in a separate network via Home Assistant Cloud):

1. Ensure you have Python 3.11+ and AppDaemon installed (`pip install appdaemon`).
2. Copy `.env.example` to `.env` in `/balkonsolar` and fill in your values:
   ```
   cp balkonsolar/.env.example balkonsolar/.env
   # Edit balkonsolar/.env with your credentials and configuration
   ```
3. The `appdaemon.yaml` configuration file uses environment variables (see below for example).
4. Create an `apps/` directory for your AppDaemon apps.
5. Run AppDaemon: `appdaemon -c /path/to/your/appdaemon/config`

Example `appdaemon.yaml`:
```yaml
appdaemon:
  latitude: !env_var APPDAEMON_LATITUDE
  longitude: !env_var APPDAEMON_LONGITUDE
  elevation: !env_var APPDAEMON_ELEVATION
  time_zone: !env_var APPDAEMON_TIMEZONE
hass:
  url: !env_var NABU_CASA_URL
  token: !env_var HOME_ASSISTANT_TOKEN
```

For more details, see the technical documentation in `memory-bank/techContext.md`.
