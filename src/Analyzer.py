import time
from kivy.logger import Logger

# constants
MIN_A_WAVE_DURATION = 10
MIN_A_WAVE_PERCENTAGE = 0.9
MIN_A_WAVE_PRESSURE_VALUE = 20

class Analyzer:
    
    a_waves = []
    
    def analyze(self, data_frame):
        
        Logger.debug("Analyzer: Starting analyzing process...")
        
        counter = 1
        minute_difference = 0
        initial_time = data_frame["time"][0]
        initial_timestamp = time.mktime(initial_time.timetuple())
        
        # setting the window size based on the minimum A wave duration
        while minute_difference < MIN_A_WAVE_DURATION:
            
            i_time = data_frame["time"][counter]
            i_timestamp = time.mktime(i_time.timetuple())
            minute_difference = int(i_timestamp - initial_timestamp) / 60
            counter = counter + 1
            
        window_size = counter
        window = [None] * window_size
        
        Logger.debug("Analyzer: Printing initial parameters.")
        Logger.debug("Analyzer: MIN_A_WAVE_DURATION %d.", MIN_A_WAVE_DURATION)
        Logger.debug("Analyzer: MIN_A_WAVE_PERCENTAGE %f.", MIN_A_WAVE_PERCENTAGE)
        Logger.debug("Analyzer: MIN_A_WAVE_PRESSURE_VALUE %d.", MIN_A_WAVE_PRESSURE_VALUE)
        Logger.debug("Analyzer: End of initial parameters.")
        
        Logger.debug("Analyzer: The window size for A waves is %d.", window_size)
        
        # calculate how many window elements we need to fulfill some condition to consider that the full window is a wave detection
        min_a_wave_true_elements = window_size * MIN_A_WAVE_PERCENTAGE
        
        Logger.info("Analyzer: The minimum elements in the window to consider that the full window is a wave detection is %d.", min_a_wave_true_elements)
        
        # initialize the window with the first elements and calculate the initial A wave true elements number
        a_wave_true_elements = 0
        values = data_frame["value"]
        times = data_frame["time"]
        
        Logger.debug("Analyzer: Starting analyzing process...")
        
        counter = 0
        while counter < window_size:
            window[counter] = values[counter] >= MIN_A_WAVE_PRESSURE_VALUE
            if window[counter]:
                a_wave_true_elements = a_wave_true_elements + 1
            counter = counter + 1
        
        # main loop
        detections = []
        detection = None
        while counter < len(values):
            # check the new element and modify the true elements in the window number if needed
            window_index = counter % window_size
            old_value = window[window_index]
            window[window_index] = values[counter] >= MIN_A_WAVE_PRESSURE_VALUE
            if not old_value and window[window_index]:
                a_wave_true_elements = a_wave_true_elements + 1
            elif old_value and not window[window_index]:
                a_wave_true_elements = a_wave_true_elements - 1
            # check if end of wave detection
            if detection != None and a_wave_true_elements < min_a_wave_true_elements:
                detection.append(times[counter - 1])
                detections.append(detection)
                Logger.debug("Analyzer: A-wave detection at [%s - %s].", detection[0], detection[1])
                detection = None
            # check if there is a wave detection
            elif detection == None and a_wave_true_elements >= min_a_wave_true_elements:
                detection = []
                # the starting time of the wave detection is the oldest element in the window
                detection.append(times[counter - window_size + 1])
            counter = counter + 1
            
        Logger.debug("Analyzer: Analyzing process finished. %d A-wave detections found.", len(detections))
        return detections