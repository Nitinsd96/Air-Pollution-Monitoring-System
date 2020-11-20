#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#
import json
from json import JSONEncoder

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

class DataUtil():
	"""
	Shell representation of class for student implementation.
	
	"""
	
	
	def __init__(self, encodeToUtf8 = False):
		pass
	
	"""return jsonData, after conversion from actuatorData"""
	def actuatorDataToJson(self, actuatorData):
		jsonData = json.dumps(actuatorData, indent = 4, cls = JsonDataEncoder, ensure_ascii = True)
		return jsonData
	
	"""return jsonData, after conversion from SensorData"""
	def sensorDataToJson(self, sensorData):
		jsonData = json.dumps(sensorData, indent = 4, cls = JsonDataEncoder, ensure_ascii = True)
		return jsonData

	"""return jsonData, after conversion from sysPerfData"""
	def systemPerformanceDataToJson(self, sysPerfData):
		jsonData = json.dumps(sysPerfData, indent = 4, cls = JsonDataEncoder, ensure_ascii = True)
		return jsonData

	"""return actuatorData, after conversion from jsonData"""	
	def jsonToActuatorData(self, jsonData):
		jsonData = jsonData.replace("\'", "\"").replace('False','false').replace('True', 'true')
		adDict = json.loads(jsonData)
# 		print("value of adDict---")
# 		print(adDict)
		ad = ActuatorData()
# 		print("value of ad---")
# 		print(ad)
		mvDict = vars(ad)
# 		print("value of mvDict---")
# 		print(mvDict)
		for key in adDict:
			if key in mvDict:
				setattr(ad, key, adDict[key])
# 		print("value of adDict---2nd")
# 		print(adDict)
		return ad
	
	"""return jsensorData, after conversion from jsonData"""
	def jsonToSensorData(self, jsonData):
		jsonData = jsonData.replace("\'", "\"").replace('False','false').replace('True', 'true')
		adDict = json.loads(jsonData)
		ad = SensorData()
		print(ad)
		mvDict = vars(ad)

		for key in adDict:
			if key in mvDict:
				setattr(ad, key, adDict[key])
		return ad

		
	"""return systemPerformaceData, after conversion from jsonData"""
	def jsonToSystemPerformanceData(self, jsonData):
		jsonData = jsonData.replace("\'", "\"").replace('False','false').replace('True', 'true')
		adDict = json.loads(jsonData)
		ad = SystemPerformanceData()
		mvDict = vars(ad)

		for key in adDict:
			if key in mvDict:
				setattr(ad, key, adDict[key])
		return ad

	
class JsonDataEncoder(JSONEncoder):
	"""
	Convenience class to facilitate JSON encoding of an object that
	can be converted to a dict.
	
	"""
	def default(self, o):
		return o.__dict__
	