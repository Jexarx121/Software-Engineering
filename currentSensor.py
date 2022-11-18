from sensor import Sensor
from battery import BatteryCell

class CurrentSensor(Sensor):
  """represents a current sensor"""

  def __init__(self):
     self._currentValue = 0

  def readBattery(self, battery):
      self._currentValue = battery.getCurrent()

  def getCurrentValue(self):
    return self._currentValue

  currentValue = property(getCurrentValue)