from temperature_toolkit.record import TemperatureRecord
from temperature_toolkit.analytics import (
    average_temperature_across_days,
    hottest_day,
    detect_extreme_days,
    temperature_range_for_each_day,
    temperature_trend,
    detect_spike,
)
from temperature_toolkit.converter import convert


def create_sample_records():
    return [
        TemperatureRecord(
            "2025-04-27", [14.2, 15.0, 13.8, 14.5, 15.1, 17.0], "celsius"
        ),
        TemperatureRecord(
            "2025-04-28", [17.1, 18.5, 16.4, 17.0, 18.0, 16.8], "celsius"
        ),
        TemperatureRecord("2025-04-29", [11.0, 9.5, 12.2, 10.0, 11.3, 10.7], "celsius"),
        TemperatureRecord(
            "2025-04-30", [20.0, 21.5, 19.8, 20.2, 21.0, 15.5], "celsius"
        ),
        TemperatureRecord("2025-05-01", [22.0, 23.5, 21.8, 22.2, 23.0], "celsius"),
        TemperatureRecord("2025-05-02", [25.0, 26.5, 24.8, 25.2, 26.0], "celsius"),
        TemperatureRecord(
            "2025-05-03", [20.0, 27.0, 28.5, 26.8, 27.2, 28.0], "celsius"
        ),
        TemperatureRecord(
            "2025-05-05", [295.52, 296.94, 298.8, 303.1, 302.27, 302.64], "kelvin"
        ),
    ]


def convert_sample_records(records):
    print("\nConverting Day 1 from Celsius to Fahrenheit...")
    records[0].convert_to("fahrenheit")
    print(records[0].get_summary())

    print("\nConverting Day 2 from Celsius to Kelvin...")
    records[1].convert_to("kelvin")
    print(records[1].get_summary())

    print("\nConverting Day 8 from Kelvin to Celsius...")
    records[7].convert_to("celsius")
    print(records[7].get_summary())

    print("\nConverting Day 8 from Celsius to Fahrenheit...")
    records[7].convert_to("fahrenheit")
    print(records[7].get_summary())


def display_summaries(records):
    for r in records:
        print(r.get_summary())


def analytics_demo(records):
    print(
        "\nAverage temperature across all days:",
        average_temperature_across_days(records),
    )
    print("Hottest day:", hottest_day(records))
    print("Extreme days above 20.5°C:", detect_extreme_days(records, 20.5))
    print("Daily temperature ranges:", temperature_range_for_each_day(records))
    print("\nTemperature trend for day4:", temperature_trend(records[3].readings))
    print("Spike detected in day7:", detect_spike(records[6].readings, threshold=3.0))


def additional_tests():
    # Empty readings test
    empty_day = TemperatureRecord("2025-05-01", [], "celsius")
    print("\nEmpty day summary:", empty_day.get_summary())

    # Kelvin to Celsius test
    kelvin_day = TemperatureRecord(
        "2025-05-01", [300.15, 295.15, 310.15, 250.30], "kelvin"
    )
    kelvin_day.convert_to("celsius")
    print("Kelvin to Celsius summary:", kelvin_day.get_summary())

    # is_above_threshold edge values
    boundary_day = TemperatureRecord("2025-05-02", [25.0, 25.0, 25.0], "celsius")
    for threshold in [24.9, 25.0, 25.1]:
        result = boundary_day.is_above_threshold(threshold)
        print(
            f"Threshold = {threshold} → is_above_threshold = {result} | Readings = {boundary_day.readings}"
        )

    # convert() same unit
    print("Convert Celsius to Celsius (100°C):", convert(100, "celsius", "celsius"))

    # convert() with unsupported unit
    try:
        convert(100, "Kojo", "celsius")
    except ValueError as e:
        print("Unsupported unit error caught:", e)

    # Empty list to analytics
    print("Average from no records:", average_temperature_across_days([]))
    print("Hottest day from no records:", hottest_day([]))
    print("Extreme days from no records:", detect_extreme_days([], 30))
    print("Range per day with no records:", temperature_range_for_each_day([]))

    # Single-value reading
    single_temp_day = TemperatureRecord("2025-05-03", [22.5], "celsius")
    print("Single-reading summary:", single_temp_day.get_summary())

    # detect_spike default threshold
    print("Spike detected (default threshold):", detect_spike([20.0, 20.1, 30.5]))

    # temperature_trend with constant readings
    print("Trend with constant values:", temperature_trend([15.0, 15.0, 15.0]))


def main():
    records = create_sample_records()
    convert_sample_records(records)
    display_summaries(records)
    analytics_demo(records)
    additional_tests()
    print("\nAll tests completed successfully.")


if __name__ == "__main__":
    main()
