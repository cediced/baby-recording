from dataclasses import dataclass
import dataclasses
from datetime import datetime
from typing import List

import pytest

from baby_recording import records, data_access, usecases


@dataclass
class SampleBottleFeedings:
    same_day: List[records.BottleFeeding]
    others: List[records.BottleFeeding]

    def get_all(self):
        together = []
        together.extend(self.same_day)
        together.extend(self.others)
        return together


@pytest.fixture(name="bottle_feeding_1")
def fixture_bottle_feeding_1():
    time = datetime(year=2021, month=12, day=21, hour=8, minute=30)
    return records.BottleFeeding(time=time, milk_remained=10, total_water=120, total_spoons=4)


@pytest.fixture(name="db_bottle_feedings")
def fixture_db_bottle_feedings():
    return data_access.InMemoryBottleFeedingDb()


@pytest.fixture(name="sample_bottle_feedings")
def fixture_sample_bottle_feedings():
    same_day = []
    others = []
    same_day.append(
        records.BottleFeeding(time=datetime(year=2021, month=12, day=21, hour=8, minute=30), milk_remained=10,
                              total_water=120, total_spoons=4))
    same_day.append(
        records.BottleFeeding(time=datetime(year=2021, month=12, day=21, hour=11, minute=30), milk_remained=10,
                              total_water=120, total_spoons=4))

    others.append(
        records.BottleFeeding(time=datetime(year=2021, month=12, day=20, hour=8, minute=30), milk_remained=10,
                              total_water=120, total_spoons=4))
    others.append(
        records.BottleFeeding(time=datetime(year=2021, month=12, day=20, hour=11, minute=30), milk_remained=10,
                              total_water=120, total_spoons=4))
    return SampleBottleFeedings(same_day=same_day, others=others)


def test_save_feedings(bottle_feeding_1, db_bottle_feedings):
    uc = usecases.SaveBottleFeeding(data_access=db_bottle_feedings, bottle_feeding=bottle_feeding_1)
    uc.execute()

    feedings = db_bottle_feedings.read_feedings(day=datetime(year=2021, month=12, day=21))
    assert bottle_feeding_1 in feedings


def test_save_and_read_two_feeding(sample_bottle_feedings, db_bottle_feedings):
    for sample in sample_bottle_feedings.get_all():
        uc = usecases.SaveBottleFeeding(data_access=db_bottle_feedings, bottle_feeding=sample)
        uc.execute()

    feedings = db_bottle_feedings.read_feedings(sample_bottle_feedings.same_day[0].get_date())
    assert len(feedings) == len(sample_bottle_feedings.same_day)
    assert feedings == sample_bottle_feedings.same_day

# save different feedings for different days and read one day, only the feedings for that day should come
# test if wrong type for save feeding
