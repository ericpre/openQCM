from multiprocessing import Queue

from openQCM.core.constants import Constants, SourceType
from openQCM.processors.Parser import ParserProcess
from openQCM.processors.Serial import SerialProcess
from openQCM.processors.SocketClient import SocketProcess
from openQCM.processors.Calibration import CalibrationProcess
from openQCM.common.fileStorage import FileStorage
from openQCM.common.logger import Logger as Log
from openQCM.core.ringBuffer import RingBuffer
import numpy as np
from time import time
#import pywt

TAG = ""#"[Worker]"

###############################################################################
# Service that creates and concentrates all processes to run the application
###############################################################################
class Worker:

    ###########################################################################
    # Creates all processes involved in data acquisition and processing
    ###########################################################################
    def __init__(self,QCS_on = None,
                      port = None,
                      speed = Constants.serial_default_overtone,
                      samples = Constants.argument_default_samples,
                      source = SourceType.serial,
                      export_enabled = False):
        """
        :param port: Port to open on start :type port: str.
        :param speed: Speed for the specified port :type speed: float.
        :param samples: Number of samples :type samples: int.
        :param source: Source type :type source: SourceType.
        :param export_enabled: If true, data will be stored or exported in a file :type export_enabled: bool.
        :param export_path: If specified, defines where the data will be exported :type export_path: str.
        """
        # data queues 
        self._queue1 = Queue()
        self._queue2 = Queue()
        self._queue3 = Queue()
        self._queue4 = Queue()
        self._queue5 = Queue()
        self._queue6 = Queue()
        
        # data buffers
        self._data1_buffer = None 
        self._data2_buffer = None 
        self._d1_buffer = None 
        self._d2_buffer = None
        self._d3_buffer = None
        self._t1_buffer = None 
        self._t2_buffer = None
        self._t3_buffer = None
        self._ser_error1 = 0
        self._ser_error2 = 0
        self._ser_err_usb= 0
        self._control_k = 0
        
        # instances of the processes
        self._acquisition_process = None
        self._parser_process = None
        
        # others
        self._QCS_on = QCS_on # QCS installed on device (unused now)
        self._port = port     # serial port 
        # overtones (str) if 'serial' is called
        # QCS (str) if 'calibration' is called 
        self._speed = speed 
        self._samples = samples
        self._source = source
        self._export = export_enabled
        
        # Supporting variables
        self._d1_store = None # data storing
        self._d2_store = None # data storing
        self._readFREQ = None # frequency range
        self._fStep    = None # sample rate
        self._overtone_name  = None # fundamental/overtones name (str)
        self._overtone_value = None # fundamental/overtones value(float)
        self._count = 0 # sweep counter
        self._flag = True
        self._timestart = 0
        
        
    ###########################################################################
    # Starts all processes, based on configuration given in constructor.
    ###########################################################################
    def start(self):
        
        if self._source == SourceType.serial:
           self._samples = Constants.argument_default_samples
        elif self._source == SourceType.calibration:
           self._samples = Constants.calibration_default_samples
           self._readFREQ = Constants.calibration_readFREQ
        # Setup/reset the internal buffers
        self.reset_buffers(self._samples)
        # Instantiates process
        self._parser_process = ParserProcess(self._queue1,self._queue2,self._queue3,self._queue4,self._queue5,self._queue6)
        # Checks the type of source
        if self._source == SourceType.serial:
            self._acquisition_process = SerialProcess(self._parser_process)
        elif self._source == SourceType.calibration:
            self._acquisition_process = CalibrationProcess(self._parser_process)
        elif self._source == SourceType.SocketClient:
            self._acquisition_process = SocketProcess(self._parser_process)
            
        if self._acquisition_process.open(port=self._port, speed=self._speed):
            if self._source == SourceType.serial:
               (self._overtone_name,self._overtone_value, self._fStep, self._readFREQ, SG_window_size, spline_points, spline_factor) = self._acquisition_process.get_frequencies(self._samples)
               #print(TAG, "Quartz Crystal Sensor installed: {}".format(self._QCS_on))
               print("")
               print(TAG, "DATA MAIN INFORMATION")
               print(TAG, "Selected frequency: {} - {}Hz".format(self._overtone_name,self._overtone_value))
               print(TAG, "Frequency start: {}Hz".format(self._readFREQ[0]))
               print(TAG, "Frequency stop:  {}Hz".format(self._readFREQ[-1]))
               print(TAG, "Frequency range: {}Hz".format(self._readFREQ[-1]-self._readFREQ[0]))
               print(TAG, "Number of samples: {}".format(self._samples-1))
               print(TAG, "Sample rate: {}Hz".format(self._fStep))
               print(TAG, "History buffer size: 180 min\n")
               print(TAG, "MAIN PROCESSING INFORMATION")
               print(TAG, "Method for baseline estimation and correction:")
               print(TAG, "Least Squares Polynomial Fit (LSP)")
               #print(TAG, "Degree of the fitting polynomial: 8")
               print(TAG, "Savitzky-Golay Filtering")
               print(TAG, "Order of the polynomial fit: {}".format(Constants.SG_order))
               print(TAG, "Size of data window (in samples): {}".format(SG_window_size))
               print(TAG, "Oversampling using spline interpolation")
               print(TAG, "Spline points (in samples): {}".format(spline_points-1))
               print(TAG, "Resolution after oversampling: {}Hz".format((self._readFREQ[-1]-self._readFREQ[0])/(spline_points-1)))
               
            elif self._source == SourceType.calibration:
               print("")
               print(TAG, "MAIN CALIBRATION INFORMATION")
               print(TAG, "Calibration frequency start:  {}Hz".format(Constants.calibration_frequency_start))
               print(TAG, "Calibration frequency stop:  {}Hz".format(Constants.calibration_frequency_stop))
               print(TAG, "Frequency range: {}Hz".format(Constants.calibration_frequency_stop-Constants.calibration_frequency_start))
               print(TAG, "Number of samples: {}".format(Constants.calibration_default_samples-1))
               print(TAG, "Sample rate: {}Hz".format(Constants.calibration_fStep))
            print(TAG, 'Training for plot...\n')
            # Starts processes
            self._acquisition_process.start()
            self._parser_process.start()
            return True
        else:
            print(TAG, 'Warning: port is not available')
            Log.i(TAG, "Warning: Port is not available")
            return False


    ###########################################################################
    # Stops all running processes
    ###########################################################################    
    def stop(self):
        
        self._acquisition_process.stop()
        self._parser_process.stop()
        '''
        for process in [self._acquisition_process, self._parser_process]:
            if process is not None and process.is_alive():
                process.stop()
                process.join(Constants.process_join_timeout_ms)
        '''
        print(TAG, 'Running processes stopped...')
        print(TAG, 'Processes finished')
        Log.i(TAG, "Running processes stopped...")
        Log.i(TAG, "Processes finished")
        
        
    ###########################################################################
    # Empties the internal queues, updating data to consumers
    ###########################################################################    
    def consume_queue1(self):
        # queue1 for serial data: amplitude
        while not self._queue1.empty():
            self._queue_data1(self._queue1.get(False))
    
    def consume_queue2(self):
        # queue2 for serial data: phase
        while not self._queue2.empty():
            self._queue_data2(self._queue2.get(False))

    def consume_queue3(self):
        # queue3 for elaborated data: resonance frequency
        while not self._queue3.empty():
            self._queue_data3(self._queue3.get(False))
            
    def consume_queue4(self):
        # queue3 for elaborated data: Q-factor/Dissipation
        while not self._queue4.empty():
            self._queue_data4(self._queue4.get(False))    
           
    def consume_queue5(self):
        # queue3 for elaborated data: Temperature
        while not self._queue5.empty():
            self._queue_data5(self._queue5.get(False)) 
    
    def consume_queue6(self):
        # queue3 for elaborated data: errors
        while not self._queue6.empty():
            self._queue_data6(self._queue6.get(False))
            
    ###########################################################################
    # Adds data to internal buffers.
    ###########################################################################    
    def _queue_data1(self,data):
        #:param data: values to add for serial data: amplitude :type data: float.
        self._data1_buffer = data
    
    #####    
    def _queue_data2(self,data):
        #:param data: values to add for serial data phase :type data: float.
        self._data2_buffer = data
        # Additional function: exports calibration data in a file if export box is checked.
        '''
        self.store_data_calibration()
        '''
    #####
    def _queue_data3(self,data):
        #:param data: values to add for Resonance frequency :type data: float.
        self._t1_store = data[0] # time (unused)
        self._d1_store = data[1] # data
        self._t1_buffer.append(data[0])
        self._d1_buffer.append(data[1])
        
    #####
    def _queue_data4(self,data):
        # Additional function: exports processed data in a file if export box is checked.
        #:param data: values to add for Q-factor/dissipation :type data: float.
        self._t2_store = data[0] # time (unused)
        self._d2_store = data[1] # data
        self._t2_buffer.append(data[0])
        self._d2_buffer.append(data[1])
    
    #####
    def _queue_data5(self,data):
        # Additional function: exports processed data in a file if export box is checked.
        #:param data: values to add for temperature :type data: float.
        self._t3_store = data[0] # time (unused)
        self._d3_store = data[1] # data 
        self._t3_buffer.append(data[0])
        self._d3_buffer.append(data[1])
        # for storing relative time 
        if  self._flag and ~np.isnan(self._d3_store):
            self._timestart=time()
            self._flag = False
        # Data Storage in csv and/or txt file 
        self.store_data()
    
        #####
    def _queue_data6(self,data):
        #:param data: values to add for serial error :type data: float.
        self._ser_error1 = data[0]
        self._ser_error2 = data[1]
        self._control_k = data[2]
        self._ser_err_usb = data[3]
        
    ###########################################################################
    # Gets data buffers for plot (Amplitude,Phase,Frequency and Dissipation) 
    ###########################################################################        
    def get_value1_buffer(self):
        #:return: float list.
        return self._data1_buffer
    
    #####
    def get_value2_buffer(self):
        #:return: float list.
        return self._data2_buffer

    #####
    def get_d1_buffer(self):
        #:return: float list.
        return self._d1_buffer.get_all()
        
    ##### Gets time buffers
    def get_t1_buffer(self):
        #:return: float list.
        return self._t1_buffer.get_all()
    
    #####
    def get_d2_buffer(self):
        #:return: float list.
        return self._d2_buffer.get_all()
    
    ##### Gets time buffers
    def get_t2_buffer(self):
        #:return: float list.
        return self._t2_buffer.get_all()
    
    #####
    def get_d3_buffer(self):
        #:return: float list.
        return self._d3_buffer.get_all()
    
    ##### Gets time buffers
    def get_t3_buffer(self):
        #:return: float list.
        return self._t3_buffer.get_all()
    
    ##### Gets serial error
    def get_ser_error(self):
        #:return: float list.
        return self._ser_error1,self._ser_error2, self._control_k, self._ser_err_usb
    

    ###########################################################################
    # Exports data in csv and/or txt file if export box is checked
    ###########################################################################
    def store_data(self): 
        # Checks the type of source
        if self._source == SourceType.serial:
          # Checks the state of the export box
          #if self._export:
          # Storing calculated data with the format: timestamp,resonance frequency,dissipation
          filenameCSV = "{}_{}".format(Constants.csv_filename, self._overtone_name)
          FileStorage.CSVsave(filenameCSV, Constants.csv_export_path,time()-self._timestart, self._d3_store, self._d1_store, self._d2_store)

          if self._export:   
              # Storing acquired sweeps
              filename = "{}_{}_{}".format(Constants.csv_sweeps_filename, self._overtone_name,self._count)
              #filename = "{}_{}".format(Constants.csv_sweeps_filename,self._count)
              path = "{}_{}".format(Constants.csv_sweeps_export_path, self._overtone_name) 
              #FileStorage.CSV_sweeps_save(filename, path, self._readFREQ, self._data1_buffer, self._data2_buffer)
              FileStorage.TXT_sweeps_save(filename, path, self._readFREQ, self._data1_buffer, self._data2_buffer)
          self._count+=1
    
    ###########################################################################
    # Checks if processes are running
    ###########################################################################
    def is_running(self):  
        #:return: True if a process is running :rtype: bool.
        return self._acquisition_process is not None and self._acquisition_process.is_alive()


    ###########################################################################
    # Gets the available ports for specified source
    ###########################################################################
    @staticmethod
    def get_source_ports(source):
        
        """
        :param source: Source to get available ports :type source: SourceType.
        :return: List of available ports :rtype: str list.
        """
        if source == SourceType.serial:
            print(TAG,'Port connected:',SerialProcess.get_ports())
            return SerialProcess.get_ports()
        elif source == SourceType.calibration:
            print(TAG,'Port connected:',CalibrationProcess.get_ports())
            return CalibrationProcess.get_ports()
        elif source == SourceType.SocketClient:
            return SocketProcess.get_default_host()
        else:
            print(TAG,'Warning: unknown source selected')
            Log.w(TAG,"Unknown source selected")
            return None
        
        
    ###########################################################################
    # Gets the available speeds for specified source
    ###########################################################################
    @staticmethod
    def get_source_speeds(source):
        
        """
        :param source: Source to get available speeds :type source: SourceType.
        :return: List of available speeds :rtype: str list.
        """
        if source == SourceType.serial:
            return SerialProcess.get_speeds()
        elif source == SourceType.calibration:
            return CalibrationProcess.get_speeds()
        elif source == SourceType.SocketClient:
            return SocketProcess.get_default_port()
        else:
            print(TAG,'Unknown source selected')
            Log.w(TAG, "Unknown source selected")
            return None
        
    
    ###########################################################################
    # Setup/Clear the internal buffers
    ###########################################################################
    def reset_buffers(self, samples):
        #:param samples: Number of samples for the buffers :type samples: int.
        
        # Initialises data buffers
        self._data1_buffer = np.zeros(samples) # amplitude
        self._data2_buffer = np.zeros(samples) # phase
        #self._d1_buffer = []  # Resonance frequency 
        #self._d2_buffer = []  # Dissipation
        #self._d3_buffer = []  # temperature
        #self._t1_buffer = []  # time (Resonance frequency)
        #self._t2_buffer = []  # time (Dissipation)
        #self._t3_buffer = []  # time (temperature)

        # Initialises supporting variables
        self._d1_store = 0
        self._d2_store = 0
        self._d3_store = 0
        self._t1_store = 0
        self._t2_store = 0
        self._t3_store = 0
        self._ser_error1 = 0
        self._ser_error2 = 0
        self._ser_err_usb= 0
        #self._control_k = 0
        
        self._d1_buffer = RingBuffer(Constants.ring_buffer_samples)  # Resonance frequency 
        self._d2_buffer = RingBuffer(Constants.ring_buffer_samples)  # Dissipation
        self._d3_buffer = RingBuffer(Constants.ring_buffer_samples)  # temperature
        self._t1_buffer = RingBuffer(Constants.ring_buffer_samples)  # time (Resonance frequency)
        self._t2_buffer = RingBuffer(Constants.ring_buffer_samples)  # time (Dissipation)
        self._t3_buffer = RingBuffer(Constants.ring_buffer_samples)  # time (temperature)
        #print(TAG,'Buffers cleared')
        #Log.i(TAG, "Buffers cleared") 

    ############################################################################
    # Gets frequency range
    ############################################################################
    
    def get_frequency_range(self):
        
        """
        :param samples: Number of samples for the buffers :type samples: int.
        :return: overtone :type overtone: float.
        :return: frequency range :type readFREQ: float list.
        """
        return self._readFREQ
    
    
    ############################################################################
    # Gets overtones name, value and frequency step
    ############################################################################
    
    def get_overtone(self):
        
        """
        :param samples: Number of samples for the buffers :type samples: int.
        :return: overtone :type overtone: float.
        :return: frequency range :type readFREQ: float list.
        """
        return self._overtone_name,self._overtone_value, self._fStep
    