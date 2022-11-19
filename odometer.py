from random import randint

class Odometer:
    def __init__(self):
        self._mileage = randint(0, 150000)
        
    def getMileage(self):
        return self._mileage
    
    def setMileage(self, mileage):
        self._mileage += mileage

    mileage = property(getMileage, setMileage)

