from dataclasses import dataclass
from datetime import datetime
from typing import List

import pytest

from baby_recording import bottle_feeding, data_access, usecases
from baby_recording.bottle_feeding import BottleFeeding, RemainingMilkHigherThanTotalError, QuantityDrunkChecker, \
    NextTime


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


def get_quantity_checker(feedings: List[BottleFeeding]):
    return QuantityDrunkChecker(minimum_quantity=100, maximum_quantity=300, feedings=feedings)


def test_save_feedings(bottle_feeding_1, db_bottle_feedings):
    uc = usecases.SaveBottleFeeding(data_access=db_bottle_feedings, bottle_feeding=bottle_feeding_1)
    uc.execute()

    feedings = db_bottle_feedings.read(day=datetime(year=2021, month=12, day=21))
    assert bottle_feeding_1 in feedings


def test_save_and_read_two_feeding(sample_bottle_feedings, db_bottle_feedings):
    for sample in sample_bottle_feedings.get_all():
        uc = usecases.SaveBottleFeeding(data_access=db_bottle_feedings, bottle_feeding=sample)
        uc.execute()

    feedings = db_bottle_feedings.read(sample_bottle_feedings.same_day[0].get_date())
    assert len(feedings) == len(sample_bottle_feedings.same_day)
    assert feedings == sample_bottle_feedings.same_day


def test_get_right_total_milk_from_formula(bottle_feeding_1):
    result = bottle_feeding_1.get_total_milk_drunk()
    assert result == bottle_feeding_1.total_milk - bottle_feeding_1.remaining_milk


def test_throw_exception_if_remaining_is_higher_than_total_milk(arbitrary_time):
    with pytest.raises(RemainingMilkHigherThanTotalError):
        BottleFeeding(time=arbitrary_time, total_milk=120, remaining_milk=120)


def test_quantity_of_milk_today(sample_bottle_feedings):
    should_quantity_drunk = sample_bottle_feedings.get_total_milk_drunk_same_day()
    checker = get_quantity_checker(feedings=sample_bottle_feedings.same_day)
    result = checker.calculate_quantity_drunk()
    assert result == should_quantity_drunk


def test_the_remaining_quantity_of_milk(sample_bottle_feedings):
    checker = QuantityDrunkChecker(minimum_quantity=100, maximum_quantity=300, feedings=sample_bottle_feedings.same_day)
    assert checker.remaining_quantity() == 50  # max 300 - drunk 250
    assert checker.minimum_reached()
    assert not checker.maximum_reached()


def test_next_feeding_time_not_reached(sample_bottle_feedings):
    nft = NextTime(minimum_hours=3, maximum_hours=4,
                   last_time=datetime(year=2021, month=12, day=21, hour=8, minute=30))
    time_now = datetime(year=2021, month=12, day=21, hour=8, minute=30)
    assert not nft.is_allowed(time_now=time_now)


def test_next_feeding_time_reached(sample_bottle_feedings):
    hour = 8
    minimum_time = 3
    nft = NextTime(minimum_hours=3, maximum_hours=4,
                   last_time=datetime(year=2021, month=12, day=21, hour=hour, minute=00))
    time_now = datetime(year=2021, month=12, day=21, hour=hour + minimum_time + 1, minute=30)
    assert nft.diff_in_hours(time_now=time_now) == 4.5
    assert nft.is_allowed(time_now=time_now)
    assert nft.is_max_over(time_now=time_now)


def test_next_time_action_needs_t_be_performed():
    hour = 22
    minimum_time = 3
    nft = NextTime(minimum_hours=3, maximum_hours=4,
                   last_time=datetime(year=2021, month=12, day=21, hour=hour, minute=00))
    nft.calculate()
    assert nft.from_time == datetime(year=2021, month=12, day=22, hour=1, minute=00)
    assert nft.to_time == datetime(year=2021, month=12, day=22, hour=2, minute=00)

# save different feedings for different days and read one day, only the feedings for that day should come
# test if wrong type for save feeding
