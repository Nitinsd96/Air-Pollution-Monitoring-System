#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import random

from programmingtheiot.data.SensorData import SensorData

class BaseSensorSimTask():
	"""
	Shell representation of class for student implementation.
	
	"""

	DEFAULT_MIN_VAL = 0.0
	DEFAULT_MAX_VAL = 1000.0
	
	def __init__(self, sensorType: int = SensorData.DEFAULT_SENSOR_TYPE, dataSet = None, minVal: float = DEFAULT_MIN_VAL, maxVal: float = DEFAULT_MAX_VAL):
		self.dataSet = dataSet
		self.sensorType = sensorType
		self.minVal = minVal
		self.maxVal = maxVal
		
		self.currentDataSetIndex = 0      						
		self.LatestSensorData = SensorData(sensorType)   
		self.useRandomizer = False    
		if self.dataSet == None :
			self.useRandomizer = True
			
	
	def generateTelemetry(self) -> SensorData:
		sensorData = SensorData(sensorType = self.sensorType)    
		newValue = 0
		sensorData.DEFAULT_SENSOR_TYPE = self.sensorType
		
		if self.useRandomizer == True :
			newValue = random.randint(self.minVal,self.maxVal)         
		else:
			newValue = self.dataSet.getDataEntry(self.currentDataSetIndex)
			if self.currentDataSetIndex == self.dataSet.getDataEntryCount():
				self.currentDataSetIndex = 0
			else:
				self.currentDataSetIndex = self.currentDataSetIndex+1
				
		sensorData.setValue(newValue)		
		self.LatestSensorData = sensorData
		return sensorData   
	
	def getTelemetryValue(self) -> float:
		if self.LatestSensorData :
			return self.LatestSensorData.getValue()
		else :
			self.LatestSensorData = self.generateTelemetry()
			return self.LatestSensorData.getValue()
	