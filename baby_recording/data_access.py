from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

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
        self.data: List[BottleFeeding] = []

    def read_feedings(self, day: datetime):
        return [feeding for feeding in self.data if
                feeding.get_date() == day]

    def save_feedings(self, feeding: BottleFeeding):
        self.data.append(feeding)
