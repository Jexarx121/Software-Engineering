import unittest
import sys, os
sys.path.insert(1, "/home/misllocal/Desktop/code/Assignments/Software Engineering/")
from bms import *


class TestBatteryManagementSystem(unittest.TestCase):

    bms = BatteryManagementSystem()

    def testSocAlgorithmGreaterThanZero(self):
        '''Test if State of Charge is greater than zero or not negative'''
        self.bms.socAlgorithm(200, 0.00016355514526367188)
        self.assertGreaterEqual(self.bms.stateOfCharge, 0)


    def testSohAlgorithmGreaterThanZero(self):
        '''Test if State of Health is greater than zero or not negative'''
        self.bms.sohAlgorithm()
        self.assertGreaterEqual(self.bms.stateOfHealth, 0)


    def testCoolingLowerThanZero(self):
        '''Test cooling amounts of temperatures in List and Battery Cell to make sure battery never goes below a minimum temperature.'''
        temperatureList = [14, 13, 34, 55, 24, 23, 32, 39]
        self.bms.cooling(temperatureList)
        self.assertGreaterEqual(min(temperatureList), 12)


if __name__ == "__main__":
    unittest.main()