from battery import BatteryCell
from ui import UI
from random import randint
from odometer import Odometer
from bms import BatteryManagementSystem

class ElectricVehicle():
  """represents an electrical vehicle"""

  NUMBER_OF_BATTERIES = 8

  def __init__(self):
      self._powerState = False
      self._lowPowerMode = False
      self._draw = 0
      self._battery = [BatteryCell()]  * ElectricVehicle.NUMBER_OF_BATTERIES
      self._odometer = Odometer()
      self._bms = BatteryManagementSystem()
      self._ui = UI()
      self._charging = False      

  def switchPowerState(self):
    '''Switch power state of vehicle - on or off'''
    self._powerState = not self._powerState
      
  def switchPowerMode(self):
    '''Switch either into or out of low power mode'''
    self.lowPowerMode = not self.lowPowerMode
      
  def run(self):
    '''Called every 'frame' (like update in c++).
    Will generate draw value and gather data from battery and odometer
    based on this. Processes this data and runs bms algos to calculate soc,
    soh and driving range. Should do some error/warning checks too.
    Then displays all in UI
    '''
    if self._charging:
      self.charge()

    if self._draw == 0: # if car idling
      self._draw += randint(0, 5)
    else:
      self._draw += randint(-2, 2)
    if self._draw > 80 and self.lowPowerMode:
      self._draw = 80

    for batteryCell in self._battery:
      batteryCell.generateData(self._draw)

    mileage = self._odometer.mileage

    # check power mode from ui
    self._ui._lowPowerMode = self._lowPowerMode

    self._bms.loadBalance(self._battery)
    self._stateOfCharge = self._bms.getStateOfCharge(self._battery)
    self._stateOfHealth = self._bms.getStateOfHealth(self._battery)
    self._drivingRange = self._bms.getDrivingRange()
    self._bms.cooling(self._battery)

    self._ui.display(self._bms.stateOfCharge, self._bms.stateOfHealth, self._bms.drivingRange, self._bms.warnings)

  def charge(self):
    '''Change charging state'''
    while self._charging:
      self._draw = -1

    for batteryCell in self._battery:
      batteryCell.generateData(self._draw)

    self._bms.loadBalance(self._battery)
    self._stateOfCharge = self._bms.getStateOfCharge(self._battery)
    self._bms.cooling(self._battery)

    self._ui.display_charging(self._stateOfCharge)

    # check if still charging

  def power(self):
    '''Not sure what this method is for?'''
    pass