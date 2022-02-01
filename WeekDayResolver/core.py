import datetime
import typing

from loguru import logger


class WDResolverAnswer:
    """
    Wrapper around WDResolver calculation result
    """

    def __init__(self, result):
        self.week_number = result


class WDResolver:
    """
    Calculates the number of the given day of the week with Sunday as first day of the week
    """
    def __init__(self, date_provided: str):
        self.date_provided = date_provided

    def calculate(self) -> typing.Optional[WDResolverAnswer]:
        try:
            dt = datetime.date.fromisoformat(self.date_provided)
        except ValueError as e:
            logger.error(f"Date-object 'fromisoformat' exception: {e}")
            return
        else:
            weekday = dt.strftime("%U")
            if weekday != "00":
                weekday = int(weekday.lstrip("0")) + 1
            else:
                weekday = 1
            return WDResolverAnswer(weekday)
