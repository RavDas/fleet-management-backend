from datetime import date, datetime

def validate_date(date_str):
    """Validate date string format"""
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        raise ValueError('Invalid date format. Expected YYYY-MM-DD')

def validate_mileage(current, due):
    """Validate mileage values"""
    if current < 0 or due < 0:
        raise ValueError('Mileage values must be non-negative')
    if due < current:
        raise ValueError('Due mileage must be greater than or equal to current mileage')
    return True