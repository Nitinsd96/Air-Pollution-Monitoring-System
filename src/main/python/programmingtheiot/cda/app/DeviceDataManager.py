#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from programmingtheiot.cda.connection.CoapClientConnector import CoapClientConnector
from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector

from programmingtheiot.cda.system.ActuatorAdapterManager import ActuatorAdapterManager
from programmingtheiot.cda.system.SensorAdapterManager import SensorAdapterManager
from programmingtheiot.cda.system.SystemPerformanceManager import SystemPerformanceManager

from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.data.ActuatorData import ActuatorData
from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.SystemPerformanceData import SystemPerformanceData

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common import ConfigConst
from programmingtheiot.data.DataUtil import DataUtil



class DeviceDataManager(IDataMessageListener):
	"""
	Shell representation of class for student implementation.
	
	"""
	
	def __init__(self, enableMqtt: bool = True, enableCoap: bool = False):
		self.sysPerfManager = SystemPerformanceManager()
		self.sensorAdapterManager = SensorAdapterManager()
		self.actuatorAdapterManager = ActuatorAdapterManager()
		self.configUtil = ConfigUtil()
		self.enableHandleTempChangeOnDevice = self.configUtil.getBoolean(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.ENABLE_HANDLE_TEMP_CHANGE_ON_DEVICE_KEY)
		self.triggerHvacTempFloor = self.configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.TRIGGER_HVAC_TEMP_FLOOR_KEY)
		self.triggerHvacTempCeiling = self.configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.TRIGGER_HVAC_TEMP_CEILING_KEY)

			
	def handleActuatorCommandResponse(self, data: ActuatorData) -> bool:
		logging("handleActuatorCommandResponse method is called...")
		self._handleUpstreamTransmission(ResourceNameEnum.CDA_ACTUATOR_RESPONSE_RESOURCE, DataUtil.actuatorDataToJson(self, data))
		pass

	
	def handleIncomingMessage(self, resourceEnum: ResourceNameEnum, msg: str) -> bool:
		logging("handleIncomingMessage method is called...") 
		self._handleIncomingDataAnalysis(DataUtil.jsonToActuatorData(self, msg))
		pass

	def handleSensorMessage(self, data: SensorData) -> bool:
			logging("handleSensorMessage method is called...")
			self._handleUpstreamTransmission(ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, DataUtil.sensorDataToJson(self, data))
			pass
		
	def handleSystemPerformanceMessage(self, data: SystemPerformanceData) -> bool:
		logging("handleSystemPerformanceMessage method is called...")
		self._handleUpstreamTransmission(ResourceNameEnum.CDA_SYSTEM_PERF_MSG_RESOURCE, DataUtil.systemPerformanceDataToJson(self, data))
		pass

	
	def startManager(self):
		logging.info("Started DeviceDataManager.")
		self.sysPerfManager.startManager()
		self.sensorAdapterManager.startManager()
		pass

		
	def stopManager(self):
		logging.info("Stopped DeviceDataManager.")
		self.sysPerfManager.stopManager()
		self.sensorAdapterManager.stopManager()
		pass


	def _handleIncomingDataAnalysis(self, msg: str):
		"""
		Call this from handleIncomeMessage() to determine if there's
		any action to take on the message. Steps to take:
		1) Validate msg: Most will be ActuatorData, but you may pass other info as well.
		2) Convert msg: Use DataUtil to convert if appropriate.
		3) Act on msg: Determine what - if any - action is required, and execute.
		"""
		logging("_handleIncomingDataAnalysis method is called...")
		self.actuatorAdapterManager.sendActuatorCommand(DataUtil.jsonToActuatorData(self, msg))
		pass
		
	def _handleSensorDataAnalysis(self, data: SensorData):
		"""
		Call this from handleSensorMessage() to determine if there's
		any action to take on the message. Steps to take:
		1) Check config: Is there a rule or flag that requires immediate processing of data?
		2) Act on data: If # 1 is true, determine what - if any - action is required, and execute.
		"""
		logging("_handleSensorDataAnalysis method is called...")
		if(self.enableHandleTempChangeOnDevice == True):
			self.actuatorData = ActuatorData ()
			self.actuatorData.actuator_type = ActuatorData.HVAC_ACTUATOR_TYPE
			self.actuatorData.COMMAND_ON
			self.actuatorAdapterManager.sendActuatorCommand(self.actuatorData) 
			pass
		
	def _handleUpstreamTransmission(self, resourceName: ResourceNameEnum, msg: str):
		"""
		Call this from handleActuatorCommandResponse(), handlesensorMessage(), and handleSystemPerformanceMessage()
		to determine if the message should be sent upstream. Steps to take:
		1) Check connection: Is there a client connection configured (and valid) to a remote MQTT or CoAP server?
		2) Act on msg: If # 1 is true, send message upstream using one (or both) client connections.
		"""
		logging("_handleUpstreamTransmission method is called...")
		pass

