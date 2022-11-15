from temperatureSensor import TemperatureSensor
from voltageSensor import VoltageSensor
from currentSensor import CurrentSensor
from battery import BatteryCell
from batteryModule import BatteryModule

class BatteryManagementSystem:

    NUMBER_OF_BATTERIES = 8

    def __init__(self):
        # all the calculaions in here

        # All battery cells made here
        # Every element in the battery pack is an object
        # of Battery Module class which represents 4 objects
        # Battery Cell, Temp, Current and Voltage Sensors
        self._batteryPack = [BatteryModule() for i in range(BatteryManagementSystem.NUMBER_OF_BATTERIES)] 

        self.temperatureSensor = TemperatureSensor()
        self.currentSensor = CurrentSensor()
        self.voltageSensor = VoltageSensor()

        self._temperatureThreshold = 0
        self._voltageThreshold = 0
        self._currentThreshold = 0

        self._stateOfCharge = 0
        self._stateOfHealth = 0

        # self.odometer = Odometer()
        # self.charger = Charger()

    def processData(self):
        '''From battery pack, read each sensor data and check for errors
        If errors exist, run their respective function 
        voltage - load balancing
        temperature - cooling'''

        
    def socAlgorithm(self):
        '''calculate SOC of battery using either Coulomb counting or Kalman filtering'''
        pass

    def sohAlgorithm(self):
        '''calculate SOH of battery using algo involving internal resistance measurement, counting charge/discharge cycles, SOC'''
        pass


    def cooling(self):
        '''cool the battery(reduce temperature) if temperature is over limit'''

        # from temperatureSensor read Data from all the BatteryCell objects
        # If one is over a temperature limit, start cooling
        pass
    
    def loadBalance(self):
        '''execute load balancing if load is unbalanced'''

        # If we're doing voltage based balancing (easiest one imo)
        # set a difference threshold between voltages (usually difference of 0.1 to 1)
        # and if any cells exceed that threshold, start balancing by
        # drainig the voltage away or sharing it with other cells
        # Sharing it out could lead to over voltage

        # Need to account for faulty cells too
        # BMS needs to detect that and prohibit load balancing with these type of cells
        pass

    def stateOfChargeWarning(self):
        # warn the user if SOC is below a threshold to start charging
        # Or if the charging is done that the charging has ceased
        # display on gui from EV method
        
        if self._stateOfCharge < 10:
            return "Battery Percent is lower than 10%. Please go to the nearest station to charge."
        elif self._stateOfCharge < 25:
            return "Battery Percent is at 25%. Please consider charging soon."
        elif self._stateOfCharge >= 80:
            return "Battery Percent is near full. Charging will be complete soon."
        elif self._stateOfCharge == 100:
            return "Battery Percent is now 100%. Please disconnect the charger to conserve battery health."

    def stateOfHealthWarning(self):
        # warn the user if the SOH is below a threshold
        # substitute the battery and display on gui from EV method

        if self._stateOfHealth < 10:
            return "Battery health is severly deteriorated. Please consider changing the battery immediately for continued and safe usage of the vehicle."
        elif self._stateOfHealth < 25:
            return "Battery health is very deteriorated. Please consider changing the battery soon for continued and safe usage of the vehicle."
        elif self._stateOfHealth < 50:
            return "Battery health has deteriorated. Please consider checking the settings for detailed viewing of the battery health status."
    
    def getStateOfCharge(self):
        return self._stateOfCharge
    
    def setStateOfCharge(self, stateOfCharge):
        self._stateOfCharge = stateOfCharge
    
    def getStateOfHealth(self):
        return self._stateOfHealth

    def setStateOfHealth(self, stateOfHealth):
        self._stateOfHealth = stateOfHealth

    def getTemperatureThreshold(self):
        return self._temperatureThreshold

    def setTemperatureThreshold(self, temperatureThreshold):
        self._temperatureThreshold = temperatureThreshold

    def getVoltageThreshold(self):
        return self._voltageThreshold
    
    def setVoltageThreshold(self, voltageThreshold):
        self._voltageThreshold = voltageThreshold

    def getCurrentThreshold(self):
        return self._currentThreshold

    def setCurrentThreshold(self, currentThreshold):
        self._currentThreshold = currentThreshold
    
    temperatureThreshold = property(getTemperatureThreshold, setTemperatureThreshold)
    voltageThreshold = property(getVoltageThreshold, setVoltageThreshold)
    currentThreshold = property(getCurrentThreshold, setVoltageThreshold)
    stateOfCharge = property(getStateOfCharge, setStateOfCharge)
    stateOfHealth = property(getStateOfHealth, setStateOfHealth)