from battery import BatteryCell
from currentSensor import CurrentSensor
from temperatureSensor import TemperatureSensor
from  voltageSensor import VoltageSensor

class BatteryModule(object):
    def __init__(self, max_voltage, max_current):
        self._batteryCell = BatteryCell(max_voltage, max_current)
        self._currentSensor = CurrentSensor()
        self._voltageSensor = VoltageSensor()
        self._temperatureSensor = TemperatureSensor()
        
    def getBatteryCell(self):
        return self._batteryCell

    def getCurrentSensor(self):
        return self._currentSensor

    def getVoltageSensor(self):
        return self._voltageSensor

    def getTemperatureSensor(self):
        return self._temperatureSensor

    batteryCell = property(getBatteryCell)
    currentSensor = property(getCurrentSensor)
    voltageSensor = property(getVoltageSensor)
    temperatureSensor = property(getTemperatureSensor)