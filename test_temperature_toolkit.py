import unittest
from temperature_toolkit.record import TemperatureRecord
from temperature_toolkit.converter import convert
from temperature_toolkit.analytics import (
    average_temperature_across_days,
    hottest_day,
    detect_extreme_days,
    temperature_range_for_each_day,
    temperature_trend,
    detect_spike,
)


class TestTemperatureToolkit(unittest.TestCase):
    def test_converter_basic(self):
        """Test basic temperature conversions."""
        self.assertAlmostEqual(convert(0, "celsius", "fahrenheit"), 32.0)
        self.assertAlmostEqual(convert(32, "fahrenheit", "celsius"), 0.0)
        self.assertAlmostEqual(convert(0, "celsius", "kelvin"), 273.15)
        self.assertAlmostEqual(convert(273.15, "kelvin", "celsius"), 0.0)
        self.assertEqual(convert(100, "celsius", "celsius"), 100)

    def test_converter_edge_cases(self):
        """Test edge cases for temperature conversion."""
        # Negative temperatures
        self.assertAlmostEqual(convert(-40, "celsius", "fahrenheit"), -40.0)
        self.assertAlmostEqual(convert(-273.15, "celsius", "kelvin"), 0.0)

        # Large values
        self.assertAlmostEqual(convert(1000, "celsius", "fahrenheit"), 1832.0)
        self.assertAlmostEqual(convert(1000, "celsius", "kelvin"), 1273.15)

        # Very small values
        self.assertAlmostEqual(
            convert(0.001, "celsius", "fahrenheit"), 32.0018, places=4
        )

        # Case insensitive
        self.assertAlmostEqual(convert(0, "CELSIUS", "FAHRENHEIT"), 32.0)
        self.assertAlmostEqual(convert(32, "Fahrenheit", "Celsius"), 0.0)

    def test_converter_all_combinations(self):
        """Test all possible scale conversion combinations."""
        # Celsius to all scales
        self.assertAlmostEqual(convert(25, "celsius", "celsius"), 25.0)
        self.assertAlmostEqual(convert(25, "celsius", "fahrenheit"), 77.0)
        self.assertAlmostEqual(convert(25, "celsius", "kelvin"), 298.15)

        # Fahrenheit to all scales
        self.assertAlmostEqual(convert(77, "fahrenheit", "celsius"), 25.0)
        self.assertAlmostEqual(convert(77, "fahrenheit", "fahrenheit"), 77.0)
        self.assertAlmostEqual(convert(77, "fahrenheit", "kelvin"), 298.15)

        # Kelvin to all scales
        self.assertAlmostEqual(convert(298.15, "kelvin", "celsius"), 25.0)
        self.assertAlmostEqual(convert(298.15, "kelvin", "fahrenheit"), 77.0)
        self.assertAlmostEqual(convert(298.15, "kelvin", "kelvin"), 298.15)

    def test_converter_errors(self):
        """Test error handling for invalid scales."""
        with self.assertRaises(ValueError):
            convert(100, "rankine", "celsius")
        with self.assertRaises(ValueError):
            convert(100, "celsius", "rankine")
        with self.assertRaises(ValueError):
            convert(100, "invalid", "celsius")
        with self.assertRaises(ValueError):
            convert(100, "celsius", "invalid")

    def test_temperature_record_summary(self):
        """Test temperature record summary functionality."""
        record = TemperatureRecord("2025-04-01", [10.0, 15.0, 20.0], "celsius")
        summary = record.get_summary()
        self.assertEqual(summary["min"], 10.0)
        self.assertEqual(summary["max"], 20.0)
        self.assertEqual(summary["avg"], 15.0)
        self.assertEqual(summary["date"], "2025-04-01")
        self.assertEqual(summary["scale"], "celsius")

    def test_temperature_record_empty_readings(self):
        """Test temperature record with empty readings."""
        record = TemperatureRecord("2025-04-01", [], "celsius")
        summary = record.get_summary()
        self.assertEqual(summary["min"], 0)
        self.assertEqual(summary["max"], 0)
        self.assertEqual(summary["avg"], 0)

    def test_temperature_record_single_reading(self):
        """Test temperature record with single reading."""
        record = TemperatureRecord("2025-04-01", [25.5], "celsius")
        summary = record.get_summary()
        self.assertEqual(summary["min"], 25.5)
        self.assertEqual(summary["max"], 25.5)
        self.assertEqual(summary["avg"], 25.5)

    def test_convert_to_all_scales(self):
        """Test convert_to method with all scale combinations."""
        # Celsius to Fahrenheit
        record = TemperatureRecord("2025-04-01", [0], "celsius")
        record.convert_to("fahrenheit")
        self.assertAlmostEqual(record.readings[0], 32.0)
        self.assertEqual(record.scale, "fahrenheit")

        # Celsius to Kelvin
        record = TemperatureRecord("2025-04-01", [0], "celsius")
        record.convert_to("kelvin")
        self.assertAlmostEqual(record.readings[0], 273.15)
        self.assertEqual(record.scale, "kelvin")

        # Fahrenheit to Celsius
        record = TemperatureRecord("2025-04-01", [32], "fahrenheit")
        record.convert_to("celsius")
        self.assertAlmostEqual(record.readings[0], 0.0)
        self.assertEqual(record.scale, "celsius")

        # Fahrenheit to Kelvin
        record = TemperatureRecord("2025-04-01", [32], "fahrenheit")
        record.convert_to("kelvin")
        self.assertAlmostEqual(record.readings[0], 273.15)
        self.assertEqual(record.scale, "kelvin")

        # Kelvin to Celsius
        record = TemperatureRecord("2025-04-01", [273.15], "kelvin")
        record.convert_to("celsius")
        self.assertAlmostEqual(record.readings[0], 0.0)
        self.assertEqual(record.scale, "celsius")

        # Kelvin to Fahrenheit
        record = TemperatureRecord("2025-04-01", [273.15], "kelvin")
        record.convert_to("fahrenheit")
        self.assertAlmostEqual(record.readings[0], 32.0)
        self.assertEqual(record.scale, "fahrenheit")

    def test_convert_to_same_scale(self):
        """Test convert_to method when target scale is the same."""
        record = TemperatureRecord("2025-04-01", [25.0], "celsius")
        original_readings = record.readings.copy()
        record.convert_to("celsius")
        self.assertEqual(record.readings, original_readings)
        self.assertEqual(record.scale, "celsius")

    def test_is_above_threshold(self):
        """Test is_above_threshold method."""
        record = TemperatureRecord("2025-04-01", [25.1, 25.5], "celsius")
        self.assertTrue(record.is_above_threshold(25.0))
        self.assertFalse(record.is_above_threshold(25.2))
        self.assertFalse(record.is_above_threshold(25.5))

    def test_is_at_or_above_threshold(self):
        """Test is_at_or_above_threshold method."""
        record = TemperatureRecord("2025-04-01", [25.0, 25.5], "celsius")
        self.assertTrue(record.is_at_or_above_threshold(25.0))
        self.assertTrue(record.is_at_or_above_threshold(24.9))
        self.assertFalse(record.is_at_or_above_threshold(25.1))

    def test_threshold_with_empty_readings(self):
        """Test threshold methods with empty readings."""
        record = TemperatureRecord("2025-04-01", [], "celsius")
        self.assertTrue(
            record.is_above_threshold(0)
        )  # All empty readings are above any threshold
        self.assertTrue(record.is_at_or_above_threshold(0))

    def test_average_temperature_across_days(self):
        """Test average temperature calculation."""
        records = [
            TemperatureRecord("day1", [10, 20], "celsius"),
            TemperatureRecord("day2", [30], "celsius"),
        ]
        self.assertEqual(average_temperature_across_days(records), 20.0)

    def test_average_temperature_empty_records(self):
        """Test average temperature with empty records."""
        self.assertEqual(average_temperature_across_days([]), 0)

    def test_average_temperature_mixed_scales(self):
        """Test average temperature with mixed temperature scales."""
        records = [
            TemperatureRecord("day1", [0], "celsius"),
            TemperatureRecord("day2", [32], "fahrenheit"),
            TemperatureRecord("day3", [273.15], "kelvin"),
        ]
        # All should be equivalent to 0°C
        self.assertAlmostEqual(average_temperature_across_days(records), 0.0)

    def test_hottest_day(self):
        """Test hottest day detection."""
        records = [
            TemperatureRecord("day1", [10, 12], "celsius"),
            TemperatureRecord("day2", [20, 22], "celsius"),
        ]
        self.assertEqual(hottest_day(records), "day2")

    def test_hottest_day_empty_records(self):
        """Test hottest day with empty records."""
        self.assertEqual(hottest_day([]), "")

    def test_hottest_day_mixed_scales(self):
        """Test hottest day with mixed temperature scales."""
        records = [
            TemperatureRecord("day1", [25], "celsius"),
            TemperatureRecord("day2", [77], "fahrenheit"),  # 25°C
            TemperatureRecord("day3", [298.15], "kelvin"),  # 25°C
        ]
        # All have same average, should return first one
        self.assertEqual(hottest_day(records), "day1")

    def test_detect_extreme_days(self):
        """Test extreme days detection."""
        records = [
            TemperatureRecord("day1", [10], "celsius"),
            TemperatureRecord("day2", [18], "celsius"),
        ]
        self.assertEqual(detect_extreme_days(records, 17), ["day2"])

    def test_detect_extreme_days_empty_records(self):
        """Test extreme days detection with empty records."""
        self.assertEqual(detect_extreme_days([], 30), [])

    def test_detect_extreme_days_boundary(self):
        """Test extreme days detection at boundary values."""
        records = [
            TemperatureRecord("day1", [25.0], "celsius"),
            TemperatureRecord("day2", [25.1], "celsius"),
        ]
        self.assertEqual(detect_extreme_days(records, 25.0), ["day2"])
        self.assertEqual(detect_extreme_days(records, 25.1), [])

    def test_temperature_range_for_each_day(self):
        """Test temperature range calculation."""
        records = [
            TemperatureRecord("day1", [5, 10], "celsius"),
            TemperatureRecord("day2", [15, 20], "celsius"),
        ]
        self.assertEqual(
            temperature_range_for_each_day(records), {"day1": (5, 10), "day2": (15, 20)}
        )

    def test_temperature_range_empty_records(self):
        """Test temperature range with empty records."""
        self.assertEqual(temperature_range_for_each_day([]), {})

    def test_temperature_range_single_reading(self):
        """Test temperature range with single reading per day."""
        records = [
            TemperatureRecord("day1", [25], "celsius"),
            TemperatureRecord("day2", [30], "celsius"),
        ]
        self.assertEqual(
            temperature_range_for_each_day(records),
            {"day1": (25, 25), "day2": (30, 30)},
        )

    def test_temperature_trend(self):
        """Test temperature trend analysis."""
        trend = temperature_trend([10, 12, 12, 8])
        self.assertEqual(trend, ["up", "same", "down"])

    def test_temperature_trend_empty_list(self):
        """Test temperature trend with empty list."""
        self.assertEqual(temperature_trend([]), [])

    def test_temperature_trend_single_value(self):
        """Test temperature trend with single value."""
        self.assertEqual(temperature_trend([25]), [])

    def test_temperature_trend_constant_values(self):
        """Test temperature trend with constant values."""
        self.assertEqual(temperature_trend([15, 15, 15]), ["same", "same"])

    def test_temperature_trend_alternating(self):
        """Test temperature trend with alternating values."""
        self.assertEqual(temperature_trend([10, 20, 10, 20]), ["up", "down", "up"])

    def test_detect_spike(self):
        """Test spike detection."""
        self.assertTrue(detect_spike([10, 20], threshold=5))
        self.assertFalse(detect_spike([10, 12], threshold=5))

    def test_detect_spike_default_threshold(self):
        """Test spike detection with default threshold."""
        self.assertTrue(detect_spike([10, 20]))  # Default threshold is 5
        self.assertFalse(detect_spike([10, 14]))  # Difference is 4, less than default 5

    def test_detect_spike_empty_list(self):
        """Test spike detection with empty list."""
        self.assertFalse(detect_spike([]))

    def test_detect_spike_single_value(self):
        """Test spike detection with single value."""
        self.assertFalse(detect_spike([25]))

    def test_detect_spike_negative_values(self):
        """Test spike detection with negative values."""
        self.assertTrue(detect_spike([-10, -20], threshold=5))
        self.assertTrue(detect_spike([10, -10], threshold=15))

    def test_detect_spike_exact_threshold(self):
        """Test spike detection at exact threshold."""
        self.assertTrue(detect_spike([10, 15], threshold=5))  # Exact threshold
        self.assertFalse(detect_spike([10, 14.9], threshold=5))  # Just below threshold


if __name__ == "__main__":
    unittest.main()
