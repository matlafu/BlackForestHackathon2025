# Project Brief: BalkonSolar

## Overview
BalkonSolar is a project focused on optimizing small-scale storage and plug-in solar systems for grid stability and cost savings. The project aims to develop an innovative solution that helps prosumers optimize their energy consumption and feed-in behavior.

## Core Requirements
- Develop a solution for optimizing small-scale battery storage
- Integrate with real-time electricity prices & grid demand APIs
- Utilize weather forecasts for solar power predictions
- Interface with battery & inverter data
- Support smart home hardware integration
- Create an open-source, low-cost solution

## Project Goals
- Support grid stability through optimized consumption and feed-in
- Reduce CO₂ emissions by efficient use of green electricity
- Maximize financial benefits for prosumers
- Ensure solution is simple, user-friendly, and scalable

## Scope
The project will focus on:
- Small-scale battery storage optimization
- Plug-in solar system integration
- Grid demand response
- Prosumer energy management
- Real-time data integration
- Smart home hardware compatibility

## Timeline
[Hackathon duration to be specified]

## Success Criteria
- Solution balances grid by optimizing consumption and feed-in
- Reduces CO₂ impact through efficient green electricity use
- Maximizes financial benefits for prosumers
- Maintains simplicity and user-friendliness
- Ensures low-cost implementation
- Provides open-source accessibility
- Includes clear documentation
- Demonstrates scalability

# [2024-05-10] Virtual Battery & AppDaemon System Updates

- Modular virtual battery system with controller, supporting activation/deactivation and external charge setting.
- Absolute imports used for all AppDaemon apps (e.g., `from virtual_battery import VirtualBattery`).
- Sensor readers (`household_consumption_reader.py`, `pv_production_reader.py`) handle 'unavailable' or non-numeric values gracefully, defaulting to 0.0 W and logging a warning.
- Both readers log their current value every minute, even if unchanged.
- Battery controller auto-turns off and logs when fully charged/discharged; can be set externally via `set_battery_charge()`.
- Debugging: Added logs to `initialize()`, checked app names in `apps.yaml`, and handled app availability.
- Noted that Home Assistant connection errors are unrelated to app logic and are usually transient.

---
