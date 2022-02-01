import datetime
import typing

from loguru import logger

from WeekDayResolver.exceptions import (
    LeapYearException,
    IncorrectDateISOFormatException,
)
from WeekDayResolver.utils import is_leap_year


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
        self.year_provided = self.date_provided.split("-")[0]

    def calculate(self) -> typing.Optional[WDResolverAnswer]:
        try:
            year = int(self.year_provided)
            dt = datetime.date.fromisoformat(self.date_provided)
        except ValueError as e:
            if e.args[0].startswith("day") and not is_leap_year(year):
                logger.error(f"Date-object 'february tall-year' exception: {e}")
                raise LeapYearException
            else:
                logger.error(f"Date-object 'fromisoformat' exception: {e}")
                raise IncorrectDateISOFormatException

        else:
            weekday = dt.strftime("%U")
            if weekday != "00":
                weekday = int(weekday.lstrip("0")) + 1
            else:
                weekday = 1
            return WDResolverAnswer(weekday)
