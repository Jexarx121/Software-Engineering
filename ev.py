from battery import BatteryCell
from threading import Thread

class ElectricVehicle():
  """represents a electrical vehicle"""
  def __init__(self):
      self._state = False
      self._batteryCell = BatteryCell()
      self._mode = True
      self._lowMode = False

      # one type of vehicle so the ranges are fixed

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