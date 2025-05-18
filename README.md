# UnQuack! ![MIT License](https://img.shields.io/badge/license-MIT-green) ![Python](https://img.shields.io/badge/python-3.11%2B-blue)

# ⚡ A BalkonSolar Project at Black Forest Hackathon, Freiburg, May 2025
Optimizing Small-Scale Storage and Plug-In Solar for Grid Stability and Cost Savings.

BalkonSolar „UnQuack!” is an open-source solution developed at the Black Forest Hackathon 2025 to empower prosumers—households with small-scale solar panels and batteries—to become active participants in the energy transition. Our system intelligently manages when to charge batteries, use solar energy directly, or feed energy back to the grid, not just for personal savings but to support grid stability and reduce CO₂ emissions.

By integrating real-time weather forecasts, electricity prices, and grid demand, UnQuack! helps users make smarter, automated decisions about their energy use. The platform is designed for simplicity, low cost, and easy integration with Home Assistant and smart home hardware, making advanced energy optimization accessible to everyone.

Get actionable insights for your individual setup—tailored recommendations help you make the most of your solar and storage system.

The first version of UnQuack! was built during the Hackathon, with the challenge, hardware, and expert support generously provided by [BalkonSolar e.V.](https://balkon.solar/). We invite contributors to join us in further developing and expanding this open-source project.

> 🎥 **Watch our pitch:** [YouTube - Hackathon Pitch (Moritz Bappert & Leah Bohr)](https://youtu.be/dRtN1CwIprc)
>
> 📑 **Presentation Slides:** [Google Slides](https://docs.google.com/presentation/d/1MwFIBHbAU6AiCBx8ojyI68AZJ_ug1l325plCxEBci9g/edit?usp=sharing)

**🏆 Challenge:** Challenge 4 - BalkonSolar
**🔗 Event:** [Black Forest Hackathon, Freiburg, May 2025](https://www.blackforesthackathon.de/may/)

---

## Table of Contents

- [Team UnQuack!](#team-unquack)
- [Challenge Description](#challenge-description)
- [System Architecture](#system-architecture)
- [How it Works](#how-it-works)
- [Main Components](#main-components)
- [Screenshots](#screenshots)
- [Quickstart Guide](#quickstart-guide)
- [Usage Guide](#usage-guide)
- [Project Structure](#project-structure)
- [Environment Variables](#environment-variables)
- [Development](#development)
- [Docker Deployment](#docker-deployment)
- [Contributing](#contributing)
- [Links & Resources](#links--resources)
- [Known Issues & Roadmap](#known-issues--roadmap)
- [Contact & Support](#contact--support)
- [Special Thanks / Credits](#special-thanks--credits)

---

## 👥 Team UnQuack!

- **Arno Trawinski** – Vibe Manager & Frontend Magician
  Built a stunning interface at lightning speed while making sure we stayed on track.
- **Leah Bohr** – Architect of our Systems Optimization Brain
  Visionary behind the logic and algorithm that powers our system's mind.
- **Apoorv Agnihotri** – Rule Wrangler & Integration Sorcerer
  Integration expert and co-architect of the smart logic.
- **Mateo Cortés Lafourcade** – Pattern Wizard & Code Enchanter
  Weaves singletons into our code, fixes bugs, and makes everything just... work.
- **Markus** – Chief Science Nerd for Grid, Solar & Data
  Knows watt's watt when it comes to energy flow, data glow, and API mojo.
- **Moritz Bappert** – Connector of Worlds, Tamer of Hardware
  Bridged the gap between software and the real world. Wrestled the AppDaemon and won.

---

## 🏁 Challenge Description

### 🚀 Optimizing Small-Scale Storage and Plug-In Solar for Grid Stability and Cost Savings

**🔍 Problem Statement:**
Small-scale battery storage for plug-in solar systems is not optimized for grid demand. Users charge batteries based on electricity prices rather than grid conditions, possibly overloading the grid at peak solar production times while missing opportunities to use excess renewable energy. There are no dynamic incentives for prosumers to adjust their energy use, leading to inefficiencies in balancing supply and demand.

**🎯 HACKATHON CHALLENGE:**
How might we develop an innovative solution that helps prosumers (users with solar and storage) optimize their energy consumption and feed-in behavior to support grid stability, reduce CO₂ emissions, and maximize financial benefits?

**📊 Available Data & Resources:**
- Real-time electricity prices & grid demand APIs
- Weather forecasts for solar power predictions
- Battery & inverter data for energy flow insights
- Smart home hardware (sockets, sensors, tablets, etc.) for prototyping

**🏆 Success Criteria:**
A successful solution should balance the grid by optimizing consumption and feed-in based on demand, reduce CO₂ impact by using green electricity efficiently, maximize financial benefits for prosumers and be simple, user-friendly, low-cost, open-source, and scalable.

**💡 Key Considerations:**
The solution should prioritize simplicity, low costs, ease of implementation, open-source accessibility, and clear documentation to ensure widespread adoption and usability.

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

## Docker Deployment

> **Note:** Docker is not fully working yet.

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

---

## Contributing

We prioritize open source and encourage community contributions to make energy optimization accessible and innovative for all.

To get started:

- Fork the repository and create your branch from `main`
- Run tests and ensure code is formatted/linted
- Open a pull request with a clear description
- For major changes, please open an issue first to discuss

---

## Links & Resources

- (to be added)

---

## Roadmap

- Improved dashboard
- Additional physical interfaces to indicate current recommendations
- Scheduling algorithm extensions:
  - Consider user intention (reduce CO2, save money, stabilize grid)
  - Consider user scheduling needs (plan high power usage)
- Detailed modelling of PV panel and storage behavior
- Voice control assistant

---

## Contact & Support

- For questions, open an issue or contact the maintainers via GitHub.


---

## Special Thanks / Credits

We would like to thank [BalkonSolar e.V.](https://balkon.solar/) for providing the challenge and for their outstanding support with hardware and expertise during the hackathon — especially Sebastian Müller for his guidance and encouragement.
