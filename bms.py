from temperatureSensor import TemperatureSensor
from voltageSensor import VoltageSensor
from currentSensor import CurrentSensor
from battery import BatteryCell

class BatteryManagementSystem:
    def __init__(self):
        # all the calculaions in here

        # All battery cells made here
        self.batteryCell1 = BatteryCell()
        self.batteryCell2 = BatteryCell()
        self.batteryCell3 = BatteryCell()
        self.batteryCell4 = BatteryCell()
        self.batteryCell5 = BatteryCell()
        self.batteryCell6 = BatteryCell()
        self.batteryCell7 = BatteryCell()
        self.batteryCell8 = BatteryCell()

        self.temperatureSensor = TemperatureSensor()
        self.currentSensor = CurrentSensor()
        self.voltageSensor = VoltageSensor()

        self._temperatureThreshold = 0
        self._voltageThreshold = 0
        self._currentThreshold = 0

        self._stateOfCharge = 0
        self._stateOfHealth

        # self.odometer = Odometer()
        # self.charger = Charger()
        
    
    def getStateOfCharge(self):
        return self._stateOfCharge
    
    def setStateOfCharge(self, stateOfCharge):
        self._stateOfCharge = stateOfCharge
    
    def getStateOfHealth(self):
        return self._stateOfHealth
        
    def socAlgorithm(self):
        '''calculate SOC of battery using either Coulomb counting or Kalman filtering'''

    def sohAlgorithm(self):
        '''calculate SOH of battery using algo involving internal resistance measurement, counting charge/discharge cycles, SOC'''

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


    
    stateOfCharge = property(getStateOfCharge)
    stateOfHealth = property(getStateOfHealth)