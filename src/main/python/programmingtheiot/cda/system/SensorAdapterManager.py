#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from apscheduler.schedulers.background import BackgroundScheduler

from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.cda.sim.TemperatureSensorSimTask import TemperatureSensorSimTask
from programmingtheiot.cda.sim.HumiditySensorSimTask import HumiditySensorSimTask
from programmingtheiot.cda.sim.PressureSensorSimTask import PressureSensorSimTask 

from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common import ConfigConst


class SensorAdapterManager(object):
	"""
	Shell representation of class for student implementation.
	

	Handling All Sensors - invoking respective classes depending on input : Simulator or Emulator
	
	Sending respective commands to store Data/Values either from Simulator or Emulator
	
	
	
	"""

	def __init__(self, useEmulator: bool = True, pollRate: int = 5, allowConfigOverride: bool = True):
		self.useEmulator = useEmulator
		self.pollRate = pollRate
		
		
		self.allowConfigOverride = allowConfigOverride
		
		self.scheduler = BackgroundScheduler()
		self.scheduler.add_job(self.handleTelemetry, 'interval', seconds = self.pollRate)
		self.dataMsgListener = None
		
		if(self.useEmulator == True):
			logging.info("Emulators are being used")
			humidityModule = __import__('programmingtheiot.cda.emulated.HumiditySensorEmulatorTask', fromlist = ['HumiditySensorEmulatorTask'])
			heClazz = getattr(humidityModule, 'HumiditySensorEmulatorTask')
			self.humidityEmulator = heClazz()
			
			pressureModule = __import__('programmingtheiot.cda.emulated.PressureSensorEmulatorTask', fromlist = ['PressureSensorEmulatorTask'])
			heClazz = getattr(pressureModule, 'PressureSensorEmulatorTask')
			self.pressureEmulator = heClazz()
			
			tempModule = __import__('programmingtheiot.cda.emulated.TemperatureSensorEmulatorTask', fromlist = ['TemperatureSensorEmulatorTask'])
			heClazz = getattr(tempModule, 'TemperatureSensorEmulatorTask')
			self.tempEmulator = heClazz()
			
			
		else:
			logging.info("Simulators are being used")
			self.dataGenerator = SensorDataGenerator()
			configUtil = ConfigUtil()
			
			humidity_floor = configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.HUMIDITY_SIM_FLOOR_KEY, SensorDataGenerator.LOW_NORMAL_ENV_HUMIDITY)
			humidity_ceiling = configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.HUMIDITY_SIM_CEILING_KEY, SensorDataGenerator.HI_NORMAL_ENV_HUMIDITY)
	
			pressure_Floor = configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.PRESSURE_SIM_FLOOR_KEY, SensorDataGenerator.LOW_NORMAL_ENV_PRESSURE)
			pressure_ceiling = configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.PRESSURE_SIM_CEILING_KEY, SensorDataGenerator.HI_NORMAL_ENV_PRESSURE)
	
			temp_floor = configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.TEMP_SIM_FLOOR_KEY, SensorDataGenerator.LOW_NORMAL_INDOOR_TEMP)
			temp_ceiling = configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.TEMP_SIM_CEILING_KEY, SensorDataGenerator.HI_NORMAL_INDOOR_TEMP)
	
	
			self.humidityData = self.dataGenerator.generateDailyEnvironmentHumidityDataSet(minValue = humidity_floor, maxValue = humidity_ceiling, useSeconds = False)
	
			self.pressureData = self.dataGenerator.generateDailyEnvironmentPressureDataSet(minValue=pressure_Floor, maxValue = pressure_ceiling, useSeconds = False)
	
			self.tempData =  self.dataGenerator.generateDailyIndoorTemperatureDataSet(minValue = temp_floor, maxValue = temp_ceiling, useSeconds = False)
	
			self.humiditySensorSimTask = HumiditySensorSimTask(self.humidityData) 
			self.pressureSensorSimTask = PressureSensorSimTask(self.pressureData)
			self.temperatureSensorSimTask = TemperatureSensorSimTask(self.tempData)
	
			logging.info("Simulated Humidity Sensor Sim Task Value is: %s ", self.humiditySensorSimTask.LatestSensorData)
			logging.info("Simulated Pressure Sensor Sim Task Value is : %s ", self.pressureSensorSimTask.LatestSensorData)
			logging.info("Simulated Temperature Sensor Sim Task Value is: %s ", self.temperatureSensorSimTask.LatestSensorData)
			self.handleTelemetry()
		pass	


		
	"""
	Displaying sensor values on console by calling Simulator/Emulator methods as per useEmulator flag
	"""
	
	def handleTelemetry(self):
		if(self.useEmulator == False):
			self.humiditySensorSimTask.generateTelemetry()
			logging.info("Simulated Humidity Sensor value is %s ",self.humiditySensorSimTask.getTelemetryValue())
			self.pressureSensorSimTask.generateTelemetry()
			logging.info("Simulated Pressure Sensor value is %s ",self.pressureSensorSimTask.getTelemetryValue())
			self.temperatureSensorSimTask.generateTelemetry()
			logging.info("Simulated Temperature Sensor value is %s ",self.temperatureSensorSimTask.getTelemetryValue())
		elif(self.useEmulator == True):
			humidity = self.humidityEmulator.generateTelemetry()
			logging.info("Emulated Humidity Sensor value is %s ",self.humidityEmulator.getTelemetryValue())
			
			pressure = self.pressureEmulator.generateTelemetry()
			logging.info("Emulated Pressure Sensor value is %s ",self.pressureEmulator.getTelemetryValue())
			
			temp = self.tempEmulator.generateTelemetry()
			logging.info("Emulated Temperature Sensor value is %s ",self.tempEmulator.getTelemetryValue())
			
		self.dataMsgListener.handleSensorMessage(humidity)
		self.dataMsgListener.handleSensorMessage(pressure)
		self.dataMsgListener.handleSensorMessage(temp)

		
	def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
		if( listener != None):
				self.dataMsgListener = listener
				logging.info("Setting listener")
				return True
			
		return False
	
	def startManager(self):
		self.scheduler.start()
	
		
	def stopManager(self):
		self.scheduler.shutdown()
		
