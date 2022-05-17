import time
import datetime
import os
import commands
import pynotify
from threading import Timer
from sht1x.Sht1x import Sht1x as SHT1x
from Adafruit_BMP085 import BMP085

dataPin=11
clkPin=7
sht1x=SHT1x(dataPin,clkPin,SHT1x.GPIO_BOARD)
picindex = 0



def main():
	while(battery_check() > 5)
		pressure()
		temperature()
		camera()
	return 0

def battery_check():
 
    rem = float(commands.getoutput("grep \"^remaining capacity\" /proc/acpi/battery/BAT0/state | awk '{ print $3 }'"))
    full = float(commands.getoutput("grep \"^last full capacity\" /proc/acpi/battery/BAT0/info | awk '{ print $4 }'"))
    state = commands.getoutput("grep \"^charging state\" /proc/acpi/battery/BAT0/state | awk '{ print $3 }'")
 
    percentage = int((rem/full) * 100)
 
    return percentage
    
def camera():
	os.system("raspistill -t 0 -o IMG_"+picindex+".jpg")
	picindex = picindex + 1
	return 0

def pressure():
	fd = open("file.txt", "w")
	for x in range(0, 10):
		bmp = BMP085(0x77)
		temp = bmp.readTemperature()
		pressure = bmp.readPressure()
		altitude = bmp.readAltitude()
		now = datetime.datetime.now()
		print now.strftime("%Y-%m-%d %H:%M:%S")
		print "Temperature: %.2f C" % temp
		print "Pressure:    %.2f hPa" % (pressure / 100.0)
		print "Altitude:    %.2f" % altitude
		print " "
		time.sleep(1)
		fd.write (now.strftime("%Y-%m-%d %H:%M:%S\n"))
		fd.write("Temperature: %.2f C\n" % temp)
		fd.write("Pressure:    %.2f hPa\n" % (pressure / 100.0))
		fd.write("Altitude:    %.2f \n\n" % altitude)
	fd.close()
	return 0

def temperature():
	count = 0
	while (count < 9):
		temperature=sht1x.read_temperature_C()
		count = count + 1
		humidity=sht1x.read_humidity()
		dewPoint=sht1x.calculate_dew_point(temperature, humidity)
		print("Temperature: {} Humidity: {} Dew Point: {}".format(temperature, humidity, dewPoint))
	return 0

if __name__ == '__main__':
	main()

