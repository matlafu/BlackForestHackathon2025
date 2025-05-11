# UnQuack! ![MIT License](https://img.shields.io/badge/license-MIT-green) ![Python](https://img.shields.io/badge/python-3.11%2B-blue)

Optimizing Small-Scale Storage and Plug-In Solar for Grid Stability and Cost Savings.

---

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [How it Works](#how-it-works)
- [Main Components](#main-components)
- [Screenshots](#screenshots)
- [Quickstart Guide](#quickstart-guide)
- [Usage Guide](#usage-guide)
- [Project Structure](#project-structure)
- [Environment Variables](#environment-variables)
- [Development](#development)
- [Contributing](#contributing)
- [Known Issues & Roadmap](#known-issues--roadmap)
- [Contact & Support](#contact--support)
- [License](#license)
- [Links & Resources](#links--resources)
- [Docker Deployment](#docker-deployment)

---

## Overview

Our Balkon Solar solution helps prosumers (users with small-scale solar panels and batteries) optimize their energy consumption and feed-in behavior to support grid stability, reduce CO₂ emissions, and maximize financial benefits.

The system uses real-time data integration from weather forecasts, electricity prices, and grid demand to intelligently manage when to charge batteries, use solar energy directly, or feed energy back to the grid.

---

## System Architecture

```
┌─────────────────────────┐     ┌─────────────────────────┐
│ External Data Sources   │     │ Home Assistant          │
│ - Weather Forecasts     │◄───►│ - Sensor Integration    │
│ - Grid Demand           │     │ - User Interface        │
| - Average grid usage    |     | - Device Control        │
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

---

## How it Works

1. **Data Collection:**
   - User data: location, solar panel size, battery size
   - Weather forecast (24h), grid demand forecast
   - Current solar production, electricity usage, battery status
   - Average energy consumption (hour, month, weekday)
2. **Data Storage:**
   - All data is stored in a local SQLite database.
3. **Optimization:**
   - Algorithm determines optimal energy flow (cronjob/event-driven).
4. **Visualization:**
   - Output is stored and displayed in a dashboard.

---

## Main Components

1. **Core Module:** Algorithm, database interface, business logic
2. **AppDaemon Integration:** Real-time device control via Home Assistant
3. **Data Management:** SQLite database for historical and optimization data
4. **API Clients:** Interfaces for external data sources

---

## Screenshots
(to be added)

---

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

---

## Usage Guide

### Basic Operation

- System automatically collects data from configured sources.
- AppDaemon apps monitor solar production and household consumption.
- Core algorithm runs hourly to determine optimal energy flow.
- Results are stored in the database and used by AppDaemon apps.
- Virtual battery controller manages charge/discharge cycles.
- RGB indicator shows system status (green=using solar, yellow=mixed, red=grid).

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

---

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

---

## Environment Variables

Edit `balkonsolar/.env` with your configuration. Example variables:

| Variable             | Description                        | Example Value         |
|----------------------|------------------------------------|----------------------|
| LATITUDE             | Your latitude                      | 47.9990              |
| LONGITUDE            | Your longitude                     | 7.8421               |
| ELEVATION            | Elevation above sea level (meters) | 0                    |
| TIMEZONE             | Timezone (TZ database name)        | Europe/Berlin        |
| NABU_CASA_URL        | Home Assistant URL                 | https://...          |
| HOME_ASSISTANT_TOKEN | Home Assistant API token           | <your-token>         |

---

## Development

- Run tests: `pytest`
- Format code: `black .`
- Lint code: `flake8`

---

## Contributing

We welcome contributions! To get started:

- Fork the repository and create your branch from `main`
- Run tests and ensure code is formatted/linted
- Open a pull request with a clear description
- For major changes, please open an issue first to discuss

---

## Known Issues & Roadmap

- Docker deployment is not fully functional (AppDaemon and Home Assistant must run on the same machine)
- Planned: Improved optimization algorithms, improved dashboard, scheduling

---

## Contact & Support

- For questions, open an issue or contact the maintainers via GitHub.

---

## License

MIT

---

## Links & Resources

- (to be added)

---

## Docker Deployment

> **Note:** Docker is not fully working yet as AppDaemon and Home Assistant must run on the same machine.

1. **Build the Docker image:**
   ```bash
   docker build -t balkonsolar .
   ```
2. **Prepare your configuration:**
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
   Open your browser and navigate to `http://localhost:5050`
5. **View logs:**
   ```bash
   docker logs balkonsolar
   ```
