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
        alternativetimes = []
        
        counter = 0
        # Each 'skipCounter' lanes, just one gets read, the others are ignored because of the impact of the excess of precision in reading time
        skipCounter = 10
        
        i = 0
        
        for x in file:
            counter = counter + 1
            if(counter == skipCounter):
                i = i + 1
                lane = file.readline().split("\t")
                exactTime = lane[0].split(",")
                exactTimeSeconds = int(exactTime[0])
                exactTimeMilliseconds = int(exactTime[1])
                # Calculates the exact time when the pressure value was recorded
                times.append(startingTime + timedelta(seconds=exactTimeSeconds, milliseconds=exactTimeMilliseconds))
                values.append(int(lane[1]))
                alternativetimes.append(i)
                counter = 0
        
        file.close()
        
        dataFrame = pd.DataFrame({
            'time': times,
            'value': values,
            'alternativetime': alternativetimes
        })
        
        return dataFrame