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
