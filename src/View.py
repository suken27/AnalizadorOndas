# _*_ coding: utf-8 _*_

from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.actionbar import ActionBar
from kivy.uix.boxlayout import BoxLayout

class MainView(BoxLayout):
    
    def __init__(self, **kwargs):
        super(MainView, self).__init__(**kwargs)
        self.add_widget(Builder.load_file("kivyFiles/actionBar.kv"))

class View(App):
    def build(self):
        return MainView()
    
View().run()