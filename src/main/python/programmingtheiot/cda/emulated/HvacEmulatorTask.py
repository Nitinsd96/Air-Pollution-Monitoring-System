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

class HvacEmulatorTask(BaseActuatorSimTask):
	"""
	Shell representation of class for student implementation.
	
	Shell representation of class for student implementation.
	Handling Hvac Emulation
	Invoking SenseHAT
	Here Actuation is to Display Value on LED
	
	"""
	enableEmulation = None
	def __init__(self):
		super(HvacEmulatorTask, self).__init__(actuatorType = ActuatorData.HVAC_ACTUATOR_TYPE, simpleName = "HVAC")
		enableEmulation = False
		if ConfigConst.ENABLE_SENSE_HAT_KEY == True:
			enableEmulation = True 
		self.sh = SenseHAT(emulate = enableEmulation)

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
				Text_to_display = " Device OFF"
				self.sh.screen.scroll_text(Text_to_display)
			else:
				logging.warning("No SenseHAT LED screen instance to clear / close.")
				return -1
	