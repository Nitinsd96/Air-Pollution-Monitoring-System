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

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask

from pisense import SenseHAT

class LedDisplayEmulatorTask(BaseActuatorSimTask):
	"""
	Shell representation of class for student implementation.
	
	Handling LEDDISPLAY Emulation
	Invoking SenseHAT
	Here Actuation is to Display Value on LED
	
	"""
	enableEmulation = None
	def __init__(self):
		super(LedDisplayEmulatorTask, self).__init__(actuatorType = ActuatorData.LED_DISPLAY_ACTUATOR_TYPE, simpleName = "LED_Display",actuatorName = ConfigConst.LED_ACTUATOR_NAME)
		if(ConfigConst.ENABLE_SENSE_HAT_KEY == True):
			self.enableEmulation = True
		elif(ConfigConst.ENABLE_SENSE_HAT_KEY == False):
			self.enableEmulation = False
		self.sh = SenseHAT(emulate = self.enableEmulation)



	""" Actuation is done by showing output on LED
		Used SenseHAT inbuilt library and methods to display String on LED	
	"""
	def _handleActuation(self, cmd: int, val: float = 0.0, stateData: str = None) -> int:
		#if the command is 'ON', scroll the state data across the screen. If the command is 'OFF', clear the LED display.
		print("jsfvbjd")
		if cmd == ActuatorData.COMMAND_ON:
			#scroll data on screen
			Text_to_Display = "Displaying DATA"
			self.sh.screen.scroll_text(Text_to_Display)
			self.sh.screen.scroll_text(stateData)
			
		else:
			#clear LED display
			Text_to_Display = "ALARM : Temperature is High"
			self.sh.screen.scroll_text(Text_to_Display)
			self.sh.screen.clear()
		