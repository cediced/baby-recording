from datetime import datetime

from baby_recording import usecases


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
