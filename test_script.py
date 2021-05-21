import time
import numpy as np
import threading
from pyOpenBCI import OpenBCIGanglion

SCALE_FACTOR_EEG = 1.2 * 8388607.0 * 1.5 * 51.0  # uV/count
SCALE_FACTOR_EEG2 = (4500000)/24/(2**23-1) 
def print_data_sample(): 
    #raw_eeg_data = np.array(sample.channels_data) * SCALE_FACTOR_EEG
    #raw_eeg_data = np.array(sample.channels_data, dtype=np.float64) * SCALE_FACTOR_EEG2
    # print(raw_eeg_data)

    try:
        board = OpenBCIGanglion(mac='F1:E4:A6:B1:AC:02')
        board.start_stream(callback)
        #raw_data = np.array(board.channels_data)
       # print(raw_data)

    finally:
        print("stopping stream")

    '''
    print("creating ganglion object")
    board = OpenBCIGanglion(mac='F1:E4:A6:B1:AC:02')
    print("creating thread")
    eeg_thread = threading.Thread(target=board.start_stream, args=(print_data_sample,))
    eeg_thread.start()
    print("recording for 10 seconds")
    time.sleep(10)
    print("stopping stream")
    print('stopping thread')
   # eeg_thread._stop_event = threading.Event()
   # eeg_thread._stop_event.set()
    board.stop_stream()
    time.sleep(5)
    board.disconnect()
    time.sleep(5)
   # board = OpenBCIGanglion(mac="F1:E4:A6:B1:AC:02")
  #  board.connect()
    eeg_thread2 = threading.Thread(target=board.start_stream, args=(print_data_sample,))
    eeg_thread2.start()
    print("creating thread2")
    time.sleep(10)
    try:
        board.stop_stream()
        print('stopping thread2')
        print('stopping stream2')
    except: 
        print("done") 
'''

oldData = None
def callback(sample):
    global oldData

    if oldData is not None:
        print("Comparing to old data")
        print(oldData)



    oldData = sample.channels_data
    print("New data")
    print(sample.channels_data)
    time.sleep(3)

print_data_sample()
