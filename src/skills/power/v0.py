def calculate_power(base, exponent):
    """
    Purpose:
    Calculate the power of a given base raised to a given exponent.

    Args:
    base (int, float): The base number.
    exponent (int): The exponent value.

    Returns:
    int, float: The result of raising base to the power of exponent.

    Example Usage:
    calculate_power(2, 10) # Returns 1024
    """
    return base ** exponent

result = calculate_power(4, 13)
print(f"4 to the power of 13 is {result}")