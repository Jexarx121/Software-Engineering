from abc import ABC, abstractmethod

class Sensor(ABC):
  """The abstract class that our 3 sensors(voltage,current,temperature) will inherit from."""

  @abstractmethod
  def readBattery(self, battery):
    """Each sensor reads the battery cell and gets its respective value from the battery"""
    pass


