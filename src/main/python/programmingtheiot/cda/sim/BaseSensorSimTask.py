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

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.SensorData import SensorData

class BaseSensorSimTask():
	"""
	Shell representation of class for student implementation.
	
	"""

	DEFAULT_MIN_VAL = 0.0
	DEFAULT_MAX_VAL = 1000.0
	
	def __init__(self, sensorType: int = SensorData.DEFAULT_SENSOR_TYPE, dataSet = None, minVal: float = DEFAULT_MIN_VAL, maxVal: float = DEFAULT_MAX_VAL):
		
# 		self.sensorName = sensorName			
		self.LatestSensorData = SensorData() 
		self.LatestSensorData.minVal = minVal
		self.LatestSensorData.maxVal = maxVal
		self.LatestSensorData.dataSet = dataSet
		self.LatestSensorData.sensorType = sensorType
		
		self.LatestSensorData.currentDataSetIndex = 0   
		  
		self.LatestSensorData.useRandomizer = False    
		if dataSet == None :
			self.LatestSensorData.useRandomizer = True
			
	
	def generateTelemetry(self) -> SensorData:
# 		sensorData = SensorData(sensorType = self.sensorType, name = self.sensorName)    
# 		sensorData.sensorType = self.LatestSensorData.sensorType
# 		#sensorData.DEFAULT_SENSOR_TYPE = self.sensorType
#  		
# 		if self.useRandomizer == True :
# 			newValue = random.randint(self.LatestSensorData.minVal,self.LatestSensorData.maxVal)         
# 		else:
# 			newValue = self.dataSet.getDataEntry(self.currentDataSetIndex)
# 			if self.currentDataSetIndex == self.dataSet.getDataEntryCount():
# 				self.currentDataSetIndex = 0
# 			else:
# 				self.currentDataSetIndex = self.currentDataSetIndex+1
#  				
# 		sensorData.setValue(newValue)		
# 		self.LatestSensorData = sensorData
		
		self.LatestSensorData.setValue(random.randint(self.LatestSensorData.minVal,self.LatestSensorData.maxVal))
		return self.LatestSensorData
	
	def getTelemetryValue(self) -> float:
		if self.LatestSensorData != None:
			return self.LatestSensorData.getValue()
		else :
			self.LatestSensorData = self.generateTelemetry()
			return self.LatestSensorData.getValue()
	