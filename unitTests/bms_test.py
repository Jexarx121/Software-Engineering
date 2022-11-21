import unittest
from bms import *


class TestBatteryManagementSystem(unittest.TestCase):

    def testSocAlgorithm(self):
# test if soc parameters can be negative
# test if soc can be too high
        pass

    def testSohAlgorithm(self):
# test if soh parameters can be negative
# test if soh can be too high
# test if chargeDischarge cycles can be 0 or 1
        pass

    def testCooling(self):
        # test if lowest temperature threshold is ever breached
        # temperature going down to negatives so added a LOW threshold to prevent that
        pass

    def testDemandPower(self):
        # test if the power change is too much

        pass