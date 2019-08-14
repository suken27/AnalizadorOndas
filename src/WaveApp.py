# _*_ coding: utf-8 _*_

from kivy.app import App
from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas

import matplotlib.patches as patches
import matplotlib.dates as mdates

from FileManager import FileManager
from PlotHandler import PlotHandler
from Analyzer import Analyzer
    
class LoadFilePopup(Popup):
    
    loadFileButton = ObjectProperty(0)
    
    def __init__(self, *args, **kwargs):
        self.caller = kwargs.get('caller')
        super(LoadFilePopup, self).__init__()
    
    def loadFile(self, file):
        self.caller.loadFile(file)
        self.dismiss()

class MainWidget(BoxLayout):
    
    loadFileButton = ObjectProperty(0)
    plotContainer = ObjectProperty(0)
    drawButton = ObjectProperty(0)
    fig = None
    press = None
    
    def loadFile(self, file):
        if self.fig != None:
            self.fig.clear()
        data_frame = FileManager().getDataFrame(file[0])
        self.fig = PlotHandler().getPlotTest(data_frame)
        wid = FigureCanvas(self.fig)
        self.fig.canvas.mpl_connect('scroll_event', self.onScroll)
        self.fig.canvas.mpl_connect('button_press_event', self.onPress)
        self.fig.canvas.mpl_connect('button_release_event', self.onRelease)
        self.fig.canvas.mpl_connect('motion_notify_event', self.onMotion)
        self.plotContainer.clear_widgets()
        self.plotContainer.add_widget(wid)
        Logger.info("File Load: File '%s' loaded successfully.", file[0])
        # detects A-waves
        detections = Analyzer().analyze(data_frame)
        # for each A-wave detection draws a rectangle around it
        for detection in detections:
            start = mdates.date2num(detection[0])
            end = mdates.date2num(detection[1])
            width = end - start
            new_rectangle = patches.Rectangle((start, detection[2]), width, detection[3], linewidth = 1, edgecolor = 'r', facecolor = 'none')
            self.fig.gca().add_patch(new_rectangle)
        
    def showLoadFilePopup(self):
        LoadFilePopup(caller=self).open()
        
    def loadDebugFile(self):
        self.loadFile(["C:\\Users\\Juanjo\\Google Drive\\MASTER\\Alumno Interno\\Sistema Nuevo\\Datos Monitorizacion\\USB SANDRA\\KLH Hab 205 12Feb2019.txt"])
        
    def zoomIn(self):
        if self.fig == None:
            return
        self.zoom(self.fig.canvas, 1/2)
        
    def zoomOut(self):
        if self.fig == None:
            return
        self.zoom(self.fig.canvas, 2)
    
    def onScroll(self, event):
        
        # if the mouse is not inside the figure, do nothing
        axes = event.canvas.figure.gca()
        if event.inaxes != axes: return
        
        Logger.debug("Event: Scroll event from mpl. x = %d, y = %d, step = %d, button = %s", event.x, event.y, event.step, event.button)
        
        if event.button == 'up':
            # deal with zoom in
            scale_factor = 1/2.
        elif event.button == 'down':
            # deal with zoom out
            scale_factor = 2.
        else:
            # deal with something that should never happen
            scale_factor = 1
            Logger.error("Event: A scroll event was captured but it was not scroll up neither scroll down.")
        
        # get event x location
        xdata = event.xdata
        self.zoom(event.canvas, scale_factor, xcenter = xdata)
       
    def zoom(self, canvas, scale_factor, xcenter = None):
        
        axes = canvas.figure.gca()
        
        # get the current x limit
        cur_xlim = axes.get_xlim()
        cur_xrange = (cur_xlim[1] - cur_xlim[0]) * 0.5
        if(xcenter == None):
            xcenter = cur_xlim[0] + cur_xrange
            
        # set new limits
        axes.set_xlim([xcenter - cur_xrange * scale_factor, xcenter + cur_xrange * scale_factor])
        
        # force re-draw
        canvas.draw()
        
    def onPress(self, event):
        
        # if the mouse is not inside the figure, do nothing
        axes = event.canvas.figure.gca()
        if event.inaxes != axes: 
            return
        
        # if the button is not the mouse left button, do nothing
        # 1 stands for MouseButton.LEFT
        if event.button != 1: 
            return
        
        Logger.debug("Event: Button press event from mpl. x = %d, y = %d, button = %s", event.x, event.y, event.button)
        
        self.press = event.xdata, event.ydata
    
    def onRelease(self, event):
        
        # if the mouse is not inside the figure, do nothing
        axes = event.canvas.figure.gca()
        if event.inaxes != axes: return
        
        # if the button is not the mouse left button, do nothing
        # 1 stands for MouseButton.LEFT
        if event.button != 1: 
            return
        
        Logger.debug("Event: Button release event from mpl. x = %d, y = %d, button = %s", event.x, event.y, event.button)
        
        self.press = None
        self.fig.canvas.draw()
    
    def onMotion(self, event):
        
        # if the mouse is not inside the figure, do nothing
        axes = event.canvas.figure.gca()
        if event.inaxes != axes: 
            return
        
        # if the mouse was not pressed, do nothing
        if self.press == None:
            return
        
        Logger.debug("Event: Button motion event from mpl. x = %d, y = %d, button = %s", event.xdata, event.ydata, event.button)

        
        prevx, prevy = self.press
        difx = prevx - event.xdata

        # set new limits
        xlim = axes.get_xlim()   
        axes.set_xlim([xlim[0] + difx, xlim[1] + difx])
        
        self.fig.canvas.draw()

class WaveApp(App):
    
    title = 'Wave Analizer'
    
    def build(self):
        mainwidget = MainWidget()
        return mainwidget
    