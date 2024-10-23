import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, iirnotch, freqz, lfilter, tf2zpk
from numpy.linalg import inv

# Load ECG data from an Excel file
file_path = r'C:\Users\97059\Desktop\Dsp\Data_ECG_raw.xlsx'
data = pd.read_excel(file_path, sheet_name=None)

# Extract ECG1 and ECG2 data
ecg1 = data['ECG1']
ecg2 = data['ECG2']

# Fix column names
ecg1.columns = ['sample_number', 'time_s', 'amplitude_mv1', 'amplitude_mv2'] + [None]*4
ecg2.columns = ['sample_number', 'time_s', 'amplitude_mv1', 'amplitude_mv2']

# Select relevant columns and drop missing values
ecg1 = ecg1[['time_s', 'amplitude_mv1', 'amplitude_mv2']].dropna()
ecg2 = ecg2[['time_s', 'amplitude_mv1', 'amplitude_mv2']].dropna()

# Convert columns to numeric, dropping non-numeric values
ecg1 = ecg1.apply(pd.to_numeric, errors='coerce').dropna()
ecg2 = ecg2.apply(pd.to_numeric, errors='coerce').dropna()

# Define the sampling rate
sampling_rate = 360  # Hz

# Add a real-time column based on the sampling rate
ecg1['real_time'] = np.arange(len(ecg1)) / sampling_rate
ecg2['real_time'] = np.arange(len(ecg2)) / sampling_rate

# Plot the original ECG signals
plt.figure(figsize=(14, 6))

plt.subplot(2, 1, 1)
plt.plot(ecg1['real_time'], ecg1['amplitude_mv1'], label='Amplitude 1', linewidth=0.5)
plt.plot(ecg1['real_time'], ecg1['amplitude_mv2'], label='Amplitude 2', linewidth=0.5, linestyle='--')
plt.title('ECG1 Signal - Lana_1210455 & Mayar_1211246 & Mohammad_1201261')
plt.xlabel('Real Time (s)')
plt.ylabel('Amplitude (mV)')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(ecg2['real_time'], ecg2['amplitude_mv1'], label='Amplitude 1', linewidth=0.5)
plt.plot(ecg2['real_time'], ecg2['amplitude_mv2'], label='Amplitude 2', linewidth=0.5, linestyle='--')
plt.title('ECG2 Signal - Lana_1210455 & Mayar_1211246 & Mohammad_1201261')
plt.xlabel('Real Time (s)')
plt.ylabel('Amplitude (mV)')
plt.legend()

plt.tight_layout()
plt.show()

# Define a low-pass filter
def low_pass_filter(data, cutoff=40, fs=360, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

# Define a high-pass filter
def high_pass_filter(data, cutoff=0.5, fs=360, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    padded_data = np.pad(data, (len(data), len(data)), mode='reflect')
    y = filtfilt(b, a, padded_data)
    return y[len(data):-len(data)]

# Define a notch filter to remove 60 Hz powerline noise
def notch_filter(data, freq=60, fs=360, quality=30):
    nyquist = 0.5 * fs
    normal_cutoff = freq / nyquist
    b, a = iirnotch(normal_cutoff, quality)
    y = filtfilt(b, a, data)
    return y

# Apply filters to ECG1 signal
ecg1_filtered_lp = low_pass_filter(ecg1['amplitude_mv1'])
ecg1_filtered_hp = high_pass_filter(ecg1_filtered_lp)
ecg1_filtered = notch_filter(ecg1_filtered_hp)

# Plot the original and filtered ECG1 signals
plt.figure(figsize=(14, 6))

plt.subplot(2, 1, 1)
plt.plot(ecg1['real_time'], ecg1['amplitude_mv1'], label='Original Signal', linewidth=0.5)
plt.title('Original ECG1 Signal')
plt.xlabel('Real Time (s)')
plt.ylabel('Amplitude (mV)')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(ecg1['real_time'], ecg1_filtered, label='Filtered Signal', linewidth=0.5, color='red')
plt.title('Filtered ECG1 Signal - Lana_1210455 & Mayar_1211246 & Mohammad_1201261')
plt.xlabel('Real Time (s)')
plt.ylabel('Amplitude (mV)')
plt.legend()

plt.tight_layout()
plt.show()

# Apply filters to ECG2 signal
ecg2_filtered_lp = low_pass_filter(ecg2['amplitude_mv1'])
ecg2_filtered_hp = high_pass_filter(ecg2_filtered_lp)
ecg2_filtered = notch_filter(ecg2_filtered_hp)

# Plot the original and filtered ECG2 signals
plt.figure(figsize=(14, 6))

plt.subplot(2, 1, 1)
plt.plot(ecg2['real_time'], ecg2['amplitude_mv1'], label='Original Signal', linewidth=0.5)
plt.title('Original ECG2 Signal')
plt.xlabel('Real Time (s)')
plt.ylabel('Amplitude (mV)')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(ecg2['real_time'], ecg2_filtered, label='Filtered Signal', linewidth=0.5, color='red')
plt.title('Filtered ECG2 Signal - Lana_1210455 & Mayar_1211246 & Mohammad_1201261')
plt.xlabel('Real Time (s)')
plt.ylabel('Amplitude (mV)')
plt.legend()

plt.tight_layout()
plt.show()

# Custom high-pass filter based on given equation
def custom_high_pass_filter(signal):
    n = len(signal)
    hp = np.zeros(n)
    for i in range(32, n):
        hp[i] = hp[i-1] - (1/32)*signal[i] + signal[i-16] - signal[i-17] + (1/32)*signal[i-32]
    return hp

# Custom low-pass filter based on given equation
def custom_low_pass_filter(signal):
    n = len(signal)
    lp = np.zeros(n)
    for i in range(12, n):
        lp[i] = 2*lp[i-1] - lp[i-2] + signal[i] - 2*signal[i-6] + signal[i-12]
    return lp

# Apply custom filters to ECG1 signal
ecg1_amplitude_mv1 = ecg1['amplitude_mv1'].values
ecg1_hp_filtered = custom_high_pass_filter(ecg1_amplitude_mv1)
ecg1_lp_filtered = custom_low_pass_filter(ecg1_hp_filtered)

# Apply custom filters to ECG2 signal
ecg2_amplitude_mv1 = ecg2['amplitude_mv1'].values
ecg2_hp_filtered = custom_high_pass_filter(ecg2_amplitude_mv1)
ecg2_lp_filtered = custom_low_pass_filter(ecg2_hp_filtered)

# Plot the original and high-pass filtered ECG1 signal
plt.figure(figsize=(14, 6))
plt.plot(ecg1['time_s'], ecg1_hp_filtered, label='High-Pass Filtered Signal', linewidth=0.5, color='orange')
plt.title('ECG1 Signal with High-Pass Filter - Lana_1210455 & Mayar_1211246 & Mohammad_1201261')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude (mV)')
plt.legend()
plt.tight_layout()
plt.show()

# Plot the original and high-pass filtered ECG2 signal
plt.figure(figsize=(14, 6))
plt.plot(ecg2['time_s'], ecg2_hp_filtered, label='High-Pass Filtered Signal', linewidth=0.5, color='orange')
plt.title('ECG2 Signal with High-Pass Filter - Lana_1210455 & Mayar_1211246 & Mohammad_1201261')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude (mV)')
plt.legend()
plt.tight_layout()
plt.show()

# Frequency response of custom high-pass filter
b_custom_hp = [-1/32] + [0]*14 + [1, -1] + [0]*14 + [1/32]
a_custom_hp = [1, -1]
w_custom_hp, h_custom_hp = freqz(b_custom_hp, a_custom_hp, worN=8000)

# Plot frequency response of custom high-pass filter
plt.figure(figsize=(14, 6))
plt.subplot(2, 1, 1)
plt.plot(0.5 * sampling_rate * w_custom_hp / np.pi, np.abs(h_custom_hp), 'b')
plt.title('Magnitude Response of High-Pass Filter - Lana_1210455 & Mayar_1211246 & Mohammad_1201261')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Gain')
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(0.5 * sampling_rate * w_custom_hp / np.pi, np.angle(h_custom_hp), 'b')
plt.title('Phase Response of High-Pass Filter - Lana_1210455 & Mayar_1211246 & Mohammad_1201261')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Phase (radians)')
plt.grid()

plt.tight_layout()
plt.show()

# Frequency response of custom low-pass filter
b_custom_lp = [1, 0, 0, 0, 0, 0, -2, 0, 0, 0, 0, 0, 1]
a_custom_lp = [1, -2, 1]
w_custom_lp, h_custom_lp = freqz(b_custom_lp, a_custom_lp, worN=8000)

# Plot frequency response of custom low-pass filter
plt.figure(figsize=(14, 6))

plt.subplot(2, 1, 1)
plt.plot(0.5 * sampling_rate * w_custom_lp / np.pi, np.abs(h_custom_lp), 'b')
plt.title('Magnitude Response of Low-Pass Filter - Lana_1210455 & Mayar_1211246 & Mohammad_1201261')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Gain')
plt.grid()

plt.subplot(2, 1, 2)
plt.plot(0.5 * sampling_rate * w_custom_lp / np.pi, np.angle(h_custom_lp), 'b')
plt.title('Phase Response of Low-Pass Filter - Lana_1210455 & Mayar_1211246 & Mohammad_1201261')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Phase (radians)')
plt.grid()

plt.tight_layout()
plt.show()

# Plot unit circle for high-pass filter
def plot_unit_circle(b, a, filter_type):
    z, p, k = tf2zpk(b, a)
    plt.figure(figsize=(8, 8))
    plt.plot(np.cos(np.linspace(0, 2 * np.pi, 100)), np.sin(np.linspace(0, 2 * np.pi, 100)), 'k--')  # Unit circle
    plt.scatter(np.real(z), np.imag(z), s=50, marker='o', color='blue', label='Zeros')
    plt.scatter(np.real(p), np.imag(p), s=50, marker='x', color='red', label='Poles')
    plt.title(f'{filter_type} Filter Zeros and Poles - Lana_1210455 & Mayar_1211246 & Mohammad_1201261')
    plt.xlabel('Real')
    plt.ylabel('Imaginary')
    plt.legend()
    plt.grid()
    plt.axhline(0, color='black', lw=0.5)
    plt.axvline(0, color='black', lw=0.5)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

# Plot unit circle for high-pass filter
plot_unit_circle(b_custom_hp, a_custom_hp, 'High-Pass')

# Plot unit circle for low-pass filter
plot_unit_circle(b_custom_lp, a_custom_lp, 'Low-Pass')
