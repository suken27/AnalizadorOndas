# _*_ coding: utf-8 _*_

import pandas as pd
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt

file = open("../input/KLH Hab 205 12Feb2019.txt", "r")
file.readline()
startingTime = datetime.strptime(file.readline().split("\t")[2][:-1], '%d/%m/%Y %H:%M:%S,%f')
print(startingTime)
for x in range(6):
    file.readline()

times = []
values = []

for x in file:
    lane = file.readline().split("\t")
    exactTime = lane[0].split(",")
    exactTimeSeconds = int(exactTime[0])
    exactTimeMilliseconds = int(exactTime[1])
    times.append(startingTime + timedelta(seconds=exactTimeSeconds, milliseconds=exactTimeMilliseconds))
    values.append(int(lane[1]))
    
dataFrame = pd.DataFrame({
    'time':times,
    'value':values
})


plt.plot(dataFrame["time"], dataFrame["value"])
plt.xlabel("Hora")
plt.ylabel("Presión intracraneal")
ax = plt.gca()

ratio = 0.01
xleft, xright = ax.get_xlim()
ybottom, ytop = ax.get_ylim()
# the abs method is used to make sure that all numbers are positive
# because x and y axis of an axes maybe inversed.
ax.set_aspect(abs((xright-xleft)/(ybottom-ytop))*ratio)

plt.show()