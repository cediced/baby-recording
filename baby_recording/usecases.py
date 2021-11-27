import datetime

from baby_recording.data_access import DataAccess, InMemoryBottleFeedingDb
from baby_recording.bottle_feeding import BottleFeeding, QuantityDrunkChecker


class SaveBottleFeeding:
    def __init__(self, data_access: DataAccess, bottle_feeding: BottleFeeding):
        self.data_access = data_access
        self.bottle_feeding = bottle_feeding

    def execute(self):
        self.data_access.save(self.bottle_feeding)


def text_remaining_milk_to_drink(
        result: int):
    return f"{result['''remaining_milk''']} ml milk remains to drink for {result['''time''']}"


class ReportRemainingMilkToDrink:
    def __init__(self,
                 data_access: InMemoryBottleFeedingDb,
                 presenter,
                 time: datetime,
                 minimum_milk_quantity,
                 maximum_milk_quantity):
        self.data_access = data_access
        self.presenter = presenter
        self.time = time
        self.minimum_milk_quantity = minimum_milk_quantity
        self.maximum_milk_quantity = maximum_milk_quantity
        self.result = None

    def execute(self):
        result = {}
        feedings = self.data_access.read(day=self.time)
        checker = QuantityDrunkChecker(minimum_quantity=self.minimum_milk_quantity,
                                       maximum_quantity=self.maximum_milk_quantity,
                                       feedings=feedings)
        result["remaining_quantity"] = checker.calculate_quantity_drunk()
        result["time"] = self.time
