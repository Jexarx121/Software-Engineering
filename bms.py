from batteryModule import BatteryModule
from odometer import Odometer
from datetime import date
from random import randint, choice
from time import time


class BatteryManagementSystem():
	'''Represents a battery management system for an electric vehicle.'''

	BATTERY_MANUFACTURE_DATE = date(2021, 1, 1)
	BATTERY_LIFETIME_ESTIMATE = 365 * 9

	NUMBER_OF_BATTERIES = 8
	DEPTH_OF_DISCHARGE = 100
	# Assuming 80 - 100% DOD
	CHARGE_DISCHARGE_MAXIMUM = 500
	MIN_TEMPERATURE = 12
	MAX_TEMPERATURE = 50
	MIN_TEMPERATURE = 12
	MAX_VOLTAGE = 500
	MAX_CURRENT = 200
	VOLTAGE_DIFF = 15

	# Kilometers that this vehicle can travel on 100% SOC
	MAXIMUM_DISTANCE = 300

	# This is the capacity at manufacture date based on voltage threshold
	BATTERY_PACK_CAPACITY = 87.5

	def __init__(self):

		self._power = 0

		self._batteryPack = [BatteryModule(BatteryManagementSystem.MAX_VOLTAGE / BatteryManagementSystem.NUMBER_OF_BATTERIES, BatteryManagementSystem.MAX_CURRENT / BatteryManagementSystem.NUMBER_OF_BATTERIES) for i in range(
			BatteryManagementSystem.NUMBER_OF_BATTERIES)]

		self.odometer = Odometer()

		self._stateOfCharge = 50
		self._distanceDriven = self.distanceDriven()

		self._initialStateOfCharge = 100
		self._initialMileage = self.odometer.mileage

		# charge discharge cycles only increase after car stops and turns on again after charging or discharging entirely 
		self._chargeDischargeCycles = 129.3

		# Might have to round this off depending on numbers
		self._maxCapacity = (1 - (self._chargeDischargeCycles / BatteryManagementSystem.CHARGE_DISCHARGE_MAXIMUM)) * BatteryManagementSystem.BATTERY_PACK_CAPACITY
		self._distanceRemaining = BatteryManagementSystem.MAXIMUM_DISTANCE * (self._stateOfCharge/100)

		self._stateOfHealth = 0
		self.sohAlgorithm()
		self._chargeThreshold = 100

	def startProcess(self, power):
		
		start = time()
  
		self.demandPower(power)
		
		dataSet = self.getData()
		totalCurrent = self.processData(dataSet[0], dataSet[1], dataSet[2])
  
		end = time()
		difference = end - start

		self.sohAlgorithm()
		self.socAlgorithm(totalCurrent, difference)
		self.distanceRemainingAlgorithm()
  
		#display some values to UI

	def powerOn(self, new_power):
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
		for module in self._batteryPack:
			module.batteryCell.state = False
			module.batteryCell.updateVoltageData(0, 0)
			module.batteryCell.updateCurrentData(0, 0)
			module.batteryCell.generateTemperatureData()
   

        

	def demandPower(self, new_power):
		'''Increments data in the battery based on the power.'''
		required_voltage = new_power * BatteryManagementSystem.MAX_VOLTAGE
		required_current = new_power * BatteryManagementSystem.MAX_CURRENT
  
		if new_power < 1:
			working_voltage = 0
			working_current = 0

			for module in self._batteryPack:
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
			for module in self._batteryPack:
				if module.batteryCell.voltage + voltage_change > (BatteryManagementSystem.MAX_VOLTAGE / BatteryManagementSystem.NUMBER_OF_BATTERIES) and battery_to_increase_voltage == None:
					battery_to_increase_voltage = module.batteryCell
				if module.batteryCell.current + current_change > (BatteryManagementSystem.MAX_CURRENT / BatteryManagementSystem.NUMBER_OF_BATTERIES) and battery_to_increase_current == None:
					battery_to_increase_current = module.batteryCell

			num_increases = power_change / 0.1
			if battery_to_increase_voltage == None:
				voltage_change = 0.1 * BatteryManagementSystem.MAX_VOLTAGE
				num_increases = int(num_increases)
				for increases in range(num_increases):
					battery_to_increase_voltage = choice(self._batteryPack).batteryCell
					battery_to_increase_voltage.updateVoltageData(new_power, voltage_change)
			else:
				battery_to_increase_voltage.updateVoltageData(new_power, voltage_change)

			if battery_to_increase_current == None:
				current_change = 0.1 * BatteryManagementSystem.MAX_CURRENT
				for increases in range(num_increases):
					battery_to_increase_current = choice(self._batteryPack).batteryCell
					battery_to_increase_current.updateCurrentData(new_power, current_change)
					battery_to_increase_current.generateTemperatureData()
			else:
				battery_to_increase_current.updateCurrentData(new_power, current_change)
				battery_to_increase_current.generateTemperatureData()
			
		else:
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
			# increasing the power needed
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
  #distance driven = 300* (1- 0.5) = 150
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
		
		# print(f"Max capacity: {self._maxCapacity}")
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
				else: 
					if self._batteryPack[temperature].batteryCell.temperature <= BatteryManagementSystem.MIN_TEMPERATURE:
						#this prevents it from going to low
						continue
					self._batteryPack[temperature].batteryCell.temperature -= 0.5
					temperatureList[temperature] -= 0.5

			if max(temperatureList) < BatteryManagementSystem.MAX_TEMPERATURE:
				break

	
	def loadBalance(self, voltageList):
		'''Execute load balancing if load is unbalanced'''
		required_voltage = self._power * BatteryManagementSystem.MAX_VOLTAGE
		voltage_per_cell = required_voltage / BatteryManagementSystem.NUMBER_OF_BATTERIES
		
		for battery_index in range(BatteryManagementSystem.NUMBER_OF_BATTERIES):
			voltage_change = voltage_per_cell - voltageList[battery_index]
			self._batteryPack[battery_index].batteryCell.updateVoltageData(self._power, voltage_change)
			voltageList[battery_index] = self._batteryPack[battery_index].batteryCell.voltage


	def stateOfChargeWarning(self):
		'''Warnings that display to the UI based on the current SOC.'''

		if self._stateOfCharge < 10:
			return "Please go to the nearest station to charge. Battery Percentage is very low."
		elif self._stateOfCharge < 25:
			return "Please consider charging soon. Battery percentage is low."
		elif self._stateOfCharge == 100:
			return "Battery Percent is now 100%."
		
		return ""

	def stateOfHealthWarning(self):
		'''Warnings that display to the UI based on the current SOH.'''

		if self._stateOfHealth < 10:
			return "Battery health is severly deteriorated."
		elif self._stateOfHealth < 25:
			return "Battery health is very deteriorated. "
		elif self._stateOfHealth < 50:
			return "Battery health has deteriorated."

		return ""

	def printLists(self, temperatureList, voltageList, currentList):
		print("----------------------------------------")
		print("Sensor Values for temperature, voltage and current")
		print(f"Temperature List: {temperatureList}")
		print(f"Voltage List: {voltageList}")
		print(f"Current List: {currentList}")
		print("----------------------------------------")

	def printAfterCooling(self, temperatureList):
		print("----------------------------------------")
		print("Sensor values for temperature after cooling")
		print(f"Temperature List: {temperatureList}")
		print("----------------------------------------")

	def printAfterLoadBalancing(self, voltageList):
		print("----------------------------------------")
		print("Sensor values for voltage after cooling")
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
		self._chargeDischargeCycles += value
	
	def getInitialStateOfCharge(self):
		return self._initialStateOfCharge

	
	temperatureThreshold = property(getTemperatureThreshold, setTemperatureThreshold)
	voltageDifference = property(getVoltageDifference, setVoltageDifference)
	currentThreshold = property(getCurrentThreshold, setCurrentThreshold)
	distanceRemaining = property(getDistanceRemaining)
	chargeDischargeCycles = property(getChargeDischargeCycles, setChargeDischargeCycles)
	stateOfCharge = property(getStateOfCharge, setStateOfCharge)
	stateOfHealth = property(getStateOfHealth, setStateOfHealth)

