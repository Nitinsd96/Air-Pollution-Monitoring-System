#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import paho.mqtt.client as mqttClient

from programmingtheiot.common import ConfigUtil
from programmingtheiot.common import ConfigConst

from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.cda.connection.IPubSubClient import IPubSubClient
from programmingtheiot.data.DataUtil import DataUtil

DEFAULT_QOS = 1

class MqttClientConnector(IPubSubClient):
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self, clientID: str = None):
		"""
		Default constructor. This will set remote broker information and client connection
		information based on the default configuration file contents.
		
		@param clientID Defaults to None. Can be set by caller. If this is used, it's
		critically important that a unique, non-conflicting name be used so to avoid
		causing the MQTT broker to disconnect any client using the same name. With
		auto-reconnect enabled, this can cause a race condition where each client with
		the same clientID continuously attempts to re-connect, causing the broker to
		disconnect the previous instance.
		"""
		
		self.mqttClient = None
		self.dataMsgListener = None
		
		self.config = ConfigUtil.ConfigUtil()

		self.host = self.config.getProperty(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.HOST_KEY, ConfigConst.DEFAULT_HOST)
		
		self.port = self.config.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.PORT_KEY, ConfigConst.DEFAULT_MQTT_PORT)
		
		self.keepAlive = self.config.getInteger(ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY, ConfigConst.DEFAULT_KEEP_ALIVE)
		
		
		self.clientID = None
# 		if not clientID and self.AUTOGEN_CLIENTID:
# 			self.clientID = 'CDAMqttClientID'
# 			logging.info("Using auto generated clientID: %s", clientID)
# 		else:
# 			self.clientID = clientID
# 			logging.info("Using requested ClientID: %s", clientID)
 			
			
		logging.info('\tMQTT Broker Host: ' + self.host)
		logging.info('\tMQTT Broker Port: ' + str(self.port))
		logging.info('\tMQTT Keep Alive:  ' + str(self.keepAlive))
		
	def connectClient(self)->bool:
		logging.info("Connecting MQTT broker: %s",self.host)
		
		if not self.mqttClient:
			logging.info("-------------------------working----------------")
			self.mqttClient = mqttClient.Client(client_id = self.clientID, clean_session = True)
			self.mqttClient.on_connect = self.onConnect
			self.mqttClient.on_disconnect = self.onDisconnect
			self.mqttClient.on_message = self.onMessage
			self.mqttClient.on_publish = self.onPublish
			self.mqttClient.on_subscribe = self.onSubscribe

		if not self.mqttClient.is_connected():
			self.mqttClient.connect(self.host, self.port, self.keepAlive)
			self.mqttClient.loop_start()
			return True
		else:
			logging.warn('MQTT client is already connected. Ignoring connect request.')
			return False
		self.mqttClient.publish(None, "dsdg", 1)
	
	def disconnectClient(self)->bool:
		logging.info("Disconnecting MQTT broker: %s",self.host)
		if self.mqttClient.is_connected():
			self.mqttClient.disconnect()
			self.mqttClient.loop_stop()
		return True
# 		else:
# 			logging.warn("MQTT client is not connected")
# 			return False
		pass
	
	
		
	def onConnect(self, client, userdata, flags, rc):
		logging.info("Connected to MQTT broker. Result code %s",str(rc))
		logging.info('[Callback] Connected to MQTT broker. Result code: ' + str(rc))
		# NOTE: Use the QoS of your choice - '1' is only an example
		self.mqttClient.subscribe(topic = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE.value, qos = 1)
		self.mqttClient.message_callback_add(sub = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE.value, callback = self.onActuatorCommandMessage)
		
		
	def onDisconnect(self, client, userdata, rc):
		#logging.info("Disconnected from MQTT broker. Result code %s",str(rc))
		pass
		
	def onMessage(self, client, userdata, msg):
		logging.info("Message received. Msg: %s", msg)
		if self.dataMsgListener:
			resourceEnum = None
		pass
			
	def onPublish(self, client, userdata, mid):
		logging.info("Published Message: %s", str(mid))
		pass
	
	def onSubscribe(self, client, userdata, mid, granted_qos):
		logging.info("Subscribed Message: %s", str(mid))
		pass
	
	def publishMessage(self, resource: ResourceNameEnum, msg, qos):
		logging.info("Called publishMessage %s", msg)
		topic = resource.value
		logging.info("Topic name is %s", topic)
# 		if(resource == None):
# 			return False
# 		#else:
		if(qos < 0 or qos >2 ):
			qos = IPubSubClient.DEFAULT_QOS
		msgInfo = self.mqttClient.publish(topic=topic, payload=msg, qos=qos)
		logging.info("Called publishMessage is called %s", msg)
		msgInfo.wait_for_publish()
		return True
		
	
	def subscribeToTopic(self, resource: ResourceNameEnum, qos):
# 		logging.info("Called subscribeToTopic %s", resource.value)
# 		logging.info("Called subscribeToTopic %s", str(resource.getResourceNameByValue(resource)))
		topic = resource.value
		#else:
		if(qos < 0 or qos >2 ):
			qos = IPubSubClient.DEFAULT_QOS
		self.mqttClient.subscribe(topic=topic, qos=qos)
		return True
	
	
	def unsubscribeFromTopic(self, resource: ResourceNameEnum):
		self.mqttClient.unsubscribe(topic=resource.value)
		pass

	def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
		logging.info("Called setDataMessageListener")
		if listener:
			self.dataMsgListener = listener
			return True
		return False

	def onActuatorCommandMessage(self, client, userdata, msg):
		logging.info('[Callback] Actuator command message received. Topic: %s.', msg.topic)
 		
		if self.dataMsgListener:
			try:
				# assumes all data is encoded using UTF-8 (between GDA and CDA)
				actuatorData = DataUtil().jsonToActuatorData(msg.payload.decode('utf-8'))
 				
				self.dataMsgListener.handleActuatorCommandMessage(actuatorData)
			except:
				logging.exception("Failed to convert incoming actuation command payload to ActuatorData: ")
