# Product Context

## Problem Statement
Small-scale battery storage for plug-in solar systems is not optimized for grid demand. Users charge batteries based on electricity prices rather than grid conditions, possibly overloading the grid at peak solar production times while missing opportunities to use excess renewable energy. There are no dynamic incentives for prosumers to adjust their energy use, leading to inefficiencies in balancing supply and demand.

## Solution Overview
BalkonSolar aims to develop an innovative solution that helps prosumers optimize their energy consumption and feed-in behavior to support grid stability, reduce CO₂ emissions, and maximize financial benefits.

## User Experience Goals
- Simple and intuitive interface for prosumers
- Real-time visibility of energy optimization
- Clear display of financial benefits
- Easy integration with existing systems
- Low-cost implementation
- Accessible open-source solution

## Target Users
- Prosumers (users with solar and storage systems)
- Small-scale solar system owners
- Energy-conscious homeowners
- Grid operators and utilities
- Renewable energy enthusiasts

## Available Resources
- Real-time electricity prices & grid demand APIs
- Weather forecasts for solar power predictions
- Battery & inverter data for energy flow insights
- Smart home hardware (sockets, sensors, tablets, etc.)
- Shelly smart meter (measures current household energy usage)
- Smart Wi-Fi LED light (status indicator, integrated with Home Assistant)
- Shelly plugs (control devices via Home Assistant)
- Solar Panels with Zendure SolarFlow 800 inverter
- Zendure battery storage

Note: This document needs to be populated with specific product details.

# Minimum Viable Product (MVP)

## What does our User want to achieve?
- **Main goal:** Optimize for grid stability/efficiency (because nobody does this yet)

## What data do we want to work with?
- Energy prices
- Weather forecast
- Battery charge level + capacity
- Current energy use (+ energy usage patterns of the user)
- Current energy production

## What logic assumptions do we have (if [condition] then [action])?
- Rules need to be defined
- Simple if-then logic to start with
- Linear optimizations with equation solving later

## How do we interact with the hardware (output)?
- Charging or discharging the battery
- Switching devices on or off (does this even make sense without the user interfering?)
- Signaling e.g. energy price via red or green light (or battery charge)

## What do we want to show to the user?
- Info / recommendations:
  - Best times during the day to use energy
  - Available charge (solar power) for the day (in simple terms: 1 load of laundry, 1h using the oven, ...)
  - When to use the battery, when to use the grid
- Show reasoning for the algorithmic decisions (when to charge/discharge, etc.)

## What settings / options do we want to give the user?
- Basic settings / configuration:
  - Orientation of the solar panels
  - Battery capacity
  - Peak solar energy output
  - Thresholds for "cheap" and "expensive" energy prices
  - Backup capacity (how much charge to always keep)
  - High solar forecast threshold
  - Location (lat / long)
  - (to be continued)
- Modes / actions

## Integration
We want to work with Home Assistant as our main Hub that controls the devices and provides us with data of the sensors (+ external data through APIs). Our solution is to be integrated closely with Home Assistant (probably running as an AppDaemon alongside).

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
