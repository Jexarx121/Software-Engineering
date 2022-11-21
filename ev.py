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
        
        
    def powerStateOff(self):
        # for process in self._process:
            # process.terminate()

        self._lowPowerMode = False
        self._power = 0 
        self._bms.powerOff()
        print("----------------------------------------")
        print(f"Vehicle shutting down.")
        print("----------------------------------------")
        
        
    def switchPowerMode(self):
        '''Switch either into or out of low power mode'''
        self._lowPowerMode = not self._lowPowerMode
        
        if self._lowPowerMode:
            self._powerLimit = 0.6
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

        # with open("simulation.txt", "r") as f:
        simulation = [0, 0.2, 0.5, 0.24, 0.28, 0.31, 0.33, 0.37, "L", 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.95, 0.95, 0.95, 0.9,
                      0.85, 0.80, 0.75, 0.70, 0.65, 0.60, 0.55, 0]
 

        # with tkinter, use after() to trigger processLoop to run it with tkintet
        for power in range(len(simulation)):

            if self._bms.stateOfCharge == 0:
                self._bms.powerOff()
                self.switchPowerState()
                break

            self._power = simulation[power]
            uiState = self.display(power)
            print(uiState)

            if simulation[power] == "L" and self._lowPowerMode == False:
                if simulation[power-1] >= 0.6:
                    continue
                else:
                    self.switchPowerMode()
                    continue
                
            if simulation[power] == "L" and self._lowPowerMode:
                self.switchPowerMode()
                continue
            
            if self._lowPowerMode and simulation[power] > 0.6:
                self._power = 0.6

            if self._power == "C":
                beforeCharge = self._bms.stateOfCharge
                timeToCharge = simulation[power+1]
                print("----------------------------------------")
                print(f"Charging battery for: {timeToCharge}s")
                print("----------------------------------------")
                self.charge(timeToCharge)
                afterCharge = self._bms.stateOfCharge
                self.disconnectCharger(beforeCharge, afterCharge)
                continue

            if simulation[power-1] == "C":
                # skip the time for charge 
                continue

            if self._power == 0:
                if self._powerState == False:
                    self.switchPowerState()
                else:
                    self.switchPowerState()
            
                continue

            if self._power == 0.2 and simulation[power-1] == 0:
                self._bms.powerOn(self._power)
                continue

            self._bms.startProcess(self._power)


    def disconnectCharger(self, beforeCharge, afterCharge):
        '''Disconnects the charger after charging time is finished.\n
        Increments the charge/discharge cycles of battery depending on the amount of charge gained and the bms DOD.'''
        if self._charging:
            self._charging = False

            incrementCycle = (afterCharge - beforeCharge / 100) / BatteryManagementSystem.DEPTH_OF_DISCHARGE
            print("----------------------------------------")
            print(f"Charge/discharge cycles increased by: {incrementCycle}")
            print("----------------------------------------")
            self._bms.chargeDischargeCycles += incrementCycle
        

    def charge(self, timeToCharge):
        '''Initiate charging. It is a blackbox algorithm in this case where the state of charge increments after a certain period.\n
        Changes charging state and increments the charge/discharge cycles.\n
        State of charge starts to trickle when reaching 100% to avoid overcharging.\n
        Charging only stops time to charge is decremented to zero.'''

        if self._powerState == False:
            self.switchPowerState()
            self._charging = True
        
        charge = self._bms.stateOfCharge
        while timeToCharge > 0:
        
            sleep(1)
            if charge == self._bms._chargeThreshold:
                # Trickling to prevent overcharge
                self._bms.stateOfCharge -= 1

            self._bms.stateOfCharge += 1

            timeToCharge -= 1
            
    
    def display(self, frame):
        '''Display what the BMS wants us to display onto the UI'''
        uiState = ""
        uiState += "========================================\n"
        uiState += f"Frame: {frame}\n"
        uiState += f"Current Charge: {self._bms.stateOfCharge}%\n"
        uiState += f"Distance Remaining (est): {self._bms.distanceRemaining}km\n"
        uiState += f"Health Status: {self._bms.stateOfHealth}%\n"
        uiState += f"Total Mileage: {self._bms.odometer.mileage}km\n"
        if self._lowPowerMode:
            uiState += f"Low Power Mode is enabled\n"

        if self._bms.stateOfChargeWarning:
            warning  = self._bms.stateOfChargeWarning()
            uiState += f"{warning}\n"

        if self._bms.stateOfHealthWarning:
            warning = self._bms.stateOfHealthWarning()
            uiState += f"{warning}\n"

        uiState += "========================================\n"

        return uiState


if __name__ == "__main__":
    ev = ElectricVehicle()
    ev.run()



    
