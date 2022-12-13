from scipy.signal import filtfilt
from scipy import stats
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
import scipy
import os
from subprocess import call


# NOTE: This File does NOT Trigger an alarm in its current state
def alarmtest(eeg_band, eeg_fft):
    dft = pd.DataFrame(columns=['band', 'val'])
    dft['band'] = eeg_band.keys()
    dft['val'] = [eeg_fft[band] for band in eeg_band]
    awakeSum = np.abs(dft._get_value(2, 'val')) + np.abs(dft._get_value(3, 'val'))  # + np.abs(dft._get_value(4,'val'))
    asleepSum = np.abs(dft._get_value(1, 'val')) + np.abs(dft._get_value(0, 'val'))
    ratio = asleepSum / (awakeSum + asleepSum)
    if os.path.exists('/home/pi/Desktop/MuseAlarm/data/models/model1/model1_ratios_11_8.csv'):
        ratioCSV1 = pd.read_csv('/home/pi/Desktop/MuseAlarm/data/models/model1/model1_ratios_11_8.csv')
        ratioCSV1.append(pd.DataFrame([time.strftime("%H:%M:%S"), ratio]))
    else:
        ratioCSV1 = pd.DataFrame([time.strftime("%H:%M:%S"), ratio])
    ratioCSV1.to_csv('/home/pi/Desktop/MuseAlarm/data/models/model1/model1_ratios_11_8.csv')
    if np.abs(ratio) <= 0.25:
        print(ratio)
        return False
    else:
        print("NO ALARM")
        print(ratio)
        return True


def bandPassFilter(signal):
    fs = 256  # sampling frequency, Hz
    lowcut = 1.0  # Hz
    highcut = 30.0  # Hz
    # 0.5∼30 Hz part of spontaneous EEG is considered in clinical medicine
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    order = 2

    b, a = scipy.signal.butter(order, [low, high], 'bandpass', analog=False)
    y = scipy.signal.filtfilt(b, a, signal, axis=0)
    return y


def fft_sig(f, clean, t):
    n = len(clean)
    dt = 0.004
    fhat = np.fft.fft(clean, n)  # Compute the FFT
    PSD = fhat * np.conj(fhat) / n  # Power spectrum (power per frequency)
    freq = (1 / (dt * n)) * np.arange(n)  # Create x-axis of frequencies
    ## Use the PSD to filter out noise
    indices = PSD > 100  # Find all freqs with large power
    PSDclean = PSD * indices  # Zero out all others
    fhat = indices * fhat  # Zero out small Fourier coeffs. in Y
    ffilt = np.fft.ifft(fhat)  # Inverse FFT for filtered time signal
    ffilt = np.real(ffilt)
    # plt.plot(t,f,color='c', label = 'Noisy')
    # plt.plot(t,clean,color ='k', label='Clean')
    # plt.plot(t, ffilt, color='b', label='Filtered')
    # plt.xlim(t[0],t[-1])
    # plt.legend()
    # plt.show()
    return ffilt


def eegAnalysisM1(af7,af8,tp9,tp10):
    data = pd.read_csv('/home/pi/Desktop/MuseAlarm/EEGsample.csv')
    # converting column data to list
    ts = data['timestamps'].tolist()
    tp9 = tp9.tolist()
    af7 = af7.tolist()
    af8 = af8.tolist()
    tp10 = tp10.tolist()
    posterior = af7 + af8  # for future applications, combining data
    anterior = tp9 + tp10
    sensors = [af7, af8, tp9, tp10]
    # Defining EEG band frequency ranges, Hz
    eeg_bands = {'Delta': (0.1, 4.0),
                 'Theta': (4.0, 8.0),
                 'Alpha': (8.0, 12.0),
                 'Beta': (12.0, 30.0),
                 'Gamma': (30.0, 45.0)}
    alarmBool = False
    for sensor_data in sensors:
        fs = 256  # Sampling Rate, Hz
        filtered_signal = bandPassFilter(sensor_data)
        filtered = fft_sig(sensor_data, filtered_signal, ts)
        eeg_band_fft = dict()
        # Take the mean of the fft amplitude for each EEG band (Only consider first channel)
        sp_bands = np.absolute(np.fft.fft(filtered))
        freq_bands = np.fft.fftfreq(filtered.shape[-1], 1.0 / fs)
        for band in eeg_bands:
            freq_ix = np.where((filtered >= eeg_bands[band][0]) &
                               (filtered <= eeg_bands[band][1]))[0]
            eeg_band_fft[band] = np.mean(filtered[freq_ix])

        if (alarmtest(eeg_bands, eeg_band_fft) == True):
            alarmBool =  True

    if (alarmBool == True):
        return True
    return False
