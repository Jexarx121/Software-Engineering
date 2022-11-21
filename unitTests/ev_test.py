import unittest
import sys, os
sys.path.insert(1, "/home/misllocal/Desktop/code/Assignments/Software Engineering/")
from ev import *

class TestEv(unittest.TestCase):

    ev = ElectricVehicle()

    def testChargeGreaterThanZero(self):
        '''Test if timeTaken parameter for charger is at least one.''' 
        timeTaken = 0
        if timeTaken > 0:
            self.ev.charge(timeTaken)
        else:
            self.assertLessEqual(timeTaken, 0)
    

    def testRunPowerPassed(self):
        '''Test if power value in list is greater than zero and less than one.'''
        simulation = [0, -2, 0.23, 2]
        for power in simulation:
            self.assertTrue(0 <= power <= 1)


if __name__ == "__main__":
    unittest.main()