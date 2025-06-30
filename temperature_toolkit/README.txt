temperature_toolkit Package Description

This package is designed to manage and analyze daily temperature data.

Modules:

1. converter.py
   - Function: convert(value, from_unit, to_unit)
     - Converts a temperature value between 'celsius', 'fahrenheit', and 'kelvin'.
     - Returns the converted value rounded to 2 decimal places.

2. record.py
   - Class: TemperatureRecord
     - Attributes:
       - date: string (e.g., '2025-04-29')
       - readings: list of floats
       - scale: 'celsius', 'fahrenheit', or 'kelvin'
     - Methods:
       - convert_to(target_scale): Converts readings to the specified scale.
       - get_summary(): Returns a summary dictionary with min, max, and avg temperatures.
       - is_above_threshold(threshold): Returns True if all readings exceed the threshold.

3. analytics.py
   - Functions:
     - average_temperature_across_days(records): Returns the mean of all temperatures.
     - hottest_day(records): Returns the date with the highest average temperature.
     - detect_extreme_days(records, threshold): Dates with any reading above threshold.
     - temperature_range_for_each_day(records): Dict of date -> (min, max) tuples.
     - temperature_trend(temps): List of 'up', 'down', or 'same' indicating change.
     - detect_spike(temps, *, threshold=5): True if any jump/drop >= threshold.

This code is modular and tested using the main.py script for correctness and edge cases.
