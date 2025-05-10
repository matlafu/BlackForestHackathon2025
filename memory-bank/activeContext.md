# Active Context

## Current Focus
- Project initialization and documentation
- Understanding requirements and scope
- Planning technical architecture
- Setting up development environment

## Recent Changes
- Created memory bank structure
- Initialized core documentation files
- Documented project brief and requirements
- Defined product context and scope
- Outlined system architecture and technical stack

## Next Steps
1. **Project Setup**
   - Create GitHub repository
   - Set up project structure
   - Initialize development environment
   - Configure CI/CD pipeline

2. **Core Development**
   - Implement data integration layer
     - Research and select specific APIs for electricity prices and grid demand
     - Develop API connectors
     - Create data models and validation
   - Build optimization engine
     - Design algorithm for battery charging/discharging
     - Implement grid demand prediction
     - Develop cost-benefit analysis

3. **Device Integration**
   - Research compatible battery and inverter types
   - Develop device management system
   - Implement smart plug integration
   - Create command execution framework

4. **User Interface**
   - Design UI/UX wireframes
   - Implement web dashboard
   - Develop mobile app
   - Create configuration interface

5. **Testing and Validation**
   - Write unit tests
   - Perform integration testing
   - Conduct end-to-end testing
   - Validate with real devices

6. **Documentation**
   - Create API documentation
   - Write user guides
   - Document installation process
   - Provide development guidelines

## Active Decisions
- Using markdown for documentation
- Implementing memory bank structure
- Focusing on open-source, low-cost solution
- Prioritizing user-friendly interface
- Ensuring scalability and maintainability
- Following microservices architecture
- Using containerization for deployment

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

# [2024-05-10] Codebase Structure & Data Flow Update

- **database_shenanigans/**: Contains all database logic for energy data. `energy_db.py` is the main utility class for interacting with the SQLite database, supporting storage and retrieval of solar output, battery status, grid usage, and algorithm output, with time filtering and context manager support. Includes scripts for DB creation and example usage.
- **core/**: Contains core logic for data integration and optimization rules. `data_integration.py` integrates weather, electricity, and grid data from external APIs (OpenWeatherMap, ENTSOE, OpenGridMap) and provides async methods to fetch/aggregate data. `rules.py` implements the main optimization algorithm for system state (use solar, charge battery, use battery, use grid).
- **data/**: Contains Pydantic data models for all major data types (weather, forecasts, prices, grid load/stability, integrated/optimization data) for validation and structured handling.
- **utils/** and **tests/**: Placeholders for utility functions and tests (currently empty).

**Data Flow:**
- Data is collected from external APIs via `DataIntegrationService` (core/data_integration.py).
- Data is validated/structured using Pydantic models (data/models.py).
- Optimization logic (core/rules.py) determines system actions.
- All relevant time series data is stored/retrieved using `EnergyDB` (database_shenanigans/energy_db.py).

**Best Practices:**
- Clear separation of concerns (integration, logic, models, persistence).
- Async data fetching for efficiency.
- Extensible, validated data models.
- Encapsulated DB utility class for all DB operations.

Last Updated: [Current Date]
