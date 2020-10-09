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

from programmingtheiot.data.ActuatorData import ActuatorData

class BaseActuatorSimTask():
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self, actuatorType: int = ActuatorData.DEFAULT_ACTUATOR_TYPE, simpleName: str = "Actuator"):
		self.actuatorType = actuatorType
		self.simpleName = simpleName
		self.latestActuatorData = ActuatorData(actuatorType)
		pass
		
	def activateActuator(self, val: float) -> bool:
		logging.info("Sending Actuator On Command")
		self.latestActuatorData.setCommand(ActuatorData.COMMAND_ON)
		return True
		pass
		
	def deactivateActuator(self) -> bool:
		logging.info("Sending Actuator Off Command")
		self.latestActuatorData.setCommand(ActuatorData.COMMAND_OFF)
		return False
		pass
		
	def getLatestActuatorResponse(self) -> ActuatorData:
		pass
	
	def getSimpleName(self) -> str:
		pass
	
	def updateActuator(self, data: ActuatorData) -> bool:
		if data != None:
			if (data.command == 0):
				self.deactivateActuator()
			else:
				self.activateActuator(data.val)
		
		self.latestActuatorData = data
		self.latestActuatorData.setStatusCode(data.getStatusCode())
		self.latestActuatorData.setAsResponse()
		return True
		pass