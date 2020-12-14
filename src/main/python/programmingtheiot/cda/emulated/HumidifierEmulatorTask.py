#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from time import sleep

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.cda.sim.BaseActuatorSimTask import BaseActuatorSimTask

from pisense import SenseHAT

class HumidifierEmulatorTask(BaseActuatorSimTask):
	"""
	Shell representation of class for student implementation.
	Handling Humidifier Emulation
	Invoking SenseHAT
	Here Actuation is to Display Value on LED
	"""
	
	enableEmulation = None
	def __init__(self):
		super(HumidifierEmulatorTask, self).__init__(actuatorType = ActuatorData.HUMIDIFIER_ACTUATOR_TYPE, simpleName = "HUMIDIFIER",actuatorName = ConfigConst.HUMIDIFIER_ACTUATOR_NAME)
		if(ConfigConst.ENABLE_SENSE_HAT_KEY == True):
			self.enableEmulation = True
		elif(ConfigConst.ENABLE_SENSE_HAT_KEY == False):
			self.enableEmulation = False
		self.sh = SenseHAT(emulate = self.enableEmulation)


	""" Actuation is done by showing output on LED
		Used SenseHAT inbuilt library and methods to display String on LED	
	"""
	def _handleActuation(self, cmd: int, val: float = 0.0, stateData: str = None) -> int:
		if cmd == ActuatorData.COMMAND_ON:
			if self.sh.screen:
			# create a message with the value and an 'ON' message, then scroll it across the LED display
				Text_to_display = " Device ON & value {}".format(val)
				self.sh.screen.scroll_text(Text_to_display)
				
				# meaning of scrolling it to LED display
			else:
				logging.warning("No SenseHAT LED screen instance to update.")
				return -1
		else:
			if self.sh.screen:
			# create a message with an 'OFF' message, then scroll it across the LED display
				Text_to_display = " ALARM: Humidity High"
				self.sh.screen.scroll_text(Text_to_display)
			else:
				logging.warning("No SenseHAT LED screen instance to clear / close.")
				return -1
			
