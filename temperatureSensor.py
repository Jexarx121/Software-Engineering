from sensor import Sensor

class TemperatureSensor(Sensor):
  """represents a temperature sensor"""

  def readBattery(self, battery):
      return super().readBattery(battery)


if __name__ == "__main__":
    pass