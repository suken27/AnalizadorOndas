# _*_ coding: utf-8 _*_

import pandas as pd
from datetime import datetime, timedelta

class FileManager:
    
    # TODO add function to check if the provided file is a valid pressure recording file.
    
    def getDataFrame(self, filePath):
        file = open(filePath, "r")
        # This skips the first lane
        file.readline()
        # I keep the starting time of pressure monitoring to calculate the exact time of pressure recording
        startingTime = datetime.strptime(file.readline().split("\t")[2][:-1], '%d/%m/%Y %H:%M:%S,%f')
        # Skip the rest of the headers
        for x in range(6):
            file.readline()
        
        times = []
        values = []
        
        for x in file:
            lane = file.readline().split("\t")
            exactTime = lane[0].split(",")
            exactTimeSeconds = int(exactTime[0])
            exactTimeMilliseconds = int(exactTime[1])
            # Calculates the exact time when the pressure value was recorded
            times.append(startingTime + timedelta(seconds=exactTimeSeconds, milliseconds=exactTimeMilliseconds))
            values.append(int(lane[1]))
        
        file.close()
        
        dataFrame = pd.DataFrame({
            'time': times,
            'value': values
        })
        
        return dataFrame