import pandas as pd
import matplotlib.pyplot as plt

file = open("../input/KLH Hab 205 12Feb2019.txt", "r")
for x in range(8):
    file.readline()

times = []
values = []

for x in file:
    lane = file.readline().split("\t")
    times.append(float(lane[0].replace(',','.')))
    values.append(int(lane[1]))
    
dataFrame = pd.DataFrame({
    'time':times,
    'value':values
})

ax = plt.gca()

dataFrame.plot(kind='line', x="time", y="value", ax=ax)
plt.show()