from sensor import Sensor

class VoltageSensor(Sensor):
    """Repressents a voltage sensor for reading a battery cell's voltage."""

    def __init__(self):
        self._voltageValue = 0

    def readBattery(self, battery):
        self._voltageValue = battery.getVoltage()

    def getVoltageValue(self):
        return self._voltageValue

    voltageValue = property(getVoltageValue)