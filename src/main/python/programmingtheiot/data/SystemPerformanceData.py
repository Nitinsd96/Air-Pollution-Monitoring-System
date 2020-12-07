#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.data.BaseIotData import BaseIotData
from numpy.distutils.cpuinfo import cpu

class SystemPerformanceData(BaseIotData):
	"""
	Shell representation of class for student implementation.
	
	"""
	DEFAULT_VAL = 0.0
	
	
	
	def __init__(self,name = ConfigConst.NOT_SET, d = None):
		
# 		super(SystemPerformanceData, self).__init__(name = ConfigConst.SYS_PERF_DATA, d = d)
		super(SystemPerformanceData, self).__init__(name = name, d = d)
		
		if d:
			self.diskUtil = d['diskUtil']
			self.cpuUtil = d['cpuUtil']
			self.memUtil = d['memUtil']
		else :
			self.diskUtil = self.DEFAULT_VAL
			self.cpuUtil = self.DEFAULT_VAL
			self.memUtil = self.DEFAULT_VAL
	
	def getCpuUtilization(self):
		return self.cpuUtil
	
	def getDiskUtilization(self):
		return self.diskUtil
	
	def getMemoryUtilization(self):
		return self.memUtil
	
	def setCpuUtilization(self, cpuUtil):
		self.cpuUtil = cpuUtil
	
	def setDiskUtilization(self, diskUtil):
		self.diskUtil  = diskUtil

	
	def setMemoryUtilization(self, memUtil):
		self.memUtil = memUtil
	
	def _handleUpdateData(self, data):
		self.memUtil = data.getMemoryUtilization()
		self.diskUtil = data.getDiskUtilization()
		self.cpuUtil = data.getCpuUtilization()
		
