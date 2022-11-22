from random import randint

class BatteryCell:
    """Represents a battery cell which consists of multiple individual batteries.\n
    Cells keep track of their own voltage , current, temperature which the sensors will read.
    This is not how sensors work in the real world but for the sensors in the simulation to read the data it has to be 'stored' by the cell."""

    MIN_CURRENT = 5
    MIN_TEMPERATURE = 12

    def __init__(self, max_voltage, max_current):
        
        self._max_voltage = max_voltage
        self._max_current = max_current

        self._voltage = 0
        self._current = 0
        self._temperature = 0
        self._state = False
        
    def updateVoltageData(self, power, voltage_change):
        """Calculates the new voltage of the battery based on the given power change."""
        if power == 0:
            self._voltage = 0
        elif power == 1:
            self._voltage = self._max_voltage
        else:
            fluctuation = self.fluctuateData(power, "voltage")
            voltage_change += fluctuation
            self._voltage += voltage_change
            if self._voltage > self._max_voltage:
                self._voltage = self._max_voltage

    def updateCurrentData(self, power, current_change):
        """Calculates the new current of the battery based on the given power change."""
        if power == 0:
            self._current = 0
        else:
            
            fluctuation = self.fluctuateData(power, "current")
            current_change += fluctuation
            self._current += current_change
            if self._current > self._max_current:
                self._current = self._max_current
            if self._current < BatteryCell.MIN_CURRENT:
                self._current = BatteryCell.MIN_CURRENT

    def generateTemperatureData(self):
        """Generates a temperature value based on current of the battery cell.\n
           In terms of simulation, the temperature proved quite difficult and thus a more random data generation for temperature is used here."""

        if self._current == 0:
            self._temperature = 0
        else:
            temp_range = round(self.current * 2.25)
            if temp_range - 5 >= BatteryCell.MIN_TEMPERATURE:
                minRange = temp_range - 5 
                maxRange = temp_range + 5
                self._temperature = randint(minRange, maxRange)
            else:
                maxRange = temp_range + BatteryCell.MIN_TEMPERATURE
                self._temperature = randint(BatteryCell.MIN_TEMPERATURE, maxRange)



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
            minRange = -3
            maxRange = 5
            
            if 0.26 <= power and power <= 0.5:
                maxRange = 7
            elif power <= 0.75:
                maxRange  = 9
                minRange = -2
            else:
                maxRange = 11
                minRange = -1
                
            
        fluctuationValue = randint(minRange, maxRange)

        return fluctuationValue

    def getVoltage(self):
        return self._voltage
    
    def getCurrent(self):
        return self._current

    def getTemperature(self):
        return self._temperature

    def setCurrent(self, current):
        self._current = current
    
    def setTemperature(self, new_temperature):
        self._temperature = new_temperature
        
    def getState(self):
        return self._state

    def setState(self, state):
        self._state = state

    voltage = property(getVoltage)
    current = property(getCurrent, setCurrent)
    temperature = property(getTemperature, setTemperature)
    state = property(getState, setState)


 
if __name__ == "__main__":
    pass