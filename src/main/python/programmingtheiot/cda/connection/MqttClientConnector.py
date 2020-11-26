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
		
		
		if not clientID and self.AUTOGEN_CLIENTID:
			self.clientID = 'CDAMqttClientID'
			logging.info("Using auto generated clientID: %s", clientID)
		else:
			self.clientID = clientID
			logging.info("Using requested ClientID: %s", clientID)
			
			
		logging.info('\tMQTT Broker Host: ' + self.host)
		logging.info('\tMQTT Broker Port: ' + str(self.port))
		logging.info('\tMQTT Keep Alive:  ' + str(self.keepAlive))
		
	def connectClient(self)->bool:
		logging.info("Connecting MQTT broker: %s",self.host)
		if not self.mqttClient:
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
	
	def disconnectClient(self)->bool:
		logging.info("Disconnecting MQTT broker: %s",self.host)
		if self.mqttClient.is_connected():
			self.mqttClient.disconnect()
			self.mqttClient.loop_stop()
			return True
		else:
			logging.warn("MQTT client is not connected")
			return False
		pass
	
	
		
	def onConnect(self, client, userdata, flags, rc):
		logging.info("Connected to MQTT broker. Result code %s",str(rc))
		pass
		
	def onDisconnect(self, client, userdata, rc):
		logging.info("Disconnected from MQTT broker. Result code %s",str(rc))
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
	
	def publishMessage(self, resource: ResourceNameEnum, msg, qos: int = IPubSubClient.DEFAULT_QOS):
		logging.info("Called publishMessage %s", msg)
		if(resource == None):
			return False
		else:
			if(qos < 0 or qos >2 ):
				qos = DEFAULT_QOS
			return True
		pass
	
	def subscribeToTopic(self, resource: ResourceNameEnum, qos: int = IPubSubClient.DEFAULT_QOS):
		logging.info("Called subscribeToTopic %s", str(resource.getResourceNameByValue(resource)))
		if(resource == None):
			return False
		else:
			if(qos < 0 or qos >2 ):
				qos = DEFAULT_QOS
			return True
		pass
	
	def unsubscribeFromTopic(self, resource: ResourceNameEnum):
		pass

	def setDataMessageListener(self, listener: IDataMessageListener) -> bool:
		logging.info("Called setDataMessageListener")
		return False
		pass
