from decimal import Decimal, InvalidOperation


def parse_integer_at_least(value, field_name, minimum=0):
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise ValueError(f"{field_name} debe ser un número entero válido.")
    try:
        parsed_value = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} debe ser un número entero válido.") from None

    if parsed_value < minimum:
        raise ValueError(f"{field_name} no puede ser menor que {minimum}.")
    return parsed_value


def parse_decimal_at_least(value, field_name, minimum=0, maximum=None):
    try:
        parsed_value = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        raise ValueError(f"{field_name} debe ser un número válido.") from None

    if not parsed_value.is_finite() or parsed_value < minimum:
        raise ValueError(f"{field_name} no puede ser menor que {minimum}.")
    if maximum is not None and parsed_value > maximum:
        raise ValueError(f"{field_name} no puede ser mayor que {maximum}.")
    return parsed_value
