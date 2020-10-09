#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

from programmingtheiot.data.BaseIotData import BaseIotData

class ActuatorData(BaseIotData):
	"""
	Shell representation of class for student implementation.
	
	"""
	DEFAULT_COMMAND = 0
	COMMAND_OFF = DEFAULT_COMMAND
	COMMAND_ON = 1

	# for now, actuators will be 1..99
	# and displays will be 100..1999
	DEFAULT_ACTUATOR_TYPE = 0
	
	HVAC_ACTUATOR_TYPE = 1
	HUMIDIFIER_ACTUATOR_TYPE = 2
	LED_DISPLAY_ACTUATOR_TYPE = 100
	
	
	command = DEFAULT_COMMAND
	
	def __init__(self, actuatorType = DEFAULT_ACTUATOR_TYPE, d = None):
		self.type = actuatorType
		super(ActuatorData, self).__init__(d = d)
		
	
	def getCommand(self) -> int:
		return self.command
	
	def getStateData(self) -> str:
		return self.stateData
		"pass"
	
	def getValue(self) -> float:
		return self.val
	
	
	def isResponseFlagEnabled(self) -> bool:
		return False
	
	def setCommand(self, command: int):
		self.command = command
	
	def setAsResponse(self):
		pass
		
	def setStateData(self, stateData: str):
		self.stateData = stateData

	
	def setValue(self, val: float):
		self.val = val
		"pass"
		
	def _handleUpdateData(self, data):
		self.command = data.getCommand()
		self.stateData = data.getStateData()
		self.val = data.getValue()
		
		