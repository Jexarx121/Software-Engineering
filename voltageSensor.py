from sensor import Sensor
from battery import BatteryCell

class VoltageSensor(Sensor):
    """repressents a voltage sensor"""

    def __init__(self):
        super().__init__()

    def readBattery(self, battery):
        return super().readBattery(battery)


if __name__ == "__main__":
    pass