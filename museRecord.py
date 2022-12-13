from muselsl import record
import time
from EEGAnalysis import *
#from PrimEEGAnalysis import *


def museRecord():
	while True:
		print('starting recording')
		record(30, '/home/pi/Desktop/MuseAlarm/EEGsample.csv')
		print('Recording has ended...analyzing with model')
		eegAnalysis()
		print('Analyzing none')
		#time.sleep(30)
