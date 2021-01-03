from enum import Enum
import numpy as np
from pyqtgraph import AxisItem
from time import strftime, localtime
import time
import datetime 

from openQCM.common.architecture import Architecture,OSType

###############################################################################    
# Enum for the types of sources. Indices MUST match app_sources constant
###############################################################################
class SourceType(Enum):
    serial = 0
    calibration = 1
    SocketClient = 2
    

###############################################################################
# Specifies the minimal Python version required
###############################################################################
class MinimalPython:
    major = 3
    minor = 2
    release = 0    
 
  
###############################################################################    
# Common constants and parameters for the application.
###############################################################################
class Constants:
    
    ##########################
    # Application Parameters #
    ##########################
    app_title = "Real-Time openQCM GUI"
    app_version = '2.1'
    app_sources = ["Measurement openQCM Q-1 Device", "Calibration openQCM Q-1 Device"]#, "Socket Client"]
    app_encoding = "utf-8"
    
    
    ###################
    # PLOT parameters #
    ###################
    plot_update_ms = 200#16
    plot_colors = ['#ff0000', '#0072bd', '#00ffff', '#edb120', '#7e2f8e', '#77ac30', '#4dbeee', '#a2142f'] 
    plot_max_lines = len(plot_colors)
    
    
    ####################
    #  SAMPLES NUMBER  #
    ####################
    argument_default_samples = 501#1001
    
    
    ####################################
    # FILTERING and FITTING parameters #
    ####################################
    # Notes:
    # left and right frequencies in the area of the resonance frequency
    # Savitzky-Golay size of the data window 
    # Savitzky-Golay order of the polynomial fit
    # Number of spline points: same as the frequency band +1 (es.5001)
    # Spline smoothing factor
    
    # Savitzky-Golay order of the polynomial fit (common for all)
    SG_order = 3

    #--------------
    # 5MHz 
    #--------------
    # left and right frequencies
    L5_fundamental = 5500
    R5_fundamental = 2500
    # Savitzky-Golay size of the data window 
    SG_window_size5_fundamental = 9
    # Spline smoothing factor
    Spline_factor5_fundamental = 0.05
    # left and right frequencies
    L5_3th_overtone = 7500
    R5_3th_overtone = 2500
    # Savitzky-Golay size of the data window 
    SG_window_size5_3th_overtone = 11
    # Spline smoothing factor
    Spline_factor5_3th_overtone = 0.01
    
    # left and right frequencies
    L5_5th_overtone = 10000
    R5_5th_overtone = 2500
    # Savitzky-Golay size of the data window 
    SG_window_size5_5th_overtone = 11
    # Spline smoothing factor
    Spline_factor5_5th_overtone = 0.01
    
    # left and right frequencies
    L5_7th_overtone = 50000
    R5_7th_overtone = 2500
    # Savitzky-Golay size of the data window 
    SG_window_size5_7th_overtone = 33
    # Spline smoothing factor
    Spline_factor5_7th_overtone = 0.01
    
    # TODO
    # left and right frequencies 
    L5_9th_overtone = 5000000
    R5_9th_overtone = 100000
    # Savitzky-Golay size of the data window 
    SG_window_size5_9th_overtone = 5
    # Spline smoothing factor
    Spline_factor5_9th_overtone = 0.5
    
    #--------------
    # 10MHz 
    #--------------
    # left and right frequencies
    L10_fundamental = 7500
    R10_fundamental = 2500
    # Savitzky-Golay size of the data window 
    SG_window_size10_fundamental = 11
    # Spline smoothing factor
    Spline_factor10_fundamental = 0.01
    
    # left and right frequencies
    L10_3th_overtone = 13500
    R10_3th_overtone = 2500
    # Savitzky-Golay size of the data window 
    SG_window_size10_3th_overtone = 11    
    # Spline smoothing factor
    Spline_factor10_3th_overtone = 0.01
    
    # left and right frequencies
    L10_5th_overtone = 23000
    R10_5th_overtone = 3000
    # Savitzky-Golay size of the data window 
    SG_window_size10_5th_overtone = 19
    # Spline smoothing factor
    Spline_factor10_5th_overtone = 0.01


    ##########################
    # SERIAL PORT Parameters #
    ##########################
    serial_default_speed = 115200
    serial_default_overtone = None
    serial_default_QCS = "@10MHz"
    serial_writetimeout_ms = 0
    serial_timeout_ms = None#0.01

    
    ######################
    # Process parameters #
    ######################
    process_join_timeout_ms = 2000
    simulator_default_speed = 0.1 # not used
    parser_timeout_ms = 0.005
    
    
    ##################
    # Log parameters #
    ##################
    log_export_path = "logged_data"
    log_filename = "{}.log".format(app_title)
    log_max_bytes = 5120
    log_default_level = 1
    log_default_console_log = False
    

    ######################################
    # File parameters for exporting data #
    ######################################
    # sets the slash depending on the OS types
    if Architecture.get_os() is (OSType.macosx or OSType.linux):
       slash="/"
    else:
       slash="\\"
       
    csv_delimiter = "," # for splitting data of the serial port and CSV file storage
    csv_default_prefix = "%Y-%b-%d_%H-%M-%S"#"%H-%M-%S-%d-%b-%Y" # Hour-Minute-Second-month-day-Year
    csv_extension = "csv"
    txt_extension = "txt"
    csv_export_path = "logged_data"
    csv_filename = (strftime(csv_default_prefix, localtime()))#+'_DataLog')
    csv_sweeps_export_path = "{}{}{}".format(csv_export_path,slash,csv_filename)
    csv_sweeps_filename = "sweep"
    
    # Calibration: scan (WRITE for @5MHz and @10MHz QCS) path: 'common\'
    csv_calibration_filename    = "Calibration_5MHz"
    csv_calibration_filename10  = "Calibration_10MHz"
    csv_calibration_export_path = "openQCM" #"common"
    
    ################## 
    # Calibration: baseline correction (READ for @5MHz and @10MHz QCS) path: 'common\'
    csv_calibration_path   = "{}{}{}.{}".format(csv_calibration_export_path,slash,csv_calibration_filename,txt_extension)
    csv_calibration_path10 = "{}{}{}.{}".format(csv_calibration_export_path,slash,csv_calibration_filename10,txt_extension)
    
    # Frequencies: Fundamental and overtones (READ and WRITE for @5MHz and @10MHz QCS)
    csv_peakfrequencies_filename   = "PeakFrequencies"
    #csv_peakfrequencies_filename   = "PeakFrequencies_5MHz"
    #csv_peakfrequencies_filename10 = "PeakFrequencies_10MHz"
    cvs_peakfrequencies_path    = "{}{}{}.{}".format(csv_calibration_export_path,slash,csv_peakfrequencies_filename,txt_extension)
    #cvs_peakfrequencies_path10 = "{}{}{}.{}".format(csv_calibration_export_path,slash,csv_peakfrequencies_filename10,txt_extension)    
    #########################    
    '''
    # Calibration: baseline correction (READ for @5MHz and @10MHz QCS) path: 'common\'
    csv_calibration_path   = "{}\{}.{}".format(csv_calibration_export_path,csv_calibration_filename,txt_extension)
    csv_calibration_path10 = "{}\{}.{}".format(csv_calibration_export_path,csv_calibration_filename10,txt_extension)
    
    # Frequencies: Fundamental and overtones (READ and WRITE for @5MHz and @10MHz QCS)
    csv_peakfrequencies_filename   = "PeakFrequencies"
    #csv_peakfrequencies_filename   = "PeakFrequencies_5MHz"
    #csv_peakfrequencies_filename10 = "PeakFrequencies_10MHz"
    cvs_peakfrequencies_path    = "{}\{}.{}".format(csv_calibration_export_path,csv_peakfrequencies_filename,txt_extension)
    #cvs_peakfrequencies_path10 = "{}\{}.{}".format(csv_calibration_export_path,csv_peakfrequencies_filename10,txt_extension)
    '''
    
    ##########################
    # CALIBRATION PARAMETERS #
    ##########################
    
    # Peak Detection - distance in samples between neighbouring peaks
    dist5  =  8000 # for @5MHz
    dist10 =  10000 # for @10MHz
    calibration_default_samples = 50001
    calibration_frequency_start =  1000000
    calibration_frequency_stop  = 51000000 
    calibration_fStep = (calibration_frequency_stop - calibration_frequency_start) / (calibration_default_samples-1)
    calibration_readFREQ  = np.arange(calibration_default_samples) * (calibration_fStep) + calibration_frequency_start
    #-------------------
    calib_fStep = 1000
    calib_fRange = 5000000 #
    calib_samples = 5001
    calib_sections = 10
    
    ###########################
    # Ring Buffers Parameters #
    ###########################
    ring_buffer_samples = 16363
    
    ##############################
    # Parameters for the average #
    ##############################  
    environment = 50 #######################################################################################################
    SG_order_environment = 1
    SG_window_environment = 3
    
    ###################
    class SocketClient: #unused
        timeout = 0.01
        host_default = "localhost"
        port_default = [5555, 8080, 9090]
        buffer_recv_size = 1024
    ###################  



'''
###############################################################################
#  Provides a date-time aware axis
###############################################################################    
class DateAxis(AxisItem):
    
    """
    A tool that provides a date-time aware axis. It is implemented as an AxisItem 
    that interprets positions as UNIX timestamps (i.e. seconds since 1970). 
    The labels and the tick positions are dynamically adjusted depending on the range.
    """

    def __init__(self, *args, **kwargs):
        AxisItem.__init__(self, *args, **kwargs)
        self._oldAxis = None
    
    def tickStrings(self, values, scale, spacing):
        ret = []
        ep = datetime.datetime(1970,1,1,0,0,0)
        tonow = (datetime.datetime.utcnow()- ep).total_seconds()
        if not values:
            return []
        if spacing >= 31622400:  #366days
            fmt = "%Y"
        elif spacing >= 2678400: #31days
            fmt = "%Y %b"
        elif spacing >= 86400:   #1day
            fmt = "%b/%d"
        elif spacing >= 3600:    #1h
            fmt = "%b/%d-%Hh"
        elif spacing >= 60:      #1m
            fmt = "%H:%M"
        elif spacing >= 1:       #1s
            fmt = "%H:%M:%S"
        else: # less than 2s (show microseconds)
            #fmt = "%S.%f"""
            fmt = '[+%fms]'  # explicitly relative to last second   
        for x in values:
            try:
                ret.append(time.strftime(fmt, time.localtime(x*.1+tonow))) #time.localtime(x*.1+tonow)
            except ValueError:  # Windows can't handle dates before 1970
                ret.append('')
            except:
                ret.append('')    
        return ret
'''
###############################################################################
#  Provides a date-time aware axis
###############################################################################  
class DateAxis(AxisItem): 
    def __init__(self, *args, **kwargs):
        super(DateAxis, self).__init__(*args, **kwargs)            
          
    def tickStrings(self, values, scale, spacing):    
        TS_MULT_us = 1e6
        try:
            z= [(datetime.datetime.utcfromtimestamp(float(value)/TS_MULT_us)).strftime("%b-%d %H:%M:%S") for value in values]
        except: 
            z= ''
        return z
        #return [(datetime.datetime.utcfromtimestamp(float(value)/TS_MULT_us)).strftime("%b-%d %H:%M:%S") for value in values]


###############################################################################
#  Provides a non scientific axis notation
###############################################################################  
class NonScientificAxis(AxisItem):
    def __init__(self, *args, **kwargs):
        super(NonScientificAxis, self).__init__(*args, **kwargs)

    def tickStrings(self, values, scale, spacing):
        return [int(value*1) for value in values] 