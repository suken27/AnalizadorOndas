# _*_ coding: utf-8 _*_

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvas

from FileManager import FileManager
from PlotHandler import PlotHandler

def drawPlot(instance):
    print("TODO")
    
def onScroll(event):
    print('scroll event from mpl ', event.x, event.y, event.step)
    
    axes = event.canvas.figure.gca()
    
    # if the mouse is not inside the figure, do nothing
    if event.inaxes != axes: return
    
    # NOTA EL ZOOM FALLA PORQUE LOS DATOS EN EL EJE X SON DEMASIADO PRECISOS Y LOS FALLOS DE PRECISION AFECTAN MUCHO, EN EL EJE Y FUNCIONA BIEN
    
    # get the current x and y limits
    cur_xlim = axes.get_xlim()
    cur_ylim = axes.get_ylim()
    cur_xrange = (cur_xlim[1] - cur_xlim[0])*.5
    cur_yrange = (cur_ylim[1] - cur_ylim[0])*.5
    print('lims ', cur_xlim[0], cur_xlim[1], cur_ylim[0], cur_ylim[1])
    xdata = event.xdata # get event x location
    ydata = event.ydata # get event y location
    if event.button == 'up':
        # deal with zoom in
        scale_factor = 1/2.
    elif event.button == 'down':
        # deal with zoom out
        scale_factor = 2.
    else:
        # deal with something that should never happen
        scale_factor = 1
    # set new limits
    axes.set_xlim([xdata - cur_xrange,
                xdata + cur_xrange])
    axes.set_ylim([ydata - cur_yrange,
                ydata + cur_yrange])
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
        self.plotContainer.add_widget(wid)
        print("ALLRIGHT")
        
    def showLoadFilePopup(self):
        LoadFilePopup(caller=self).open()

class WaveApp(App):
    
    title = 'Wave Analizer'
    
    def build(self):
        mainwidget = MainWidget()
        mainwidget.drawButton.bind(on_press=drawPlot)
        return mainwidget
    