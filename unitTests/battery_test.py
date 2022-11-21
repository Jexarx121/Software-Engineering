import unittest
from battery import *

class TestBattery(unittest.TestCase):

    battery = BatteryCell(62.5, 25)

    def testGeneratureTemperatureData(self):
        '''Test various conditions in the generateTemperatureData method.'''
        
        # check if temperature are negative or zero
        self.assertGreaterEqual(self.battery.temperature, 0)

        # check if values are higher than threshold
        

    def testUpdateCurrentData(self):
        '''Test if various conditions in the updateCurrentData method.'''

        # check if values are negative

        # check if values are higher than threshold
        self.assertLessEqual(self.battery.current, 25)


if __name__ == "__main__":
    unittest.main()

