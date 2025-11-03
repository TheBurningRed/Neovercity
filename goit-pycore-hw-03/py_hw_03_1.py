from datetime import datetime, date

def get_days_from_today(date_string: str) -> int:
    try:
        date_parsed = datetime.strptime(date_string, '%Y-%m-%d').date()
    except ValueError:
        print('Failed to parse date string')
        return None

    diff = date_parsed - date.today()
    return diff.days

print(get_days_from_today('2025-10-25'))