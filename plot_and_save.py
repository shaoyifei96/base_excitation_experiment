#collect and graph
import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation      
import numpy as np

ser_motor  = serial.Serial('/dev/ttyACM0')
ser_sensor = serial.Serial('/dev/ttyACM1')
length     = 500
count      = [0]
motor_data = [0]
pot_data   = [0]
ultra_data = [0]

for i in range(length):
	count += [i]
	try:
		motor_data += [float(ser_motor.readline())]
	except ValueError:
		motor_data += [0]
	garbage = ser_sensor.readline()
	data=ser_sensor.readline().strip('\r\n').split(',')
	pot_data   += [data[0]]	
	ultra_data += [data[1]]
	plt.scatter(count,ultra_data)
	plt.scatter(count,motor_data,color='r')
	plt.pause(0.001)
plt.show()
#for i in range(length):
ser_motor.close()
ser_sensor.close()