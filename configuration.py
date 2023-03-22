import json
from pprint import pprint

class Configuration:
	json_conf = []
	def __init__(self):
		print("Init Configuration")
		self.conffile = "./noaamonitor_conf.json"
		self.readConfiguration()

	def readConfiguration(self):
		print("Reading configuration file")
		with open(self.conffile, 'r') as handle:
			self.json_conf = json.load(handle)

	def saveConfiguration(self):
		with open(self.conffile, 'w') as outfile:
			json.dump(self.json_conf, outfile)

	def getMinioHost(self):
		if "minio_host" not in self.json_conf["configuration"]:
			self.json_conf["configuration"]["minio_host"]=""
			self.saveConfiguration()
		return self.json_conf["configuration"]["minio_host"]

	def setMinioHost(self, value):
		self.json_conf["configuration"]["minio_host"] = value

	def getMinioAccessKey(self):
		if "minio_host" not in self.json_conf["configuration"]:
			self.json_conf["configuration"]["minio_access"]=""
			self.saveConfiguration()
		return self.json_conf["configuration"]["minio_access"]

	def setMinioAccessKey(self, value):
		self.json_conf["configuration"]["minio_access"] = value
		self.saveConfiguration()

	def getMinioSecretKey(self):
		if "minio_host" not in self.json_conf["configuration"]:
			self.json_conf["configuration"]["minio_secret"]=""
			self.saveConfiguration()
		return self.json_conf["configuration"]["minio_secret"]

	def setMinioSecretKey(self, value):
		self.json_conf["configuration"]["minio_secret"] = value
		self.saveConfiguration()
