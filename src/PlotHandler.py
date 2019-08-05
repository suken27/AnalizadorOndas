# _*_ coding: utf-8 _*_

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

class PlotHandler:
    
    def getPlotTest(self, dataFrame):
        plt.plot(dataFrame["time"], dataFrame["value"])
        plt.xlabel("Hora")
        plt.ylabel("Presión intracraneal")
        ax = plt.gca()
        
        ratio = 0.1
        xleft, xright = ax.get_xlim()
        ybottom, ytop = ax.get_ylim()
        # the abs method is used to make sure that all numbers are positive
        # because x and y axis of an axes maybe inversed.
        ax.set_aspect(abs((xright-xleft)/(ybottom-ytop))*ratio)
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