def parse_float(value : str) -> float:
    if value in ('-', '*', ' ', '/', '+'):
        return 0.0

    try:
        parts = value.split('.')
        
        if len(parts) > 1:
            integer_part = ''.join(parts[:-1])
            decimal_part = parts[-1]
            new_value = f"{integer_part}.{decimal_part}"
        else:
            new_value = value
        
        return float(new_value)
    except ValueError:
        return 0.0