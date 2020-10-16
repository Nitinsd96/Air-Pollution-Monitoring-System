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
	
	"""

	def __init__(self):
		super(LedDisplayEmulatorTask, self).__init__(actuatorType = ActuatorData.LED_DISPLAY_ACTUATOR_TYPE, simpleName = "LED_Display")
		#obj = SenseHAT()
		self.emulate_flag = False
		if ConfigConst.ENABLE_SENSE_HAT_KEY == False:
			self.emulate_flag = True 
		#doubt
		enableEmulation = ConfigUtil._getConfig()
		self.sh = SenseHAT(emulate = enableEmulation)

	def _handleActuation(self, cmd: int, val: float = 0.0, stateData: str = None) -> int:
		#if the command is 'ON', scroll the state data across the screen. If the command is 'OFF', clear the LED display.
		
		