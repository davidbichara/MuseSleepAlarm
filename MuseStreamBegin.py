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

def start_stream():
    
    while True:
        muses = list_muses()

        while not muses: #if not muses:
            if os.path.exists('/home/pi/Desktop/MuseAlarm/data/connected.csv'):
                os.remove('/home/pi/Desktop/MuseAlarm/data/connected.csv')
            print('No Muses Found')
        else:
            try:
                f = open('/home/pi/Desktop/MuseAlarm/data/connected.csv', 'w')
                writer = csv.writer(f)
                f.close()
                #t2 = mp.Process(target=recordThread, args=())
                #t2.start()
                stream(str(muses[0]['address']))

                # Note: Streaming is synchronous, so code here will not execute until the stream has been closed
                #persists no connection to GUI
                if os.path.exists('/home/pi/Desktop/MuseAlarm/data/connected.csv'):
                    os.remove('/home/pi/Desktop/MuseAlarm/data/connected.csv')
            except(KeyboardInterrupt):
                print('Stream has ended')


if __name__ == "__main__":

    #appends working directory to path
    sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
    print("Working Directory added to path")

    sys.path.append(os.getcwd())
    sys.path.append('/home/pi/Desktop/MuseAlarm/waveloading.gif')
    sys.path.append('/home/pi/Desktop/MuseAlarm/checklist.png')
    sys.path.append('/home/pi/Desktop/MuseAlarm/data/connected.csv')
    print("Working Directory added to path")

    if os.path.exists('/home/pi/Desktop/MuseAlarm/data/connected.csv'):
        os.remove('/home/pi/Desktop/MuseAlarm/data/connected.csv')

    stopAlarmCSV = pd.DataFrame([''])
    stopAlarmCSV.to_csv('/home/pi/Desktop/Method2/alarmStop.csv')
    
    #starts the UI process
    t1 = mp.Process(target=GenerateUI, args=())
    #t1.start()
    t1.start()
    start_stream()
    t1.kill()
