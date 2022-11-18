from sensor import Sensor
from battery import BatteryCell

class VoltageSensor(Sensor):
    """repressents a voltage sensor"""

    def __init__(self):
        self._voltageValue = 0

    def readBattery(self, battery):
        self._voltageValue = battery.getVoltage()

    def getVoltageValue(self):
        return self._voltageValue

    voltageValue = property(getVoltageValue)