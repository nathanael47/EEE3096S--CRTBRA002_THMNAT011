import busio
import time
import math
import threading
import datetime
import digitalio
import board
from board import *
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

counter = 0
interval = 10 
start = datetime.datetime.now()

def setup():

	# create the spi bus
	spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

	# create the cs (chip select)
	cs = digitalio.DigitalInOut(board.D5)
	# create the mcp object
	mcp = MCP.MCP3008(spi, cs)

	# create an analog input channel on pin 0
	global chan_temp, chan_light, button
	chan_temp = AnalogIn(mcp, MCP.P1)
	chan_light = AnalogIn(mcp, MCP.P2)

	# create an interrupt for button
	#GPIO.setmode(GPIO.BCM)
	#GPIO.setup(21,GPIO.IN, pull_up_down = GPIO.PUD_UP)

	#GPIO.add_event_detect(21,GPIO.FALLING,callback=change_interval,bouncetime=200)
	button = digitalio.DigitalInOut(board.D17)
	button.switch_to_input(pull=digitalio.Pull.UP)


def print_time_thread():

	thread = threading.Timer(interval, print_time_thread)
	thread.daemon = True
	thread.start()
	time = math.floor((datetime.datetime.now()-start).total_seconds())
	temp_reading = chan_temp.value
	temp = round((chan_temp.voltage-0.5)/0.01,2) 
	light_reading = chan_light.value
	print(str(time) + "s		" + str(temp_reading) + "			" + str(temp) + " C		" + str(light_reading))

if __name__ == "__main__":

	print("Runtime		Temp Reading 		Temp		Light Reading")
	setup()
	print_time_thread()

	while True:
		if not  button.value:
			counter += 1
			if counter == 1:
				interval = 5
				time.sleep(10)
			elif counter == 2:
				interval = 1
				time.sleep(5)
			else:
				interval = 10
				counter = 0
				time.sleep(1)
		pass


