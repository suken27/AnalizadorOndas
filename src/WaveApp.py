# _*_ coding: utf-8 _*_

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

def drawPlot(instance):
    print("TODO")
    
class LoadFilePopup(Popup):
    pass

class MainWidget(BoxLayout):
    
    loadFileButton = ObjectProperty(0)
    
    plotContainer = ObjectProperty(0)
    drawButton = ObjectProperty(0)
    
    def loadFile(self, file):
        print("FILE LOAD")
        
    def showLoadFilePopup(self):
        LoadFilePopup().open()

class WaveApp(App):
    
    title = 'Wave Analizer'
    
    def build(self):
        mainwidget = MainWidget()
        mainwidget.drawButton.bind(on_press=drawPlot)
        return mainwidget