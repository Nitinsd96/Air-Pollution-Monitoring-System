#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

from programmingtheiot.data.SensorData import SensorData

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.cda.sim.BaseSensorSimTask import BaseSensorSimTask
from programmingtheiot.cda.sim.SensorDataGenerator import SensorDataGenerator

from pisense import SenseHAT

class PressureSensorEmulatorTask(BaseSensorSimTask):
	"""
	Shell representation of class for student implementation.
	
	
	Handling HumiditySensor Emulation
	Invoking SenseHAT
	Sensing/Storing Data from SenseHat Emulator
	
	
	"""
	enableEmulation = None
	def __init__(self, dataSet = None):
		super(PressureSensorEmulatorTask, self).__init__(SensorData.PRESSURE_SENSOR_TYPE, minVal = SensorDataGenerator.LOW_NORMAL_ENV_PRESSURE, maxVal = SensorDataGenerator.HI_NORMAL_ENV_PRESSURE)
		if(ConfigConst.ENABLE_SENSE_HAT_KEY == True):
			self.enableEmulation = True
		elif(ConfigConst.ENABLE_SENSE_HAT_KEY == False):
			self.enableEmulation = False
		self.sh = SenseHAT(emulate = self.enableEmulation)
	
	
	"""Returning Object with latest value for humidity"""
	def generateTelemetry(self) -> SensorData:
		sensorData = SensorData(sensorType = 2)
		sensorVal = self.sh.environ.pressure		
		sensorData.setValue(sensorVal)
		self.LatestSensorData = sensorData

		return self.LatestSensorData
