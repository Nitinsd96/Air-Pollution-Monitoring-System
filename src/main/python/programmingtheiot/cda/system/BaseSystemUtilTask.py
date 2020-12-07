#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#
import logging
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.SensorData import SensorData

class BaseSystemUtilTask():
	"""
	Shell representation of class for student implementation.
	
	"""
	latestSensorData = None
	def __init__(self,sensorName = ConfigConst.NOT_SET):
		###
		# TODO: fill in the details here
		self.sensorName = sensorName
		
		pass
	
	def generateTelemetry(self) -> SensorData:
		###
		# TODO: fill in the details here
		#
		# NOTE: Use self._getSystemUtil() to retrieve the value from the sub-class
		"""telemetry generation using SensorData"""
		self.latestSensorData = SensorData()
		self.latestSensorData.setValue(self._getSystemUtil())
		return self.latestSensorData
		
	def getTelemetryValue(self) -> float:
		"""
 		val = self._getSystemUtil()
 		logging.info("Sensor Value is %s",val )
 		return val
 		"""
		if self.latestSensorData == None :
			self.generateTelemetry()
		return self.latestSensorData.getValue()
		
 		
	
	def _getSystemUtil(self) -> float:
		"""
		Template method implemented by sub-class.
		
		Retrieve the system utilization value as a float.
		
		@return float
		"""
		pass
		