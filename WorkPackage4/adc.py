import busio
import math
import RPi.GPIO as GPIO
import threading
import datetime
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

global start
start = datetime.datetime.now()
global interval
interval = 10.0
global counter 
counter = 0

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)
# create the mcp object
mcp = MCP.MCP3008(spi, cs)

# create an analog input channel on pin 0
chan_temp = AnalogIn(mcp, MCP.P2)
chan_light = AnalogIn(mcp, MCP.P3)

#print("Raw ADC Value: ", chan.value)
#print("ADC Voltage: " + str(chan.voltage) + "V")

def setup():
	#board D21
	#GPIO.setmode(GPIO.BOARD)
	GPIO.setup(21,GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.add_event_detect(21,GPIO.FALLING,callback=change_interval,bouncetime=200)

def print_time_thread():
	thread = threading.Timer(interval, print_time_thread)
	thread.daemon = True
	thread.start()
	time = math.floor((datetime.datetime.now()-start).total_seconds())
	temp_reading = chan_temp.value
	temp = round((chan_temp.voltage-0.5)/0.01,2) 
	light_reading = chan_light.value
	print(str(time) + "s		" + str(temp_reading) + "			" + str(temp) + " C		" + str(light_reading))

def change_interval(channel):
	counter += 1
	print("hello")
	if counter == 1:
		interval = 5
	elif couter == 2:
		interval = 1
	else:
		counter = 0
		interval = 10

if __name__ == "__main__":
	print("Runtime		Temp Reading 		Temp		Light Reading")
	setup()
	print_time_thread()

	while True:
		pass
