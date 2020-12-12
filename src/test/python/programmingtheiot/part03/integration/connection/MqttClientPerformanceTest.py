import logging
import unittest

import time

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.data.SensorData import SensorData
from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum
from programmingtheiot.common.DefaultDataMessageListener import DefaultDataMessageListener


class MqttClientPerformanceTest(unittest.TestCase):

    NS_IN_MILLIS = 1000000
    
    # NOTE: We'll use only 10,000 requests for MQTT
    MAX_TEST_RUNS = 10000
    
    @classmethod
    def setUpClass(self):
        logging.getLogger().setLevel(logging.INFO)
        logging.basicConfig(format = '%(asctime)s:%(module)s:%(levelname)s:%(message)s', level = logging.DEBUG)
        
    def setUp(self):
        self.mqttClient = MqttClientConnector(clientID = 'CDAMqttClientPerformanceTest001')
        pass

    def tearDown(self):
        pass

    @unittest.skip("Ignore for now.")
    def testConnectAndDisconnect(self):
        startTime = time.time_ns()
        
        self.assertTrue(self.mqttClient.connectClient())
        self.assertTrue(self.mqttClient.disconnectClient())
        
        endTime = time.time_ns()
        elapsedMillis = (endTime - startTime) / self.NS_IN_MILLIS
        
        logging.info("Connect and Disconnect: " + str(elapsedMillis) + " ms")
        
    @unittest.skip("Ignore for now.")
    def testPublishQoS0(self):
        self._execTestPublish(self.MAX_TEST_RUNS, 0)

    @unittest.skip("Ignore for now.")
    def testPublishQoS1(self):
        self._execTestPublish(self.MAX_TEST_RUNS, 1)

    #@unittest.skip("Ignore for now.")
    def testPublishQoS2(self):
        self._execTestPublish(self.MAX_TEST_RUNS, 2)
    
    #@unittest.skip
    def _execTestPublish(self, maxTestRuns: int, qos: int):
        self.assertTrue(self.mqttClient.connectClient())
        
        sensorData = SensorData()
        payload = DataUtil().sensorDataToJson(sensorData)
        
        startTime = time.time_ns()
        
        for seqNo in range(0, maxTestRuns):
            self.mqttClient.publishMessage(resource = ResourceNameEnum.CDA_SENSOR_MSG_RESOURCE, msg = payload, qos = qos)
            
        endTime = time.time_ns()
        elapsedMillis = (endTime - startTime) / self.NS_IN_MILLIS
        
        self.assertTrue(self.mqttClient.disconnectClient())
        
        logging.info("Publish message - QoS " + str(qos) + " [" + str(maxTestRuns) + "]: " + str(elapsedMillis) + " ms")


if __name__ == "__main__":
    unittest.main()