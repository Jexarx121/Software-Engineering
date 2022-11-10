from abc import ABC, abstractmethod

class Sensor(ABC):
  """the abstract class that our 3 sensors(voltage,current,temperature) will inherit from"""

  def __init__(self):
        pass

  @abstractmethod
  def readBattery(self, battery):
    """each sensor reads the battery cell(s) and gets its respective value from the battery"""
    pass

  def processData(self):
    # From Jack's data flow diagram, the sensors do some basic processing
    # The sensors will check their respective values and check if they're within range
    # If outside range, raise a fault or alert the BMS
    pass

