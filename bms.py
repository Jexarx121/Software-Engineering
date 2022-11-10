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