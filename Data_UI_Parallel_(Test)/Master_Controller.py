from multiprocessing import Process, Pipe
import time
import Data_Code
import UI_Code


if __name__ == '__main__':
    data_pipe_UI, data_pipe_Data = Pipe()
    UI_process = Process(target=UI_Code.master, args=(data_pipe_UI,))
    Data_process = Process(target=Data_Code.master, args=(data_pipe_Data,))
    UI_process.start()
    Data_process.start()
    while(True):
        time.sleep(1)