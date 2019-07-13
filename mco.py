#!/usr/bin/env python3

''' 
	mco.py
	Eric Ayars
	June 2016

	A simplistic program to allow communication with and data collection from 
	the MCO.

	Special commands are as follows:
		quit - quits the program
		c - collects data. 'c' must be followed by the number of drive cycles
			and then the filename in which to save the data.
			Addition: 'c' also plots a phase space plot of the data and saves it.
		p - plots last data set. If 'p' is followed by 's' (i.e. 'p s') then it
			saves the figure also.

	All other commands are sent directly to the MCO.
	e.g. 
		freq?
		ampl 400
		coil 1
		etc.
'''

from pylab import *
import serial
from sys import argv

# command-line invocation should include port. (probably either 0 or 1.)
#port = '/dev/ttyACM%d' % int(argv[1])
#port = '/dev/cu.usbmodem953781'
port = '/dev/cu.usbmodem9537801'


ser = serial.Serial(port, 115200, timeout=1) 

# startup test
ser.write(b'*idn?\n')
print(ser.readline().decode())

command = ''

def getData(N, file):
	# gets N periods worth of data, saves raw data lines to a file.

	N = 256*N
	print("Saving %d data points to file '%s'." % (N, file))

	# get useful data from the MCO
	ser.write(b'freq?\n')
	freq = float(ser.readline())
	ser.write(b'ampl?\n')
	ampl = int(ser.readline())

	# open the file and write the header
	fh = open(file, 'w')
	fh.write(b'# Frequency = %0.2f\n# Amplitude = %d\n' %(freq, ampl))

	# Activate data reporting
	ser.write(b'rept 1\n')

	# drop lines until the end of a drive cycle.
	line = ser.readline()
	while int(line.split()[0]) != 255:
		line = ser.readline()

	# collect N data lines
	for j in range(N):
		fh.write(ser.readline())
	ser.write(b'rept 0\n')

	# clean up
	fh.close()

def showPlot(file, save=False, polar=False):

	# get the data
	phase, angle, velocity = loadtxt(file, unpack=True)

	# plot the phase space graph, cartesian
	if not polar:
		ax = subplot(111)
		ax.plot(angle*2.*pi/1016., velocity*2.*pi/1016., 'b,')
		xlabel('Angle (radians)')
		ylabel('Angular Velocity (radians/second)')
		xlim(-pi, pi)

	# plot the phase space graph, polar
	else:
		ax = subplot(111, projection='polar')
		ax.plot(angle*2.*pi/1016., velocity*2.*pi/1016., 'b,')
		ax.set_rmax(max(ceil(abs(velocity))))
		ax.grid(True)

	title(file)

	# save the plot
	if save:
		savefig(file+'.pdf')

	# show the plot
	show()


# Main loop
while command != 'quit':
	command = input('-> ')

	# parse command
	
	# go through some special cases here

	if command == 'quit':
		continue
	
	if command == '':
		print(ser.readline().decode())
		continue

	com = command.split()
	if com[0] == 'c':
		# c for collect. Follow 'c' with N and filename.
		# Note: no error-checking! Do it right or suffer. :-(
		N = int(com[1])
		filename = com[2]
		getData(N, filename)
		continue
	if (com[0] == 'p') or (com[0] == 'l'):
		save_figure = False
		if filename:
			try:
				if com[1] == 's':
					save_figure = True
			except:
				pass
			if com[0] == 'l':
				showPlot(filename, save=save_figure, polar=True)
			else:
				showPlot(filename, save=save_figure, polar=False)
		else:
			print('No filename given.')
		continue
	if com[0] == 'f':
		# flush serial buffer --occasionally useful!
		ser.read(4096)

	# No special case, just write and read.
	ser.write(command.encode('utf-8'))
	print(ser.readline().decode())

ser.close()

