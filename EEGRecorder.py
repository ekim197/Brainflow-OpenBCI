import numpy as np
from CSVWriter import CSVWriter

import time
from datetime import datetime

import threading
import atexit
import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations


SCALE_FACTOR_EEG = 1.0 # V/count
DEFAULT_FS = 200
DEFAULT_CHANNELS = [0, 1, 2, 3] # All 4  channels of Ganglion

class EEGRecorder: 
    def __init__(self, live, output_filename, channels=DEFAULT_CHANNELS):
        self.fs = DEFAULT_FS
        self.output_filename = output_filename
        self.started = False
        self.live = live
        self.channels = channels
        atexit.register(self.end)
    
    ############################
    ## STREAM CONTROL METHODS ##
    ############################
    def start(self):
        print("start recording called")
        if self.live: 
           # from pyOpenBCI import OpenBCIGanglion
            print("LIVE: started eeg recording")
            header = ["timestamp"] + self.channels
            self.csv_writer = CSVWriter(self.output_filename, column_headers=header)

            #Setting up Brainflow stuff
            params = BrainFlowInputParams()
            params.serial_port = '/dev/ttyACM0'
            params.timeout = 3
            params.ip_port = 0
            params.ip_protocol = 0
            params.ip_address = ""


            board = BoardShim(1, params)
            board.prepare_session()


           # self.board = OpenBCIGanglion(mac='F1:E4:A6:B1:AC:02')
           # self.eeg_thread = threading.Thread(target=self.board.start_stream, args=(self.record_data_sample,))
            self.eeg_thread = threading.Thread(target=self.record_data_sample_brainflow, args=(board))
            self.eeg_thread.start()
            self.started = True

    def end(self): 
        print("end recording called")
        if self.started: 
            print("LIVE: ended eeg recording")
            if self.live:
                print("in self.live")
                self.board.stop_stream()
                time.sleep(5)
               # self.board.disconnect()
                self.board.release_session()
                time.sleep(5)


            self.started = False

    ####################
    ## HELPER METHODS ##
    ####################
    def record_data_sample(self, sample):
        # Get timestamp
        now = time.time()
        
        # Get the scaled channel data
        if self.live: 
           #raw_eeg_data = np.array(sample.channels_data) * SCALE_FACTOR_EEG
            raw_eeg_data = np.array(sample.get_current_board_data())
        else :
            raw_eeg_data = np.array(sample) 
        
        # Record to CSV
        row_data = [now]
        row_data.extend(raw_eeg_data[self.channels])
        self.csv_writer.writerow(row_data)



    def record_data_sample_brainflow(self, board):
        # Get timestamp
        board.start_session()

        now = time.time()

        # Get the scaled channel data
        if self.live:
            raw_eeg_data = np.array(sample.get_current_board_data())
        # else :
        #     raw_eeg_data = np.array(sample)

        # Record to CSV
        row_data = [now]
        row_data.extend(raw_eeg_data[self.channels])
        self.csv_writer.writerow(row_data)



