from battery import BatteryCell
from currentSensor import CurrentSensor
from temperatureSensor import TemperatureSensor
from  voltageSensor import VoltageSensor

class BatteryModule(object):
    def __init__(self, max_voltage, max_current):
        self.batteryCell = BatteryCell(max_voltage, max_current)
        self.currentSensor = CurrentSensor()
        self.voltageSensor = VoltageSensor()
        self.temperatureSensor = TemperatureSensor()