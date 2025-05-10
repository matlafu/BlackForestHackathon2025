# Technical Context

## Technology Stack
### Backend
- **Language**: Python 3.11+
  - FastAPI for API development
  - Pydantic for data validation
  - SQLAlchemy for database ORM
  - APScheduler for task scheduling
  - Pandas for data analysis

### Frontend
- **Framework**: React with TypeScript
  - Material-UI for component library
  - Redux for state management
  - Chart.js for data visualization
  - React Query for API data fetching

### Data Storage
- **Time Series**: InfluxDB
- **Relational**: PostgreSQL
- **Cache**: Redis

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **API Gateway**: Nginx
- **Message Broker**: RabbitMQ

### Development Tools
- **Version Control**: Git
- **CI/CD**: GitHub Actions
- **Testing**: pytest, Jest
- **Documentation**: Sphinx, Storybook
- **Code Quality**: Black, ESLint, Prettier

## Development Setup
1. **Prerequisites**
   - Python 3.11+
   - Node.js 18+
   - Docker and Docker Compose
   - Git

2. **Local Development**
   - Clone repository
   - Set up virtual environment
   - Install dependencies
   - Configure environment variables
   - Run development servers

3. **Testing Environment**
   - Unit tests
   - Integration tests
   - End-to-end tests
   - Performance tests

## Dependencies
### Backend Dependencies
- fastapi==0.104.1
- uvicorn==0.24.0
- sqlalchemy==2.0.23
- pydantic==2.5.2
- pandas==2.1.3
- influxdb-client==1.36.1
- redis==5.0.1
- pika==1.3.2
- pytest==7.4.3

### Frontend Dependencies
- react==18.2.0
- typescript==5.3.3
- @mui/material==5.15.1
- @reduxjs/toolkit==2.0.1
- chart.js==4.4.1
- @tanstack/react-query==5.8.7

## Hardware Used
- Shelly smart meter (measures current household energy usage)
- Smart Wi-Fi LED light (status indicator, integrated with Home Assistant)
- Shelly plugs (control devices via Home Assistant)
- Solar Panels with Zendure SolarFlow 800 inverter
- Zendure battery storage

## Technical Constraints
- **Hardware Requirements**: Minimal resource usage for Raspberry Pi compatibility
- **Network**: Support for local network operation
- **Security**: Secure device communication and data storage
- **Scalability**: Support for multiple devices and users
- **Compatibility**: Support for various battery and inverter types
- **Performance**: Real-time data processing and decision making
- **Reliability**: Fault tolerance and error recovery
- **Maintainability**: Clear documentation and code structure

Note: Needs to be updated with specific technical details.

# MVP Technical Implications

Refer to the Minimum Viable Product (MVP) section in productContext.md for the current project focus. The MVP requires:
- Integration with Home Assistant as the main hub for device and sensor data.
- Support for data sources: energy prices, weather forecasts, battery charge/capacity, current energy use, and production.
- Initial implementation of simple rule-based (if-then) logic for optimization, with plans for linear optimization in later stages.
- Hardware interaction for battery charging/discharging, device switching, and signaling.
- User interface to display recommendations, available charge, and algorithmic reasoning.
