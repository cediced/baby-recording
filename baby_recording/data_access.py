from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from baby_recording.bottle_feeding import BottleFeeding


class DataAccess(ABC):
    @abstractmethod
    def read(self, day: datetime):
        raise NotImplementedError

    @abstractmethod
    def save(self, feeding: BottleFeeding):
        raise NotImplementedError


class InMemoryBottleFeedingDb(DataAccess):
    def __init__(self):
        self.records: List[BottleFeeding] = []

    def read(self, day: datetime):
        return [record for record in self.records if
                record.get_date() == day]

    def save(self, feeding: BottleFeeding):
        self.records.append(feeding)
