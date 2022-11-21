from random import randint

class Odometer:
    def __init__(self):
        self._mileage = 13040#randint(0, 150000)
        
    def getMileage(self):
        return self._mileage
    
    def setMileage(self, mileage):
        self._mileage = mileage

    mileage = property(getMileage, setMileage)

