
from scipy.signal import filtfilt
from scipy import stats
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy
import calendar
import time
from datetime import datetime
import os
import traceback
from subprocess import call


def alarmtest(eeg_band, eeg_fft):
    dft = pd.DataFrame(columns=['band', 'val'])
    dft['band'] = eeg_band.keys()
    dft['val'] = [eeg_fft[band] for band in eeg_band]
    awakeSum = np.abs(dft._get_value(2, 'val')) + np.abs(dft._get_value(3, 'val'))  # + np.abs(dft._get_value(4,'val'))
    asleepSum = np.abs(dft._get_value(1, 'val')) + np.abs(dft._get_value(0, 'val'))
    # Alpha Protocol:
    # Simple redout of alpha power, divided by delta waves in order to rule out noise
    ratio = (dft._get_value(2, 'val') / np.abs(dft._get_value(0, 'val')))
   
    print(dft)
    if np.abs(ratio) < 0.5:
        print("SOUND ALARM")
        print(ratio)
    else:
        print("NO ALARM")
        print(ratio)


def bandPassFilter(signal):
    fs = 256  # sampling frequency, Hz
    lowcut = 1.0  # Hz
    highcut = 30.0  # Hz

    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    order = 2

    b, a = scipy.signal.butter(order, [low, high], 'bandpass', analog=False)
    y = scipy.signal.filtfilt(b, a, signal, axis=0)
    n = len(y)
    fhat = np.fft.fft(np.abs(y))  # Compute the FFT
    PSD = fhat * np.conj(fhat)  # Power spectrum (power per frequency)
    return fhat

def alarm(PSD):
    delta=0
    theta=0
    alpha=0
    beta = 0
    gamma = 0
    eeg_bands = {'Delta': (0.1, 4.0),
                 'Theta': (4.0, 8.0),
                 'Alpha': (8.0, 12.0),
                 'Beta': (12.0, 30.0),
                 'Gamma': (30.0, 45.0)}
    for val in PSD:
        if 1 <= val < 4:
            delta+=1
        if 4 <= val <= 8:
            theta+=1
        if 8 <= val <= 12:
            alpha+=1
        if 12 <= val <=30:
            beta+=1
        if 30 <= val <= 60:
            gamma+=1
    thresh = (delta+theta)/(alpha+beta+gamma+theta+delta)
    print("delta: "+ str(delta)+ " theta: "+str(theta)+" alpha: "+str(alpha)+" beta: "+str(beta)+" gamma: "+str(gamma))
    
    if np.abs(thresh) > 0.25:
        current_GMT= time.gmtime()
        time_stamp = calendar.timegm(current_GMT)
        date_time = datetime.fromtimestamp(time_stamp)
        timeCSV.append(date)
        print("SOUND ALARM")
        return True, thresh
    else:
        print("NO ALARM")
        return False, thresh

def eegAnalysis():
    try:
        data = pd.read_csv("/home/pi/Desktop/MuseAlarm/EEGsample.csv")
    except Exception:
        print("Exception in EEG analysis", traceback.print_exc())
        return
    # converting column data to list
    ts = data['timestamps'].tolist()
    tp9 = data['TP9'].tolist()
    af7 = data['AF7'].tolist()
    af8 = data['AF8'].tolist()
    tp10 = data['TP10'].tolist()
    posterior = af7 + af8  # for future applications, combining data
    anterior = tp9 + tp10
    sensors = [tp9, tp10, af7, af8]
    ratios = []
    alarmBool = False
    for sensor_data in sensors:
        fs = 256  # Sampling Rate, Hz
        filtered_signal = bandPassFilter(sensor_data)
        [electrodeAlarm, ratio]=alarm(filtered_signal)
        ratios.append(ratio)
        if(electrodeAlarm==True):
            alarmBool = True
    #telemtery = pd.DataFrame({'time': [], 'TP9': [], 'TP10': [], 'AF7': [], 'AF8':[]})

    tp9 = ratios[0]
    tp10 = ratios[1]
    af7 = ratios[2]
    af8 = ratios[3]
    if(alarmBool==True):
        duration = 1
        freq = 440
        call(["amixer", "-D", "pulse", "sset", "Master", str(100) + "%"])
        stopAlarmCSV = False
        os.remove('/home/pi/Desktop/Method2/alarmStop.csv')       
        while stopAlarmCSV != True:
            print(stopAlarmCSV)
            os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
            time.sleep(2)
            if os.path.exists('/home/pi/Desktop/Method2/alarmStop.csv'):  # arr
                stopAlarmCSV = True
            

eegAnalysis()
