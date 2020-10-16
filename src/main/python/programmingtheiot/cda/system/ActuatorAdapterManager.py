#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from programmingtheiot.common.IDataMessageListener import IDataMessageListener

from programmingtheiot.data.ActuatorData import ActuatorData

from programmingtheiot.cda.sim.HumidifierActuatorSimTask import HumidifierActuatorSimTask
from programmingtheiot.cda.sim.HvacActuatorSimTask import HvacActuatorSimTask


class ActuatorAdapterManager(object):
	"""
	Shell representation of class for student implementation.
	
	"""
	useEmulator = None
	dataMsgListener = None 

	
	def __init__(self, useEmulator: bool = False):
		self.useEmulator = useEmulator
		if(self.useEmulator == True):
			logging("Emulators will be used")
			
			humidifierModule = __import__('programmingtheiot.cda.emulated.HumidifierEmulatorTask', fromlist = ['HumidifierEmulatorTask'])
			hueClazz = getattr(humidifierModule, 'HumidifierEmulatorTask')
			self.humidifierEmulator = hueClazz()
			
			hvacModule = __import__('programmingtheiot.cda.emulated.hvacEmulatorTask', fromlist = ['HvacEmulatorTask'])
			hueClazz = getattr(hvacModule, 'HvacEmulatorTask')
			self.hvacEmulator = hueClazz()
			
			LedDisplayModule = __import__('programmingtheiot.cda.emulated.LedDisplayEmulatorTask', fromlist = ['LedDIsplayEmulatorTask'])
			hueClazz = getattr(LedDisplayModule, 'LedEmulatorTask')
			self.LedDisplayEmulator = hueClazz()
			
		else:
			logging.info("Testing ActuatorAdapterManager class [using simulators]...")
			# create the humidifier actuator
			self.humidifierActuator = HumidifierActuatorSimTask()
			# create the HVAC actuator
			self.hvacActuator = HvacActuatorSimTask()
			pass


	def sendActuatorCommand(self, data: ActuatorData) -> bool:
		logging.info("Actuator command received. Processing...")
		if(self.useEmulator == False):
			if(data.type == data.HUMIDIFIER_ACTUATOR_TYPE):
				if(data.getCommand()==0):
					logging.info("Emulating HUMIDIFIER actuator OFF:")
					logging.info("---------------------------------------")
				else:
					logging.info("Emulating HUMIDIFIER actuator ON:")
					logging.info(" Humidifier value : %s", data.val) 
			elif (data.type == data.HVAC_ACTUATOR_TYPE):
				if(data.getCommand()==0):
					logging.info("Emulating HVAC actuator OFF:")
					logging.info("---------------------------------------")
			else:
				logging.info("Emulating HVAC actuator ON:")
				logging.info(" HVAC value : %s", data.actuatorValue)
			return True
		else:
			return False

		pass
	
	def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
		if( listener != None):
			self.dataMsgListener = listener 
		else:
			self.dataMsgListener = False

		pass
