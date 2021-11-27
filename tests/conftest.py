from dataclasses import dataclass
from datetime import datetime
from typing import List

import pytest

from baby_recording import data_access, bottle_feeding
from baby_recording.bottle_feeding import BottleFeeding


@dataclass
class SampleBottleFeedings:
    same_day: List[BottleFeeding]
    others: List[BottleFeeding]

    def get_all(self):
        together = []
        together.extend(self.same_day)
        together.extend(self.others)
        return together

    def get_total_milk_drunk_same_day(self):
        return sum([feeding.get_total_milk_drunk() for feeding in self.same_day])


@pytest.fixture(name="arbitrary_time")
def fixture_arbitrary_time():
    return datetime(year=2021, month=12, day=21, hour=8, minute=30)


@pytest.fixture(name="bottle_feeding_1")
def fixture_bottle_feeding_1() -> BottleFeeding:
    time = datetime(year=2021, month=12, day=21, hour=8, minute=30)
    return BottleFeeding(time=time, total_milk=120, remaining_milk=10)


@pytest.fixture(name="db_bottle_feedings")
def fixture_db_bottle_feedings():
    return data_access.InMemoryBottleFeedingDb()


@pytest.fixture(name="sample_bottle_feedings")
def fixture_sample_bottle_feedings():
    same_day = []
    others = []
    same_day.append(
        bottle_feeding.BottleFeeding(time=datetime(year=2021, month=12, day=21, hour=8, minute=30),
                                     total_milk=135,
                                     remaining_milk=10))
    same_day.append(
        bottle_feeding.BottleFeeding(time=datetime(year=2021, month=12, day=21, hour=11, minute=30),
                                     total_milk=135,
                                     remaining_milk=10))

    others.append(
        bottle_feeding.BottleFeeding(time=datetime(year=2021, month=12, day=20, hour=8, minute=30),
                                     total_milk=135,
                                     remaining_milk=10)
    )
    others.append(
        bottle_feeding.BottleFeeding(time=datetime(year=2021, month=12, day=20, hour=11, minute=30),
                                     total_milk=135,
                                     remaining_milk=10))
    return SampleBottleFeedings(same_day=same_day, others=others)
