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
	
	"""

	def __init__(self):
		super(HvacEmulatorTask, self).__init__(actuatorType = ActuatorData.HVAC_ACTUATOR_TYPE, simpleName = "HVAC")
		#obj = SenseHAT()
		self.emulate_flag = False
		if ConfigConst.ENABLE_SENSE_HAT_KEY == False:
			self.emulate_flag = True 
		#doubt
		enableEmulation = ConfigUtil._getConfig()
		self.sh = SenseHAT(emulate = enableEmulation)

	def _handleActuation(self, cmd: int, val: float = 0.0, stateData: str = None) -> int:
		if cmd == ActuatorData.COMMAND_ON:
			if self.sh.screen:
			# create a message with the value and an 'ON' message, then scroll it across the LED display
				logging.info("value %f and ON",ActuatorData.val)
				
				# meaning of scrolling it to LED display
			else:
				logging.warning("No SenseHAT LED screen instance to update.")
				return -1
		else:
			if self.sh.screen:
			# create a message with an 'OFF' message, then scroll it across the LED display
				logging.info("Off")
			else:
				logging.warning("No SenseHAT LED screen instance to clear / close.")
				return -1
	