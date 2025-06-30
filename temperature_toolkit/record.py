from typing import List, Dict, Any


class TemperatureRecord:
    def __init__(self, date: str, readings: List[float], scale: str) -> None:
        """
        Initialize a TemperatureRecord with a date, list of readings, and temperature scale.

        Args:
            date (str): The date of the record.
            readings (List[float]): List of temperature readings.
            scale (str): The temperature scale ('celsius', 'fahrenheit', 'kelvin').
        """
        self.date = date
        self.readings = readings
        self.scale = scale.lower()  # Store scale in lowercase for consistency

    def convert_to(self, target_scale: str) -> None:
        """
        Convert all readings to the target temperature scale.

        Args:
            target_scale (str): The target temperature scale ('celsius', 'fahrenheit', 'kelvin').
        """
        from .converter import convert

        target_scale = target_scale.lower()
        if target_scale == self.scale:
            return  # No conversion needed if already in target scale
        self.readings = [
            convert(temp, self.scale, target_scale) for temp in self.readings
        ]
        self.scale = target_scale  # Update the scale

    def get_summary(self) -> Dict[str, Any]:
        """
        Return a summary dictionary with date, scale, min, max, and average of readings.

        Returns:
            Dict[str, Any]: Summary with keys 'date', 'scale', 'min', 'max', 'avg'.
        """
        if not self.readings:
            return {
                "date": self.date,
                "scale": self.scale,
                "min": 0,
                "max": 0,
                "avg": 0,
            }
        return {
            "date": self.date,
            "scale": self.scale,
            "min": round(min(self.readings), 2),
            "max": round(max(self.readings), 2),
            "avg": round(sum(self.readings) / len(self.readings), 2),
        }

    def is_above_threshold(self, threshold: float) -> bool:
        """
        Check if all readings are strictly above the given threshold.

        Args:
            threshold (float): The threshold value.

        Returns:
            bool: True if all readings are above the threshold, False otherwise.
        """
        return all(temp > threshold for temp in self.readings)

    def is_at_or_above_threshold(self, threshold: float) -> bool:
        """
        Check if all readings are at or above the given threshold.

        Args:
            threshold (float): The threshold value.

        Returns:
            bool: True if all readings are at or above the threshold, False otherwise.
        """
        return all(temp >= threshold for temp in self.readings)
