from ev import *

class StateTransitioning():
    
    def __init__(self):
        pass

    def stateTransitioningTest(self):
            """State Transitioning Testing"""
            #since we have off state, on state, charging state, and low power state = 4 states
            #we need to check if these all work
            
            # testing normal powered on state with power off state
            print("*****************************")
            print("\n State Transition Test for normal powered mode\n")
            print("*****************************")
            stateTest1 = ElectricVehicle()
            stateTest1.run([0, 0.2, 0.4, 0.5, 0.3, 0])
            
            print("*****************************")
            print("\n State Transition Test for charging mode\n")
            print("*****************************")
            sleep(2)
            
            #testing charging state 
            stateTest2 = ElectricVehicle()
            stateTest2.run(["C", 5])
            
            print("*****************************")
            print("\n State Transition Test for low power mode.\n")
            print("*****************************")
            sleep(2)
            
            #testing low power mode and seeing if the vehicle functions correctly
            stateTest3 = ElectricVehicle()
            stateTest3.run([0,"L", 0.5, 0.6, 0.6, 0])
            
            print("*****************************")
            print("\n State Transition Test for all states combined\n")
            print("*****************************")
            sleep(2)
            #turns on, enters low power mode, drives, turns off low power mode, turns off car, charges car,
            #turns on car drives a bit(normal mode) and turns off. = captures all states
            stateTest4 = ElectricVehicle()
            stateTest4.run([0, 0.2, "L", 0.4, 0.5, "L", 0.3, 0, "C", 5, 0, 0.2, 0.3, 0.4, 0])
            
if __name__ == "__main__":
    myTest= StateTransitioning()
    myTest.stateTransitioningTest()
    