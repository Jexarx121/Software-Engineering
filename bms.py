from temperatureSensor import TemperatureSensor
from voltageSensor import VoltageSensor
from currentSensor import CurrentSensor
from battery import BatteryCell
from batteryModule import BatteryModule
from datetime import date, today
from random import randint

class BatteryManagementSystem:

	NUMBER_OF_BATTERIES = 8
	BATTERY_MANUFACTURE_DATE = date(2021, 1, 1)
	CHARGE_DISCHARGE_MAXIMUM = 500
	BATTERY_LIFETIME_ESTIMATE = 4
	MAX_TEMPERATURE = 60

	def __init__(self):
		# all the calculaions in here

		# All battery cells made here
		# Every element in the battery pack is an object
		# of Battery Module class which represents 4 objects
		# Battery Cell, Temp, Current and Voltage Sensors

		self._max_voltage = 500
		self._max_current = 250

		self._batteryPack = [BatteryModule(self._max_voltage / BatteryManagementSystem.NUMBER_OF_BATTERIES, self._max_current / BatteryManagementSystem.NUMBER_OF_BATTERIES) for i in range(BatteryManagementSystem.NUMBER_OF_BATTERIES)] 

		self.temperatureSensor = TemperatureSensor()
		self.currentSensor = CurrentSensor()
		self.voltageSensor = VoltageSensor()

		# Each threshold is based off the battery cell threshold
		# Max threshold in battery / NUMBEROFBATTERIES
		self._temperatureThreshold = 0
		self._voltageThreshold = 0
		self._currentThreshold = 0

		self._stateOfCharge = 50
		self._stateOfHealth = 0

		# self.odometer = Odometer()
		# self.charger = Charger()
		
	def startProcess(self):
		start = time()
		
		self.demandPower()

		totalValues = self.getData()
		totalCurrent = totalValues[0]
		totalVoltage = totalValues[1]

		end = time()
		difference = end - start
				
		#we pass total current and time taken to soc algorithm
		self.socAlgorithm(totalCurrent, difference)
		self.sohAlgorithm()
				
		# display updated values to UI like SOC
		
		
	def demandPower(self):

		pass


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

		self.processData(temperatureValues, voltageValues, currentValues)

	def processData(self, temperatureList, voltageList, currentList):
		'''From battery pack, read each sensor list and check for errors.
		If errors exist, run their respective function.'''

		totalVoltage = 0
		totalCurrent = 0
		averageTemperature = 0

		for value in range(NUMBER_OF_BATTERIES):
			
			if temperatureList[value] >= self._temperatureThreshold:
				# cooling will change the current value in List
				# cooling will display a warning during the process
				# increasing the power needed 
				self.cooling(self._batteryPack[temperature])

			if voltageList[value] >= self._voltageThreshold:
				self.loadBalance()
			totalVoltage += voltage
			
			if currrentList[value] >= self._currentThreshold:
				totalCurrent += current
				

		return totalCurrent, totalVoltage
		# some display shennanigans as well

		  	
		
	def socAlgorithm(self, totalCurrent, timeTaken):
		'''calculate SOC of battery using either Coulomb counting or Kalman filtering'''

		# use time.time to measure times between each frame for the battery generation
		# read the data from sensors and bms starts processing data
		# time that moment or even check for errors and time after that
		# feed that time for Coulomb Counting
		# Q = I * t, I - total Current, t - time taken

		# totalCurrent = 25(each battery) therefore 150, timeTaken be 0.04seconds
		amountOfCoulombs = totalCurrent * timeTaken # = amp hours 150 * 0.004 = 0.6, maxCapacity =100
		#currentStateOfCharge 

		self._stateOfCharge -= amountOfCoulombs #67 - 0.6 = 66.4
		# soc will a value between 0 - maxCapacity
							
		self._stateOfCharge = (self._stateOfCharge / maxCapacity) * 100 # soc = 66.4% = 66.4%
		#runnning example = totalCurrent = 150, timeTaken = 0.04, self._stateOfCharge = 67
		#amountOfCoulombs = 150 * 0.04 = 0.6
		#self._stateOfCharge = 67 - 0.6 = 66.4
		#self._stateOfCharge = 66.4/ 100 * 100 = 66.4% to the GUI
		#self._stateOfCharge = 66.4/80 * 100 = 83% to the GUI (alternative example with lower maxCapacity)
		

		#current capacity will always be less than max capacity
		pass

	def sohAlgorithm(self):
		'''calculate SOH of battery using algo involving internal resistance measurement, counting charge/discharge cycles, SOC'''

		'''SOH is calculated by getting the average of charge/discharge cycles lifetime and battery lifetime, based on estimated lifetimes'''

		chargeDischargeCyclesPercentage = self._chargeDischargeCycles / self.CHARGE_DISCHARGE_MAXIMUM
		batteryLifetimePercentage = (today()-self.BATTERY_MANUFACTURE_DATE).years / 4
		return (chargeDischargeCyclesPercentage+batteryLifetimePercentage) * 50

		def distanceRemainingAlgorithm(self, mileage, stateOfCharge):
			distanceDriven = mileage - self._initialMileage
			stateOfChargeUsed = stateOfCharge - self._initialStateOfCharge
			return (distanceDriven/stateOfChargeUsed) * stateOfCharge

		def cooling(self):
			'''cool the battery(reduce temperature) if temperature is over limit'''

		# from temperatureSensor read Data from all the BatteryCell objects
		# If one is over a temperature limit, start cooling
		pass

		def loadBalance(self):
			'''execute load balancing if load is unbalanced'''

		# If we're doing voltage based balancing (easiest one imo)
		# set a difference threshold between voltages (usually difference of 0.1 to 1)
		# and if any cells exceed that threshold, start balancing by
		# drainig the voltage away or sharing it with other cells
		# Sharing it out could lead to over voltage

		# Need to account for faulty cells too
		# BMS needs to detect that and prohibit load balancing with these type of cells
		pass

		def stateOfChargeWarning(self):
		# warn the user if SOC is below a threshold to start charging
		# Or if the charging is done that the charging has ceased
		# display on gui from EV method

			if self._stateOfCharge < 10:
				return "Battery Percent is lower than 10%. Please go to the nearest station to charge."
			elif self._stateOfCharge < 25:
				return "Battery Percent is at 25%. Please consider charging soon."
			elif self._stateOfCharge >= 80:
				return "Battery Percent is near full. Charging will be complete soon."
			elif self._stateOfCharge == 100:
				return "Battery Percent is now 100%. Please disconnect the charger to conserve battery health."

	def stateOfHealthWarning(self):
		# warn the user if the SOH is below a threshold
		# substitute the battery and display on gui from EV method

		if self._stateOfHealth < 10:
			return "Battery health is severly deteriorated. Please consider changing the battery immediately for continued and safe usage of the vehicle."
		elif self._stateOfHealth < 25:
			return "Battery health is very deteriorated. Please consider changing the battery soon for continued and safe usage of the vehicle."
		elif self._stateOfHealth < 50:
			return "Battery health has deteriorated. Please consider checking the settings for detailed viewing of the battery health status."
	
	def getStateOfCharge(self):
		return self._stateOfCharge
	
	def setStateOfCharge(self, stateOfCharge):
		self._stateOfCharge = stateOfCharge
	
	def getStateOfHealth(self):
		return self._stateOfHealth

	def setStateOfHealth(self, stateOfHealth):
		self._stateOfHealth = stateOfHealth

	def getTemperatureThreshold(self):
		return self._temperatureThreshold

	def setTemperatureThreshold(self, temperatureThreshold):
		self._temperatureThreshold = temperatureThreshold

	def getVoltageThreshold(self):
		return self._voltageThreshold
	
	def setVoltageThreshold(self, voltageThreshold):
		self._voltageThreshold = voltageThreshold

	def getCurrentThreshold(self):
		return self._currentThreshold

	def setCurrentThreshold(self, currentThreshold):
		self._currentThreshold = currentThreshold
	
	temperatureThreshold = property(getTemperatureThreshold, setTemperatureThreshold)
	voltageThreshold = property(getVoltageThreshold, setVoltageThreshold)
	currentThreshold = property(getCurrentThreshold, setVoltageThreshold)
	stateOfCharge = property(getStateOfCharge, setStateOfCharge)
	stateOfHealth = property(getStateOfHealth, setStateOfHealth)

