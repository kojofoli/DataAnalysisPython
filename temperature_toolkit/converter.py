def convert(value: float, original_scale: str, target_scale: str) -> float:
    """
    Convert a temperature value from one scale to another.

    Args:
        value (float): The temperature value to convert.
        original_scale (str): The original scale ('celsius', 'fahrenheit', 'kelvin').
        target_scale (str): The target scale ('celsius', 'fahrenheit', 'kelvin').

    Returns:
        float: The converted temperature value, rounded to 2 decimal places.

    Raises:
        ValueError: If the original or target scale is invalid.
    """
    # Normalize scale names for case-insensitive comparison
    original_scale = original_scale.lower()
    target_scale = target_scale.lower()

    # Valid temperature scales
    valid_scales = ["celsius", "fahrenheit", "kelvin"]

    # Validate input scales
    if original_scale not in valid_scales:
        raise ValueError(
            f"Invalid original scale: {original_scale}. Use 'celsius', 'fahrenheit', or 'kelvin'."
        )
    if target_scale not in valid_scales:
        raise ValueError(
            f"Invalid target scale: {target_scale}. Use 'celsius', 'fahrenheit', or 'kelvin'."
        )

    # No conversion needed if scales are the same
    if original_scale == target_scale:
        return round(value, 2)

    # Step 1: Convert original value to Celsius
    if original_scale == "fahrenheit":
        celsius = (value - 32) * 5 / 9
    elif original_scale == "kelvin":
        celsius = value - 273.15
    else:  # original_scale == 'celsius'
        celsius = value

    # Step 2: Convert Celsius to target scale
    if target_scale == "fahrenheit":
        converted_value = celsius * 9 / 5 + 32
    elif target_scale == "kelvin":
        converted_value = celsius + 273.15
    else:  # target_scale == 'celsius'
        converted_value = celsius

    return round(converted_value, 2)
