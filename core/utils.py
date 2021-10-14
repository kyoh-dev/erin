from datetime import datetime


def date_display_fmt(date_string: str) -> str:
    return datetime.strptime(date_string, "%Y%m%d").strftime("%d/%m/%Y")


def date_storage_fmt() -> str:
    ...
