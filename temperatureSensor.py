from sensor import Sensor
from battery import BatteryCell

class TemperatureSensor(Sensor):
  """represents a temperature sensor"""

  def readBattery(self, battery):
      return super().readBattery(battery)


if __name__ == "__main__":
    pass