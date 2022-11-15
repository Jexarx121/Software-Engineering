from battery import BatteryCell
from currentSensor import CurrentSensor
from temperatureSensor import TemperatureSensor
from  voltageSensor import VoltageSensor

class BatteryModule:
    def __init__(self):
        self.batteryCell = BatteryCell()
        self.currentSensor = CurrentSensor()
        self.voltageSensor = VoltageSensor()
        self.temperatureSensor = TemperatureSensor()