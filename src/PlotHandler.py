# _*_ coding: utf-8 _*_

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

class PlotHandler:
    
    def getPlotTest(self, dataFrame):
        plt.plot(dataFrame["time"], dataFrame["value"], linewidth=0.5)
        plt.xlabel("Time")
        plt.ylabel("Intracranial pressure")
        plt.grid()
        ax = plt.gca()
        ax.set(autoscale_on=False)
        
        return plt.gcf()
        
    def getTestFigure(self):
        fig = mpl.figure.Figure(figsize=(2, 2))
        t = np.arange(0.0, 100.0, 0.01)
        s = np.sin(0.08 * np.pi * t)
        axes = fig.gca()
        axes.plot(t, s)
        axes.set_xlim(0, 50)
        axes.grid(True)
        return fig