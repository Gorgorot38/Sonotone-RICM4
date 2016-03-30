# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 11:13:49 2016

@author: manuel
"""

#! /usr/bin/env python3
# -*- coding: utf-8 -*-
 
from kivy.app import App
#kivy.require("1.8.0")
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.button import Button

class LoginScreen(GridLayout):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 10 #Nombre de colonne
        
        #Ligne 1
        Frequence = [32,64,124,220,440,880,1320,1760,2220,2640]
        for i in Frequence:
            self.add_widget(Label(text="{0}Hz".format(i)))
        
        # Ligne 2
        
        self.s1 = Slider(orientation='vertical',min=-10, max=10, value=0)
        self.add_widget(self.s1)
        self.s2 = Slider(orientation='vertical',min=-10, max=10, value=0)
        self.add_widget(self.s2)
        self.s3 = Slider(orientation='vertical',min=-10, max=10, value=0)
        self.add_widget(self.s3)
        self.s4 = Slider(orientation='vertical',min=-10, max=10, value=0)
        self.add_widget(self.s4)
        self.s5 = Slider(orientation='vertical',min=-10, max=10, value=0)
        self.add_widget(self.s5)
        self.s6 = Slider(orientation='vertical',min=-10, max=10, value=0)
        self.add_widget(self.s6)
        self.s7 = Slider(orientation='vertical',min=-10, max=10, value=0)
        self.add_widget(self.s7)
        self.s8 = Slider(orientation='vertical',min=-10, max=10, value=0)
        self.add_widget(self.s8)
        self.s9 = Slider(orientation='vertical',min=-10, max=10, value=0)
        self.add_widget(self.s9)
        self.s10 = Slider(orientation='vertical',min=-10, max=10, value=0)
        self.add_widget(self.s10)
        
        #Ligne 3
        def callback(instance):
            print('The button <%s> is being pressed' % instance.text)
        
        self.button = Button(text='LAUNCH', font_size=14)
        self.button.bind(on_press=callback)
        self.add_widget(self.button)
        
        for i in range(8):
            self.add_widget(Label(text=""))
        
        
      
        self.button = Button(text='EXIT', font_size=14)
        self.button.bind(on_press=callback)
        self.add_widget(self.button)
        
        #Ligne 4
#        
#        self.add_widget(Label(text=str(self.s1.value))
        # Ligne 3
#        def OnSliderValueChange(instance,value):
#            some_label.text = str(value)
#        self.add_widget(Label(text=self.s1.bind(self.s1.value))

#        self.label

#
#        my_slider.bind(value=OnSliderValueChange)
#        
#        self.add_widget(Label(text="Password:"))
#        self.password = TextInput(multiline=False, password=True)
#        self.add_widget(self.password)
#
#        self.add_widget(Label(text="Two Factor Auth:"))
#        self.tfa = TextInput(multiline=False)
#        self.add_widget(self.tfa)


class SimpleKivy(App):
    def build(self):
        ls = LoginScreen()
        return ls

if __name__ == "__main__":
    SimpleKivy().run()