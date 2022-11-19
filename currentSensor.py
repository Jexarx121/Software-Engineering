from sensor import Sensor

class CurrentSensor(Sensor):
  """Represents a current sensor for reading a battery cell's current."""

  def __init__(self):
     self._currentValue = 0

  def readBattery(self, battery):
      self._currentValue = battery.getCurrent()

  def getCurrentValue(self):
    return self._currentValue

  currentValue = property(getCurrentValue)