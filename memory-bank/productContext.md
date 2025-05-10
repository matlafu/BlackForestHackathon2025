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
