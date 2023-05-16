import re
from datetime import datetime


def is_number(input: str) -> bool:
    return input.isdigit()


def is_valid_date(input: str, date_format: str):
    try:
        datetime.strptime(input, date_format)
        return True
    except ValueError:
        return False


def is_date(input: str) -> bool:
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    return bool(re.match(pattern, input))


def is_alphanumeric(input: str) -> bool:
    pattern = r'^[A-Za-z0-9]+$'
    return bool(re.match(pattern, input))
