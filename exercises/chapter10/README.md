# Constrained Device Application (Connected Devices)

## Lab Module 10

Be sure to implement all the PIOT-CDA-* issues (requirements) listed at [PIOT-INF-10-001 - Chapter 10](https://github.com/orgs/programming-the-iot/projects/1#column-10488510).

### Description

NOTE: Include two full paragraphs describing your implementation approach by answering the questions listed below.

What does your implementation do? 
This implementation adds intelligent edge messaging using MQTT and / or CoAP to handle various messaging scenarios between GDA and CDA

How does your implementation work?
This implementation works with the use of MQTT and / or CoAP to process sensor messages the CDA and trigger actuation events from both the CDA and GDA. The logic handles actuation triggers at the source (CDA), while tracking trending values (GDA) to trigger preemptive actuation events.
### Code Repository and Branch

NOTE: Be sure to include the branch (e.g. https://github.com/programming-the-iot/python-components/tree/alpha001).

URL: https://github.com/NU-CSYE6530-Fall2020/constrained-device-app-Nitinsd96/tree/chapter10

### UML Design Diagram(s)

NOTE: Include one or more UML designs representing your solution. It's expected each
diagram you provide will look similar to, but not the same as, its counterpart in the
book [Programming the IoT](https://learning.oreilly.com/library/view/programming-the-internet/9781492081401/).
![UML Diagram](Capture.JPG "UML")

### Unit Tests Executed

NOTE: TA's will execute your unit tests. You only need to list each test case below
(e.g. ConfigUtilTest, DataUtilTest, etc). Be sure to include all previous tests, too,
since you need to ensure you haven't introduced regressions.

- DeviceDataManagerCallbackTest.py
- ActuatorDataTest.py
- DataUtilTest.py
- SensorDataTest.py
- SystemPerformanceDataTest.py

### Integration Tests Executed

NOTE: TA's will execute most of your integration tests using their own environment, with
some exceptions (such as your cloud connectivity tests). In such cases, they'll review
your code to ensure it's correct. As for the tests you execute, you only need to list each
test case below (e.g. SensorSimAdapterManagerTest, DeviceDataManagerTest, etc.)

- MqttClientConnectorTest
- DeviceDataManagerIntegrationTest

EOF.
