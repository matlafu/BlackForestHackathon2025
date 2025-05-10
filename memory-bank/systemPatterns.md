# System Patterns

## Architecture Overview
The BalkonSolar solution will follow a modular, event-driven architecture with the following components:

1. **Core Optimization Engine**
   - Central decision-making system
   - Algorithm for optimizing battery charging/discharging
   - Grid demand prediction
   - Cost-benefit analysis
   - MVP: Start with simple if-then rule logic as described in productContext.md, with plans to evolve to linear optimization.

2. **Data Integration Layer**
   - API connectors for external data sources
   - Data normalization and validation
   - Real-time data processing
   - Historical data storage

3. **Device Management System**
   - Battery and inverter control
   - Smart plug integration
   - Device state management
   - Command execution

4. **User Interface**
   - Web dashboard
   - Mobile app
   - Configuration interface
   - Status monitoring

5. **Notification System**
   - Alert management
   - User notifications
   - System status updates
   - Action recommendations

## Design Patterns
- **Event-Driven Architecture**: For real-time data processing and system responses
- **Microservices**: For modular, scalable components
- **Repository Pattern**: For data access abstraction
- **Strategy Pattern**: For pluggable optimization algorithms
- **Observer Pattern**: For event notification
- **Factory Pattern**: For device management
- **Adapter Pattern**: For API integrations
- **MVP Logic Evolution**: Begin with simple rule-based logic (see productContext.md MVP), with a roadmap to more advanced optimization patterns.

## Component Relationships
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  User Interface │◄────┤  Optimization   │◄────┤  Data Integration│
│                 │     │     Engine      │     │                 │
└────────┬────────┘     └────────┬────────┘     └─────────────────┘
         │                       │                       ▲
         │                       │                       │
         ▼                       ▼                       │
┌─────────────────┐     ┌─────────────────┐             │
│  Notification   │     │    Device       │◄────────────┘
│     System      │     │   Management    │
└─────────────────┘     └─────────────────┘
```

## Technical Decisions
- **Open Source**: All components will be open source for community contribution
- **API-First**: Design APIs before implementation for better integration
- **Containerization**: Use Docker for consistent deployment
- **Event Streaming**: Implement real-time data processing
- **Modular Design**: Enable easy extension and customization
- **Low Resource Usage**: Optimize for minimal hardware requirements
- **Standard Protocols**: Use industry-standard protocols for device communication

Note: To be updated as system architecture evolves.

## Hardware Used
- Shelly smart meter (measures current household energy usage)
- Smart Wi-Fi LED light (status indicator, integrated with Home Assistant)
- Shelly plugs (control devices via Home Assistant)
- Solar Panels with Zendure SolarFlow 800 inverter
- Zendure battery storage

# [2024-05-10] Virtual Battery & AppDaemon System Updates

- Modular virtual battery system with controller, supporting activation/deactivation and external charge setting.
- Absolute imports used for all AppDaemon apps (e.g., `from virtual_battery import VirtualBattery`).
- Sensor readers (`household_consumption_reader.py`, `pv_production_reader.py`) handle 'unavailable' or non-numeric values gracefully, defaulting to 0.0 W and logging a warning.
- Both readers log their current value every minute, even if unchanged.
- Battery controller auto-turns off and logs when fully charged/discharged; can be set externally via `set_battery_charge()`.
- Debugging: Added logs to `initialize()`, checked app names in `apps.yaml`, and handled app availability.
- Noted that Home Assistant connection errors are unrelated to app logic and are usually transient.

# [2024-05-10] DevOps & Simulation Improvements

- Virtual Environment Management: If venv/ or .venv/ is deleted or broken, recreate with python3.11 -m venv venv and reinstall dependencies. Use .gitignore to exclude venv/ and its subfolders from git tracking. Use git rm -r --cached venv/ to remove venv/ from the repo but keep it locally.
- AppDaemon & Home Assistant Integration: AppDaemon must be able to connect to Home Assistant and see the correct domains/entities (e.g., light). If an entity is unavailable in Home Assistant, AppDaemon cannot control it. Always check Home Assistant's Developer Tools > States for entity status.
- Fake Controllers for Testing: fake_controllers.py now contains only "action" classes that trigger/test actions on real device apps (e.g., battery, RGB bulb). The fake RGB bulb controller cycles through red, yellow, and green every 10 seconds for demo/testing.
- Debugging Tips: If git still shows ignored files, use git rm --cached to untrack them. .gitignore only prevents new files from being tracked, not files already in the repo.

---
