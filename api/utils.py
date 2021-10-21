from typing import Union


def collect_assignees(assignee_list: list[Union[str, None]]) -> str:
    return ', '.join(filter(None, assignee_list))
