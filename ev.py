from battery import BatteryCell
from ui import UI
from tkinter import *
from random import randint
from odometer import Odometer
from bms import BatteryManagementSystem
from time import sleep
from multiprocessing import *

class ElectricVehicle():
    """represents an electrical vehicle"""

    NUMBER_OF_BATTERIES = 8

    def __init__(self):
        self._powerState = False
        self._lowPowerMode = False
        self._powerLimit = 0
        self._power = 0
        # self._odometer = Odometer()
        self._bms = BatteryManagementSystem()
        self._ui = UI()
        self._process = []
        self._charging = False      

    def switchPowerState(self):
        '''Switch power state of vehicle - on or off'''
        self._powerState = not self._powerState
        
        if self._powerState == False:
            self.powerStateOff()
        else:
            self.powerStateOn()
        
        
    def powerStateOff(self):
        for process in self._process:
            process.terminate()

        self._lowPowerMode = False
        # Kill ui when off (make screen black)
        self._ui.exit()
        self._power = 0
        
        
    def powerStateOn(self):
        self._power = 20
        self._ui.start()
        
        
    def switchPowerMode(self):
        '''Switch either into or out of low power mode'''
        self._lowPowerMode = not self._lowPowerMode
        
        # if normal mode turn into low power mode
        #if in low power mode switch to normal mode?
        
        if self._lowPowerMode:
            self._powerLimit = 60
        else:
            self._powerLimit = 0
        
        # if were above 60 when driver presses low power mode.
        
    def limitPower(self):
        while self._power > self._powerLimit:
            # slowly decline the power
            self._power -= 4
        
        
    def run(self):
        '''Called every 'frame' (like update in c++).
        Will generate draw value and gather data from battery and odometer
        based on this. Processes this data and runs bms algos to calculate soc,
        soh and driving range. Should do some error/warning checks too.
        Then displays all in UI
        '''
        if self._charging:
        
            self._process = []
            chargingProcess = Process(target=self.charge()) #sends to charge method
            self._process.append(chargingProcess)
            chargingProcess.start()
        
        if self._lowPowerMode:
            self.limitPower()
        

        if self._power == 0: # if car idling
            self._power += randint(0, 5)
        else:
            self._power += randint(-2, 2)
        if self._power > 80 and self.lowPowerMode:
            self._power = 80

        for batteryCell in self._battery:
            batteryCell.generateData(self._power)

        mileage = self._odometer.mileage

        # check power mode from ui
        self._ui._lowPowerMode = self._lowPowerMode

        self._bms.loadBalance(self._battery)
        self._stateOfCharge = self._bms.getStateOfCharge(self._battery)
        self._stateOfHealth = self._bms.getStateOfHealth(self._battery)
        self._drivingRange = self._bms.getDrivingRange()
        self._bms.cooling(self._battery)

        self.display(self._bms.stateOfCharge, self._bms.stateOfHealth, self._bms.drivingRange, self._bms.warnings)

    def charge(self):
        '''Change charging state'''
        
        # Process so function is interruptable from outside
        if self._powerState == False:
            self.powerStateOn()
            self._charging = True
        
        charge = self._bms.stateOfCharge
        while self._charging == True:
        
            sleep(10)
            if charge == threshold:
                # Trickling to prevent overcharge
                self._bms.stateOfCharge -= 1
                self.display("Warning, Battery is full.")

            self._bms.stateOfCharge += 1
            self.display(self.bms.stateOfCharge)
        

    def power(self):
        '''Not sure what this method is for?'''
        pass

    def display(self):
        '''Display what the BMS wants us to display onto the UI'''

if __name__ == "__main__":
    ev = ElectricVehicle()
    ev._ui.progressBar(ev._bms.stateOfCharge)


    
