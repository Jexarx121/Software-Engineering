from random import randint

class Odometer:
    def __init__(self):
        self._mileage = randint(0, 150000)
        
    def get_mileage(self):
        '''
        We need to decide how we will track passing of time / progress in the journey in our program
        Could be:
            - related to draw / load of the battery
            - could run in separate thread increasing independent of power used
            - could be based on time since last checked
            - could be random
        '''

        self._mileage += randint(5, 25)
        return self._mileage

    mileage = property(get_mileage)

