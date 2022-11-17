from random import randint

class BatteryCell:
    """represents a battery cell"""
    # cells produce voltage , current, temperature which the sensors will read.

    # static variable that will give each cell an id
    id = 0

    def __init__(self):

        if BatteryCell.id >= 8:
            return "All the battery cells have been made."

        self._id = BatteryCell.id
        self._voltage = 0
        self._current = 0
        self._temperature = 0
        self._state = False

        self._oldPower = 0

        # static variable incremented each instantiation 
        # Battery cell amount variable - curerntly 8
        BatteryCell.id += 1

        # Stored in some data structure 
        # Each cell has quite a few batteries
        
    def generateVoltageData(self, power):
        '''generate random voltage values for the battery cells'''

        # gets fed from bms change in power
        # sensor will then read it calling respective getter method
        # if no power change - generate same amount of power with fluctuations from plusMinus method

        if power <= 0 or power >= 1:
            return 'There is a fault with the amount of power required for the vehicle.'

        # Voltage - 200V - 400V - threshold needs be derived from power
        # All parameters divided by number of cells
        maxVoltage = 500 / BatteryCell.id
        oldVoltage = self._voltage

        self._voltage = 0

    # Try and base the current value based on power and voltage
    # Current = Power / Voltage
    def generateCurrentData(self, power):
        ''' Generates a random current value for the battery cells'''

        # Current - 100A - 250A - derive current from both power parameter and voltage
        if power <= 0 or power >= 1:
            return 'There is a fault with the amount of power required for the vehicle.'

        maxCurrent = 250 / BatteryCell.id
        currentGenerated = maxCurrent * power

        currentGenerated += self.plusMinus(power)

        self._voltage = currentGenerated
        return self._current


    def generateTemperatureData(self, power):
        '''Generates a random temperature value for the battery cells'''


        # Temperature - 50 degrees C upper bound - heat derived from both current and voltage 
        # temperature ranges are consistently same range regardless of car - quicker cooling
        maxTemperature = 50 
        temperatureGenerated = maxTemperature * power
        self._temperature = randint(temperatureGenerated, maxTemperature)
        self._temperature += self.plusMinus(power)

        return self._temperature


    # generates random values added to each parameter to randomise each further
    # based on power needed for ev, the demand for current, voltage and temperature
    # goes higher and therefore the random value does too   
    def plusMinus(self, power):
        minRange = -5
        maxRange = 5
        
        if power <= 0.25:
            randomValue = randint(minRange, maxRange)
        elif power <= 0.5:
            maxRange = 10
            randomValue = randint(minRange, maxRange)
        elif power <= 0.75:
            maxRange  = 15
            minRange = -2
            randomValue = randint(minRange, maxRange)
        else:
            maxRange = 20
            minRange = 0
            randomValue = randint(minRange, maxRange)

        return randomValue

    def checkDataRange(self, generatedValue, oldValue):
        threshold = 20
        minRange = generatedValue + threshold
        maxRange = generatedValue - threshold

        if oldValue in range(minRange, maxRange):
            return True
        
        return False

    def getState(self):
        return self._state

    def setState(self, state):
        self._state = state

    def getVoltage(self):
        return self._voltage

    def setVoltage(self, voltage):
        self._voltage = voltage
    
    def getCurrent(self):
        return self._current

    def setCurrent(self, current):
        self._current = current

    def getTemperature(self):
        return self._temperature

    def setTemperature(self, temperature):
        self._temperature = temperature

    def getId(self):
        return self._id


    id = property(getId)
    state = property(getState, setState)
    current = property(getCurrent, setCurrent)
    voltage = property(getVoltage, setVoltage)
    temperature = property(getTemperature, setTemperature)

 
if __name__ == "__main__":
    battery1 = BatteryCell()
    battery2 = BatteryCell()

    print(battery1.id)
    print(battery2.id)