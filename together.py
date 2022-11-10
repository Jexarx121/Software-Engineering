from sensors import Sensor
from random import randint
from Ev import ElectricVehicle
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


class TemperatureSensor(Sensor):
  """represents a temperature sensor"""

  def readBattery(self, battery):
      return super().readBattery(battery)


class CurrentSensor(Sensor):
  """represents a current sensor"""

  def readBattery(self, battery):
      return super().readBattery(battery)


class VoltageSensor(Sensor):
  """represents a voltage sensor"""

  def __init__(self):
      super().__init__()

  def readBattery(self, battery):
      return super().readBattery(battery)


class BatteryCell:
  """represents a battery cell"""
# cells produce voltage , current, temperature which the sensors will read.
  id = 0
  def __init__(self):
      self._voltage = 0
      self._current = 0
      self._temperature = 0
      self._state = False
      self.id = BatteryCell.id
      BatteryCell.id += 1
      
  def getState(self):
      return self._state

  def setState(self, state):
      self._state = state


  def generateData(self, power):
      '''generate values for voltage, current and temperature'''
      pass


  state = property(getState, setState)
      
from battery import BatteryCell
from threading import Thread

class ElectricVehicle():
  """represents a electrical vehicle"""
  def __init__(self):
      self._state = False
      self._batteryCell = BatteryCell()
      self._mode = True
      self._lowMode = False

      # thread that simulates when running the vehicle
      # random values to simulate driving in various conditions
      # that dictate the amount of power drawn from batteries
      # depending on mode as well
      self._power = 0
      

  def getState(self):
      return self._state 

  def switchPowerState(self):
      if self._state:
          self._batteryCell.state = True
          return

      self._batteryCell.state = False
      
  def switchPowerMode(self):
    # Depending on the current power mode
    # The opposite will turn on
    # BMS then will limit the voltage, current and temperature of the cells
    # Load will be reduced
    # power will be reduced
    pass
      
  def run(self):
    # Display the UI that will show the attributes of the vehicle running
    # Tkinter display that will read attributes over time and display
    pass
    
  def charge(self):
    # SOC of vehicle will now start charging
    # EV power will reduce to zero or almost zero
    # SOC will be checked constantly and looped until a value reached
    # Trickling will then start to avoid discharging
    pass
    
  def power(self):
    pass
    # T

class BatteryManagementSystem:
  def __init__(self):
      # all the calculaions in here
      self.battery = Battery()
      self.odometer = Odometer()
      self.charger = Charger()
    
  
  def getStateOfCharge(self):
    '''calculate SOC of battery using either Coulomb counting or Kalman filtering'''
    pass
  
  def getStateOfHealth(self):
    '''calculate SOH of battery using algo involving internal resistance measurement, counting charge/discharge cycles, SOC'''
    
  def cooling(self):
    '''cool the battery(reduce temperature) if temperature is over limit'''
    pass
  
  def loadBalance(self):
    '''execute load balancing if load is unbalanced'''
    pass
  
  stateOfCharge = property(getStateOfCharge)
  stateOfHealth = property(getStateOfHealth)
  state = property(getState)
    