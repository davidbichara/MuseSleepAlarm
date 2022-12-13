# From https://github.com/alexandrebarachant/muse-lsl/blob/master/examples/neurofeedback.py

#from EEGAnalysis import eegAnalysisM1
import numpy as np  # Module that simplifies computations on matrices
from pylsl import StreamInlet, resolve_byprop  # Module to receive EEG data
import threading
import multiprocessing as mp
from time import sleep
import datetime
import sys
import argparse
import os
import pandas as pd

# Handy little enum to make code more readable


# run2 = threading.Thread(target=start_stream, args=())
# run2.start()
#t2 = mp.Process(target=start_stream, args=())
#t2.start()


def findemptyfile(type):
    try:
        found = False
        index = 0
        while found == False:
            fileName = type + str(index) + ".csv"
            file = open(fileName, 'r')
            if file.read() == "":
                found = True
            index = index + 1
    except IOError:
        found = True
    return type + str(index) + ".csv"


def generateline(relaxed, alphaR, betaC, thetaR):
    global main
    main = ''
    main += '{0},{1},{2},{3}'.format(relaxed, alphaR, betaC, thetaR) + '\n'
    return main


def csvwrite(relaxed_status, final, file_name):
    if file_name == None:
        fileName = findemptyfile(str(relaxed_status + "_RecordedData"))
    else:
        fileName = file_name
    file = open(fileName, 'w+')
    file.write(final)


def data_reader():
    # Wait for stream to begin
    sleep(20)
    time = 30
    """ EXPERIMENTAL PARAMETERS """
    # Modify these to change aspects of the signal processing

    # Length of the EEG data buffer (in seconds)
    # This buffer will hold last n seconds of data and be used for calculations
    BUFFER_LENGTH = 30

    # Length of the epochs used to compute the FFT (in seconds)
    EPOCH_LENGTH = 1

    # Amount of overlap between two consecutive epochs (in seconds)
    OVERLAP_LENGTH = 0.8

    # Amount to 'shift' the start of each next consecutive epoch
    SHIFT_LENGTH = EPOCH_LENGTH - OVERLAP_LENGTH

    # Index of the channel(s) (electrodes) to be used
    # 0 = left ear, 1 = left forehead, 2 = right forehead, 3 = right ear
    INDEX_CHANNEL1 = [0]
    INDEX_CHANNEL2 = [1]
    INDEX_CHANNEL3 = [2]
    INDEX_CHANNEL4 = [3]


    """ 1. CONNECT TO EEG STREAM """

    # Search for active LSL streams
    print('Looking for an EEG stream...')
    streams = resolve_byprop('type', 'EEG', timeout=2)
    
    if len(streams) == 0:
        #persists no connection to GUI
        connectionCSV = pd.DataFrame(['Not Connected'])
        print(connectionCSV.head())
        connectionCSV.to_csv('/home/pi/Desktop/Method2/connection.csv')
        raise RuntimeError('Can\'t find EEG stream.')

    # Set active EEG stream to inlet and apply time correction
    print("Start acquiring data")
    inlet = StreamInlet(streams[0], max_chunklen=12)
    eeg_time_correction = inlet.time_correction()

    # Get
    # the stream info and description
    info = inlet.info()

    # Get the sampling frequency
    # This is an important value that represents how many EEG data points are
    # collected in a second. This influences our frequency band calculation.
    # for the Muse 2016, this should always be 256
    fs = 256

    """ 2. INITIALIZE BUFFERS """

    # Initialize raw EEG data buffer
    eeg_buffer1 = np.zeros((int(fs * BUFFER_LENGTH), 1))
    eeg_buffer2 = np.zeros((int(fs * BUFFER_LENGTH), 1))
    eeg_buffer3 = np.zeros((int(fs * BUFFER_LENGTH), 1))
    eeg_buffer4 = np.zeros((int(fs * BUFFER_LENGTH), 1))
    filter_state = None  # for use with the notch filter

    # Compute the number of epochs in "buffer_length"
    n_win_test = int(np.floor((BUFFER_LENGTH - EPOCH_LENGTH) /
                              SHIFT_LENGTH + 1))

    # Initialize the band power buffer (for plotting)
    # bands will be ordered: [delta, theta, alpha, beta]
    #band_buffer = np.zeros((n_win_test, 4))

    """ 3. GET DATA """

    # The try/except structure allows to quit the while loop by aborting the
    # script with <Ctrl-C>
    print('Press Ctrl-C in the console to break the while loop.')

    # try:
    endTime = datetime.datetime.now() + datetime.timedelta(minutes=time)
    # The following loop acquires data, computes band powers, and calculates neurofeedback metrics based on those band powers
    while True:
        if datetime.datetime.now() >= endTime:
            break

        """ 3.1 ACQUIRE DATA """
        # Obtain EEG data from the LSL stream
        eeg_data, timestamp = inlet.pull_chunk(
            timeout=1, max_samples=int(SHIFT_LENGTH * fs))

        # store data for each channel
        ch_data1 = np.array(eeg_data)[:, INDEX_CHANNEL1]
        ch_data2 = np.array(eeg_data)[:, INDEX_CHANNEL2]
        ch_data3 = np.array(eeg_data)[:, INDEX_CHANNEL3]
        ch_data4 = np.array(eeg_data)[:, INDEX_CHANNEL4]

        # Update EEG buffer with the new data

        """ 3.2 Analyze Data and Determine whether Alarm is called"""
        # Get newest samples from the buffer
        alarmBool = eegAnalysisM1(ch_data1,ch_data2, ch_data3, ch_data4,timestamp)

        #if analysis returns true boolean ->> trigger alarm sound
        if(alarmBool == True):
            stopAlarmCSV = pd.DataFrame([''])
            print(stopAlarmCSV.head())
            stopAlarmCSV.to_csv('/home/pi/Desktop/MuseAlarm/data/alarm/alarmStop.csv')
            duration = 1
            freq = 770
            call(["amixer", "-D", "pulse", "sset", "Master", str(100) + "%"])
            if os.path.exists('/home/pi/Desktop/MuseAlarm/data/connection.csv'):  # arr
                stopAlarmCSV = pd.read_csv('/home/pi/Desktop/MuseAlarm/data/alarm/alarmStop.csv').iloc[0, 1]
            if os.path.exists('/home/pi/Desktop/MuseAlarm/data/models/model1/time_11_8.csv'):  # arr
                modelOne = pd.read_csv('/home/pi/Desktop/MuseAlarm/data/models/model1/time_11_8.csv')
                modelOne.append(pd.DataFrame([time.strftime("%H:%M:%S")]))
            else:
                modelOne = pd.DataFrame([time.strftime("%H:%M:%S")])
            modelOne.to_csv('/home/pi/Desktop/MuseAlarm/data/models/model1/time_11_8.csv')

        #persists alarm until stopped

        while stopAlarmCSV != 'Stop':
            print(stopAlarmCSV)
            os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))
            time.sleep(2)
            if os.path.exists('/home/pi/Desktop/MuseAlarm/data/alarm/alarmStop.csv'):  # arr
                stopAlarmCSV = pd.read_csv('/home/pi/Desktop/MuseAlarm/data/alarm/alarmStop.csv').iloc[0, 1]


    # data_epoch = utils.get_last_data(eeg_buffer,
        #                                  EPOCH_LENGTH * fs)
        #
        # # Compute band powers
        # band_powers = utils.compute_band_powers(data_epoch, fs)
        # band_buffer, _ = utils.update_buffer(band_buffer,
        #                                      np.asarray([band_powers]))
        # # Compute the average band powers for all epochs in buffer
        # # This helps to smooth out noise
        # smooth_band_powers = np.mean(band_buffer, axis=0)

        # print('Delta: ', band_powers[Band.Delta], ' Theta: ', band_powers[Band.Theta],
        #       ' Alpha: ', band_powers[Band.Alpha], ' Beta: ', band_powers[Band.Beta])



    # csvwrite(mind_state, final, file_name)
    print(str(time) + ' minutes of data gathered, Writing CSV')
    return


