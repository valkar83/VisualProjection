# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 20:08:34 2021

@author: valkar
"""
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty,ListProperty
from kivy.core.window import Window

class Cadreur(Widget):
    hauteurCadreur=NumericProperty(0)
    largeurCadreur=NumericProperty(0)
    centrex=NumericProperty(0)
    centrey=NumericProperty(0)
    r=NumericProperty(0)
    ##Pour la taille des boutons
    btLCercl=NumericProperty(10)
    btHCercl=NumericProperty(10)
    gris=ListProperty()
    marron=ListProperty()
    orange=ListProperty()
    def __init__(self, **kwargs):
        self.marron=[0.43,0.2,0,1]
        self.gris=[0.71,0.69,0.67,1]
        self.orange=[1,0.55,0,1]
        self.btLCercl=10
        self.btHCercl=10
        self.ratioH=0.75
        self.ratioW=0.8
        super().__init__(**kwargs)
        self.hauteurCadreur=Window.height*self.ratioH
      
        self.largeurCadreur=Window.width*self.ratioW
        self.differenceL=round((Window.width-self.largeurCadreur)/2,2)
        self.differenceH=round((Window.height-self.hauteurCadreur)/2,2)
        self.centrex=round(self.largeurCadreur/2,2)+self.differenceL
        self.centrey=round(self.hauteurCadreur/2,2)+self.differenceH*2

        self.r=round((1/4)*self.largeurCadreur,2)
        if self.r>self.hauteurCadreur:
            self.r=(self.hauteurCadreur-self.hauteurCadreur*0.1)/2
        Window.bind(on_resize=self.on_rechang)

        
    def on_rechang(self,centrex,centrey,r,*largs):
        self.hauteurCadreur=Window.height*self.ratioH
        self.largeurCadreur=Window.width*self.ratioW
        self.differenceL=round((Window.width-self.largeurCadreur)/2,2)
        self.centrex=round(self.largeurCadreur/2,2)+self.differenceL
        self.centrey=round(self.hauteurCadreur/2,2)+self.differenceH*2.2
        self.r=round((1/4)*self.largeurCadreur,2)
        if self.r>(self.hauteurCadreur/2):
            self.r=(self.hauteurCadreur-self.hauteurCadreur*0.1)/2
