
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
import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.DataUtil import DataUtil



class DeviceDataManager(IDataMessageListener):
	"""
	Shell representation of class for student implementation.
	
	"""
	
	def __init__(self, enableMqtt: bool = True, enableCoap: bool = False):
		if enableMqtt==True:
			self.mqttClient = MqttClientConnector(clientID = 'CDAMqttClientConnectorTest001')
			self.mqttClient.setDataMessageListener(self)
			
		self.sysPerfManager = SystemPerformanceManager()
		self.sysPerfManager.setDataMessageListener(self)
		
		self.sensorAdapterManager = SensorAdapterManager()
		self.sensorAdapterManager.setDataMessageListener(self)
		
		self.actuatorAdapterManager = ActuatorAdapterManager()
		self.actuatorAdapterManager.setDataMessageListener(self)
		
		self.configUtil = ConfigUtil()
		self.dataUtil = DataUtil()
		
		self.enableHandleTempChangeOnDevice = self.configUtil.getBoolean(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.ENABLE_HANDLE_TEMP_CHANGE_ON_DEVICE_KEY)
		self.triggerHvacTempFloor = self.configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.TRIGGER_HVAC_TEMP_FLOOR_KEY)
		self.triggerHvacTempCeiling = self.configUtil.getFloat(ConfigConst.CONSTRAINED_DEVICE, ConfigConst.TRIGGER_HVAC_TEMP_CEILING_KEY)

	"""this method recieves the ActuatorData and also calls to handle upstream transmission"""		
	def handleActuatorCommandResponse(self, data: ActuatorData) -> bool:
		logging("handleActuatorCommandResponse method is called...")
		d = self.dataUtil.actuatorDataToJson(data)
		logging.info("Incoming actuator response received (from actuator manager):"+ d)
		self._handleUpstreamTransmission(ResourceNameEnum.CDA_ACTUATOR_RESPONSE_RESOURCE, d)
		return True

	def handleIncomingMessage(self, resourceEnum: ResourceNameEnum, msg: str) -> bool:
		logging("handleIncomingMessage method is called...") 
		self._handleIncomingDataAnalysis(DataUtil.jsonToActuatorData(self, msg))
		return True

	def handleSensorMessage(self, data: SensorData) -> bool:
		logging.info("handleSensorMessage method is called...")
		self._handleUpstreamTransmission(ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, DataUtil.sensorDataToJson(self, data))
		self._handleSensorDataAnalysis(data)
		return True
		
	def handleSystemPerformanceMessage(self, data: SystemPerformanceData) -> bool:
		logging("handleSystemPerformanceMessage method is called...")
		self._handleUpstreamTransmission(ResourceNameEnum.CDA_SYSTEM_PERF_MSG_RESOURCE, DataUtil.systemPerformanceDataToJson(self, data))
		return True
		
	def startManager(self):
		logging.info("Started DeviceDataManager.")
		self.mqttClient.connectClient()
		self.sysPerfManager.startManager()
		self.sensorAdapterManager.startManager()
		
		pass

		
	def stopManager(self):
		logging.info("Stopped DeviceDataManager.")
		self.sysPerfManager.stopManager()
		self.sensorAdapterManager.stopManager()
		self.mqttClient.disconnectClient()
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
		logging.info("_handleSensorDataAnalysis method is called...")
# 		if(self.enableHandleTempChangeOnDevice == True):
		if(data.getValue() > self.triggerHvacTempCeiling):
			logging.info("------------------sensor data handling called-------------------")
			logging.info(f"{data.getValue()}<---sensor---limit--->{self.triggerHvacTempCeiling}")
			ad = ActuatorData(actuatorType = ActuatorData.HVAC_ACTUATOR_TYPE)
			ad.setValue(0)
			ad.setCommand(ActuatorData.COMMAND_OFF)
			print(ad)
			self.actuatorAdapterManager.sendActuatorCommand(ad) 
			pass
		
	def _handleUpstreamTransmission(self, resourceName: ResourceNameEnum, msg: str):
		"""
		Call this from handleActuatorCommandResponse(), handlesensorMessage(), and handleSystemPerformanceMessage()
		to determine if the message should be sent upstream. Steps to take:
		1) Check connection: Is there a client connection configured (and valid) to a remote MQTT or CoAP server?
		2) Act on msg: If # 1 is true, send message upstream using one (or both) client connections.
		"""
		logging.info("_handleUpstreamTransmission method is called...")

		self.mqttClient.subscribeToTopic( resourceName, 1)
		self.mqttClient.publishMessage( resourceName, msg, 1)
		pass
	
	def handleActuatorCommandMessage(self, data: ActuatorData) -> bool:
		if data:
			logging.info("-----------------Processing actuator command message.----------------")
			
			# TODO: add further validation before sending the command
			self.actuatorAdapterManager.sendActuatorCommand(data)
			return True
		else:
			logging.warning("Received invalid ActuatorData command message. Ignoring.")
			return False

