from bms import BatteryManagementSystem
from time import sleep
from threading import Thread
from ui import UI


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
        self._ui = UI()
        self.destroyThread = False

    def switchPowerState(self):
        '''Switch power state of vehicle - on or off.'''
        self._powerState = not self._powerState

        if self._powerState == False:
            self.powerStateOff()
        else:
            print("----------------------------------------")
            print(f"Vehicle powered on.")
            print("----------------------------------------")

    def powerStateOff(self):
        """Switch power state of the vehicle - off."""
        print("----------------------------------------")
        print(f"Vehicle powered off.")
        print("----------------------------------------")
        self._lowPowerMode = False
        self._power = 0
        self._bms.powerOff()

    def switchPowerMode(self):
        '''Switch either into or out of low power mode.'''
        self._lowPowerMode = not self._lowPowerMode

        if self._lowPowerMode:
            self._powerLimit = 0.6
            self._ui._lowPowerModeLabel['text'] = "Low Power Mode is enabled."
        else:
            self._powerLimit = 0
            self._ui._lowPowerModeLabel['text'] = ""

    def runThread(self, simulation):
        '''Simulation of a trip with an electric vehicle. \n
        BMS will constantly run its operations while the vehicle simulates different through different scenarios.\n
        UI will show these changes during the trip. '''

        self.display()
        sleep(1)
        
        for power in range(len(simulation)):
            print("====================================")
            print(f"Frame: {power}")
            print("====================================")
            self._power = simulation[power]
            
            if simulation[power-1] == "C":
                continue

            # check if the simulation includes charging
            # number after charging represents the time charged
            if type(simulation[power]) == str and (simulation[power] in ["C", "L"]):
                if self._power == "C":
                    timeToCharge = simulation[power+1]
                    self.charge(timeToCharge)
                    continue

                # Toggles Low power mode
                # Forces car to ignore powers greater than 0.6
                if simulation[power] == "L" and self._lowPowerMode == False:
                    if simulation[power-1] >= 0.6:
                        print(
                            "*Warning* Can NOT enter Low Power mode. Reduce speed to enter Low Power mode")
                        continue
                    else:
                        self.switchPowerMode()
                        continue
                elif simulation[power] == "L" and self._lowPowerMode:
                    self.switchPowerMode()
                    continue
            
            #make sure no arbitary string is processed besides C or L
            if type(simulation[power]) == str and (simulation[power] not in ["C", "L"]):
                continue

            #make sure power is within defined range of 0.0 and 1.0
            if 0 > self._power or self._power > 1:
                continue

            if self._lowPowerMode and simulation[power] > 0.6:
                self._power = 0.6

            # Check if the vehicle turns on or off during the simulation
            if self._power == 0:
                self.switchPowerState()
                continue

            # turn off vehicle with SOC reaching 0
            if self._bms.stateOfCharge <= 0:
                self._bms.powerOff()
                self.switchPowerState()
                break
            # skip the number after charging since it's not a power for the trip
            
            if self._powerState == False:
                continue
            
            # checks if the vehicle turns off in the middle of the trip
            # Vehicle power right after turning on is 0.2.
            if simulation[power-1] == 0:
                if self._power == 0.2:
                    self._bms.powerOn(self._power)
                    continue
                else:
                    self.switchPowerState()
                    break

            self._bms.startProcess(self._power)
            sleep(1)
            self.display()

        # Give a delay before closing tkinter window for thread to end
        self._ui._root.after(100, self._ui.exit)

    def disconnectCharger(self, beforeCharge, afterCharge):
        '''Disconnects the charger after charging time is finished.\n
        Increments the charge/discharge cycles of battery depending on the amount of charge gained and the bms DOD.'''
        if self._charging:
            self._charging = False

            incrementCycle = (afterCharge - beforeCharge) / 100
            print("----------------------------------------")
            print(f"Charge/discharge cycles increased by: {incrementCycle}")
            print("----------------------------------------")
            self._bms.chargeDischargeCycles += incrementCycle

        self._bms.calculateNewMaxCapacity()

    def charge(self, timeToCharge):
        '''Initiate charging. It is a blackbox algorithm in this case where the state of charge increments after a certain period.\n
        Changes charging state and increments the charge/discharge cycles.\n
        State of charge starts to trickle when reaching 100% to avoid overcharging.\n
        Charging only stops time to charge is decremented to zero.'''
        if timeToCharge <= 0:
            return "Time to charge should be a value greater than 0."

        if self._powerState == False:
            self.switchPowerState()
            self._charging = True

        beforeCharge = self._bms.stateOfCharge
        while timeToCharge > 0:

            if self._bms.stateOfCharge == self._bms._chargeThreshold:
                # Trickling to prevent overcharge
                self._bms.stateOfCharge -= 1

            # increment charge and decrement timer
            self._bms.stateOfCharge += 1
            timeToCharge -= 1

            # update the ui correspondly to the incrementing charge
            self._ui._batteryPercentLabel[
                'text'] = f"Battery Percent: {round(self._bms.stateOfCharge, 2)}%"
            self._ui._batteryPercentProgress['value'] = self._bms.stateOfCharge
            self._ui._chargeLabel['text'] = f"Vehicle is currently charging. ({timeToCharge}s)."

            sleep(1)
        self.switchPowerState()

        # need to update distance driven to match new soc
        self._bms.distanceRemainingAlgorithm()
        self._ui._distanceRemaining["text"] = f"{round(self._bms.distanceRemaining,2)}km"
        afterCharge = self._bms.stateOfCharge

        self._ui._chargeLabel['text'] = ""
        self.disconnectCharger(beforeCharge, afterCharge)

    def display(self):
        '''Display what the BMS wants us to display onto the UI.'''
        self._ui._batteryPercentProgress['value'] = self._bms.stateOfCharge
        self._ui._batteryPercentLabel[
            'text'] = f"Battery Percent: {round(self._bms.stateOfCharge, 2)}%"
        self._ui._healthPercentProgress['value'] = self._bms.stateOfHealth
        self._ui._healthPercentLabel[
            'text'] = f"Battery Health: {round(self._bms.stateOfHealth, 2)}%"

        self._ui._distanceRemaining['text'] = f"{round(self._bms.distanceRemaining, 2)}km"
        self._ui._totalMileage['text'] = f"{round(self._bms.odometer.mileage, 2)}km"

        if self._lowPowerMode:
            self._ui._lowPowerModeLabel['text'] = "Low Power Mode is enabled."

        self._ui._socWarning['text'] = self._bms.stateOfChargeWarning()
        self._ui._sohWarning['text'] = self._bms.stateOfHealthWarning()

    def run(self,simulation):

        start = Thread(target=self.runThread,args=(simulation,))
        start.start()
        self._ui._root.mainloop()

if __name__ == "__main__":
    simulation = [0, 0.2, 0.23, 0.24, 0.28, 0.31, 0.33, 0.37, 0, "C", 5, 0, 0.2,
                  0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.95, 0.95, 0.95, 0.9,
                  0.85, 0.80, 0.75, 0.70, 0.65,"L", 0.59, 0.3, 0.4, 0.42, 0.43, 0.39, "L", 0]

    ev = ElectricVehicle()
    ev.run(simulation)

