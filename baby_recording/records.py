from abc import ABC
from datetime import datetime
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


class QuantityDrunkChecker:
    def __init__(self, minimum_quantity, maximum_quantity, feedings: List[BottleFeeding]):
        assert minimum_quantity < maximum_quantity, f"minimum milk {minimum_quantity} is higher than maximum allowed {maximum_quantity}"
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
