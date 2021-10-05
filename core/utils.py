from datetime import datetime


def parse_date_string(date_string: str) -> str:
    return datetime.strptime(date_string, '%Y%m%d').strftime('%d/%m/%Y')
