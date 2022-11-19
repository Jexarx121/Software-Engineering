from battery import BatteryCell
from ui import UI
from random import randint
from bms import BatteryManagementSystem
from time import sleep
from multiprocessing import Process
from threading import Thread

class ElectricVehicle():
    """Represents an electrical vehicle."""

    def __init__(self):
        self._powerState = False
        self._lowPowerMode = False
        self._powerLimit = 0
        self._power = 0
        self._bms = BatteryManagementSystem()
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
        self._power = 0
        
        
    def powerStateOn(self):
        self._power = 20
        
        
    def switchPowerMode(self):
        '''Switch either into or out of low power mode'''
        sleep(5)
        self._lowPowerMode = not self._lowPowerMode
        
        if self._lowPowerMode:
            self._powerLimit = 60
        else:
            self._powerLimit = 0

        
    def limitPower(self):
        while self._power > self._powerLimit:
            # slowly decline the power
            self._power -= 4
        
        
    def run(self):
        '''Simulation of a trip with an electric vehicle. \n
        BMS will constantly run its operations while the vehicle simulates different through different scenarios.\n
        UI will show these changes during the trip. '''
        with open("simulation.txt", "r") as f:
            simulation = []
 
        # with tkinter, use after() to trigger processLoop to run it with tkintet
        for power in range(len(simulation)):

            uiState = self.display(power)
            print(uiState)
            # -1 values represent charging in the trip
            if power == -1:
                self.charge()

            self._bms.startProcess(power)

        
        

    def charge(self):
        '''Initiate charging. It is a blackbox algorithm in this case where the state of charge increments after a certain period.\n
        Changes charging state and increments the charge/discharge cycles.\n
        State of charge starts to trickle when reaching 100% to avoid overcharging.\n
        Charging only stops when driver disconnects plug.'''
        self._bms.chargeDischargeCycles += 1

        # Process so function is interruptable from outside
        if self._powerState == False:
            self.powerStateOn()
            self._charging = True
        
        charge = self._bms.stateOfCharge
        while self._charging == True:
        
            sleep(10)
            if charge == self._bms._chargeThreshold:
                # Trickling to prevent overcharge
                self._bms.stateOfCharge -= 1

            self._bms.stateOfCharge += 1

    
    def disconnectCharger(self):
        """Simulate driver disconnecting charger."""
        if self._charging:
            self._charging = False



    def display(self, frame):
        '''Display what the BMS wants us to display onto the UI'''
        uiState = ""
        uiState += "========================================\n"
        uiState += f"Frame: {frame}\n"
        uiState += f"Current Charge: {self._bms.stateOfCharge}\n"
        uiState += f"Distance Remaining (est): {self._bms.distanceRemaining}\n"
        uiState += f"Health Status: {self._bms.stateOfHealth}\n"
        uiState += f"Total Mileage: {self._bms.odometer.mileage}\n"
        if self._lowPowerMode:
            uiState += f"Low Power Mode is enabled\n"

        if self._bms.stateOfChargeWarning:
            uiState += f"{self._bms.stateOfChargeWarning}\n"

        if self._bms.stateOfHealthWarning:
            uiState += f"{self._bms.stateOfHealthWarning}\n"

        uiState += "========================================\n"

        return uiState


if __name__ == "__main__":
    ev = ElectricVehicle()



    
