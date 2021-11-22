from baby_recording.data_access import DataAccess
from baby_recording.records import BottleFeeding


class SaveBottleFeeding:
    def __init__(self, data_access: DataAccess, bottle_feeding: BottleFeeding):
        self.data_access = data_access
        self.bottle_feeding = bottle_feeding

    def execute(self):
        self.data_access.save_feedings(self.bottle_feeding)
