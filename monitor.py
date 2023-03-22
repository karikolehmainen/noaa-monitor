
import predict
import time
import os
import subprocess
import requests
import json
import os.path
from os import path
from datetime import datetime
from telnetlib import Telnet
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from PIL import Image

NOAA15_id = 25338
NOAA18_id = 28654
NOAA19_id = 33591

def getTLE(satid):
	uri = "https://tle.ivanstanojevic.me/api/tle/"+str(satid)
	response = requests.get(uri, headers={'User-Agent': 'Foo bar'})
	data = response.json()
	name = "0 "+data["name"]
	ret = (name,data["line1"],data["line2"])
	print(ret)
	return ret

NOAA15TLE = getTLE(NOAA15_id)
NOAA18TLE = getTLE(NOAA18_id)
NOAA19TLE = getTLE(NOAA19_id)
NOAA15_Freq = 137620000
NOAA18_Freq = 137912500
NOAA19_Freq = 137100000
last_sat = "NOAA15"
QTH_Oulu = (65.006, 25.49, 0.0)
QTH_Utsjoki = (69.87,27.0, 90.0)
QTH = QTH_Utsjoki

def takeSecond(elem):
	return elem[1]

def nextPasses():
	times = []
	ts = datetime.now().timestamp()
	print(ts)

	p = predict.transits(NOAA15TLE,QTH)
	transit = next(p)
	print("NOAA-15: %f\t%f" % (transit.start-ts,transit.duration()))
	times.append([NOAA15_Freq,transit.start-ts,transit.duration()])

	p = predict.transits(NOAA18TLE,QTH)
	transit = next(p)
	print("NOAA-18: %f\t%f" % (transit.start-ts,transit.duration()))
	times.append([NOAA18_Freq,transit.start-ts,transit.duration()])
	
	p = predict.transits(NOAA19TLE,QTH)
	transit = next(p)
	print("NOAA-19: %f\t%f" % (transit.start-ts,transit.duration()))
	times.append([NOAA19_Freq,transit.start-ts,transit.duration()])
	return times
	
def getCurrentCoords(satellite):
	ret = [0,0]
	if (satellite[0] == NOAA15_Freq):
		ts = datetime.now().timestamp()
		obs = predict.observe(NOAA15TLE,QTH,at=ts)
		ret[0] = obs["latitude"]
		ret[1] = obs["longitude"]
	elif (satellite[0] == NOAA18_Freq):
		ts = datetime.now().timestamp()
		obs = predict.observe(NOAA18TLE,QTH,at=ts)
		ret[0] = obs["latitude"]
		ret[1] = obs["longitude"]
	elif (satellite[0] == NOAA19_Freq):
		ts = datetime.now().timestamp()
		obs = predict.observe(NOAA19TLE,QTH,at=ts)
		ret[0] = obs["latitude"]
		ret[1] = obs["longitude"]
	return ret

def startRecord(satellite, duration):
	output = ""
	sat = "137.62M"
	global last_sat
	if (satellite[0] == NOAA15_Freq):
		print("Start Gqrx with NOAA-15 settings")
		sat = "NOAA 15"
		last_sat = "NOAA15"
	elif (satellite[0] == NOAA18_Freq):
		sat = "NOAA 18"
		last_sat = "NOAA18"
		print("Start Gqrx with NOAA-18 settings")
	elif (satellite[0] == NOAA19_Freq):
		sat = "NOAA 19"
		last_sat = "NOAA19"
		print("Start Gqrx with NOAA-19 settings")
	print(last_sat)
	output = subprocess.run(["./noaa_record_rtl_fm.sh",sat,str(duration),"./output.wav"])
	print(output)

def captureAPT():
	times = nextPasses()
	times.sort(key=takeSecond)
	print(times)
	coords = []
	sat = times[0]
	if (sat[1] < 0):
		sleeptime = 0
		overtime = sat[2]+sat[1]
	else:
		sleeptime = sat[1]
		overtime = sat[2]
	if (overtime < 100):
		sat = times[1]
		if (sat[1] < 0):
			sleeptime = 0
			overtime = sat[2]+sat[1]
		else:
			sleeptime = sat[1]
			overtime = sat[2]
	print("Sleeping for "+str(sleeptime/60)+" minutes for freq "+str(sat[0]))
	time.sleep(sleeptime)
	coords.append(getCurrentCoords(sat))
	startRecord(sat,int(overtime))
	coords.append(getCurrentCoords(sat))
	return coords

def convertImage(file,sat):
	now = datetime.now()
	outfile = sat+"_"+now.strftime("%Y-%m-%d_%H-%M")+".png"
	outpath = outfile.split("/")
	outfile = outpath[len(outpath)-1]
	outfile = "apt-images/"+outfile
	print(outfile)
	output = subprocess.run(["aptdec", "-e", "d", str(file),"-o",outfile])
	print("file conversion result:\n"+str(output)+"\n=================")
	im = Image.open(outfile)
	width,height = im.size
	vs_left = 86
	vs_rigth = 952
	ir_left = 1128
	ir_right = 1994
	top = 0
	bottom = height
	im1 = im.crop((vs_left,top,vs_rigth,bottom))
	im2 = im.crop((ir_left,top,ir_right,bottom))
	im1.save(outfile+"-vs.png")
	im2.save(outfile+"-ir.png")
	return outfile

def printMetaData(file,coords):
	print("printMetaData")
	filebody = file.split(".")[0]
	print(file)
	print(coords)
	data = {
		'vs_imagefile': filebody+"-vs.png",
		'ir_imagefile': filebody+"-ir.png",
		'coords': [
			{'lat':coords[0][0],'lon':coords[0][1]},
			{'lat':coords[1][0],'lon':coords[1][1]}
		]
	}

	json_string = json.dumps(data)
	print(json_string)
	json_file = filebody+".json"
	with open(json_file,'w') as outfile:
		json.dump(json_string,outfile)
	print("saved metadata to file: "+json_file)
	
def main():
	patterns = ["*"]
	ignore_patterns = None
	ignore_directories = False
	case_sensitive = True
	go_recursively = True
	print("file observer running")
	while(1):
		coords = captureAPT()
		if (len(coords) > 0):
			print(coords)
			print("created wave file: "+"./output.wav")
			imgfile = convertImage("./output.wav",last_sat)
			printMetaData(imgfile,coords)
main()

