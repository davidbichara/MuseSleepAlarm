# From https://github.com/alexandrebarachant/muse-lsl/blob/master/examples/startMuseStream.py
from muselsl import stream
from musel.muselsl.stream import list_muses
import DataCSV
import multiprocessing as mp
import threading
from gui import GenerateUI
import pandas as pd
import csv
import os, sys
import time

########################################################################################################################################
#start_stream(): Checks if muses exist and attempts to connect, start a stream, and update the connection status
#Parms: None
#Returns: None
########################################################################################################################################

def start_stream():
    
    while True:
        #Search for Muses
        muses = list_muses()

        while not muses: #if not muses:
            if os.path.exists('/home/pi/Desktop/Method2/connected.txt'):
                os.remove('/home/pi/Desktop/Method2/connected.txt')
            print('No Muses Found')
        else:
            try:
                f = open('/home/pi/Desktop/Method2/connected.txt', 'w+')
                writer = csv.writer(f)
                f.close()
                f = pd.DataFrame()
                f.to_csv('connected.csv')
                print("Writing File")
                #t2 = mp.Process(target=recordThread, args=())
                #t2.start()
                stream(str(muses[0]['address']))

                # Note: Streaming is synchronous, so code here will not execute until the stream has been closed
                #persists no connection to GUI
                if os.path.exists('/home/pi/Desktop/Method2/connected.txt'):
                    os.remove('/home/pi/Desktop/Method2/connected.txt')
            except(KeyboardInterrupt):
                print('Stream has ended')

########################################################################################################################################
#__main__: Main function of the program, launches program and starts mutiprocesses to manage program
#Parms: None
#Returns: None
########################################################################################################################################
                
                
if __name__ == "__main__":

    #appends working directory to path
    sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
    print("Working Directory added to path")

    sys.path.append(os.getcwd())
    #sys.path.append('/home/pi/Desktop/MuseAlarm/waveloading.gif')
    #sys.path.append('/home/pi/Desktop/MuseAlarm/checklist.png')
    #sys.path.append('/home/pi/Desktop/Model2/connected.csv')
    print("Working Directory added to path")

    if os.path.exists('/home/pi/Desktop/Method2/connected.csv'):
        os.remove('/home/pi/Desktop/Method2/connected.csv')

    stopAlarmCSV = pd.DataFrame([''])
    stopAlarmCSV.to_csv('/home/pi/Desktop/Method2/alarmStop.csv')
    
    #starts the UI process
    t1 = mp.Process(target=GenerateUI, args=())
    #t1.start()
    t1.start()
    start_stream()
    #Shut down stream 
    t1.kill()
