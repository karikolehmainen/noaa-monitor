from minio import Minio
import urllib3

class MinioConnector:
	def __init__(self, conf):
		self.minio_server = conf.getMinioHost()
		self.access_key = conf.getMinioAccessKey()
		self.secret_key = conf.getMinioSecretKey()
		self.client = Minio(self.minio_server, self.access_key, self.secret_key, secure=False)

	def getBuckets(self):
		buckets = self.client.list_buckets()
		return buckets


	def pushImage(self, bucket, name, file, mdata):
		print("MinioConnector.pushImage("+str(bucket)+","+str(name)+","+str(file)+","+str(mdata)+")")
		result = self.client.fput_object(bucket, name, file,"image/png", metadata=mdata)
		return result
