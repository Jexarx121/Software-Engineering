from random import randint

class Odometer:
    def __init__(self):
        self._mileage = randint(0, 150000)
        
    def get_mileage(self):
        self._mileage += randint(0, 5)
        return self._mileage

    mileage = property(get_mileage)

