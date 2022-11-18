from sensor import Sensor
from battery import BatteryCell

class TemperatureSensor(Sensor):
  """represents a temperature sensor"""
  def __init__(self):
     self._temperatureValue = 0

  def readBattery(self, battery):
      self._temperatureValue = battery.getTemperature()

  def getTemperatureValue(self):
    return self._temperatureValue

  temperatureValue = property(getTemperatureValue)