from abc import ABC
from datetime import datetime


class Record(ABC):
    def __init__(self, time: datetime):
        self.time = time

    def get_date(self):
        return datetime(self.time.year, self.time.month, self.time.day)


class BottleFeeding(Record):
    def __init__(self, time: datetime, milk_remained, total_water, total_spoons):
        super().__init__(time)
        self.time = time
        self.milk_remained = milk_remained
        self.total_water = total_water
        self.total_spoons = total_spoons

    def __eq__(self, other):
        return self.time == other.time \
               and self.milk_remained == other.milk_remained \
               and self.total_water == other.total_water \
               and self.total_spoons == other.total_spoons
