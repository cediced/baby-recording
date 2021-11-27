from abc import ABC
from datetime import datetime, timedelta
from typing import List


class Record(ABC):
    def __init__(self, time: datetime):
        self.time = time

    def get_date(self):
        return datetime(self.time.year, self.time.month, self.time.day)


class BottleFeeding(Record):
    def __init__(self, time: datetime, total_milk, remaining_milk):
        super().__init__(time)
        self.time = time

        if remaining_milk >= total_milk:
            raise RemainingMilkHigherThanTotalError

        self.remaining_milk = remaining_milk
        self.total_milk = total_milk

    def __eq__(self, other):
        return self.time == other.time \
               and self.remaining_milk == other.remaining_milk

    def get_total_milk_drunk(self):
        return self.total_milk - self.remaining_milk


class RemainingMilkHigherThanTotalError(Exception):
    pass


def assert_max_higher_than_min(min, max):
    assert min < max, f"minimum {min} is higher than maximum allowed {max}"


class QuantityDrunkChecker:
    def __init__(self, minimum_quantity, maximum_quantity, feedings: List[BottleFeeding]):
        assert_max_higher_than_min(minimum_quantity, maximum_quantity)
        self.minimum_quantity = minimum_quantity
        self.maximum_quantity = maximum_quantity
        self.feedings = feedings

    def calculate_quantity_drunk(self):
        return sum([feeding.get_total_milk_drunk() for feeding in self.feedings])

    def remaining_quantity(self):
        return self.maximum_quantity - self.calculate_quantity_drunk()

    def minimum_reached(self):
        return self.minimum_quantity < self.calculate_quantity_drunk()

    def maximum_reached(self):
        return self.calculate_quantity_drunk() > self.maximum_quantity


class NextTime:
    def __init__(self, minimum_hours: int, maximum_hours: int, last_time: datetime):
        assert_max_higher_than_min(minimum_hours, maximum_hours)
        self.minimum_hours = minimum_hours
        self.maximum_hours = maximum_hours
        self.last_time = last_time
        self.from_time = None
        self.to_time = None

    def diff_in_hours(self, time_now):
        diff = time_now - self.last_time
        in_seconds = diff.total_seconds()
        in_hours = in_seconds / 3600
        return in_hours

    def is_allowed(self, time_now: datetime):
        return self.diff_in_hours(time_now) > self.minimum_hours

    def is_max_over(self, time_now):
        return self.diff_in_hours(time_now) > self.maximum_hours

    def calculate(self):
        self.from_time = self.last_time + timedelta(hours=self.minimum_hours)
        self.to_time = self.last_time + timedelta(hours=self.maximum_hours)
