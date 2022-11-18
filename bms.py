from batteryModule import BatteryModule
from odometer import Odometer
from datetime import date
from random import randint
from time import time


class BatteryManagementSystem():

	NUMBER_OF_BATTERIES = 8
	BATTERY_MANUFACTURE_DATE = date(2021, 1, 1)
	CHARGE_DISCHARGE_MAXIMUM = 500
	BATTERY_LIFETIME_ESTIMATE = 4
	MAX_TEMPERATURE = 60

	# Kilometers that this vehicle can travel on 100% SOC
	MAXIMUM_DISTANCE = 300

	# This is the capacity at manufacture date based on voltage threshold
	BATTERY_PACK_CAPACITY = 87.5

	def __init__(self):

		self._batteryPack = [BatteryModule() for i in range(
			BatteryManagementSystem.NUMBER_OF_BATTERIES)]

		self.odometer = Odometer()

		# Each threshold is based off the battery cell threshold
		# Max threshold in battery / NUMBEROFBATTERIES
		# KEVIN DECIDES ON THRESHOLD FROM BATTERY CELL
		self._temperatureThreshold = 0
		self._currentThreshold = 0

		self._voltageDifference = 0

		self._stateOfCharge = 80
		self._distanceDriven = BatteryManagementSystem.MAXIMUM_DISTANCE * (1 - (self._stateOfCharge/100))

		self._stateOfHealth = 100
		self._maxCapacity = (self._stateOfHealth / 100) * BatteryManagementSystem.BATTERY_PACK_CAPACITY

		self._initialStateOfCharge = self._stateOfCharge
		self._initialMileage = self.odometer.mileage

		self._chargeDischargeCycles = 0
		self._distanceRemaining = 0


	def startProcess(self, power):
		
		start = time()
  
		self.demandPower()
		
		dataSet = self.getData()
		totalCurrent = self.processData(dataSet[0], dataSet[1], dataSet[2])
  
		end = time()
		difference = end - start

		self.sohAlgorithm()
		self.socAlgorithm(totalCurrent, difference)
		self.distanceRemainingAlgorithm(self.odometer.mileage)
  
		#display some values to UI

	# KWECADUCK THE MAGNUS!!!!
	def demandPower(self):
		'''Generates data from the battery based on the change in power.
		Afterwards then calls the getData method.'''
		pass
	# KWECADUCK THE MAGNUS!!!!

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

		if max(temperatureList) >= self._temperatureThreshold:
			# increasing the power needed
			self.cooling(temperatureList)

		if max(voltageList) - min(voltageList) > self._voltageDifference:
			self.loadBalance(voltageList)

		totalCurrent = sum(currentList)

		return totalCurrent


	def socAlgorithm(self, totalCurrent, timeTaken):
		'''Calculate SOC of battery using Coulomb counting.
		Q = I * t where I is the current and t is the time taken for the current to flow (each frame).
		Based on those parameters, we can calculate the amount of coulombs used 
		when discharging the battery.'''

		amountOfCoulombs = totalCurrent * timeTaken
		self._stateOfCharge -= amountOfCoulombs  

		# Only reason for SOC being a percentage is for the display
		# Hence WE DO NOT NEED IT HERE


	def sohAlgorithm(self):
		'''SOH is calculated by getting the average of charge/discharge cycles lifetime and battery lifetime, based on estimated lifetimes'''

		chargeDischargeCyclesPercentage = self._chargeDischargeCycles / BatteryManagementSystem.CHARGE_DISCHARGE_MAXIMUM
		batteryLifetimePercentage = ((date.today()-self.BATTERY_MANUFACTURE_DATE)).days / BatteryManagementSystem.BATTERY_LIFETIME_ESTIMATE

		# Only reason for SOH being a percentage is for the display
		# Hence WE DO NOT NEED IT HERE
		self._stateOfHealth = ((chargeDischargeCyclesPercentage+batteryLifetimePercentage) / 2) 
		self._maxCapacity = (self._stateOfHealth / 100) * BatteryManagementSystem.BATTERY_PACK_CAPACITY


	def distanceRemainingAlgorithm(self, mileage):
		'''Calculate the amount of SOC used and the distance driven.
		Based off that, calculate the distance remaining.'''

		stateOfChargeUsed = self._initialStateOfCharge - self._stateOfCharge
		self._distanceRemaining = (self._distanceDriven/stateOfChargeUsed) * self._stateOfCharge


	def cooling(self, temperatureList):
		'''Reduce the temperature of the battery pack if temperature is over temperature threshold.
		For battery cells that are lower than the temperature threshold, it cools them slightly less.'''
		
		while True:
			for temperature in range(temperatureList):
				if temperatureList[temperature] >= self._temperatureThreshold:
					temperatureList[temperature] -= 1
				else:
					temperatureList[temperature] -= 0.5

			if max(temperatureList) < self._temperatureThreshold:
				break

	
	def loadBalance(self, voltageList):
		'''Execute load balancing if load is unbalanced'''

		# If we're doing voltage based balancing (easiest one imo)
		# set a difference threshold between voltages (usually difference of 0.1 to 1)
		# and if any cells exceed that threshold, start balancing by
		# drainig the voltage away or sharing it with other cells
		# Sharing it out could lead to over voltage

		# Need to account for faulty cells too
		# BMS needs to detect that and prohibit load balancing with these type of cells
		pass

	def stateOfChargeWarning(self):
		'''Warnings that display to the UI based on the current SOC.'''

		if self._stateOfCharge < 10:
			return "Battery Percent is lower than 10%. Please go to the nearest station to charge."
		elif self._stateOfCharge < 25:
			return "Battery Percent is at 25%. Please consider charging soon."
		elif self._stateOfCharge >= 80:
			return "Battery Percent is near full."
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

	
	def display(self):
		pass
	
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
	
	temperatureThreshold = property(getTemperatureThreshold, setTemperatureThreshold)
	voltageDifference = property(getVoltageDifference, setVoltageDifference)
	currentThreshold = property(getCurrentThreshold, setCurrentThreshold)
	stateOfCharge = property(getStateOfCharge, setStateOfCharge)
	stateOfHealth = property(getStateOfHealth, setStateOfHealth)

