# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 20:03:52 2021

@author: valkar
"""
from kivy.properties import NumericProperty,StringProperty,ListProperty,ObjectProperty,BooleanProperty
from cadreur import Cadreur
from math import sqrt,acos,asin,degrees
from bouton import points_du_cercle,Boutons_angle

def angle_cercle(ctrx,ctry,ptx,pty,r):
    thetaX=[]
    thetaY=[]
    theta=800

    thetaX.append(round(degrees(acos((ptx-ctrx)/r)),0))
    #Avec le cosinus, il y a une symétrie avec l'axe des abcisses
    #Combien de degrès avec 180°
    if thetaX[0]<0:
        thetaX[0]=360+thetaX[0]
    if thetaX[0]<180:
        diff=180-thetaX[0]
        thetaX.append(thetaX[0]+2*diff)
    else:
        diff=thetaX[0]-180
        thetaX.append(thetaX[0]-2*diff)
    thetaY.append(round(degrees(asin((pty-ctry)/r)),0))
    #Avec le sinus, il y a une symétrie avec l'axe des ordonnées
    #Combien de degrès avec 90°
    if thetaY[0]<0:
        thetaY[0]=360+thetaY[0]
    if thetaY[0]<180:
        if thetaY[0]<90:
            diff=90-thetaY[0]
            thetaY.append(thetaY[0]+2*diff)
        else:
            diff=thetaY[0]-90
            thetaY.append(thetaY[0]-2*diff)
    else:
        if thetaY[0]<270:
            diff=270-thetaY[0]
            thetaY.append(thetaY[0]+2*diff)
        else:
            diff=thetaY[0]-270
            thetaY.append(thetaY[0]-2*diff)

    for i in range(2):
        for j in range(2):

            if thetaX[i]==thetaY[j]:
                theta=thetaX[i]
                break
    if theta==800:
        print('ERREUR : angle non égalisé')
        theta='Nul'
    return theta
def longueur(centrex,centrey,ptx,pty):
    long=sqrt((ptx-centrex)**2+(pty-centrey)**2)
    return long


class Fleche(Cadreur):
    preCouleur=ListProperty([])
    fleCouleur=ListProperty([])
    ctr=ObjectProperty(None)
    ptRef=ObjectProperty(None)
    taille=NumericProperty(20.0)
    ptX1=NumericProperty(0)
    ptY1=NumericProperty(0)
    ptX2=NumericProperty(0)
    ptY2=NumericProperty(0)
    ctrX=NumericProperty(0)
    ctrY=NumericProperty(0)
    deviation=NumericProperty(50)
    aMaj=BooleanProperty(False)
    def __init__(self,centre,ptRef,taille,nomFleche,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.compteurAppel=0
        self.nomFleche=nomFleche
        self.ctr=centre
        self.ptRef=ptRef
        self.taille=taille
        self.fleCouleur=[0,1,0,0]
        #Compteur d'évément qui sera utilisé dans la fct on_chgt
        self.cpt_chgt=0
        self.rayonRef=longueur(self.ctr.cordx,self.ctr.cordy,
                                  self.ptRef.cordx,self.ptRef.cordy)

        self.angleRef=angle_cercle(self.ctr.cordx, self.ctr.cordy, self.ptRef.cordx,
                                   self.ptRef.cordy, self.rayonRef)

        #Maintenant, nous récupérons les 2 points espacés d'un angle de 30° (valeur arbitraire)

        #Pour le premier point
        self.deviPlus=self.angleRef+self.deviation
        self.ptX1=points_du_cercle(self.ctr.cordx,self.ctr.cordy,self.taille,self.deviPlus)[0]
        self.ptY1=points_du_cercle(self.ctr.cordx,self.ctr.cordy,self.taille,self.angleRef+self.deviation)[1]

        #Pour le point au centre
        self.ctrX=self.ctr.cordx
        self.ctrY=self.ctr.cordy

        #Pour le troisième point
        self.deviMoins=self.angleRef-self.deviation
        self.ptX2=points_du_cercle(self.ctr.cordx,self.ctr.cordy,self.taille,self.deviMoins)[0]
        self.ptY2=points_du_cercle(self.ctr.cordx,self.ctr.cordy,self.taille,self.deviMoins)[1]     

        
        
        if self.nomFleche =='Fleche Direct' or self.nomFleche=='Fleche Indirect E':


            pass
        else:
            self.ctr.bind(cordx=self.on_maj)
            self.ctr.bind(cordy=self.on_maj)
            self.ptRef.bind(cordx=self.on_maj)
            self.ptRef.bind(cordy=self.on_maj)
        self.bind(ptRef=self.on_chgt)
        self.bind(ctr=self.on_chgt)


        #A la changement de couleur
        self.bind(fleCouleur=self.on_couleur)
    def on_chgt(self,cordx,cordy):
        self.cpt_chgt+=1
        if ((self.nomFleche=='axeX') or (self.nomFleche=='axeY')):
            self.cpt_chgt=2
        if (self.cpt_chgt>=2) and ((self.ctr.cordx !=self.ptRef.cordx) or (self.nomFleche=='axeY')):
            self.cpt_chgt=0
            self.rayonRef=longueur(self.ctr.cordx,self.ctr.cordy,
                                      self.ptRef.cordx,self.ptRef.cordy)

            self.angleRef=angle_cercle(self.ctr.cordx, self.ctr.cordy, self.ptRef.cordx,
                                       self.ptRef.cordy, self.rayonRef)
    
            #Maintenant, nous récupérons les 2 points espacés d'un angle de 30° (valeur arbitraire)
            #Pour le premier point
            self.deviPlus=self.angleRef+self.deviation
            self.ptX1=points_du_cercle(self.ctr.cordx,self.ctr.cordy,self.taille,self.deviPlus)[0]
            self.ptY1=points_du_cercle(self.ctr.cordx,self.ctr.cordy,self.taille,self.angleRef+self.deviation)[1]
    
            #Pour le point au centre
            self.ctrX=self.ctr.cordx
            self.ctrY=self.ctr.cordy
    
            #Pour le troisième point
            self.deviMoins=self.angleRef-self.deviation
            self.ptX2=points_du_cercle(self.ctr.cordx,self.ctr.cordy,self.taille,self.deviMoins)[0]
            self.ptY2=points_du_cercle(self.ctr.cordx,self.ctr.cordy,self.taille,self.deviMoins)[1]        
            
    def on_maj(self,cordx,cordy,*largs):
    #C'est utilisé quand la fenêtre s'aggrandit



        if self.fleCouleur[3]==1:
            self.rayonRef=longueur(self.ctr.cordx,self.ctr.cordy,
                                  self.ptRef.cordx,self.ptRef.cordy)
            self.angleRef=angle_cercle(self.ctr.cordx, self.ctr.cordy, self.ptRef.cordx,
                                   self.ptRef.cordy, self.rayonRef)

            #Pour le premier point
            self.deviPlus=self.angleRef+self.deviation
            self.ptX1=points_du_cercle(self.ctr.cordx,self.ctr.cordy,self.taille,self.deviPlus)[0]
            self.ptY1=points_du_cercle(self.ctr.cordx,self.ctr.cordy,self.taille,self.angleRef+self.deviation)[1]
            #Pour le point au centre
            self.ctrX=self.ctr.cordx
            self.ctrY=self.ctr.cordy 
            #Pour le troisième point
            self.deviMoins=self.angleRef-self.deviation
            self.ptX2=points_du_cercle(self.ctr.cordx,self.ctr.cordy,self.taille,self.deviMoins)[0]
            self.ptY2=points_du_cercle(self.ctr.cordx,self.ctr.cordy,self.taille,self.deviMoins)[1]        
        
        if self.nomFleche=='axeX':
            self.aMaj=True
    def on_couleur(self,r,centrex,**kwargs):
        #Lorsqu'une flèche devient visible

        if self.fleCouleur[3]==1:
            self.rayonRef=longueur(self.ctr.cordx,self.ctr.cordy,
                                  self.ptRef.cordx,self.ptRef.cordy)
            self.angleRef=angle_cercle(self.ctr.cordx, self.ctr.cordy, self.ptRef.cordx,
                                   self.ptRef.cordy, self.rayonRef)
    
            #Pour le premier point
            self.deviPlus=self.angleRef+self.deviation
            self.ptX1=points_du_cercle(self.ctr.cordx,self.ctr.cordy,self.taille,self.deviPlus)[0]
            self.ptY1=points_du_cercle(self.ctr.cordx,self.ctr.cordy,self.taille,self.angleRef+self.deviation)[1]
            #Pour le point au centre
            self.ctrX=self.ctr.cordx
            self.ctrY=self.ctr.cordy
            #Pour le troisième point
            self.deviMoins=self.angleRef-self.deviation
            self.ptX2=points_du_cercle(self.ctr.cordx,self.ctr.cordy,self.taille,self.deviMoins)[0]
            self.ptY2=points_du_cercle(self.ctr.cordx,self.ctr.cordy,self.taille,self.deviMoins)[1]


class IndicSens(Cadreur):
    #C'est la classe qui gère tous les éléments de l'affichage du sens du cercle
    
    longueurBarre=NumericProperty(1.0)
    sens=StringProperty('')
    def __init__(self,sensOk,**kwargs):
        self.ctrIndiPlus=''
        self.ctrIndiMoins=''
        self.angleRefPlus=0
        self.angleRefMoins=0
        self.ptRefMoins=''
        self.ptRefPlus=''
        self.sens=sensOk
        super().__init__(**kwargs)
        self.ratio=1.4
        for i in range(10,90):
            if i>=50:
                j=i-40+0.5
            else:j=i
            self.nom=Boutons_angle(j, self.ratio)
            #Nous allons y associer une couleur verte
            self.nom.couleur=[0,1,0,1]
            self.add_widget(self.nom)
        self.j=0
#Le but ici est de tracer les 2 droites afin de former une flèche
        ##Pour déterminer le centre et le point de référence des 2 extrêmes
        for widget in self.walk():
            if isinstance(widget,Boutons_angle):
                if self.ctrIndiPlus=='' or self.ctrIndiMoins=='':
                    self.ctrIndiPlus=widget
                    self.ctrIndiMoins=widget
                if self.j==1:
                    self.ptRefMoins=widget
                if widget.angle>self.ctrIndiPlus.angle:
                    self.ptRefPlus=self.ctrIndiPlus
                    self.ctrIndiPlus=widget
                if widget.angle<self.ctrIndiMoins.angle:
                    self.ctrIndiMoins=widget
                self.j+=1
        self.flecheTrigo=Fleche(self.ctrIndiPlus,self.ptRefPlus,20.0,'trigoSens')
        self.add_widget(self.flecheTrigo)

        self.flecheHoraire=Fleche(self.ctrIndiMoins,self.ptRefMoins,20.0,'horaireSens')
        self.add_widget(self.flecheHoraire)
        if self.sens=='Direct':
            self.flecheTrigo.fleCouleur[3]=1
            
        else:
            self.flecheHoraire.fleCouleur[3]=1

        self.bind(sens=self.on_alerte)
        #On va créer l'objet cercle sens
        self.crclIndicSens=cercl_sens(self.sens)
        self.add_widget(self.crclIndicSens)
    def on_alerte(self,bx,by,**kwargs):
        if self.sens=='Direct':
            self.flecheTrigo.fleCouleur[3]=1
            self.flecheHoraire.fleCouleur[3]=0
            self.crclIndicSens.couleurAxe[3]=0
            self.crclIndicSens.couleurPoint[3]=1
            self.crclIndicSens.nom='Sens trigonomètrique'
        else:
            self.flecheTrigo.fleCouleur[3]=0
            self.flecheHoraire.fleCouleur[3]=1
            self.crclIndicSens.couleurAxe[3]=1
            self.crclIndicSens.couleurPoint[3]=0
            self.crclIndicSens.nom='Sens horaire'

class cercl_sens(Cadreur):
    ctrIndicX=NumericProperty(0)
    ctrIndicY=NumericProperty(0)
    rIndicSens=NumericProperty(0)
    x60=NumericProperty(0)
    y60=NumericProperty(0)
    x120=NumericProperty(0)
    y120=NumericProperty(0)
    x240=NumericProperty(0)
    y240=NumericProperty(0)
    x300=NumericProperty(0)
    y300=NumericProperty(0)
    couleurAxe=ListProperty([0,1,0,0])
    couleurPoint=ListProperty([0,1,0,1])
    nom=StringProperty('')
    def __init__(self,sensOk,**kwargs):
        super().__init__(**kwargs)
        self.sens=sensOk
        if self.sens=='Direct':
        #On va calculer le centre du cercle d'information de IndicSens
            self.rIndic=self.r*1.4+((0.2*self.r)*1.4*1.1)
            self.rIndicSens=0.2*self.r
            self.ctrIndicX,self.ctrIndicY=points_du_cercle(self.centrex,self.centrey,self.rIndic,30)
            self.x60,self.y60=points_du_cercle(self.ctrIndicX,self.ctrIndicY,self.rIndicSens,30)
            self.x120,self.y120=points_du_cercle(self.ctrIndicX,self.ctrIndicY,self.rIndicSens,120)
            self.x240,self.y240=points_du_cercle(self.ctrIndicX,self.ctrIndicY,self.rIndicSens,210)
            self.x300,self.y300=points_du_cercle(self.ctrIndicX,self.ctrIndicY,self.rIndicSens,300)
            self.nom='Sens Trigonométrique'
        self.bind(r=self.on_position)
        
    def on_position(self,*largs):
        self.rIndic=self.r*1.4+((0.2*self.r)*1.4*1.1)
        self.rIndicSens=0.2*self.r
        self.ctrIndicX,self.ctrIndicY=points_du_cercle(self.centrex,self.centrey,self.rIndic,30)
        self.x60,self.y60=points_du_cercle(self.ctrIndicX,self.ctrIndicY,self.rIndicSens,30)
        self.x120,self.y120=points_du_cercle(self.ctrIndicX,self.ctrIndicY,self.rIndicSens,120)
        self.x240,self.y240=points_du_cercle(self.ctrIndicX,self.ctrIndicY,self.rIndicSens,210)
        self.x300,self.y300=points_du_cercle(self.ctrIndicX,self.ctrIndicY,self.rIndicSens,300)