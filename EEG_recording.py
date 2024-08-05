import mne
import pyedflib
from pylsl import StreamInlet, resolve_stream
import pandas as pd
import numpy as np
import time

# Initialize the streaming layer
print("Looking for an EEG stream...")
streams = resolve_stream()
inlet = StreamInlet(streams[0])
print("Stream found!")

# Initialize the colomns of your data and your dictionary to capture the data.
columns = ['Time', 'FZ', 'C3', 'CZ', 'C4', 'PZ', 'PO7', 'OZ', 'PO8', 'AccX', 'AccY', 'AccZ',
           'Gyro1', 'Gyro2', 'Gyro3', 'Battery', 'Counter', 'Validation', 'Triggers']
s_freq = 250.0  # Sampling rate (Hz)
channel_names = ['FZ', 'C3', 'CZ', 'C4', 'PZ', 'PO7', 'OZ', 'PO8']  # List of channel names
# data_dict = dict((k, []) for k in columns)

data_only, all_data, all_triggers = [], [], []
num_char = 40
trig = 1

def main():
    global trig, data_only
    # Start recording
    while trig <= num_char:
        # Data is collected at 250 Hz. Let's stop data collection after 60 seconds.
        # Meaning we stop when we collect 250*60 samples.
        temp_time, triggers = [], []
        while len(temp_time) < s_freq/2:
            # Get the streamed data. Columns of sample are equal to the columns variable,
            # only the first element being timestamp concatenate timestamp and data in 1 list
            data, timestamp = inlet.pull_sample()
            all_data.append([timestamp] + data)
            temp_time.append(timestamp)
            data = data[1:9]
            data_only.append(data)
            all_triggers.append(trig)
            # print(len(temp_time))
        print(trig)
        trig += 1

    data_only = np.array(data_only)
    data_only = data_only.T
    # Create an Info object with sampling rate and channel information
    info = mne.create_info(ch_names=channel_names, sfreq=s_freq, ch_types='eeg')
    # Create a Raw object containing the data and info
    raw = mne.io.RawArray(data_only, info)
    # Save the data in EDF or XDF format (replace with your preferred format)
    raw.save('EEG_recording.fif', overwrite=True)
    print("EEG recording saved in fif format!")

    # Lastly, save our data and triggers to a CSV format.
    print(len(all_triggers))
    data_df = pd.DataFrame(all_data)
    data_df['Triggers'] = all_triggers
    data_df.columns = columns
    data_df.to_csv('EEG_data.csv', index=False)
    print("EEG recording saved in .csv format!")

if __name__ == '__main__':
    main()