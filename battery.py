from random import randint

class BatteryCell:
    """Represents a battery cell which consists of multiple individual batteries.\n
    Cells keep track of their own voltage , current, temperature which the sensors will read.
    This is not how sensors work in the real world but for the sensors in the simulation to read the data it has to be 'stored' by the cell."""

    def __init__(self, max_voltage, max_current):
        
        self._max_voltage = max_voltage
        self._max_current = max_current

        self._voltage = 0
        self._current = 0
        self._temperature = 0
        self._state = False
        
    def updateVoltageData(self, power, voltage_change):
        """Calculates the new voltage of the battery based on the given power change."""

        fluctuation = self.fluctuateData(power, "voltage")
        power_change += fluctuation
        self._voltage += voltage_change

    def generateCurrentData(self, power, current_change):
        """Calculates the new current of the battery based on the given power change."""

        fluctuation = self.fluctuateData(power, "current")
        power_change += fluctuation
        self._voltage += current_change

    def generateTemperatureData(self, power):
        """Generates a random temperature value for the battery cells.\n
           In terms of simulation, the temperature proved quite difficult and thus a more random data generation for temperature is used here."""

        maxTemperature = 50 
        temperatureGenerated = maxTemperature * power
        self._temperature = randint(temperatureGenerated, maxTemperature)



    def fluctuateData(self, power, data_type):
        """Generates a fluctuation in data based on the data type of the battery data being changed. This fluctuation is also based on the current power of the EV."""
        if data_type == "voltage":
            minRange = -3
            maxRange = 3
            
            if power >= 0.26 and power <= 0.5:
                maxRange = 5
            elif power <= 0.75:
                maxRange  = 8
                minRange = -2
            else:
                maxRange = 10
                minRange = -1
        else:
            minRange = -5
            maxRange = 5
            
            if 0.26 >= power and power <= 0.5:
                maxRange = 8
            elif power <= 0.75:
                maxRange  = 12
                minRange = -2
            else:
                maxRange = 15
                minRange = 0
                
            
        fluctuationValue = randint(minRange, maxRange)

        return fluctuationValue

    def getVoltage(self):
        return self._voltage
    
    def getCurrent(self):
        return self._current

    def getTemperature(self):
        return self._temperature

    def getState(self):
        return self._state

    def setState(self, state):
        self._state = state

    voltage = property(getVoltage)
    current = property(getCurrent)
    temperature = property(getTemperature)
    state = property(getState, setState)

 
if __name__ == "__main__":
    battery1 = BatteryCell()
    battery2 = BatteryCell()