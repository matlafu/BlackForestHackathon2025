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
