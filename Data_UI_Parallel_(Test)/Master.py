from multiprocessing import Process, Pipe
import time
import Arduino_to_Python
import UI_Example_Code


if __name__ == '__main__':
    data_pipe_UI, data_pipe_Data = Pipe()
    UI_process = Process(target=UI_Example_Code.master, args=(data_pipe_UI,))
    Data_process = Process(target=Arduino_to_Python.master, args=(data_pipe_Data,))
    UI_process.start()
    Data_process.start()
    while(True):
        time.sleep(1)