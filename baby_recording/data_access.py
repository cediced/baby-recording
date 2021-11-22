from abc import ABC, abstractmethod
from datetime import datetime
from baby_recording.records import BottleFeeding


class DataAccess(ABC):
    @abstractmethod
    def read_feedings(self, day: datetime):
        raise NotImplementedError

    @abstractmethod
    def save_feedings(self, feeding: BottleFeeding):
        raise NotImplementedError


class InMemoryDb(DataAccess):
    def __init__(self):
        self.data = []

    def read_feedings(self, day: datetime):
        return [feeding for feeding in self.data if
                feeding.time.day == day.day and feeding.time.year == day.year and feeding.time.month == day.month]

    def save_feedings(self, feeding: BottleFeeding):
        self.data.append(feeding)
