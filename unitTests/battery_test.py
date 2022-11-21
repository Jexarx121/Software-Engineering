import unittest
import sys, os
sys.path.insert(1, "/home/misllocal/Desktop/code/Assignments/Software Engineering/")

from battery import BatteryCell
from random import randint


class TestBattery(unittest.TestCase):

    battery = BatteryCell(62.5, 25)

    def testUpdateCurrentDataGreaterEqual(self):
        '''Test if current is greater than zero or not negative'''

        self.battery.updateCurrentData(0.03, 0.09)
        self.assertGreaterEqual(self.battery.current, 0)


    def testCurrentLessThanThreshold(self):
        '''Test if generated current values are less or equal to threhsold.'''

        self.battery.updateCurrentData(0.05, 0.09)
        self.assertLessEqual(self.battery.current, 25)


    def testTemperatureGreaterEqual(self):
        '''Check if temperature are negative or zero'''
        
        self.battery.current = 20
        self.battery.generateTemperatureData()
        self.assertGreaterEqual(self.battery.temperature, 0)
        

    def testTemperatureRaises(self):
        '''Check if randint range in generateTemperature method is not empty.'''

        self.battery.current = 25
        
        with self.assertRaises(ValueError):
            self.battery.generateTemperatureData()
            self.battery.temperature = randint(4, 1)
            

if __name__ == "__main__":
    unittest.main()

