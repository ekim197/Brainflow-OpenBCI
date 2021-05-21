import time
from datetime import datetime

import numpy as np
import pandas as pd
import pyeeg
import threading
import random

from PowerBinModel import PowerBinModel
from DataProcessingHelper import filterEEG
from pyOpenBCI import OpenBCIGanglion
import atexit

class Test:
    def __init__(self):
        pass

    def startStream(self):
        print("LIVE: started eeg streaming")
   
        self.channels = ['C4', 'Cz', 'C3', 'EOG']
        self.board = OpenBCIGanglion(mac='F1:E4:A6:B1:AC:02')
        # self.eeg_thread = threading.Thread(target=self.board.start_stream, args=(self.push_data_sample,))
        self.four_seconds_ago = datetime.now().timestamp()
        self.four_second_data = []
        self.eeg_thread = threading.Thread(target=self.board.start_stream, args=(self.callback,))

        self.eeg_thread.start()


    def callback(self, sample):
        now = datetime.now().timestamp()
        diff = now - self.four_seconds_ago 

        if diff >= 3.95 and diff <= 4.05: # roughly within 4 second block
            self.four_seconds_ago = now
            data = [i for i in self.four_second_data]
            self.four_second_data = [] # clear out four_second_data for new block of 4 seconds


            # testing data input: print(data)
            # create a thread to avoid if statement and data processing blocking 
            # data collection
            pre_processing_thread = threading.Thread(target=self.preprocessing, args=(data,))
            pre_processing_thread.start()

        self.four_second_data.append(sample.channels_data)

    def preprocessing(self, data):
        # append data such that each channel contains a list of 
        # all timepoints/eeg data for this channel
        channel_data = []
        for channel in self.channels:
            channel_data.append([])

        for row in data:
            row_list = list(row)
            for i in range(len(row_list)):
                channel_data[i].append(row_list[i])
        
        # convert data to single row of dict of column --> list
        pd_dict = []
        pd_dict.append({
            '0': channel_data[0],
            '1': channel_data[1],
            '2': channel_data[2],
            '3': channel_data[3]
        })

        processed_data_final = pd.DataFrame.from_dict(pd_dict)
        print(processed_data_final.head())
        print("Columns are:", processed_data_final.columns)

test = Test()
test.startStream()
