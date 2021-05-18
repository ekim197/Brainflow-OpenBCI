import argparse 
import time
import numpy as np
import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations
import pandas as pd

def main():
    BoardShim.enable_dev_board_logger()

    params = BrainFlowInputParams()
    params.serial_port = '/dev/ttyACM0'
   # params.mac_address = 'F1:E4:A6:B1:AC:02'
    params.timeout = 3
    params.ip_port = 0
    params.ip_protocol = 0
    params.ip_address = ""


    board = BoardShim(1, params)
    board.prepare_session()

    board.start_stream(45000, '')
    time.sleep(5)
    print("streaming")
    data = board.get_board_data()
    df = pd.DataFrame(data, columns=['0', '1', '2','3'])
    board.stop_stream()
    board.release_session()
    print("HI")
    print(data)

if __name__ == "__main__":
        main()

