# Temperature Toolkit

A comprehensive Python toolkit for temperature data analysis, conversion, and analytics. This project provides tools for managing temperature records, converting between different temperature scales, and performing various analytical operations on temperature data.

## Features

- **Temperature Conversion**: Convert between Celsius, Fahrenheit, and Kelvin scales
- **Data Management**: Create and manage temperature records with multiple readings per day
- **Analytics**: Perform various analyses including averages, trends, spike detection, and more
- **Robust Error Handling**: Comprehensive input validation and error handling
- **Type Safety**: Full type hints for better code clarity and IDE support

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. Clone or download this repository
2. Navigate to the project directory
3. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies (if any):
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
Temperature_project/
├── main.py                          # Main demonstration script
├── test_temperature_toolkit.py      # Comprehensive test suite
├── README.md                        # This file
├── temperature_toolkit/             # Main package
│   ├── __init__.py                  # Package initialization
│   ├── record.py                    # TemperatureRecord class
│   ├── converter.py                 # Temperature conversion functions
│   ├── analytics.py                 # Analytics functions
│   └── README.txt                   # Package documentation
└── venv/                           # Virtual environment (if created)
```

## Usage

### Basic Usage

```python
from temperature_toolkit.record import TemperatureRecord
from temperature_toolkit.converter import convert
from temperature_toolkit.analytics import average_temperature_across_days

# Create temperature records
day1 = TemperatureRecord('2025-04-01', [20.5, 22.1, 19.8], 'celsius')
day2 = TemperatureRecord('2025-04-02', [68, 72, 65], 'fahrenheit')

# Convert temperatures
day2.convert_to('celsius')  # Convert all readings to Celsius

# Get summary statistics
summary = day1.get_summary()
print(f"Day 1: Min={summary['min']}°C, Max={summary['max']}°C, Avg={summary['avg']}°C")

# Perform analytics
records = [day1, day2]
avg_temp = average_temperature_across_days(records)
print(f"Average temperature across all days: {avg_temp}°C")
```

### Temperature Conversion

```python
from temperature_toolkit.converter import convert

# Convert between different scales
celsius_to_fahrenheit = convert(25, 'celsius', 'fahrenheit')  # 77.0
fahrenheit_to_kelvin = convert(32, 'fahrenheit', 'kelvin')    # 273.15
kelvin_to_celsius = convert(298.15, 'kelvin', 'celsius')     # 25.0

# Case insensitive
result = convert(0, 'CELSIUS', 'FAHRENHEIT')  # 32.0
```

### Analytics Functions

```python
from temperature_toolkit.analytics import (
    hottest_day,
    detect_extreme_days,
    temperature_trend,
    detect_spike
)

# Find the hottest day
hottest = hottest_day(records)

# Detect days with temperatures above threshold
extreme_days = detect_extreme_days(records, threshold=25.0)

# Analyze temperature trends
trends = temperature_trend([20, 22, 21, 25])  # ['up', 'down', 'up']

# Detect temperature spikes
has_spike = detect_spike([20, 22, 30, 25], threshold=5)  # True
```

## Module Documentation

### temperature_toolkit.record

The `TemperatureRecord` class represents a collection of temperature readings for a specific date.

**Key Methods:**
- `__init__(date, readings, scale)`: Initialize a record
- `convert_to(target_scale)`: Convert all readings to target scale
- `get_summary()`: Get min, max, and average temperatures
- `is_above_threshold(threshold)`: Check if all readings are above threshold
- `is_at_or_above_threshold(threshold)`: Check if all readings are at or above threshold

### temperature_toolkit.converter

Provides temperature conversion between Celsius, Fahrenheit, and Kelvin scales.

**Functions:**
- `convert(value, original_scale, target_scale)`: Convert temperature value between scales

**Supported Scales:**
- `'celsius'` (or `'C'`)
- `'fahrenheit'` (or `'F'`)
- `'kelvin'` (or `'K'`)

### temperature_toolkit.analytics

Collection of analytical functions for temperature data analysis.

**Functions:**
- `average_temperature_across_days(records)`: Calculate average across all days
- `hottest_day(records)`: Find date with highest average temperature
- `detect_extreme_days(records, threshold)`: Find days above temperature threshold
- `temperature_range_for_each_day(records)`: Get min/max for each day
- `temperature_trend(temps)`: Analyze trend between consecutive readings
- `detect_spike(temps, threshold=5)`: Detect temperature spikes

## Running Tests

To run the comprehensive test suite:

```bash
python test_temperature_toolkit.py
```

Or run with verbose output:

```bash
python -m unittest test_temperature_toolkit -v
```

## Running the Demo

To see the toolkit in action with sample data:

```bash
python main.py
```

This will demonstrate:
- Temperature conversions between all scales
- Creating and managing temperature records
- Various analytics functions
- Edge case handling

## Error Handling

The toolkit includes comprehensive error handling:

- **Invalid Temperature Scales**: Raises `ValueError` with descriptive message
- **Empty Data**: Gracefully handles empty readings and record lists
- **Edge Cases**: Handles negative temperatures, very large/small values
- **Type Safety**: Full type hints for better error detection

## Examples

### Example 1: Weather Station Data Analysis

```python
# Simulate weather station data
weather_data = [
    TemperatureRecord('2025-04-01', [15.2, 18.5, 12.8, 20.1], 'celsius'),
    TemperatureRecord('2025-04-02', [62, 68, 55, 72], 'fahrenheit'),
    TemperatureRecord('2025-04-03', [290.15, 295.15, 285.15], 'kelvin')
]

# Convert all to Celsius for analysis
for record in weather_data:
    record.convert_to('celsius')

# Perform analysis
avg_temp = average_temperature_across_days(weather_data)
hottest = hottest_day(weather_data)
extreme_days = detect_extreme_days(weather_data, 18.0)

print(f"Average temperature: {avg_temp}°C")
print(f"Hottest day: {hottest}")
print(f"Days above 18°C: {extreme_days}")
```

### Example 2: Temperature Monitoring

```python
# Monitor temperature changes
readings = [20.5, 22.1, 25.8, 23.2, 19.5]

# Check for trends
trend = temperature_trend(readings)
print(f"Temperature trend: {trend}")

# Check for spikes
if detect_spike(readings, threshold=3.0):
    print("Temperature spike detected!")
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For questions, issues, or contributions, please open an issue on the project repository. 