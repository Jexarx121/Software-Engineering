from ev import *
from time import sleep


class BoundaryAnalysis():
    
    def __init__(self):
        pass
    
    def boundaryValueAnalysis(self):
        """Boundary Value Analysis with equivalence partitioning"""
        #since our range for the ev is 0-1 we shall pick -1, 1 and 2
        #since we also allow for "C" and "L", we will test "L" and a random other string, lets say "K"
        #in the following tests a 0 is required to start the ev which is then followed by our tests
        
        #following lists have 0 followed by 0.2 to allow car to start which
        #then tests the boundaries
        print("\nBeginning Boundary Value Analysis...\n")
        sleep(2)

        print("*****************************")
        print("\n BVA Test for valid value of 1 \n")
        print("*****************************")
        
        # this will work
        boundaryTest2 = ElectricVehicle()
        boundaryTest2.run([0, 0.2, 1])
        sleep(2)

        print("*****************************")
        print("\n BVA Test for invalid value of -1\n")
        print("*****************************")
        # #this should not work @ -1
        boundaryTest3 = ElectricVehicle()
        boundaryTest3.run([0, 0.2, -1])
        sleep(1)
 
        print("*****************************")
        print("\n BVA Test for invalid value of 2\n")
        print("*****************************")
        # this should do nothing @ 2
        boundaryTest4 = ElectricVehicle()
        boundaryTest4.run([0, 0.2, 2])
        sleep(1)
        
        print("*****************************")
        print("\n BVA Test for invalid value of \"K\"\n")
        print("*****************************")
        # this should do nothing since K is not in defined range
        boundaryTest5 = ElectricVehicle()
        boundaryTest5.run([0, 0.2,"K"])
        sleep(1)
        
        print("*****************************")
        print("\n BVA Test for valid value of \"L\"\n")
        print("*****************************")
        #this will work
        boundaryTest6 = ElectricVehicle()
        boundaryTest6.run([0, 0.2,"L"])
        sleep(1)
        
if __name__ == "__main__":
    myTest= BoundaryAnalysis()
    myTest.boundaryValueAnalysis()
    