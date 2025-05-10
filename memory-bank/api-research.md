# API Research for BalkonSolar

+Note: The APIs and data sources listed here are required for the MVP as defined in productContext.md (energy prices, weather, battery, usage, production).

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

## 1. Weather Data APIs

### OpenWeatherMap API
- **Description**: Comprehensive weather data including solar radiation
- **Key Features**:
  - Solar radiation data
  - Cloud cover predictions
  - Temperature forecasts
  - 5-day/3-hour forecast
- **Pricing**: Free tier available (60 calls/minute)
- **Documentation**: https://openweathermap.org/api
- **Pros**:
  - Well-documented
  - Reliable service
  - Good free tier
- **Cons**:
  - Solar data might need paid tier
  - Rate limits on free tier

### Solcast API
- **Description**: Specialized in solar radiation data
- **Key Features**:
  - Solar radiation forecasts
  - Historical solar data
  - Real-time solar data
  - High accuracy
- **Pricing**: Free tier available
- **Documentation**: https://docs.solcast.com/
- **Pros**:
  - Specialized in solar data
  - High accuracy
  - Good documentation
- **Cons**:
  - Limited free tier
  - More expensive than general weather APIs

### Open-Meteo API
- **Description**: Open-source weather API
- **Key Features**:
  - Solar radiation
  - Temperature
  - Cloud cover
  - Free to use
- **Pricing**: Free
- **Documentation**: https://open-meteo.com/
- **Pros**:
  - Completely free
  - No API key required
  - Good documentation
- **Cons**:
  - Less specialized in solar data
  - Rate limits

## 2. Electricity Price APIs

### ENTSOE API
- **Description**: European Network of Transmission System Operators
- **Key Features**:
  - Day-ahead prices
  - Real-time prices
  - Historical data
  - European coverage
- **Pricing**: Requires registration
- **Documentation**: https://transparency.entsoe.eu/
- **Pros**:
  - Official source
  - Comprehensive data
  - European coverage
- **Cons**:
  - Complex registration
  - Limited free access

### EPEX SPOT API
- **Description**: European Power Exchange
- **Key Features**:
  - Day-ahead prices
  - Intraday prices
  - Historical data
- **Pricing**: Requires subscription
- **Documentation**: https://www.eex.com/
- **Pros**:
  - Reliable source
  - Real-time data
  - European coverage
- **Cons**:
  - Expensive
  - Complex integration

### Local Utility APIs
- **Description**: Various utility company APIs
- **Key Features**:
  - Local price data
  - Real-time rates
  - Historical data
- **Pricing**: Varies by utility
- **Documentation**: Varies by utility
- **Pros**:
  - Local data
  - Direct integration
- **Cons**:
  - Limited coverage
  - Inconsistent APIs

## 3. Grid Demand APIs

### ENTSOE API (Grid Data)
- **Description**: Same as above, but for grid data
- **Key Features**:
  - Grid load data
  - Demand forecasts
  - Grid stability metrics
- **Pricing**: Requires registration
- **Documentation**: https://transparency.entsoe.eu/
- **Pros**:
  - Official source
  - Comprehensive data
- **Cons**:
  - Complex registration
  - Limited free access

### OpenGridMap API
- **Description**: Open-source grid data
- **Key Features**:
  - Grid topology
  - Load data
  - Historical data
- **Pricing**: Free
- **Documentation**: https://opengridmap.com/
- **Pros**:
  - Open source
  - Free to use
  - Community-driven
- **Cons**:
  - Limited real-time data
  - Coverage gaps

### Local Grid Operator APIs
- **Description**: Various grid operator APIs
- **Key Features**:
  - Local grid data
  - Real-time load
  - Stability metrics
- **Pricing**: Varies by operator
- **Documentation**: Varies by operator
- **Pros**:
  - Local data
  - Direct integration
- **Cons**:
  - Limited coverage
  - Inconsistent APIs

## Recommended API Stack

### Primary Stack
1. **Weather Data**: OpenWeatherMap API
   - Good balance of features and cost
   - Reliable service
   - Well-documented

2. **Electricity Prices**: ENTSOE API
   - Official source
   - Comprehensive data
   - European coverage

3. **Grid Demand**: ENTSOE API
   - Same as above
   - Integrated solution
   - Official source

### Backup Stack
1. **Weather Data**: Open-Meteo API
   - Free alternative
   - No API key required
   - Good fallback option

2. **Electricity Prices**: Local Utility APIs
   - Direct integration
   - Local data
   - Backup for price data

3. **Grid Demand**: OpenGridMap API
   - Free alternative
   - Open source
   - Community data

## Implementation Considerations

### Data Integration
- Implement API adapters for each service
- Create data normalization layer
- Handle rate limiting
- Implement caching
- Set up error handling

### Fallback Strategy
- Use backup APIs when primary fails
- Cache data for offline operation
- Implement retry mechanisms
- Log API failures

### Cost Optimization
- Implement efficient caching
- Batch API requests
- Use webhooks where available
- Monitor API usage

### Security
- Secure API key storage
- Implement rate limiting
- Use HTTPS
- Validate data
