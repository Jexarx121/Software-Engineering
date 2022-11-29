from batteryModule import BatteryModule
from odometer import Odometer
from random import choice
from time import time


class BatteryManagementSystem():
	'''Represents a battery management system for an electric vehicle.'''

	# All constants are based off of real life statistics and averaged between low to high ranges.
	NUMBER_OF_BATTERIES = 8
	DEPTH_OF_DISCHARGE = 100
	CHARGE_DISCHARGE_MAXIMUM = 500 #Based off 100% DOD.
	MIN_TEMPERATURE = 12
	MAX_TEMPERATURE = 50
	MAX_VOLTAGE = 500
	MAX_CURRENT = 200
	VOLTAGE_DIFF = 15
	MAXIMUM_DISTANCE = 300 # Kilometers that this vehicle can travel on 100% SOC
	BATTERY_PACK_CAPACITY = 87.5 # This is the capacity at manufacture date based on voltage threshold

	def __init__(self):

		self._power = 0

		self._batteryPack = [BatteryModule(BatteryManagementSystem.MAX_VOLTAGE / BatteryManagementSystem.NUMBER_OF_BATTERIES, BatteryManagementSystem.MAX_CURRENT / BatteryManagementSystem.NUMBER_OF_BATTERIES) for i in range(
			BatteryManagementSystem.NUMBER_OF_BATTERIES)]

		self.odometer = Odometer()

		self._stateOfCharge = 50 # can start off at any number here between 0 - 100
		self._distanceDriven = self.distanceDriven()

		self._initialStateOfCharge = 100
		self._initialMileage = self.odometer.mileage

		# charge discharge cycles only increase after car stops and turns on again after charging or discharging entirely 
		self._chargeDischargeCycles = 129.3

		self._maxCapacity = 0
		self.calculateNewMaxCapacity()

		self._stateOfHealth = 0
		self.sohAlgorithm()

		self._distanceRemaining = BatteryManagementSystem.MAXIMUM_DISTANCE * (self._stateOfCharge/100)
		self._chargeThreshold = 100
		


	def startProcess(self, power):
		"""Runs function to updata data in the batteries, retrieve them from the sensors and processes them with all other bms functions."""
		
		start = time()
  
		self.demandPower(power)
		
		dataSet = self.getData()
		totalCurrent = self.processData(dataSet[0], dataSet[1], dataSet[2])
  
		end = time()
		difference = end - start

		self.sohAlgorithm()
		self.socAlgorithm(totalCurrent, difference)
		self.distanceRemainingAlgorithm()
  

	def powerOn(self, new_power):
		"""Sets the initial values of each battery in the battery pack when the EV is powered on"""
		self._power = new_power
		required_voltage = new_power * BatteryManagementSystem.MAX_VOLTAGE
		required_current = new_power * BatteryManagementSystem.MAX_CURRENT

		voltage_per_cell = required_voltage / BatteryManagementSystem.NUMBER_OF_BATTERIES
		current_per_cell = required_current / BatteryManagementSystem.NUMBER_OF_BATTERIES

		for module in self._batteryPack:
			module.batteryCell.state = True
			module.batteryCell.updateVoltageData(self._power, voltage_per_cell)
			module.batteryCell.updateCurrentData(self._power, current_per_cell)
			module.batteryCell.generateTemperatureData()

     
	def powerOff(self):
		"""'Turns off each battery in the battery pack by setting all values to 0"""
		for module in self._batteryPack:
			module.batteryCell.state = False
			module.batteryCell.updateVoltageData(0, 0)
			module.batteryCell.updateCurrentData(0, 0)
			module.batteryCell.generateTemperatureData()
    

	def demandPower(self, new_power):
		'''Increments data in the battery based on the new power of the EV. This method is run each time the EV's power changes and facilitates the 'updating' of battery data as a result of this power change'''
		required_voltage = new_power * BatteryManagementSystem.MAX_VOLTAGE
		required_current = new_power * BatteryManagementSystem.MAX_CURRENT
  
		if new_power < 1: #Checks to make sure power is not at maximum
			working_voltage = 0
			working_current = 0

			for module in self._batteryPack: #Calculates the current voltage and current in the battery pack
				working_voltage += module.batteryCell.voltage
				working_current += module.batteryCell.current
		
			power_change = new_power - self._power
			if working_voltage >= required_voltage: 
				voltage_change = power_change * BatteryManagementSystem.MAX_VOLTAGE
			else:
				voltage_change = 0
			if working_current >= required_current:
				current_change = power_change * BatteryManagementSystem.MAX_CURRENT
			else:
				current_change = 0	
    
			battery_to_increase_voltage = None
			battery_to_increase_current = None
			for module in self._batteryPack: #Checks if there is a battery in the battery pack that can accept the full increase to voltage/current
				if module.batteryCell.voltage + voltage_change > (BatteryManagementSystem.MAX_VOLTAGE / BatteryManagementSystem.NUMBER_OF_BATTERIES) and battery_to_increase_voltage == None:
					battery_to_increase_voltage = module.batteryCell
				if module.batteryCell.current + current_change > (BatteryManagementSystem.MAX_CURRENT / BatteryManagementSystem.NUMBER_OF_BATTERIES) and battery_to_increase_current == None:
					battery_to_increase_current = module.batteryCell
			
			num_increases = power_change / 0.01
			num_increases = int(num_increases)

			if battery_to_increase_voltage == None: #If there is no battery to accept the total increase, a random cell is increased by 0.01 power for as many times as 0.01 divides into the power change
				voltage_change = 0.01 * BatteryManagementSystem.MAX_VOLTAGE
				for increases in range(num_increases):
					battery_to_increase_voltage = choice(self._batteryPack).batteryCell
					battery_to_increase_voltage.updateVoltageData(new_power, voltage_change)
			else:
				battery_to_increase_voltage.updateVoltageData(new_power, voltage_change)

			if battery_to_increase_current == None:
				current_change = 0.01 * BatteryManagementSystem.MAX_CURRENT
				for increases in range(num_increases):
					battery_to_increase_current = choice(self._batteryPack).batteryCell
					battery_to_increase_current.updateCurrentData(new_power, current_change)
					battery_to_increase_current.generateTemperatureData()
			else:
				battery_to_increase_current.updateCurrentData(new_power, current_change)
				battery_to_increase_current.generateTemperatureData()
			
		else: #If the battery is at full power, sets the batteries as such
			for module in self._batteryPack:
				module.batteryCell.updateVoltageData(new_power, 0)
				module.batteryCell.updateCurrentData(new_power, 0)
				module.batteryCell.generateTemperatureData()
			
		self._power = new_power


	def getData(self):
		'''Causes the sensors to get the data produced
		from the batteries and power through the demandPower method.
		Reads all the batteries's parameters, stores them in a list
		and sends them to processData afterwards.'''

		temperatureValues = []
		voltageValues = []
		currentValues = []

		for batteryModule in self._batteryPack:

			currentBatteryCell = batteryModule.batteryCell

			batteryModule.temperatureSensor.readBattery(currentBatteryCell)
			batteryModule.currentSensor.readBattery(currentBatteryCell)
			batteryModule.voltageSensor.readBattery(currentBatteryCell)

			temperatureValues.append(batteryModule.temperatureSensor.temperatureValue)
			voltageValues.append(batteryModule.voltageSensor.voltageValue)
			currentValues.append(batteryModule.currentSensor.currentValue)

		return temperatureValues, voltageValues, currentValues

	def processData(self, temperatureList, voltageList, currentList):
		'''From battery pack, read each sensor list and check for errors.
		If errors exist, run their respective function.'''

		totalCurrent = 0
		self.printLists(temperatureList, voltageList, currentList)

		if max(temperatureList) > BatteryManagementSystem.MAX_TEMPERATURE:
			self.cooling(temperatureList)
			self.printAfterCooling(temperatureList)
			

		if max(voltageList) - min(voltageList) > BatteryManagementSystem.VOLTAGE_DIFF or max(voltageList) > (BatteryManagementSystem.MAX_VOLTAGE / BatteryManagementSystem.NUMBER_OF_BATTERIES):
			self.loadBalance(voltageList)
			self.printAfterLoadBalancing(voltageList)

		totalCurrent = sum(currentList)

		return totalCurrent

	
	def distanceDriven(self):
		'''Get the distance driven on current charge from the max distance.'''
		distanceDriven = BatteryManagementSystem.MAXIMUM_DISTANCE * (1 - (self._stateOfCharge/100))
		return distanceDriven
		

	def socAlgorithm(self, totalCurrent, timeTaken):
		'''Calculate SOC of battery using Coulomb counting.
		Q = I * t where I is the current and t is the time taken for the current to flow (each frame).
		Based on those parameters, we can calculate the amount of coulombs used 
		when discharging the battery.'''
		print("----------------------------------------")
		print(f"Total time used to calculate: {timeTaken}")
		print("----------------------------------------")
		amountOfCoulombs = totalCurrent * timeTaken
		self._stateOfCharge -= amountOfCoulombs  


	def sohAlgorithm(self):
		'''SOH is calculated by getting the average of charge/discharge cycles lifetime and battery lifetime, based on estimated lifetimes.'''
		
		self._stateOfHealth = (self._maxCapacity / BatteryManagementSystem.BATTERY_PACK_CAPACITY) * 100


	def distanceRemainingAlgorithm(self):
		'''Calculate the amount of SOC used and the distance driven.
		Based off that, calculate the distance remaining.\n
		Add the distance driven to the odometer too.'''

		#need to get the difference between distance driven before update and after
		lastDistanceDriven = self._distanceDriven
		#now update it based on new soc
		self._distanceDriven = self.distanceDriven()
		#get difference
		difference = self._distanceDriven-lastDistanceDriven
		#add this to mileage
		self.odometer.mileage = self.odometer.mileage + difference


		stateOfChargeUsed = self._initialStateOfCharge - self._stateOfCharge
		self._distanceRemaining = float((self._distanceDriven/stateOfChargeUsed) * self._stateOfCharge)


	def cooling(self, temperatureList):
		'''Reduce the temperature of the battery pack if temperature is over temperature threshold.
		For battery cells that are lower than the temperature threshold, it cools them slightly less.'''
		
		while True:
			for temperature in range(len(temperatureList)):
				if temperatureList[temperature] >= BatteryManagementSystem.MAX_TEMPERATURE:
					self._batteryPack[temperature].batteryCell.temperature -= 1
					temperatureList[temperature] -= 1
				elif temperatureList[temperature] <= BatteryManagementSystem.MIN_TEMPERATURE:
					continue
				else:
					self._batteryPack[temperature].batteryCell.temperature -= 0.5
					temperatureList[temperature] -= 0.5

			if max(temperatureList) < BatteryManagementSystem.MAX_TEMPERATURE:
				break

	
	def loadBalance(self, voltageList):
		'''Execute load balancing if voltage across the battery pack has a difference of 15 volts.'''
		required_voltage = self._power * BatteryManagementSystem.MAX_VOLTAGE
		voltage_per_cell = required_voltage / BatteryManagementSystem.NUMBER_OF_BATTERIES
		
		for battery_index in range(BatteryManagementSystem.NUMBER_OF_BATTERIES): #Redistributes power evenly by increasing or discreasing each battery as required to reach the equalised voltage amount
			voltage_change = voltage_per_cell - voltageList[battery_index]
			self._batteryPack[battery_index].batteryCell.updateVoltageData(self._power, voltage_change)
			voltageList[battery_index] = self._batteryPack[battery_index].batteryCell.voltage #Updates the passed in list of voltages for use with printing the results of load balancing


	def calculateNewMaxCapacity(self):
		"""Calculates the new max capacity after charge/discharge cycles have been incremented."""
		self._maxCapacity =  (1 - (self._chargeDischargeCycles / BatteryManagementSystem.CHARGE_DISCHARGE_MAXIMUM)) * BatteryManagementSystem.BATTERY_PACK_CAPACITY
		

	def stateOfChargeWarning(self):
		'''Warnings that display to the UI based on the current SOC.'''

		if self._stateOfCharge < 10:
			return "Please go to the nearest station to charge. Battery Percentage is very low."
		elif self._stateOfCharge < 25:
			return "Please consider charging soon. Battery percentage is low."
		elif self._stateOfCharge == 100:
			return "Battery Percent is now full. Please disconnect charger if plugged in."
		
		return ""


	def stateOfHealthWarning(self):
		'''Warnings that display to the UI based on the current SOH.'''

		if self._stateOfHealth < 40:
			return "Battery health is severely deteriorated."
		elif self._stateOfHealth < 60:
			return "Battery health is very deteriorated. "
		elif self._stateOfHealth < 75:
			return "Battery health has slightly deteriorated."

		return ""


	def printLists(self, temperatureList, voltageList, currentList):
		"""Prints out the list of sensor data after retrieving it."""
		print("----------------------------------------")
		print("Sensor Values for temperature, voltage and current")
		print(f"Temperature List: {temperatureList}")
		print(f"Voltage List: {voltageList}")
		print(f"Current List: {currentList}")
		print("----------------------------------------")


	def printAfterCooling(self, temperatureList):
		"""Prints out the temperature of the list after cooling funciton has occured.\n
		These values also show up on the battery cell itself based off index of the battery pack list."""
		print("----------------------------------------")
		print("Sensor values for temperature after cooling")
		print(f"Temperature List: {temperatureList}")
		print("----------------------------------------")


	def printAfterLoadBalancing(self, voltageList):
		"""Prints out the voltage of the list after load balancing funciton has occured.\n
		These values also show up on the battery cell itself based off index of the battery pack list."""
		print("----------------------------------------")
		print("Sensor values for voltage after load balancing.")
		print(f"Voltage List: {voltageList}")
		print("----------------------------------------")

	
	def getStateOfCharge(self):
		return self._stateOfCharge
	
	def setStateOfCharge(self, stateOfCharge):
		self._stateOfCharge = stateOfCharge
	
	def getStateOfHealth(self):
		return self._stateOfHealth

	def setStateOfHealth(self, stateOfHealth):
		self._stateOfHealth = stateOfHealth

	def getDistanceRemaining(self):
		return self._distanceRemaining

	def getTemperatureThreshold(self):
		return self._temperatureThreshold

	def setTemperatureThreshold(self, temperatureThreshold):
		self._temperatureThreshold = temperatureThreshold

	def getVoltageDifference(self):
		return self._voltageDifference
	
	def setVoltageDifference(self, voltageDifference):
		self._voltageDifference = voltageDifference

	def getCurrentThreshold(self):
		return self._currentThreshold

	def setCurrentThreshold(self, currentThreshold):
		self._currentThreshold = currentThreshold

	def getChargeDischargeCycles(self):
		return self._chargeDischargeCycles

	def setChargeDischargeCycles(self, value):
		self._chargeDischargeCycles = value
	
	def getInitialStateOfCharge(self):
		return self._initialStateOfCharge

	
	temperatureThreshold = property(getTemperatureThreshold, setTemperatureThreshold)
	voltageDifference = property(getVoltageDifference, setVoltageDifference)
	currentThreshold = property(getCurrentThreshold, setCurrentThreshold)
	distanceRemaining = property(getDistanceRemaining)
	chargeDischargeCycles = property(getChargeDischargeCycles, setChargeDischargeCycles)
	stateOfCharge = property(getStateOfCharge, setStateOfCharge)
	stateOfHealth = property(getStateOfHealth, setStateOfHealth)

