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

#initialising variables used through the code
counter = 0 #counter to help change the intervals
interval = 10 #initialising the interval to 10 seconds
start = datetime.datetime.now() #getting the current time 

def setup():

	# create the spi bus
	spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

	# create the cs (chip select)
	cs = digitalio.DigitalInOut(board.D5)
	# create the mcp object
	mcp = MCP.MCP3008(spi, cs)

	# create an analog input channel on pin 0
	global chan_temp, chan_light, button
	chan_temp = AnalogIn(mcp, MCP.P1) #To get the temperature value from the pin 2
	chan_light = AnalogIn(mcp, MCP.P2) #To get the LED value of from the LDR in pin 3

	# create an interrupt for button
	#GPIO.setmode(GPIO.BCM)
	#GPIO.setup(21,GPIO.IN, pull_up_down = GPIO.PUD_UP)

	#GPIO.add_event_detect(21,GPIO.FALLING,callback=change_interval,bouncetime=200)

	#creating the button 
	button = digitalio.DigitalInOut(board.D17) #Referencing the pin on which the button is connected onto on the GPIO
	button.switch_to_input(pull=digitalio.Pull.UP) #Making the button an input 

#creating a funtion to get the time 
def print_time_thread():

	thread = threading.Timer(interval, print_time_thread) #creatign a thread 
	thread.daemon = True
	thread.start() #starting the thread 
	time = math.floor((datetime.datetime.now()-start).total_seconds()) #getting the second that had passed since the time has started 
	temp_reading = chan_temp.value #getting the temperature reading from the ADC 
	temp = round((chan_temp.voltage-0.5)/0.01,2) #converting the ADC value to a value in degrees celcuis 
	light_reading = chan_light.value #obtaining the light reading 
	#following will print out the values in the format that is needed 
	print(str(time) + "s		" + str(temp_reading) + "			" + str(temp) + " C		" + str(light_reading))

#This will run the program when called 
if __name__ == "__main__":

	print("Runtime		Temp Reading 		Temp		Light Reading") #This prints out the heading for the table when the program is run 
	setup() #this will run our setup function intialising variable and pins 
	print_time_thread() #will run our function to get adc values and print out the temperature in degrees and LDR adc value 

	#this will run the program until the user exits 
	while True:
		#this will be triggered when the button is pressede 
		if not  button.value:
			counter += 1 #increment the counter everytime the button is pressed 
			#case when the counter is 1
			if counter == 1:
				interval = 5 #Change the interval to 5 seconds
				time.sleep(10) #this will allow the thread to complete then change the interval

			#case when the counter is 2
			elif counter == 2:
				interval = 1 #Change the interval to 1 seconds
				time.sleep(5) #this will allow the thread to complete then change the interval
			#case when the counter is 0
			else:
				interval = 10 #Change the interval to 10 seconds
				counter = 0 #changes the counter back to 0 as there is only 3 cases 
				time.sleep(1) #this will allow the thread to complete then change the interval
		#else let the program continuosly run when the button is not pressed
		pass


