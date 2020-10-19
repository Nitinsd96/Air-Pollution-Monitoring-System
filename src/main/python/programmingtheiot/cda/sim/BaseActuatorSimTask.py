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
		
		self.LatestActuatorData = ActuatorData(actuatorType)
		self.simpleName = simpleName
	
		
	def activateActuator(self, val: float) -> bool:
		logging.info("Sending Actuator On Command")
		self.LatestActuatorData.command = ActuatorData.COMMAND_ON
		return True
		
	def deactivateActuator(self) -> bool:
		logging.info("Sending Actuator Off Command")
		self.LatestActuatorData.command = ActuatorData.COMMAND_OFF
		return True

		
	def getLatestActuatorResponse(self) -> ActuatorData:
		return self.LatestActuatorData

	
	def getSimpleName(self) -> str:
		return self.simpleName
	
	
	def updateActuator(self, data: ActuatorData) -> bool:
		if data != None:
			if (data.getCommand() == 0):
				self.deactivateActuator()
			else:
				self.activateActuator(data.getCommand())
				self.LatestActuatorData = data
				self.LatestActuatorData.setAsResponse()
		return True
