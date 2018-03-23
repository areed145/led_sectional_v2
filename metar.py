#import urllib2
import xml.etree.ElementTree as ET
#import time
#from neopixel import *
#import sys
#import os


# LED strip configuration:
LED_COUNT      = 50      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 128     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
#LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

#strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)

#strip.begin()

airports = ['', #1
            '', #2
            '', #3
            '', #4
            'KSBA', #5
            '', #6
            '', #7
            'KNTD', #8
            'KCMA', #9
            'KNTD', #10
            '', #11
            '', #12
            'KVNY', #13
            'KWHP', #14
            'KBUR', #15
            'KBFL', #16
            'KNID', #17
            'KDAG', #18
            'KWJF', #19
            'KPMD', #20
            '', #21
            'KEDW', #22
            '', #23
            'KMHV', #24
            '', #25
            'KLAX', #26
            'KHHR', #27
            'KLGB', #28
            'KSLI', #29
            'KSNA', #30
            '', #31
            '', #32
            'KONT', #33
            'KRAL', #34
            'KRIV', #35
            'KSBD', #36
            'KL35', #37
            'KPSP', #38
            '', #39
            '', #40
            '', #41
            '', #42
            'KNFG', #43
            'KCRQ', #44
            '', #45
            'KMYF', #46
            'KSAN', #47
            'KNZY', #48
            'KAVX'] #49

print(airports)

mydict = {
	"":""
}

url = "https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&hoursBeforeNow=1.5&stationString="
for airportcode in airports:
	if airportcode == "''":
		continue
	print(airportcode)
	url = url + airportcode + ","

print(url)
content = urllib2.urlopen(url).read()
print(content)


root = ET.fromstring(content)


for metar in root.iter('METAR'):
	if airportcode == "''":
		continue
	stationId = metar.find('station_id').text
	flightCateory = metar.find('flight_category').text
	print(stationId + " " + flightCateory)
	if stationId in mydict:
		print("duplicate, only save first metar")
	else:
		mydict[stationId] = flightCateory
	
	

print(mydict)

i = 0
for airportcode in airports:
	if airportcode == "''":
		i = i +1
		continue
	print("")
	color = Color(0,0,0)

	flightCateory = mydict.get(airportcode,"No")
	print(airportcode + " " + flightCateory)

	if  flightCateory != "No":
		
		if flightCateory == "VFR":
			print("VFR")
			color = Color(255,0,0)
		elif flightCateory == "MVFR":
			color = Color(0,0,255)
			print("MVFR")
		elif flightCateory == "IFR":
			color = Color(0,255,0)
			print("IFR")
		elif flightCateory == "LIFR":
			color = Color(0,128,128)
			print("LIFR")
	else:
		color = Color(255,255,255)
		print("N/A")

	print("Setting light " + str(i) + " for " + airportcode + " " + flightCateory + " " + str(color))
	strip.setPixelColor(i, color)
	strip.show()
	
	i = i+1
print("")
print("fin")











