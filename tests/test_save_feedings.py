from datetime import datetime
from baby_recording import records, data_access, usecases


def test_save_feedings():
    time = datetime(year=2021, month=12, day=21, hour=8, minute=30)
    bottle_feeding = records.BottleFeeding(time=time, milk_remained=10, total_water=120, total_spoons=4)
    db = data_access.InMemoryDb()

    uc = usecases.SaveBottleFeeding(data_access=db, bottle_feeding=bottle_feeding)
    uc.execute()

    feedings = db.read_feedings(day=datetime(year=2021, month=12, day=21))
    assert bottle_feeding in feedings

# test if wrong type for save feeding
