from datetime import datetime

import pytest

from baby_recording import records, data_access, usecases


@pytest.fixture(name="bottle_feeding_1")
def fixture_bottle_feeding_1():
    time = datetime(year=2021, month=12, day=21, hour=8, minute=30)
    return records.BottleFeeding(time=time, milk_remained=10, total_water=120, total_spoons=4)


@pytest.fixture(name="db_bottle_feedings")
def fixture_db_bottle_feedings():
    return data_access.InMemoryBottleFeedingDb()


def test_save_feedings(bottle_feeding_1, db_bottle_feedings):
    uc = usecases.SaveBottleFeeding(data_access=db_bottle_feedings, bottle_feeding=bottle_feeding_1)
    uc.execute()

    feedings = db_bottle_feedings.read_feedings(day=datetime(year=2021, month=12, day=21))
    assert bottle_feeding_1 in feedings


def test_save_and_read_two_feeding():
    pass

# save different feedings for different days and read one day, only the feedings for that day should come
# test if wrong type for save feeding
