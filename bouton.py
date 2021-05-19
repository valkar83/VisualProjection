# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 19:58:37 2021

@author: valkar
"""
from kivy.properties import NumericProperty,ListProperty

from math import cos,sin,radians
from cadreur import Cadreur
    
def points_du_cercle(centrex,centrey,r,angle):
    xpos=round(centrex+r*cos(radians(angle)),2)
    ypos=round(centrey+r*sin(radians(angle)),2)
    return xpos,ypos

class Boutons_cercle(Cadreur):
    cordx=NumericProperty(0)
    cordy=NumericProperty(0)
    angle=NumericProperty(0)
    couleur=ListProperty([])
    def __init__(self,angle, **kwargs):
        super().__init__(**kwargs)
        #les coordonéees du cercle qui agence les widgets du cercle entre-eux
        self.angle=angle
        self.cordx=points_du_cercle(self.centrex, self.centrey, self.r, self.angle)[0]
        self.cordy=points_du_cercle(self.centrex, self.centrey, self.r, self.angle)[1]
        self.bind(r=self.on_chgt)
        
    def miseAjour(self,repx,repy):
        self.cordx=repx
        self.cordy=repy
        
    def on_touch_move(self,touch):
        if self.collide_point(*touch.pos):
            return True
        else:
            return False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            return True

        else:

            return False
    def on_chgt(self,centrex,centrey,**largs):
        self.cordx=points_du_cercle(self.centrex, self.centrey, self.r, self.angle)[0]
        self.cordy=points_du_cercle(self.centrex, self.centrey, self.r, self.angle)[1]
class Bouton_centre(Cadreur):
    cordx=NumericProperty(0)
    cordy=NumericProperty(0)
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.cordx=self.centrex
        self.cordy=self.centrey
        self.bind(r=self.on_chgt)
    def on_chgt(self,r,cordx,**kwargs):
        self.cordx=self.centrex
        self.cordy=self.centrey
class Boutons_angle(Cadreur):
    cordx=NumericProperty(0)
    cordy=NumericProperty(0)
    angle=NumericProperty(0)
    rayon=NumericProperty(0)
    couleur=ListProperty([])
    def __init__(self,angle,ratio,**kwargs):
        super().__init__(**kwargs)  
        self.ratio=ratio
        self.angle=angle
        self.rayon=self.r*self.ratio
        self.couleur=[1,0,0,0]
        self.cordx=points_du_cercle(self.centrex, self.centrey, self.rayon, self.angle)[0]
        self.cordy=points_du_cercle(self.centrex, self.centrey, self.rayon, self.angle)[1]
        self.bind(r=self.on_chgt)

    def on_chgt(self,centrex,centrey,**largs):
        self.rayon=self.r*self.ratio
        self.cordx=points_du_cercle(self.centrex, self.centrey, self.rayon, self.angle)[0]
        self.cordy=points_du_cercle(self.centrex, self.centrey, self.rayon, self.angle)[1]