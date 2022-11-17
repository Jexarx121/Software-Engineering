from battery import BatteryCell
from currentSensor import CurrentSensor
from temperatureSensor import TemperatureSensor
<<<<<<< HEAD
from voltageSensor import VoltageSensor
=======
from  voltageSensor import VoltageSensor
>>>>>>> 739710a707871469ef13b0e173c03a70b5539b23

class BatteryModule:
    def __init__(self):
        self.batteryCell = BatteryCell()
        self.currentSensor = CurrentSensor()
        self.voltageSensor = VoltageSensor()
        self.temperatureSensor = TemperatureSensor()