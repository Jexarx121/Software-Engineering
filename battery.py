def Battery():

    def __init__(self):
        self._current = 0
        self._temperature = 0
        self._voltage = 0
        self._cells = {}

    def getVoltage(self):
        return self._current

    def getCurrent(self):
        return self._voltage

    def getTemperature(self):
        return self._temperature

    voltage = property(getVoltage)
    current = property(getCurrent)
    temperature = property(getTemperature)

if __name__ == "__main__":
    pass