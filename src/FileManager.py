# _*_ coding: utf-8 _*_

import pandas as pd
from datetime import datetime, timedelta
from kivy.logger import Logger

class FileManager:
    
    # TODO add function to check if the provided file is a valid pressure recording file.
    
    def getDataFrame(self, file_path):
        file = open(file_path, "r")
        # Save the recording interval
        # Example of the interval format "Interval=\t0,025\ss"
        interval = int(file.readline().split("\t")[1].split(" ")[0].split(",")[1])
        # I keep the starting time of pressure monitoring to calculate the exact time of pressure recording
        starting_time = datetime.strptime(file.readline().split("\t")[2][:-1], '%d/%m/%Y %H:%M:%S,%f')
        # Skip the rest of the headers
        for x in range(6):
            file.readline()
        
        times = []
        values = []
        alternative_times = []
        
        counter = 0
        # Each 'skipCounter' lanes, just one gets read, the others are ignored because of the impact of the excess of precision in reading time
        skip_counter = 40
        
        interval_addition = 0
        i = 0
        
        for x in file:
            counter = counter + 1
            if(counter == skip_counter):
                i = i + 1
                try:
                    lane = file.readline().split("\t")
                    value = int(lane[1])
                # I found sometimes the input data contains 'NaN' as value in some intervals
                except ValueError:
                    interval_addition = interval_addition + skip_counter * interval
                    counter = 0
                    continue
                except:
                    Logger.error("File Manager: Parsing error. lane[0] = %s, lane[1] = %s.", lane[0], lane[1])
                    raise
                # Calculates the exact time when the pressure value was recorded
                interval_addition = interval_addition + skip_counter * interval
                times.append(starting_time + timedelta(milliseconds=interval_addition))
                values.append(value)
                alternative_times.append(i)
                counter = 0
        
        file.close()
        
        data_frame = pd.DataFrame({
            'time': times,
            'value': values,
            'alternative_time': alternative_times
        })
        
        return data_frame