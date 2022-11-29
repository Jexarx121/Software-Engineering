
class Odometer:
    """Keeps the total mileage that the vehicle has driven in its lifetime."""
    def __init__(self):
        self._mileage = 38790 # 129.3*300 (charge cycles * max distance) 
        
    def getMileage(self):
        return self._mileage
    
    def setMileage(self, mileage):
        self._mileage = mileage

    mileage = property(getMileage, setMileage)


