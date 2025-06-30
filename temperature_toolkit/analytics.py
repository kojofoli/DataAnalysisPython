from typing import List, Dict, Tuple
from .converter import convert
from .record import TemperatureRecord


def average_temperature_across_days(records: List[TemperatureRecord]) -> float:
    """
    Calculate the average temperature across all days and readings.

    Args:
        records (List[TemperatureRecord]): List of TemperatureRecord objects.

    Returns:
        float: Average temperature rounded to 2 decimals, or 0 if no readings.
    """
    all_readings = [temp for record in records for temp in record.readings]
    return round(sum(all_readings) / len(all_readings), 2) if all_readings else 0


def hottest_day(records: List[TemperatureRecord]) -> str:
    """
    Find the date with the highest average temperature (in Celsius).

    Args:
        records (List[TemperatureRecord]): List of TemperatureRecord objects.

    Returns:
        str: Date string of the hottest day, or '' if records is empty.
    """
    if not records:
        return ""

    def avg_in_celsius(record: TemperatureRecord) -> float:
        if not record.readings:
            return float("-inf")
        temps_c = [convert(t, record.scale, "celsius") for t in record.readings]
        return sum(temps_c) / len(temps_c)

    return max(records, key=avg_in_celsius).date


def detect_extreme_days(
    records: List[TemperatureRecord], threshold: float
) -> List[str]:
    """
    Detect days where any reading exceeds the given threshold.

    Args:
        records (List[TemperatureRecord]): List of TemperatureRecord objects.
        threshold (float): Temperature threshold.

    Returns:
        List[str]: Dates where any reading is above the threshold.
    """
    return [
        record.date
        for record in records
        if any(temp > threshold for temp in record.readings)
    ]


def temperature_range_for_each_day(
    records: List[TemperatureRecord],
) -> Dict[str, Tuple[float, float]]:
    """
    Get the min and max temperature for each day.

    Args:
        records (List[TemperatureRecord]): List of TemperatureRecord objects.

    Returns:
        Dict[str, Tuple[float, float]]: Mapping of date to (min, max) temperature tuple (rounded to 2 decimals).
    """
    result: Dict[str, Tuple[float, float]] = {}
    for record in records:
        if record.readings:
            result[record.date] = (
                round(min(record.readings), 2),
                round(max(record.readings), 2),
            )
        else:
            result[record.date] = (0, 0)
    return result


def temperature_trend(temps: List[float]) -> List[str]:
    """
    Analyze the trend between consecutive temperature readings.

    Args:
        temps (List[float]): List of temperature values.

    Returns:
        List[str]: List of 'up', 'down', or 'same' indicating trend between readings.
    """
    if len(temps) < 2:
        return []
    trend: List[str] = []
    for i in range(1, len(temps)):
        if temps[i] > temps[i - 1]:
            trend.append("up")
        elif temps[i] < temps[i - 1]:
            trend.append("down")
        else:
            trend.append("same")
    return trend


def detect_spike(temps: List[float], *, threshold: float = 5) -> bool:
    """
    Detect if there is a temperature spike between consecutive readings.

    Args:
        temps (List[float]): List of temperature values.
        threshold (float, optional): Minimum difference to consider as a spike. Defaults to 5.

    Returns:
        bool: True if a spike is detected, False otherwise.
    """
    for i in range(1, len(temps)):
        if abs(temps[i] - temps[i - 1]) >= threshold:
            return True
    return False
