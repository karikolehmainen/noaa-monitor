from configuration import *
from minio_connector import *

configuration = Configuration()

connector = MinioConnector(configuration)

def test_getbuckets():
	result = connector.getBuckets()
	print(result)


def test_pushobject():
	# Upload data with metadata.
	result = connector.pushImage("apt", "test_object", "./noaa19.png",{"ImageTimestamp": "one"})
	#result = connector.pushImage("apt", "test_object", "./noaa19.png","{\"Image Timestamp\": \"one\"}")
	#result = connector.pushImage("apt", "test_object", "./noaa19.png","")
	print("created {0} object; etag: {1}, version-id: {2}".format(result.object_name, result.etag, result.version_id,),)
test_getbuckets()
test_pushobject()
