from datetime import datetime

import pytest

from baby_recording import usecases, data_access


@pytest.fixture(name="db_sampled_feedings")
def fixture_db_sampled_feedings(sample_bottle_feedings, db_bottle_feedings):
    for sample in sample_bottle_feedings.get_all():
        uc = usecases.SaveBottleFeeding(data_access=db_bottle_feedings, bottle_feeding=sample)
        uc.execute()

def test_calculate_remaining_milk_to_drink():
    assert False
