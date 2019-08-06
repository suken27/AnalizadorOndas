# _*_ coding: utf-8 _*_

from kivy.app import App
from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas

from FileManager import FileManager
from PlotHandler import PlotHandler

def drawPlot(instance):
    print("TODO")
    
def onScroll(event):
    Logger.debug("Event: Scroll event from mpl %d %d %d %s", event.x, event.y, event.step, event.button)
    
    axes = event.canvas.figure.gca()
    
    # if the mouse is not inside the figure, do nothing
    if event.inaxes != axes: return
    
    # get the current x limit
    cur_xlim = axes.get_xlim()
    cur_xrange = (cur_xlim[1] - cur_xlim[0]) * 0.5
    xdata = event.xdata # get event x location
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
    # set new limits
    axes.set_xlim([xdata - cur_xrange * scale_factor, xdata + cur_xrange * scale_factor])
    event.canvas.draw() # force re-draw
    
def onPress():
    pass

    
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
    
    def loadFile(self, file):
        dataFrame = FileManager().getDataFrame(file[0])
        fig = PlotHandler().getPlotTest(dataFrame)
        wid = FigureCanvas(fig)
        fig.canvas.mpl_connect('scroll_event', onScroll)
        self.plotContainer.clear_widgets()
        self.plotContainer.add_widget(wid)
        Logger.info("File Load: File '%s' loaded successfully.", file[0])
        
    def showLoadFilePopup(self):
        LoadFilePopup(caller=self).open()
        
    def loadDebugFile(self):
        self.loadFile(["C:\\Users\\Juanjo\\Google Drive\\MASTER\\Alumno Interno\\Sistema Nuevo\\Datos Monitorizacion\\USB SANDRA\\KLH Hab 205 12Feb2019.txt"])

class WaveApp(App):
    
    title = 'Wave Analizer'
    
    def build(self):
        mainwidget = MainWidget()
        mainwidget.drawButton.bind(on_press=drawPlot)
        return mainwidget
    