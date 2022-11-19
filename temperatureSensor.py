from sensor import Sensor

class TemperatureSensor(Sensor):
  """Represents a temperature sensor for reading battery cell's temperature."""

  def __init__(self):
     self._temperatureValue = 0

  def readBattery(self, battery):
      self._temperatureValue = battery.getTemperature()

  def getTemperatureValue(self):
    return self._temperatureValue

  temperatureValue = property(getTemperatureValue)