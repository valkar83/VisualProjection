from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors import ToggleButtonBehavior,ButtonBehavior
from kivy.properties import NumericProperty,StringProperty,BooleanProperty,ListProperty,ObjectProperty
from kivy.core.window import Window
from kivy.weakproxy import WeakProxy
from random import randint

from math import cos,sin,sqrt,radians,acos,asin,degrees
###########################   FONCTIONS    ###################################
def calcul_angle(angleDeProjection,complementaire,exterieur,nomAxe,angleAxe,angleciAxe):
    if angleDeProjection=='alpha':
        if complementaire==False:
            if exterieur:
                #AngleAxe correspond à l'angle xMoins et xPlus
                return angleciAxe-angleAxe
            #Dans le cas des angles intérieures
            else:
                if nomAxe=='yPlus':
                    return angleciAxe-angleAxe
                else:
                    #Condition
                    if angleciAxe==0:
                       return -angleAxe
                    else:
                       return angleciAxe-angleAxe
    ##Si l'angle de projection est béta
    else:
        if complementaire==False:
            if exterieur:
                #AngleAxe correspond à l'angle yMoins et yPlus
                return angleciAxe-angleAxe
            else:
                if nomAxe=='xPlus':
                    return angleciAxe-angleAxe
                else:
                    #Ici on cible Yplus
                    if angleciAxe==90:
                        
                        return angleciAxe-abs(angleAxe)
                    else:
                        return angleciAxe-angleAxe
            
def transform_en_alpha(angleATrans):
    #Quand béta est compris entre 270 et 359
    if (angleATrans>=270) and (angleATrans<360):
        alfa=angleATrans-270
        return alfa
    else:
        alfa=angleATrans+90
        return alfa
def transform_en_beta(angleATrans):
    #Quand alpha est compris entre 90 et 360 non inclus
    if (angleATrans>=90) and (angleATrans<360):
        betaRef=angleATrans-90
        return betaRef
    else:
        betaRef=angleATrans+270
        return betaRef
def transform_neg_alpha(angleTrans):
    if (angleTrans<=180) and (angleTrans>90):
        alphaRef=angleTrans-270
        return alphaRef
    #Fonction qui définit les points du cercle        
    else:
        alphaRef=angleTrans+90
        return alphaRef
            
def transform_neg_beta(angleTrans):
    if (angleTrans>-180) and (angleTrans<=-90):
        betaRef=270+angleTrans
        return betaRef
    #Fonction qui définit les points du cercle        
    else:
        betaRef=angleTrans-90
        return betaRef
        
    
def points_du_cercle(centrex,centrey,r,angle):
    xpos=round(centrex+r*cos(radians(angle)),2)
    ypos=round(centrey+r*sin(radians(angle)),2)
    return xpos,ypos

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
    
def points_cardinaux(centrex,centrey,r,angle):
    xpos=round(centrex+r*cos(radians(angle)),2)
    ypos=round(centrey+r*sin(radians(angle)),2)
    #La coordonnée y de xPlus se confond avec la coordonnée y du centre
    #Si x position est supérieure à centre x, alors x Plus, 
    #Le même raisonnement est tenu pour les autres conditions
    if ((centrey*0.99<ypos)and(ypos<centrey*1.01)) and xpos>centrex:
        if ((angle>= 358.5) and (angle <= 360)) or  ((angle >=0) and (angle <= 1.5)):
            angle=0
        return True,"xPlus",xpos,ypos,angle
    elif ypos>centrey and ((xpos<1.01*centrex) and (xpos>0.99*centrex)):
        if angle <= 91.5 and angle >= 88.5:
            angle=90
        return True,"yPlus",xpos,ypos,angle
    elif ((centrey*0.99<ypos)and(ypos<centrey*1.01)) and xpos<centrex:
        if angle <= 181.5 and angle >= 178.5:
            angle=180
        return True,"xMoins",xpos,ypos,angle
    elif ypos<centrey and ((xpos<1.01*centrex) and (xpos>0.99*centrex)):
        if angle <= 271.5 and angle >= 268.5:
            angle=270
        return True,"yMoins",xpos,ypos,angle
    else:
        return False,""
    
def longueur(centrex,centrey,ptx,pty):
    long=sqrt((ptx-centrex)**2+(pty-centrey)**2)
    return long

def determineur(nomAngle,angleActiv,Direct,angle1,angleE=0,angleI=0):
   
    if nomAngle=='alpha':

        lettreAngle='α'
    else:
        lettreAngle='ß'
        #En ce qui concerne la projection directe
        #Si l'angle est positif
    if Direct:
        if angle1>0:
            signeDirec=' + '
            chiffreDirec='cos('+str(angle1)+')'
            signeLiteralDirec=' + '
            literalDirec='cos('+lettreAngle+')'
   
        else:
            signeDirec=' + '
            chiffreDirec='cos('+str(angle1)+')'
            signeLiteralDirec=' + '
            literalDirec='cos('+lettreAngle+')'
        #Pour la projection sur x : cos(afficheDirec)x
        #Si l'angle est supérieur est à 180°
        #Si l'angle supplémentaire est activé
        if angleActiv:
            if abs(angle1)>180:
                #Supérieur à 180° et positif
                if angle1>0:
                    signeLiteralDirecEq=' + '
                    literalDirecEq='cos(δ + π)'
                    signeLiteralDirecEqEq=' - '
                    literalDirecEqEq='cos(δ)'
                #supérieur à 180° (abs) et négatif
                else:
                    signeLiteralDirecEq=' + '
                    literalDirecEq='cos(-δ-π)'
                    signeLiteralDirecEqEq=' - '
                    literalDirecEqEq='-cos(δ)'
            else:
                #inférieur à 180° et positif
                if angle1>0:
                    signeLiteralDirecEq=' + '
                    literalDirecEq='cos('+lettreAngle+')'
                    signeLiteralDirecEqEq=' + '
                    literalDirecEqEq='cos('+lettreAngle+')'
                #inférieur à 180° (abs) et négatif
                else:
                    signeLiteralDirecEq=' + '
                    literalDirecEq='cos(-'+lettreAngle+')'
                    signeLiteralDirecEqEq=' + '
                    literalDirecEqEq='cos('+lettreAngle+')'
        #Si l'angle supplémentaire n'est pas activé
        else:
            if angle1>0:
                signeLiteralDirecEq=' + '
                literalDirecEq='cos('+lettreAngle+')'
                signeLiteralDirecEqEq=' + '
                literalDirecEqEq='cos('+lettreAngle+')'
            else:
                signeLiteralDirecEq=' + '
                literalDirecEq='cos(-'+lettreAngle+')'
                signeLiteralDirecEqEq=' + '
                literalDirecEqEq='cos('+lettreAngle+')'
        return signeDirec,chiffreDirec,signeLiteralDirec,literalDirec,signeLiteralDirecEq,literalDirecEq,signeLiteralDirecEqEq,literalDirecEqEq
    #si c'est indirect
    else:

        if (round(cos(radians(angle1)),2)==-round(sin(radians(abs(angleE))),2)):
            #L'angle est positif
            if angleE>=0:
                if angleI==90:
                    signeIndirec='+'
                    chiffreIndirec='cos('+str(angle1)+')'
                    signeLiteral='+'
                    literalIndirec='cos('+lettreAngle+'+π/2)'
                    signeLiteralEq='-'
                    literalIndirecEq='sin('+lettreAngle+')'
                #forcément -270
                elif angleI==-270:
                    signeIndirec='+'
                    chiffreIndirec='cos('+str(angle1)+')'
                    signeLiteral='+'
                    literalIndirec='cos('+lettreAngle+'-3π/2)'
                    signeLiteralEq='-'
                    literalIndirecEq='sin('+lettreAngle+')'
                else:
                    if angleE==0:
                            
                        if angleI==-90:
                            signeIndirec='+'
                            chiffreIndirec='cos('+str(angle1)+')'
                            signeLiteral='+'
                            literalIndirec='cos(-π/2)'
                            signeLiteralEq='+'
                            literalIndirecEq='0'
                    elif angleE==180:
                        if angleI==-90:
                            signeIndirec='+'
                            chiffreIndirec='cos('+str(angle1)+')'
                            signeLiteral='+'
                            literalIndirec='cos(π/2)'
                            signeLiteralEq='+'
                            literalIndirecEq='0'
                    else:
                        print(angle1)
                        print(angleE)
                        print(angleI)
                        print('bizarre1')
            #L'angle E est négatif
            else:

                if angleI==-90:
                    signeIndirec='+'
                    chiffreIndirec='cos('+str(angle1)+')'
                    signeLiteral='+'
                    literalIndirec='cos(-'+lettreAngle+'-π/2)'
                    signeLiteralEq='-'
                    literalIndirecEq='sin('+lettreAngle+')'
                    
                #forcément +270
                elif angleI==270:
                    signeIndirec='+'
                    chiffreIndirec='cos('+str(angle1)+')'
                    signeLiteral='+'
                    literalIndirec='cos('+lettreAngle+'+3π/2)'
                    signeLiteralEq='-'
                    literalIndirecEq='sin('+lettreAngle+')'
                
                else:
                    if angleE==-180:
                        
                        if angleI==90:
                            signeIndirec='+'

                            chiffreIndirec='cos('+str(angle1)+')'
                            signeLiteral='+'
                            literalIndirec='cos(-π/2)'
                            signeLiteralEq='+'
                            literalIndirecEq='0'
                        else:
                            print(angle1)
                            print(angleE)
                            print(angleI)
                            print('bizarre21')
                    else:
                        
                        print(angle1)
                        print(angleE)
                        print(angleI)
                        print('bizarre2')
        else:
            #L'angle est positif
            if angleE>=0:
                if angleI==-90:
                    signeIndirec='+'
                    chiffreIndirec='cos('+str(angle1)+')'
                    signeLiteral='+'
                    literalIndirec='cos('+lettreAngle+'-π/2)'
                    signeLiteralEq='+'
                    literalIndirecEq='sin('+lettreAngle+')'
                #forcément +270
                elif angleI==270:
                    signeIndirec='+'
                    chiffreIndirec='cos('+str(angle1)+')'
                    signeLiteral='+'
                    literalIndirec='cos('+lettreAngle+'+3π/2)'
                    signeLiteralEq='+'
                    literalIndirecEq='sin('+lettreAngle+')'
                else:
                    print(angle1)
                    print(angleE)
                    print(angleI)
                    print('bizarre3')
            #L'angle E est négatif
            else:
                if angleI==90:
                    signeIndirec='+'
                    chiffreIndirec='cos('+str(angle1)+')'
                    signeLiteral='+'
                    literalIndirec='cos(-'+lettreAngle+'+π/2)'
                    signeLiteralEq='+'
                    literalIndirecEq='sin('+lettreAngle+')'
                #forcément -270
                elif angleI ==-270:
                    signeIndirec='+'
                    chiffreIndirec='cos('+str(angle1)+')'
                    signeLiteral='+'
                    literalIndirec='cos(-'+lettreAngle+' -3π/2)'
                    signeLiteralEq='+'
                    literalIndirecEq='sin('+lettreAngle+')'
                else:
                    print(angle1)
                    print(angleE)
                    print(angleI)
                    print('bizarre4')
        return signeIndirec,chiffreIndirec,signeLiteral,literalIndirec,signeLiteralEq,literalIndirecEq
                
def directionneur(angleProjection,nomAxe,angleCible,ratioAngle,listeAngle,nomFleche):
    #Fonction utilisée pour gérer le sens des flèches

    if nomAxe=='xPlus' or nomAxe=='yPlus':
        ###############################################################
        ##############################"Pour la flèche, 
        if angleCible==0:
            j=359
            centre=listeAngle[str(angleCible),str(ratioAngle)][0]
            ptRef=listeAngle[str(j),str(ratioAngle)][0]
            #fleche sens trigo
            nomFleche.ctr=centre
            nomFleche.ptRef=ptRef
        else:                    
            j=angleCible-1
            centre=listeAngle[str(angleCible),str(ratioAngle)][0]
            ptRef=listeAngle[str(j),str(ratioAngle)][0]
            #fleche sens trigo
            nomFleche.ctr=centre
            nomFleche.ptRef=ptRef
    if nomAxe=='xMoins' or nomAxe=='yMoins':
        if angleCible==180:
            j=179
            centre=listeAngle[str(angleCible),str(ratioAngle)][0]
            ptRef=listeAngle[str(j),str(ratioAngle)][0]
            #fleche sens trigo
            nomFleche.ctr=centre
            nomFleche.ptRef=ptRef

        else:                    
            j=angleCible+1
            centre=listeAngle[str(angleCible),str(ratioAngle)][0]
            ptRef=listeAngle[str(j),str(ratioAngle)][0]
            #fleche sens trigo
            nomFleche.ctr=centre
            nomFleche.ptRef=ptRef

#####################                         ################################
#Créer les Widget
class Cadreur(Widget):
    hauteurCadreur=NumericProperty(0)
    largeurCadreur=NumericProperty(0)
    centrex=NumericProperty(0)
    centrey=NumericProperty(0)
    r=NumericProperty(0)
    def __init__(self, **kwargs):
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
        self.centrey=round(self.hauteurCadreur/2,2)+self.differenceH*2

        self.r=round((1/4)*self.largeurCadreur,2)
        if self.r>(self.hauteurCadreur/2):
            self.r=(self.hauteurCadreur-self.hauteurCadreur*0.1)/2

class Barres(Cadreur):
    
    ctrPtxVirtuel=NumericProperty(0)
    ctrPtyVirtuel=NumericProperty(0)
    chaine=StringProperty('')
    #angle
    angleAxe=NumericProperty(0)
    #points cardinaux
    ptPlusx=NumericProperty(0)
    ptxVirtuel=NumericProperty(0)
    ptPlusy=NumericProperty(0)
    ptyVirtuel=NumericProperty(0)
    ptMoinsx=NumericProperty( 0)
    ptMoinsy=NumericProperty(0)
    #pour la hauteur et largeur du Widget
    hauteurWidget=NumericProperty(0)
    largeurWidget=NumericProperty(0)
    ptsSpeciaux={}
    #pour la largeur du canva du widget
    largeurCanva=NumericProperty(1)
    etatActuel=StringProperty('')
    etatChange=StringProperty('')
    ##Couleur
    couleur=ListProperty([])
    
    def __init__(self,interact,chaine,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.interact=interact
        self.ctrPtxVirtuel=self.centrex
        self.ctrPtyVirtuel=self.centrey
        self.interact=interact
        self.chaine=chaine
        self.interact=interact
        self.largeurCanva=5.0
        self.couleur=[0,0,0,1]
        #Appel de la méthode quand la fenêtre est redimensionné
        self.bind(r=self.on_chgt)
        for i in range(0,360):
            d=points_cardinaux(self.centrex, self.centrey, self.r, i)
            if d[0]:
                self.ptsSpeciaux[d[1]]=[d[2],d[3],d[4]]

        if interact:
            if chaine=='xBar':
                self.etatActuel="xPlus"
                self.etatChange="xMoins"
                self.ptPlusx=self.ptsSpeciaux[self.etatActuel][0]
                self.ptPlusy=self.ptsSpeciaux[self.etatActuel][1]
                self.angleAxe=self.ptsSpeciaux[self.etatActuel][2]
                self.ptxVirtuel=self.ptPlusx
                self.ptyVirtuel=self.ptPlusy
                self.hauteurWidget=self.largeurCanva*2
                self.largeurWidget=longueur(self.centrex, self.centrey,
                                            self.ptPlusx,self.ptPlusy)
            else:
                self.etatActuel='yPlus'
                self.etatChange='yMoins'
                self.largeurWidget=self.largeurCanva
                self.ptPlusx=self.ptsSpeciaux[self.etatActuel][0]
                self.ptPlusy=self.ptsSpeciaux[self.etatActuel][1]
                self.angleAxe=self.ptsSpeciaux[self.etatActuel][2]
                self.ptxVirtuel=self.ptPlusx
                self.ptyVirtuel=self.ptPlusy
                self.hauteurWidget=longueur(self.centrex, self.centrey,
                                            self.ptPlusx,self.ptPlusy)
        else:
            self.ptxVirtuel=0
            self.ptyVirtuel=0
        
    def on_touch_down(self, touch):
        if self.interact:
            if self.collide_point(*touch.pos):
                if self.chaine=='xBar':
                    self.ptPlusx=self.ptsSpeciaux[self.etatChange][0]
                    self.ptPlusy=self.ptsSpeciaux[self.etatChange][1]

                    if self.etatChange=='xMoins':
                        self.ctrPtxVirtuel=self.ptPlusx
                        self.ctrPtyVirtuel=self.ptPlusy
                        self.ptxVirtuel=self.centrex
                        self.ptyVirtuel=self.centrey
                    else:
                        self.ctrPtxVirtuel=self.centrex
                        self.ctrPtyVirtuel=self.centrey
                        self.ptxVirtuel=self.ptPlusx
                        self.ptyVirtuel=self.ptPlusy
                        
                    self.tamponEtat=self.etatActuel
                    self.etatActuel=self.etatChange
                    self.etatChange=self.tamponEtat
                    self.angleAxe=self.ptsSpeciaux[self.etatActuel][2]

                    return True
                else:
                    self.ptPlusx=self.ptsSpeciaux[self.etatChange][0]
                    self.ptPlusy=self.ptsSpeciaux[self.etatChange][1]
                    if self.etatChange=='yMoins':
                        self.ctrPtxVirtuel=self.ptPlusx
                        self.ctrPtyVirtuel=self.ptPlusy
                        self.ptxVirtuel=self.centrex
                        self.ptyVirtuel=self.centrey
                    else:
                        self.ctrPtxVirtuel=self.centrex
                        self.ctrPtyVirtuel=self.centrey
                        self.ptxVirtuel=self.ptPlusx
                        self.ptyVirtuel=self.ptPlusy
                        
                    self.tamponEtat=self.etatActuel
                    self.etatActuel=self.etatChange
                    self.etatChange=self.tamponEtat
                    self.angleAxe=self.ptsSpeciaux[self.etatActuel][2]

                    return True
                    
            else:
                return False
    ## On MAJ le centre, le rayon, les pts speciaux
    #ainsi que la hauteur et la largeur du widget considéré
    def on_chgt(self,centrex,centrey):
    
        for i in range(0,360):
            d=points_cardinaux(self.centrex, self.centrey, self.r, i)
            if d[0]:
                self.ptsSpeciaux[d[1]]=[d[2],d[3],d[4]]

        #Modification pour bx et by
        if self.interact:
            if self.chaine=='xBar':
                self.ptPlusx=self.ptsSpeciaux[self.etatActuel][0]
                self.ptPlusy=self.ptsSpeciaux[self.etatActuel][1]
                self.largeurWidget=longueur(self.centrex, self.centrex,
                                            self.ptPlusx,self.ptPlusy)
                if self.etatActuel=='xMoins':
                    self.ctrPtxVirtuel=self.ptPlusx
                    self.ctrPtyVirtuel=self.ptPlusy
                    self.ptxVirtuel=self.centrex
                    self.ptyVirtuel=self.centrey
                else:
                    self.ctrPtxVirtuel=self.centrex
                    self.ctrPtyVirtuel=self.centrey
                    self.ptxVirtuel=self.ptPlusx
                    self.ptyVirtuel=self.ptPlusy
                    
            else:
                self.ptPlusx=self.ptsSpeciaux[self.etatActuel][0]
                self.ptPlusy=self.ptsSpeciaux[self.etatActuel][1]
                self.hauteurWidget=longueur(self.centrex, self.centrey,
                                            self.ptPlusx,self.ptPlusy)
                if self.etatActuel=='yMoins':
                    self.ctrPtxVirtuel=self.ptPlusx
                    self.ctrPtyVirtuel=self.ptPlusy
                    self.ptxVirtuel=self.centrex
                    self.ptyVirtuel=self.centrey
                else:
                    self.ctrPtxVirtuel=self.centrex
                    self.ctrPtyVirtuel=self.centrey
                    self.ptxVirtuel=self.ptPlusx
                    self.ptyVirtuel=self.ptPlusy
       
        else:
            self.ctrPtxVirtuel=self.centrex
            self.ctrPtyVirtuel=self.centrey
        
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
    def __init__(self,centre,ptRef,taille,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.compteurAppel=0
        self.nomFleche=''
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
        
        self.bind(ptRef=self.on_chgt)
        self.bind(ctr=self.on_chgt)
        self.ctr.bind(cordx=self.on_maj)
        self.ctr.bind(cordy=self.on_maj)
        self.ptRef.bind(cordx=self.on_maj)
        self.ptRef.bind(cordy=self.on_maj)
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
            
    #Pour modifier la position des flèches -> réagir au touché de l'utilisateur
    def on_maj(self,cordx,cordy):
        self.compteurAppel+=1
        #Prendre en compte un cas particulier, celui des flèches des axes
        if (self.compteurAppel>=4) and (self.fleCouleur[3]==1):

            self.compteurAppel=0
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
    #Lorsqu'une flèche devient visible
    def on_couleur(self,r,centrex,**kwargs):
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
        else:
            pass

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

class Choix_angle(ToggleButton):
    angle=StringProperty('')
    etat=StringProperty('down')
    hauteur=NumericProperty(0)
    largeur=NumericProperty(0)
    def __init__(self,angle,ratioHauteur,ratioLargeur, **kwargs):
        super().__init__(**kwargs)
        self.angle=angle
        self.ratioHauteur=ratioHauteur
        self.ratioLargeur=ratioLargeur

        if self.angle=='α':
            self.state='down'
        else:
            self.state='normal'
    
        self.hauteur=Window.height*ratioHauteur
        self.largeur=Window.width*ratioLargeur

        Window.bind(on_resize=self.on_relocal)
        
    def on_relocal(self,ratioHauteur,ratioLargeur,essai,**kwargs):
        self.hauteur=Window.height*self.ratioHauteur
        self.largeur=Window.width*self.ratioLargeur

class Assembleur(Cadreur):
    
##On déféinit les coordonnées qui seront 'envoyées' à bUtilisateur
    ex=NumericProperty(0)
    ey=NumericProperty(0)
    #ex et ey sont les 2 points de coordonnées de la barre utilisateur
    sens=StringProperty('')
    directProjec=NumericProperty(0)
    indirectIntProjec=NumericProperty(0)
    indirectExtProjec=NumericProperty(0)
    angleProjection=StringProperty('')
    angleSup=BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.marron=[0.43,0.2,0,1]
        self.gris=[0.71,0.69,0.67,1]
        self.orange=[1,0.55,0,1]
        
        #On récupère un nombre aléatoirement pour initialier la barre utilisateur
        self.alea=265
        self.chaine="b"
        # On ajoute les barres x et y notamment
        self.bx=Barres(True,'xBar')
        self.by=Barres(True,'yBar')
        self.bx.couleur=self.gris
        self.by.couleur=self.gris
        self.bUtilisateur=Barres(False,'Utilisateur')
        self.bUtilisateur.couleur=self.orange
        self.add_widget(self.bx)
        self.add_widget(self.by)
        # self.add_widget(self.flecheBarreY)
        self.add_widget(self.bUtilisateur)
        #Ici on a lié de façon permenante les propriétés ex,ey à ceux de l'instance barre utilisateur
        self.bind(ex=self.bUtilisateur.setter('ptxVirtuel'))
        self.bind(ey=self.bUtilisateur.setter('ptyVirtuel'))
        ##p, déterminer les coordonnées de chaque bouton ainsi que les
        #points spéciaux
        for i in range(0,360):
            self.chaine="b"+str(i)
            self.chaine=Boutons_cercle(i)
            if i==0:
                self.bxPlus=self.chaine
            elif i==90:
                self.byPlus=self.chaine
            elif i==180:
                self.bxMoins=self.chaine
            elif i==270:
                self.byMoins=self.chaine
            self.add_widget(self.chaine)
            self.chaine.couleur=self.marron
            #pour initialiser le placement
            if self.alea==i:
                self.cible=self.chaine
                
                self.ex=self.chaine.cordx
                self.ey=self.chaine.cordy
        self.boutonCentre=Bouton_centre()

        self.flecheBarreX=Fleche(self.bxPlus,self.boutonCentre,20.0)
        self.flecheBarreX.fleCouleur=self.gris
        self.flecheBarreX.nomFleche='axeX'
        self.add_widget(self.flecheBarreX)
        #On associe la flèche à by
        self.flecheBarreY=Fleche(self.byPlus,self.boutonCentre,20.0)
        self.flecheBarreY.fleCouleur=self.gris
        self.flecheBarreY.nomFleche='axeY'
        self.add_widget(self.flecheBarreY)
        ############################################################################
        ##Nous allons maintenant déclarer la première projection
        ##On s'occupe des propriétés qui seront utilisées par les classes de Projection
        self.axeX=self.bx.etatActuel
        self.angleAxeX=self.bx.ptsSpeciaux[self.bx.etatActuel][2]
        self.axeY=self.by.etatActuel
        self.angleAxeY=self.by.ptsSpeciaux[self.by.etatActuel][2]
        self.alpha=True
        self.beta=False
        if self.axeX[1:]==self.axeY[1:]:
            self.sens='Direct'
        else:
            self.sens='Indirect'   
        self.bind(r=self.on_chgt)
        self.angleProjection='alpha'
        self.pjx=ProjectionDirect('xPlus','alpha',self.bx.etatActuel,self.bx.angleAxe,
                                  self.by.etatActuel,self.by.angleAxe,self.cible.angle)
        self.pjx=WeakProxy(self.pjx)
        self.add_widget(self.pjx)
        #Le sens du repère        
        self.pjy=ProjectionIndirect('yPlus','alpha',self.bx.etatActuel,self.bx.angleAxe,
                                  self.by.etatActuel,self.by.angleAxe,self.cible.angle)
        self.pjy=WeakProxy(self.pjy)
        self.add_widget(self.pjy)
        #Le sens du repère
        self.bx.bind(etatActuel=self.pjx.setter('axeX'))
        self.by.bind(etatActuel=self.pjx.setter('axeY'))
        self.bx.bind(angleAxe=self.pjx.setter('angleAxeX'))
        self.by.bind(angleAxe=self.pjx.setter('angleAxeY'))
        
        self.bx.bind(etatActuel=self.pjy.setter('axeX'))
        self.by.bind(etatActuel=self.pjy.setter('axeY'))
        self.bx.bind(angleAxe=self.pjy.setter('angleAxeX'))
        self.by.bind(angleAxe=self.pjy.setter('angleAxeY'))
        
        ##Nous récupérons et lions les angles produits par pjx et pjy
        self.directProjec=self.pjx.angleMesure
        self.indirectExtProjec=self.pjy.angleMesureE
        self.indirectIntProjec=self.pjy.angleMesureI
        #Les projections renvoient leurs valeurs
        self.pjx.bind(angleMesure=self.setter('directProjec'))
        self.pjy.bind(angleMesureE=self.setter('indirectExtProjec'))
        self.pjy.bind(angleMesureI=self.setter('indirectIntProjec'))

        #on va relier le changement d'état actuel à une fonction interne
        #le but de cette manoeuvre est de déterminer le sens des axes
        self.bx.bind(etatActuel=self.on_sens)
        self.by.bind(etatActuel=self.on_sens)
        
        #Ici nous créons la classe qui représente graphiquement le sens
        self.indication=IndicSens(self.sens)
        self.add_widget(self.indication)
        #on lie la propriété de sens Assembleur à la propriété sens IndicSens
        self.bind(sens=self.indication.setter('sens'))

        self.btd=Choix_angle('δ',10/100,90/100)
        ##On crééer les boutons pour le choix des angles
        self.bta=Choix_angle('α',5/100,70/100)
        self.btb=Choix_angle('ß',5/100,80/100)
        
        self.add_widget(self.bta)
        self.add_widget(self.btb)
        self.add_widget(self.btd)
        self.bta.bind(state=self.on_angle)
        self.btb.bind(state=self.on_angle)

    def on_sens(self,bx,by):
        self.axeX=self.bx.etatActuel
        self.axeY=self.by.etatActuel
        if self.axeX=='xPlus':
            self.flecheBarreX.ctr=self.bxPlus
        else:
            self.flecheBarreX.ctr=self.bxMoins
        if self.axeY=='yPlus':
            self.flecheBarreY.ctr=self.byPlus
        else:
            self.flecheBarreY.ctr=self.byMoins
            
        if self.axeX[1:]==self.axeY[1:]:
            self.sens='Direct'
        else:
            self.sens='Indirect'
    def on_touch_down(self,touch):
        for widget in self.walk():
            if isinstance(widget,Boutons_cercle):
                if widget.on_touch_down(touch):
                    #On retient l'angle précédent
                    self.pjx.anglePre=self.cible.angle
                    self.pjy.anglePre=self.cible.angle
                    self.cible=widget
                    self.pjx.angleCible=widget.angle
                    self.pjy.angleCible=widget.angle
                    self.ex=self.cible.cordx
                    self.ey=self.cible.cordy
                    return True

            elif isinstance(widget,Barres):
                if widget.on_touch_down(touch):
                    self.bx.on_touch_down(touch)
                    self.by.on_touch_down(touch)
                    return True
        else:
            self.bta.dispatch('on_touch_down',touch)
            self.btb.dispatch('on_touch_down',touch)
            return False

     #pour la barre Utilisateur quand le doigt de l'utilisateur ne lève pas
    def on_touch_move(self,touch):
        for widget in self.walk():
            if isinstance(widget,Boutons_cercle):
                if widget.on_touch_move(touch):
                    #On récupère l'angle précédent
                    self.pjx.anglePre=self.cible.angle
                    self.pjy.anglePre=self.cible.angle                
                    self.cible=widget
                    self.pjx.angleCible=widget.angle
                    self.pjy.angleCible=widget.angle
                    self.ex=widget.cordx
                    self.ey=widget.cordy
                    return True
        else:
            return False
     #pour mettre à jour la longueur de la barre utilisateur quand la fenêtre s'aggrandit
    def on_chgt(self,*largs):
        self.ex=points_du_cercle(self.centrex, self.centrey, self.r, self.cible.angle)[0]
        self.ey=points_du_cercle(self.centrex, self.centrey, self.r, self.cible.angle)[1]

    def on_angle(self,*largs):
         if (self.bta.state=='down') and (self.btb.state=='normal'):
             self.angleProjection='alpha'
             self.pjx.nomDeProjection=self.angleProjection
             self.pjy.nomDeProjection=self.angleProjection
             
         elif (self.bta.state=='normal') and (self.btb.state=='down'):
             self.angleProjection='beta'

             self.pjx.nomDeProjection=self.angleProjection

             self.pjy.nomDeProjection=self.angleProjection
            #Désactivation des barres avec les propriétés des projections
class IndicSens(Cadreur):
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
        self.ratio=1.2
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
        self.flecheTrigo=Fleche(self.ctrIndiPlus,self.ptRefPlus,20.0)
        self.add_widget(self.flecheTrigo)

        self.flecheHoraire=Fleche(self.ctrIndiMoins,self.ptRefMoins,20.0)
        self.add_widget(self.flecheHoraire)
        if self.sens=='Direct':
            self.flecheTrigo.fleCouleur[3]=1
            
        else:
            self.flecheHoraire.fleCouleur[3]=1

        self.bind(sens=self.on_alerte)
        
    def on_alerte(self,bx,by,**kwargs):
        if self.sens=='Direct':
            self.flecheTrigo.fleCouleur[3]=1
            self.flecheHoraire.fleCouleur[3]=0
        else:
            self.flecheTrigo.fleCouleur[3]=0
            self.flecheHoraire.fleCouleur[3]=1

class ProjectionDirect(Widget):
    #Pour le calcul des angles, le sens direct est pris par défaut
    #dans le sens horaire => angle négatif
    #dans le sens trigo => angle positif
    #et ceux, même si le sens effectif est indirect
    #ça sera à l'intérpréteur de trancher sur le signe réel
    angleSupp=BooleanProperty(False)
    axeX=StringProperty('')
    axeY=StringProperty('')
    angleDeProjection=StringProperty('')
    nomDeProjection=StringProperty('')
    angleCible=NumericProperty(0)
    angleAxeX=NumericProperty(0)
    angleAxeY=NumericProperty(0)
    angleMesure=NumericProperty(0)
    anglePre=NumericProperty(0)
    dincrement=NumericProperty(0)
    def __init__(self,nomAxe,nomDeProjection,nomAxeX,angleAxeX,nomAxeY,angleAxeY,angleCible,**kwargs):
        super().__init__(**kwargs)
        self.nomAxe=nomAxe
        self.nomDeProjection=nomDeProjection
        self.axeX=nomAxeX
        self.angleAxeX=angleAxeX
        self.axeY=nomAxeY
        self.angleAxeY=angleAxeY
        self.angleCible=angleCible
        self.dincrementO=1
        self.dincrementP=1
        self.angleSup=False
        self.listeAngle={}
        self.listeAngleNeg={}
        self.listeAngleBeta={}
        self.listeAngleBetaNeg={}
        self.listeFlecheHoraire={}
        self.listeFlecheTrigo={}
        if self.nomDeProjection=='alpha':
            #Création des angles axes pour alpha
            if self.axeX=='xPlus':
                self.ratioP=4/5
                self.ratioC=0.85
                ###Calcul angleMesure
                self.angleMesure=calcul_angle(self.nomDeProjection, False,
                                              True, self.axeX, self.angleAxeX,
                                              self.angleCible)
                for i in range(self.angleAxeX,360,self.dincrementP):
                    self.nom='px',str(i)
                    self.nom=Boutons_angle(i,self.ratioP)
                    self.add_widget(self.nom)
                    self.nomDelta='delta',str(i)
                    self.nomDelta=Boutons_angle(i,self.ratioC)
                    self.add_widget(self.nomDelta)
                    if i <= self.angleCible:
                        self.nom.couleur[3]=1
                    if self.nom.angle<=359 and self.nom.angle>180:
                        self.angleNegatif=self.nom.angle-360
                    else:self.angleNegatif=self.nom.angle
                    #On créé ici, les valeurs qui seront utilisées par l'angle béta
                    self.angleBetaRef=self.nom.angle-90
                    if self.angleBetaRef<0:
                        self.angleBetaRef=360+self.angleBetaRef
                    #On créé ici les valeurs qui seront utilisées par l'angle béta négatif
                    if self.angleBetaRef>180:
                        self.angleBetaRefNeg=self.angleBetaRef-360
                    else: self.angleBetaRefNeg=self.angleBetaRef
                    ##On créer la liste des angles associées aux objets

                    self.listeAngle[str(self.nom.angle),
                                    str(self.ratioP)]=[self.nom,
                                                       self.angleNegatif,
                                                       self.angleBetaRef,
                                                       self.angleBetaRefNeg]
                    self.listeAngleBeta[str(self.angleBetaRef),
                                        str(self.ratioP)]=[self.nom]
                    self.listeAngleBeta[str(self.angleBetaRef),
                                        str(self.ratioC)]=[self.nomDelta]
                    self.listeAngleBetaNeg[str(self.angleBetaRefNeg),
                                            str(self.ratioP)]=[self.nom]
                    self.listeAngleBetaNeg[str(self.angleBetaRefNeg),
                                            str(self.ratioC)]=[self.nomDelta]
                    self.listeAngleNeg[str(self.angleNegatif),
                                       str(self.ratioP)]=[self.nom,self.ratioP]
                    self.listeAngle[str(self.nomDelta.angle),
                                    str(self.ratioC)]=[self.nomDelta,self.angleNegatif]
                    self.listeAngleNeg[str(self.angleNegatif),
                                       str(self.ratioC)]=[self.nomDelta]
                ##Maintenant,associons une flèche aux angles

                if self.angleCible==0:
                    j=359
                    self.centre=self.listeAngle[str(self.angleCible),str(self.ratioP)][0]
                    self.ptRef=self.listeAngle[str(j),str(self.ratioP)][0]
                    #fleche sens trigo
                    self.flecheDirec=Fleche(self.centre, self.ptRef, 10.0)
                    self.add_widget(self.flecheDirec)

                else:
                    j=self.angleCible-1
                    self.centre=self.listeAngle[str(self.angleCible),str(self.ratioP)][0]
                    self.ptRef=self.listeAngle[str(j),str(self.ratioP)][0]
                    #fleche sens trigo
                    self.flecheDirec=Fleche(self.centre, self.ptRef, 10.0)
                    self.add_widget(self.flecheDirec)
                self.flecheDirec.fleCouleur=[1,0,0,0]
                self.flecheDirec.fleCouleur[3]=1

                #Pour les angles deltas
                if self.angleSupp:
                    if self.angleCible>180:
                        for i in range(181,self.angleCible+1,self.dincrementO):
                            self.angleDelta=self.listeAngle[str(i),str(self.ratioC)][0]
                            self.angleDelta.couleur[3]=1

        #Maintenant nous allons lier le chgt d'angle et d'axe à l'update
        self.bind(angleCible=self.on_lisse)
        self.bind(angleAxeX=self.on_changement)
        self.bind(angleAxeY=self.on_changement)
        self.bind(nomDeProjection=self.on_changement)

    def on_lisse(self,anglePre,angleCible):
        if self.nomDeProjection=='alpha':
            if self.axeX=='xPlus':
                directionneur('alpha',self.axeX,self.angleCible,self.ratioP,
                              self.listeAngle,self.flecheDirec)
          
                #On récupère la mesure de l'angle
                self.angleMesure=calcul_angle(self.nomDeProjection, False, True, self.axeX, self.angleAxeX, self.angleCible)
                #on récupére la différence à colorier
                self.angleDiff=self.angleCible-self.anglePre
                #Il y a 4 conditions afin d'optimiser le traitement des angles deltas
                if (self.angleCible>180) and (self.anglePre>180):
                    #Afficher les autres angles
                    if self.angleDiff>=0:
                        self.dincrementP=1
                        self.dincrementO=1
                        for i in range(self.anglePre,self.angleCible,self.dincrementP):
                            self.widgetP=self.listeAngle[str(i),str(self.ratioP)][0]
                            self.widgetP.couleur[3]=1
                            if self.angleSupp:
                                self.widgetD.couleur[3]=1
                                self.widgetD=self.listeAngle[str(i),str(self.ratioC)][0]

                    else:
                        self.dincrementO=-1
                        self.dincrementP=-1
                        for i in range(self.anglePre,self.angleCible,self.dincrementP):
                            self.widgetP=self.listeAngle[str(i),str(self.ratioP)][0]
                            self.widgetP.couleur[3]=0
                            if self.angleSupp:
                                self.widgetD.couleur[3]=0
                                self.widgetD=self.listeAngle[str(i),str(self.ratioC)][0]
                
                elif (self.angleCible>180) and (self.anglePre<=180):
                    self.dincrementO=1
                    #Pour colorier les angles deltas
                    for i in range(181,self.angleCible+1,self.dincrementO):
                        if self.angleSupp:
                            self.angleDelta=self.listeAngle[str(i),str(self.ratioC)][0]
                            self.angleDelta.couleur[3]=1
                    if self.angleDiff>=0:
                        self.dincrementP=1
                        #Pour les angles normaux
                        for i in range(self.anglePre,self.angleCible,self.dincrementP):
                            self.widgetP=self.listeAngle[str(i),str(self.ratioP)][0]
                            self.widgetP.couleur[3]=1
                    else:
                        self.dincrementP=-1
                        for i in range(self.anglePre,self.angleCible,self.dincrementP):
                            self.widgetP=self.listeAngle[str(i),str(self.ratioP)][0]
                            self.widgetP.couleur[3]=0
                elif (self.angleCible<=180) and (self.anglePre>180):
                    self.dincrementO=-1
                    for i in range(self.anglePre,180,self.dincrementO):
                        if self.angleSupp:
                            self.angleDelta=self.listeAngle[str(i),str(self.ratioC)][0]
                            self.angleDelta.couleur[3]=0
                    if self.angleDiff>=0:
                        self.dincrementP=1
                        #Pour les angles normaux
                        for i in range(self.anglePre,self.angleCible,self.dincrementP):
                            self.widgetP=self.listeAngle[str(i),str(self.ratioP)][0]
                            self.widgetP.couleur[3]=1
                    else:
                        self.dincrementP=-1
                        for i in range(self.anglePre,self.angleCible,self.dincrementP):
                            self.widgetP=self.listeAngle[str(i),str(self.ratioP)][0]
                            self.widgetP.couleur[3]=0
                elif (self.angleCible<=180) and (self.anglePre<=180):
                    
                    if self.angleDiff>=0:
                        self.dincrementP=1
                        #Pour les angles normaux
                        for i in range(self.anglePre,self.angleCible,self.dincrementP):
                            self.widgetP=self.listeAngle[str(i),str(self.ratioP)][0]
                            self.widgetP.couleur[3]=1
                    else:
                        self.dincrementP=-1
                        for i in range(self.anglePre,self.angleCible,self.dincrementP):
                            self.widgetP=self.listeAngle[str(i),str(self.ratioP)][0]
                            self.widgetP.couleur[3]=0
            elif self.axeX=='xMoins':
                #Cela signifie ice que l'axe positif est suivant xMoins

                self.angleNeg=self.listeAngle[str(self.angleCible),str(self.ratioP)][1]
                directionneur('alpha',self.axeX,self.angleNeg,self.ratioP,
                              self.listeAngleNeg,self.flecheDirec)

                #Si c'est xMoins, nous allons utiliser les angles négatifs
                self.angleNeg=self.listeAngle[str(self.angleCible),str(self.ratioP)][1]
                ###Calcul angleMesure avec xMoins
                self.angleMesure=calcul_angle(self.nomDeProjection, False, True, self.axeX, self.angleAxeX, self.angleNeg)
                
                self.anglePreNeg=self.listeAngle[str(self.anglePre),str(self.ratioP)][1]
                self.angleDiff=self.angleNeg-self.anglePreNeg
                    
                #Il y a 4 conditions afin d'optimiser le traitement des angles deltas
                if (self.angleNeg<0) and (self.anglePreNeg<0):
                    #Afficher les autres angles
                    if self.angleDiff<=0:
                        self.dincrementP=-1
                        self.dincrementO=-1
                        for i in range(self.anglePreNeg,self.angleNeg,self.dincrementP):
                            self.widgetP=self.listeAngleNeg[str(i),str(self.ratioP)][0]
                            self.widgetP.couleur[3]=1
                            if self.angleSupp:
                                self.widgetD=self.listeAngleNeg[str(i),str(self.ratioC)][0]
                                self.widgetD.couleur[3]=1

                    else:
                        self.dincrementO=1
                        self.dincrementP=1

                        for i in range(self.anglePreNeg,self.angleNeg,self.dincrementP):
                            self.widgetP=self.listeAngleNeg[str(i),str(self.ratioP)][0]
                            self.widgetP.couleur[3]=0
                            if self.angleSupp:
                                self.widgetD=self.listeAngleNeg[str(i),str(self.ratioC)][0]
                                self.widgetD.couleur[3]=0
                elif (self.angleNeg<0) and (self.anglePreNeg>=0):
                    self.dincrementO=-1
                    if self.angleSupp:
                        #Pour colorier les angles deltas
                        for i in range(-1,self.angleNeg,self.dincrementO):
                            self.widgetD=self.listeAngleNeg[str(i),str(self.ratioC)][0]
                            self.widgetD.couleur[3]=1
            
                    if self.angleDiff<=0:
                        self.dincrementP=-1
                        for i in range(self.anglePreNeg,self.angleNeg,self.dincrementP):
                            self.widget=self.listeAngleNeg[str(i),str(self.ratioP)][0]
                            self.widget.couleur[3]=1
                    else:
                        self.dincrementP=1
                        for i in range(self.anglePreNeg,self.angleNeg,self.dincrementP):
                           self.widget=self.listeAngleNeg[str(i),str(self.ratioP)][0]
                           self.widget.couleur[3]=0
                           
                elif (self.angleNeg>=0) and (self.anglePreNeg<0):
                    self.dincrementO=1
                    if self.angleSupp:
                    #Pour colorier les angles deltas
                        for i in range(self.anglePreNeg,1,self.dincrementO):
                            self.widgetD=self.listeAngleNeg[str(i),str(self.ratioC)][0]
                            self.widgetD.couleur[3]=0
                    if self.angleDiff<=0:
                        self.dincrementP=-1
                        for i in range(self.anglePreNeg,self.angleNeg,self.dincrementP):
                            self.widget=self.listeAngleNeg[str(i),str(self.ratioP)][0]
                            self.widget.couleur[3]=1
                    else:
                        self.dincrementP=1
                        for i in range(self.anglePreNeg,self.angleNeg,self.dincrementP):
                           self.widget=self.listeAngleNeg[str(i),str(self.ratioP)][0]
                           self.widget.couleur[3]=0
                           
                elif (self.angleNeg>=0) and (self.anglePre>=0):
                    if self.angleDiff<=0:
                        self.dincrementP=-1
                        for i in range(self.anglePreNeg,self.angleNeg,self.dincrementP):
                            self.widget=self.listeAngleNeg[str(i),str(self.ratioP)][0]
                            self.widget.couleur[3]=1
                    else:
                        self.dincrementP=1
                        for i in range(self.anglePreNeg,self.angleNeg,self.dincrementP):
                           self.widget=self.listeAngleNeg[str(i),str(self.ratioP)][0]
                           self.widget.couleur[3]=0
#############################################################################################◘
#############################################################################################  
        #angleBeta
        else:
            if self.axeY=='yPlus':
                #On récupère la mesure de l'angle par rapport au béta référence
                ###############################################################
                directionneur('beta',self.axeY,self.angleCible,self.ratioP,
                              self.listeAngle,self.flecheDirec)
                
                self.angleCibleBeta=self.listeAngle[str(self.angleCible),
                                                 str(self.ratioP)][2]
                self.anglePreBeta=self.listeAngle[str(self.anglePre),
                                                str(self.ratioP)][2]
                self.angleMesure=0
                self.angleAxeYBeta=transform_en_beta(self.angleAxeY)
 

                self.angleMesure=calcul_angle(self.nomDeProjection, False, True,
                                              self.axeY, self.angleAxeYBeta, self.angleCibleBeta)
                #on récupére la différence à colorier
                self.angleDiff=self.angleCibleBeta-self.anglePreBeta
                #Il y a 4 conditions afin d'optimiser le traitement des angles deltas
                if (self.angleCibleBeta>180) and (self.anglePreBeta>180):
                    #Afficher les autres angles
                    if self.angleDiff>=0:
                        self.dincrementP=1
                        self.dincrementO=1
                        for i in range(self.anglePreBeta,self.angleCibleBeta,self.dincrementP):
                            self.widgetP=self.listeAngleBeta[str(i),str(self.ratioP)][0]
                            self.widgetP.couleur[3]=1
                            if self.angleSupp:
                                self.widgetD=self.listeAngleBeta[str(i),str(self.ratioC)][0]
                                self.widgetD.couleur[3]=1

                    else:
                        self.dincrementO=-1
                        self.dincrementP=-1
                        for i in range(self.anglePreBeta,self.angleCibleBeta,self.dincrementP):
                            self.widgetP=self.listeAngleBeta[str(i),str(self.ratioP)][0]
                            self.widgetP.couleur[3]=0
                            if self.angleSupp:
                                self.widgetD.couleur[3]=0
                                self.widgetD=self.listeAngle[str(i),str(self.ratioC)][0]
                elif (self.angleCibleBeta>180) and (self.anglePreBeta<=180):
                    self.dincrementO=1
                    if self.angleSupp:
                        #Pour colorier les angles deltas
                        for i in range(181,self.angleCibleBeta+1,self.dincrementO):
                                self.angleDelta=self.listeAngleBeta[str(i),str(self.ratioC)][0]
                                self.angleDelta.couleur[3]=1
                    if self.angleDiff>=0:
                        self.dincrementP=1
                        #Pour les angles normaux
                        for i in range(self.anglePreBeta,self.angleCibleBeta,self.dincrementP):
                            self.widgetP=self.listeAngleBeta[str(i),str(self.ratioP)][0]
                            self.widgetP.couleur[3]=1
                    else:
                        self.dincrementP=-1
                        for i in range(self.anglePreBeta,self.angleCibleBeta,self.dincrementP):
                            self.widgetP=self.listeAngleBeta[str(i),str(self.ratioP)][0]
                            self.widgetP.couleur[3]=0
                elif (self.angleCibleBeta<=180) and (self.anglePreBeta>180):
                    self.dincrementO=-1
                    if self.angleSupp:
                        for i in range(self.anglePreBeta,180,self.dincrementO):
                                self.angleDelta=self.listeAngleBeta[str(i),str(self.ratioC)][0]
                                self.angleDelta.couleur[3]=0
                    if self.angleDiff>=0:
                        self.dincrementP=1
                        #Pour les angles normaux
                        for i in range(self.anglePreBeta,self.angleCibleBeta,self.dincrementP):
                            self.widgetP=self.listeAngleBeta[str(i),str(self.ratioP)][0]
                            self.widgetP.couleur[3]=1
                    else:
                        self.dincrementP=-1
                        for i in range(self.anglePreBeta,self.angleCibleBeta,self.dincrementP):
                            self.widgetP=self.listeAngleBeta[str(i),str(self.ratioP)][0]
                            self.widgetP.couleur[3]=0
                elif (self.angleCibleBeta<=180) and (self.anglePreBeta<=180):
                    if self.angleDiff>=0:
                        self.dincrementP=1
                        #Pour les angles normaux
                        for i in range(self.anglePreBeta,self.angleCibleBeta,self.dincrementP):
                            self.widgetP=self.listeAngleBeta[str(i),str(self.ratioP)][0]
                            self.widgetP.couleur[3]=1 
                    else:
                        self.dincrementP=-1
                        for i in range(self.anglePreBeta,self.angleCibleBeta,self.dincrementP):
                            self.widgetP=self.listeAngleBeta[str(i),str(self.ratioP)][0]
                            self.widgetP.couleur[3]=0
        #yMoins
            elif self.axeY=='yMoins':
                #Si c'est xMoins, nous allons utiliser les angles négatifs
                self.angleNeg=self.listeAngle[str(self.angleCible),str(self.ratioP)][1]
                self.angleBetaNeg=transform_neg_beta(self.angleNeg)
                  ###############################################################
                ##############################"Pour la flèche, 
                directionneur('beta',self.axeY,self.angleCible,self.ratioP,
                              self.listeAngle,self.flecheDirec)

                ##AngleRef pour le béta positif et ainsi le mettre dans la fonction
                self.anglePreBetaNeg=self.listeAngle[str(self.anglePre),str(self.ratioP)][3]
                ###Calcul angleMesure avec xMoins
                self.angleAxeYBeta=transform_neg_beta(-90)
                self.angleMesure=calcul_angle(self.nomDeProjection, False, True,
                                              self.axeY, self.angleAxeYBeta, self.angleBetaNeg)
                
                self.angleDiff=self.angleBetaNeg-self.anglePreBetaNeg
                    
                #Il y a 4 conditions afin d'optimiser le traitement des angles deltas
                if (self.angleBetaNeg<0) and (self.anglePreBetaNeg<0):
                    #Afficher les autres angles
                    if self.angleDiff<=0:
                        self.dincrementP=-1
                        self.dincrementO=-1
                        for i in range(self.anglePreBetaNeg,self.angleBetaNeg,self.dincrementP):
                            self.widgetP=self.listeAngleBetaNeg[str(i),str(self.ratioP)][0]
                            self.widgetP.couleur[3]=1
                            if self.angleSupp:
                                self.widgetD=self.listeAngleBetaNeg[str(i),str(self.ratioC)][0]
                                self.widgetD.couleur[3]=1
                    else:
                        self.dincrementO=1
                        self.dincrementP=1
                        for i in range(self.anglePreBetaNeg,self.angleBetaNeg,self.dincrementP):
                            self.widgetP=self.listeAngleBetaNeg[str(i),str(self.ratioP)][0]
                            self.widgetP.couleur[3]=0
                            if self.angleSupp:
                                self.widgetD=self.listeAngleBetaNeg[str(i),str(self.ratioC)][0]
                                self.widgetD.couleur[3]=0
                elif (self.angleBetaNeg<0) and (self.anglePreBetaNeg>=0):
                    self.dincrementO=-1
                    if self.angleSupp:
                        #Pour colorier les angles deltas
                        for i in range(-1,self.angleBetaNeg,self.dincrementO):
                            self.widgetD=self.listeAngleBetaNeg[str(i),str(self.ratioC)][0]
                            self.widgetD.couleur[3]=1
            
                    if self.angleDiff<=0:
                        self.dincrementP=-1
                        for i in range(self.anglePreBetaNeg,self.angleBetaNeg,self.dincrementP):
                            self.widget=self.listeAngleBetaNeg[str(i),str(self.ratioP)][0]
                            self.widget.couleur[3]=1
                    else:
                        self.dincrementP=1
                        for i in range(self.anglePreBetaNeg,self.angleBetaNeg,self.dincrementP):
                           self.widget=self.listeAngleBetaNeg[str(i),str(self.ratioP)][0]
                           self.widget.couleur[3]=0      
                elif (self.angleBetaNeg>=0) and (self.anglePreBetaNeg<0):
                    self.dincrementO=1
                    if self.angleSupp:
                    #Pour colorier les angles deltas
                        for i in range(self.anglePreBetaNeg,0,self.dincrementO):
                            self.widgetD=self.listeAngleBetaNeg[str(i),str(self.ratioC)][0]
                            self.widgetD.couleur[3]=0
                    if self.angleDiff<=0:
                        self.dincrementP=-1
                        for i in range(self.anglePreBetaNeg,self.angleBetaNeg,self.dincrementP):
                            self.widget=self.listeAngleBetaNeg[str(i),str(self.ratioP)][0]
                            self.widget.couleur[3]=1
                    else:
                        self.dincrementP=1
                        for i in range(self.anglePreBetaNeg,self.angleBetaNeg,self.dincrementP):
                           self.widget=self.listeAngleBetaNeg[str(i),str(self.ratioP)][0]
                           self.widget.couleur[3]=0                    
                elif (self.angleBetaNeg>=0) and (self.anglePre>=0):
                    if self.angleDiff<=0:
                        self.dincrementP=-1
                        for i in range(self.anglePreBetaNeg,self.angleBetaNeg,self.dincrementP):
                            self.widget=self.listeAngleBetaNeg[str(i),str(self.ratioP)][0]
                            self.widget.couleur[3]=1
                    else:
                        self.dincrementP=1
                        for i in range(self.anglePreBetaNeg,self.angleBetaNeg,self.dincrementP):
                           self.widget=self.listeAngleBetaNeg[str(i),str(self.ratioP)][0]
                           self.widget.couleur[3]=0
    def on_changement(self,anglePre,angleCible):
        if self.nomDeProjection=='alpha':
            if self.axeX=='xPlus':
                directionneur('alpha',self.axeX,self.angleCible,self.ratioP,
                              self.listeAngle,self.flecheDirec)
               
                #On récupère la mesure de l'angle
                #On récupère la mesure de l'angle
                self.angleMesure=calcul_angle(self.nomDeProjection, False, True, self.axeX, self.angleAxeX, self.angleCible)
                if self.angleCible>180:
                    self.dincrementP=1
                    self.dincrementO=1
                    for i in range(self.angleAxeX,self.angleCible,self.dincrementP):
                        self.widgetP=self.listeAngle[str(i),str(self.ratioP)][0]
                        self.widgetD=self.listeAngle[str(i),str(self.ratioC)][0]
                        self.widgetP.couleur[3]=1
                        self.widgetD.couleur[3]=0
                        #QUe les boutons qui sont supérieurs à 180°
                        if self.angleSupp:
                            if i>180:
                                self.widgetD.couleur[3]=1
                else:
                    self.dincrementP=1
                    for i in range(self.angleAxeX,self.angleCible,self.dincrementP):
                        self.widgetP=self.listeAngle[str(i),str(self.ratioP)][0]
                        self.widgetD=self.listeAngle[str(i),str(self.ratioC)][0]
                        self.widgetP.couleur[3]=1
                        self.widgetD.couleur[3]=0

                if (359-self.angleCible)>0:
                    for i in range(self.angleCible,359):
                        self.widgetP=self.listeAngle[str(i),str(self.ratioP)][0]
                        self.widgetD=self.listeAngle[str(i),str(self.ratioC)][0]
                        self.widgetD.couleur[3]=0
                        self.widgetP.couleur[3]=0                    
            elif self.axeX=='xMoins':
                self.angleNeg=self.listeAngle[str(self.angleCible),str(self.ratioC)][1]

                directionneur('alpha',self.axeX,self.angleNeg,self.ratioP,
                              self.listeAngleNeg,self.flecheDirec)
                self.flecheDirec.canvas.ask_update()
  
                ###Calcul angleMesure avec xMoins
                self.angleMesure=calcul_angle(self.nomDeProjection, False, True, self.axeX, self.angleAxeX, self.angleNeg)

                self.anglePreNeg=self.listeAngle[str(self.angleCible),str(self.ratioC)][1]
                if self.angleNeg<0:
                    self.dincrementP=-1
                    self.dincrementO=-1
                    for i in range(self.angleAxeX,self.angleNeg,self.dincrementP):
                        self.widgetP=self.listeAngleNeg[str(i),str(self.ratioP)][0]
                        self.widgetD=self.listeAngleNeg[str(i),str(self.ratioC)][0]
                        self.widgetD.couleur[3]=0
                        self.widgetP.couleur[3]=1
                        
                        if self.angleSupp:
                            if i<0:
                                self.widgetD.couleur[3]=1
                else:
                    self.dincrementP=-1
                    for i in range(self.angleAxeX,self.angleNeg,self.dincrementP):
                        self.widgetP=self.listeAngleNeg[str(i),str(self.ratioP)][0]
                        self.widgetD=self.listeAngleNeg[str(i),str(self.ratioC)][0]
                        self.widgetP.couleur[3]=1
                        self.widgetD.couleur[3]=0
                if (-179-self.angleCible)<0:
                    for i in range(self.angleNeg,-180,-1):
                        self.widgetP=self.listeAngleNeg[str(i),str(self.ratioP)][0]
                        self.widgetD=self.listeAngleNeg[str(i),str(self.ratioC)][0]
                        self.widgetD.couleur[3]=0
                        self.widgetP.couleur[3]=0  
    ###################################################################################
    ###################################################################################
    #BETA
        else:
            if self.axeY=='yPlus':
                ###############################################################
                ##############################"Pour la flèche, 
                self.flecheDirec.canvas.ask_update()
                directionneur('beta',self.axeY,self.angleCible,self.ratioP,
                              self.listeAngle,self.flecheDirec)

                self.angleCibleBeta=self.listeAngle[str(self.angleCible),
                                                 str(self.ratioP)][2]
                self.anglePreBeta=self.listeAngle[str(self.anglePre),
                                                str(self.ratioP)][2]
                self.angleAxeYBeta=transform_en_beta(self.angleAxeY)
 

                self.angleMesure=calcul_angle(self.nomDeProjection, False, True,
                                              self.axeY, self.angleAxeYBeta, self.angleCibleBeta)
                if self.angleCibleBeta>180:
                    self.dincrementP=1
                    self.dincrementO=1
                    for i in range(0,self.angleCibleBeta+1,self.dincrementP):
                        self.widgetP=self.listeAngleBeta[str(i),str(self.ratioP)][0]
                        self.widgetD=self.listeAngleBeta[str(i),str(self.ratioC)][0]
                        self.widgetP.couleur[3]=1
                        self.widgetD.couleur[3]=0
                        if self.angleSup:
                            #QUe les boutons qui sont supérieurs à 180°
                            if i>180:
                                self.widgetD.couleur[3]=1
                else:
                    self.dincrementP=1

                    for i in range(0,self.angleCibleBeta+1,self.dincrementP):
              
                        self.widgetP=self.listeAngleBeta[str(i),str(self.ratioP)][0]
                        self.widgetD=self.listeAngleBeta[str(i),str(self.ratioC)][0]
                        self.widgetP.couleur[3]=1
                        self.widgetD.couleur[3]=0

                if (359-self.angleCibleBeta)>0:
                    for i in range(self.angleCibleBeta,359):
                        self.widgetP=self.listeAngleBeta[str(i),str(self.ratioP)][0]
                        self.widgetD=self.listeAngleBeta[str(i),str(self.ratioC)][0]
                        self.widgetD.couleur[3]=0
                        self.widgetP.couleur[3]=0                    
            elif self.axeY=='yMoins':
                self.angleNeg=self.listeAngle[str(self.angleCible),str(self.ratioP)][1]
                self.angleBetaNeg=transform_neg_beta(self.angleNeg)
                directionneur('beta',self.axeY,self.angleCible,self.ratioP,
                              self.listeAngle,self.flecheDirec)
                self.angleAxeYBeta=transform_neg_beta(-90)
                self.angleMesure=calcul_angle(self.nomDeProjection, False, True,
                                              self.axeY, self.angleAxeYBeta, self.angleBetaNeg)
                if self.angleBetaNeg<0:
                    self.dincrementP=-1
                    self.dincrementO=-1
                    for i in range(180,self.angleBetaNeg+1,self.dincrementP):
                        self.widgetP=self.listeAngleBetaNeg[str(i),str(self.ratioP)][0]
                        self.widgetD=self.listeAngleBetaNeg[str(i),str(self.ratioC)][0]
                        self.widgetP.couleur[3]=1
                        self.widgetD.couleur[3]=0
                        if self.angleSup:
                            if i<0:
                                self.widgetD.couleur[3]=1
                else:
                    self.dincrementP=-1
                    for i in range(180,self.angleBetaNeg,self.dincrementP):
                        self.widgetP=self.listeAngleBetaNeg[str(i),str(self.ratioP)][0]
                        self.widgetD=self.listeAngleBetaNeg[str(i),str(self.ratioC)][0]
                        self.widgetP.couleur[3]=1
                        self.widgetD.couleur[3]=0
                if (-179-self.angleCible)<0:
                    for i in range(self.angleBetaNeg,-180,-1):
                        self.widgetP=self.listeAngleBetaNeg[str(i),str(self.ratioP)][0]
                        self.widgetD=self.listeAngleBetaNeg[str(i),str(self.ratioC)][0]
                        self.widgetD.couleur[3]=0
                        self.widgetP.couleur[3]=0     

class ProjectionIndirect(Widget):
    #Pour le calcul des angles, le sens direct est pris par défaut
    #dans le sens horaire => angle négatif
    #dans le sens trigo => angle positif
    #et ceux, même si le sens est indirect. 
    #ça sera à l'intérpréteur de trancher sur le signe réel

    axeX=StringProperty('')
    axeY=StringProperty('')
    nomDeProjection=StringProperty('')
    nomAngle=StringProperty('')
    angleCible=NumericProperty(0)
    angleAxeX=NumericProperty(0)
    angleAxeY=NumericProperty(0)
    angleMesureI=NumericProperty(0)
    angleMesureE=NumericProperty(0)
    anglePre=NumericProperty(0)
    angleDiff=NumericProperty(0)
    dincrementE=NumericProperty(0)
    dincrementI=NumericProperty(0)
    def __init__(self,nomAxe,angleDeProjection,nomAxeX,angleAxeX,nomAxeY,angleAxeY,angleCible,**kwargs):
        #Contrairement à Projection DIrect, pas de gestion d'un béta Référencé=>
        #Plus d'algo => algo plus complexe
        super().__init__(**kwargs)
        self.nomAxe=nomAxe
        self.nomDeProjection=angleDeProjection
        self.axeX=nomAxeX
        self.angleAxeX=angleAxeX
        self.axeY=nomAxeY
        self.angleAxeY=angleAxeY
        self.angleCible=angleCible
        self.listeAngle={}
        self.listeAngleNeg={}
        self.listeFleInt={}
        self.nomAxe=nomAxe
        ##ICI LES COULEURS
        self.indigo=[0.18,0,0.42,0]
        self.violetClair=[0.26,0,0.573,0]
        if self.nomDeProjection=='alpha':
            if self.nomAxe=='yPlus':
                self.ratioI=0.4
                self.ratioE=0.45
                #Pour le contour intérieur
                self.dincrementI=-1
                
                ##On va calculer l'angle intérieur
                self.angleMesureI=calcul_angle(self.nomDeProjection,
                                               False, False, self.axeY,
                                               self.angleAxeY, self.angleAxeX)
                #Puis l'angle intérieur
                self.angleMesureE=calcul_angle(self.nomDeProjection,
                                               False, True, self.axeX,
                                               self.angleAxeX, self.angleCible)
    
                for i in range(359,-1,self.dincrementI):
                    self.nom='pys'
                    self.nom=Boutons_angle(i,self.ratioI)
                    self.nom.couleur=self.violetClair
                    # self.nom.couleur=self.violetClair
                    self.add_widget(self.nom)
                    #C'est le contour intérieur
                    if ((self.angleAxeX<=i) and (self.angleAxeY>=i)):
                        self.nom.couleur[3]=1
                    else:
                        self.nom.couleur[3]=0
                    if self.nom.angle<=359 and self.nom.angle>180:
                        self.angleNegatif=self.nom.angle-360
                    else:self.angleNegatif=self.nom.angle
                    #Pour les angles négatifs du cercle intérieur
                    self.listeAngle[str(self.nom.angle),
                                    str(self.ratioI)]=[self.nom,self.angleNegatif]



                    self.listeAngleNeg[str(self.angleNegatif),
                                       str(self.ratioI)]=[self.nom]
                #Pour les angles Extérieurs
                self.dincrementE=1
                #C'est le contour extérieur
                for i in range(0,360,self.dincrementE):
                    self.nom='py'
                    self.nom=Boutons_angle(i,self.ratioE)
                    ###Les couleurs
                    self.nom.couleur=self.indigo
                    self.add_widget(self.nom)
                    if i<= self.angleCible:
                        self.nom.couleur[3]=1
                    self.listeAngle[str(self.nom.angle),str(self.ratioE)]=[self.nom]
                    self.bind(angleCible=self.on_lisse)
                #On crééait les angles  négatif du contour extérieur
                    if self.nom.angle<=359 and self.nom.angle>180:
                        self.angleNegatif=self.nom.angle-360
                    else:self.angleNegatif=self.nom.angle
                    ##On créer la liste des angles associées aux objets
                    self.listeAngle[str(self.nom.angle),
                                    str(self.ratioE)]=[self.nom,
                                                       self.angleNegatif]
                    self.listeAngleNeg[str(self.angleNegatif),
                                       str(self.ratioE)]=[self.nom]
                if self.angleCible==0:
                    j=359
                    self.centre=self.listeAngle[str(self.angleCible),str(self.ratioE)][0]
                    self.ptRef=self.listeAngle[str(j),str(self.ratioE)][0]
                    #fleche sens trigo
                    self.flecheDirecE=Fleche(self.centre, self.ptRef, 10.0)
                    self.flecheDirecE.fleCouleur=self.indigo

                    self.add_widget(self.flecheDirecE)

                else:
                    j=self.angleCible-1
                    self.centre=self.listeAngle[str(self.angleCible),str(self.ratioE)][0]
                    self.ptRef=self.listeAngle[str(j),str(self.ratioE)][0]
                    #fleche sens trigo
                    self.flecheDirecE=Fleche(self.centre, self.ptRef, 10.0)
                    self.flecheDirecE.fleCouleur=self.indigo
                    self.add_widget(self.flecheDirecE)

                self.flecheDirecE.fleCouleur[3]=1
               
                #Pour positionner les flèches intérieures
                for i in range(360):
                    if i ==0:
                        h=359
                        t=1
                        self.centre=self.listeAngle[str(i),str(self.ratioI)][0]
                        self.ptRefH=self.listeAngle[str(h),str(self.ratioI)][0]
                        self.ptRefT=self.listeAngle[str(t),str(self.ratioI)][0]
                        self.flecheDirecH=Fleche(self.centre,self.ptRefH,10.0)
                        self.flecheDirecT=Fleche(self.centre,self.ptRefT,10.0)
                        #Ici on modifie la couleur des fleches
                        self.flecheDirecH.fleCouleur=self.violetClair
                        self.flecheDirecT.fleCouleur=self.violetClair
                        self.add_widget(self.flecheDirecH)
                        self.add_widget(self.flecheDirecT)
                        self.listeFleInt[str(i),'horaire']=[self.flecheDirecH]
                        self.listeFleInt[str(i),'trigo']=[self.flecheDirecT]
                    elif i==90 or i==180 or i==270:
                        h=i+1
                        t=i-1
                        self.centre=self.listeAngle[str(i),str(self.ratioI)][0]
                        self.ptRefH=self.listeAngle[str(h),str(self.ratioI)][0]
                        self.ptRefT=self.listeAngle[str(t),str(self.ratioI)][0]
                        self.flecheDirecH=Fleche(self.centre,self.ptRefH,10.0)
                        self.flecheDirecT=Fleche(self.centre,self.ptRefT,10.0)
                        self.flecheDirecH.fleCouleur=self.violetClair
                        self.flecheDirecT.fleCouleur=self.violetClair
                        self.add_widget(self.flecheDirecH)
                        self.add_widget(self.flecheDirecT)
                        self.listeFleInt[str(i),'horaire']=[self.flecheDirecH]
                        self.listeFleInt[str(i),'trigo']=[self.flecheDirecT]
                self.flecheActuelI=self.listeFleInt[str(0),'trigo'][0]
                self.flecheActuelI.fleCouleur[3]=1
                

         

        self.bind(angleAxeX=self.on_changement)
        self.bind(angleAxeY=self.on_changement)
        self.bind(angleCible=self.on_lisse)
        self.bind(nomDeProjection=self.on_changement)

    def on_lisse(self,anglePre,angleCible):
        if self.nomDeProjection=='alpha':
            if self.axeY=='yPlus' or self.axeY=='yMoins':
                if self.axeX=='xPlus':
                    ###############################################################
                    ##############################"Pour la flèche, 
                    directionneur('alpha',self.axeX,self.angleCible,self.ratioE,
                              self.listeAngle,self.flecheDirecE)
       
                    #Nous calculons l'angle intérieur
                    self.angleMesureI=calcul_angle(self.nomDeProjection, False, False, self.axeY,
                                                   self.angleAxeY, self.angleAxeX)
                    #puis l'angle extérieur
                    self.angleMesureE=calcul_angle(self.nomDeProjection, False, True, self.axeX,
                                                   self.angleAxeX, self.angleCible)
                    
                    ###############################################################
                    ##############################"Pour la flèche, 
                    if self.angleCible==0:
                        j=359
                        self.centre=self.listeAngle[str(self.angleCible),str(self.ratioE)][0]
                        self.ptRef=self.listeAngle[str(j),str(self.ratioE)][0]
                        #fleche sens trigo
                        self.flecheDirecE.ctr=self.centre
                        self.flecheDirecE.ptRef=self.ptRef
                    else:                    
                        j=self.angleCible-1
                        self.centre=self.listeAngle[str(self.angleCible),str(self.ratioE)][0]
                        self.ptRef=self.listeAngle[str(j),str(self.ratioE)][0]
                        #fleche sens trigo
                        self.flecheDirecE.ctr=self.centre
                        self.flecheDirecE.ptRef=self.ptRef
                    ###############################################################
                    self.angleDiff=self.angleCible-self.anglePre

                    if self.angleDiff>0:
                        self.dincrement=1
                        for i in range(self.anglePre,self.angleCible,self.dincrement):
                            self.widget=self.listeAngle[str(i),str(self.ratioE)][0]
                            self.widget.couleur[3]=1
                    else:
                        self.dincrement=-1
                        for i in range(self.anglePre,self.angleCible,self.dincrement):
                            self.widget=self.listeAngle[str(i),str(self.ratioE)][0]
                            self.widget.couleur[3]=0
                elif self.axeX=='xMoins':
                    ###############################################################
                    ##############################"Pour la flèche, 
                    directionneur('alpha',self.axeX,self.angleCible,self.ratioE,
                              self.listeAngle,self.flecheDirecE)
                    if self.angleCible==359:
                        j=0
                        self.centre=self.listeAngle[str(self.angleCible),str(self.ratioE)][0]
                        self.ptRef=self.listeAngle[str(j),str(self.ratioE)][0]
                        #fleche sens trigo
                        self.flecheDirecE.ctr=self.centre
                        self.flecheDirecE.ptRef=self.ptRef
        
                    else:                    
        
                        j=self.angleCible+1
                        self.centre=self.listeAngle[str(self.angleCible),str(self.ratioE)][0]
                        self.ptRef=self.listeAngle[str(j),str(self.ratioE)][0]
                        #fleche sens trigo
                        self.flecheDirecE.ctr=self.centre
                        self.flecheDirecE.ptRef=self.ptRef
                    ###############################################################
                    self.anglePreNeg=self.listeAngle[str(self.anglePre),str(self.ratioE)][1]
                    self.angleCibleNeg=self.listeAngle[str(self.angleCible),str(self.ratioE)][1]
                    #Nous calculons l'angle intérieur
                    self.angleMesureI=calcul_angle(self.nomDeProjection, False, False, self.axeY,
                                                   self.angleAxeY, self.angleAxeX)
                    #puis l'angle extérieur
                    self.angleMesureE=calcul_angle(self.nomDeProjection, False, True, self.axeX,
                                                   self.angleAxeX, self.angleCibleNeg)
    
                    self.angleDiff=self.angleCibleNeg-self.anglePreNeg
                    if self.angleDiff>0:
                        self.dincrement=1
                        for i in range(self.anglePreNeg,self.angleCibleNeg,self.dincrement):
                            self.widget=self.listeAngleNeg[str(i),str(self.ratioE)][0]
                            self.widget.couleur[3]=0
                    else:
                        self.dincrement=-1
                        for i in range(self.anglePreNeg,self.angleCibleNeg,self.dincrement):
                            self.widget=self.listeAngleNeg[str(i),str(self.ratioE)][0]
                            self.widget.couleur[3]=1
#################################BETA################################################
#######################################################################################
        else:
            if self.axeX=='xPlus'or self.axeX=='xMoins':
                if self.axeY=='yPlus':
                    #On récupère la mesure de l'angle par rapport au béta référence
                    ###############################################################
                    ##############################"Pour la flèche, 
        
                    directionneur('beta',self.axeY,self.angleCible,self.ratioE,
                              self.listeAngle,self.flecheDirecE)
                    #Nous calculons l'angle intérieur
                    self.angleMesureI=calcul_angle(self.nomDeProjection, False, False, self.axeX,
                                                  self.angleAxeX, self.angleAxeY)
              
                    #puis l'angle extérieur
                    self.angleAxeYBeta=transform_en_beta(self.angleAxeY)

                    self.betaRef=transform_en_beta(self.angleCible)
                    self.preBetaRef=transform_en_beta(self.anglePre)
    
                    self.angleMesureE=calcul_angle(self.nomDeProjection, False, True,
                                              self.axeY, self.angleAxeYBeta, self.betaRef)

     
                    self.angleDiff=self.betaRef-self.preBetaRef
                    if self.angleDiff>0:
                        self.dincrement=1
                        for i in range(self.preBetaRef,self.betaRef,self.dincrement):
                            i=transform_en_alpha(i)
                            self.widget=self.listeAngle[str(i),str(self.ratioE)][0]
                            self.widget.couleur[3]=1
                    else:
                        self.dincrement=-1
                        for i in range(self.preBetaRef,self.betaRef,self.dincrement):
                            i=transform_en_alpha(i)
                            self.widget=self.listeAngle[str(i),str(self.ratioE)][0]
                            self.widget.couleur[3]=0
                
                elif self.axeY=='yMoins':
                    ###############################################################
                    ##############################"Pour la flèche,    
                    if self.angleCible==359:
                        j=0
                        self.centre=self.listeAngle[str(self.angleCible),str(self.ratioE)][0]
                        self.ptRef=self.listeAngle[str(j),str(self.ratioE)][0]
                        #fleche sens trigo
                        self.flecheDirecE.ctr=self.centre
                        self.flecheDirecE.ptRef=self.ptRef
                    else:                    
                        j=self.angleCible+1
                        self.centre=self.listeAngle[str(self.angleCible),str(self.ratioE)][0]
                        self.ptRef=self.listeAngle[str(j),str(self.ratioE)][0]
                        #fleche sens trigo
                        self.flecheDirecE.ctr=self.centre
                        self.flecheDirecE.ptRef=self.ptRef
                    ###############################################################
            
                    self.anglePreNeg=self.listeAngle[str(self.anglePre),str(self.ratioE)][1]
                    self.angleCibleNeg=self.listeAngle[str(self.angleCible),str(self.ratioE)][1]
                    self.betaPreNeg=transform_neg_beta(self.anglePreNeg)
                    self.betaNeg=transform_neg_beta(self.angleCibleNeg)
                    #Nous calculons l'angle intérieur
                    self.angleMesureI=calcul_angle(self.nomDeProjection, False, False, self.axeX,
                                                    self.angleAxeX, self.angleAxeY)

                    
                    # #puis l'angle extérieur
                    self.angleAxeYBetaNeg=transform_neg_beta(-90)
                    self.angleMesureE=calcul_angle(self.nomDeProjection, False, True,
                                              self.axeY, self.angleAxeYBetaNeg, self.betaNeg)
    
                    self.angleDiff=self.betaNeg-self.betaPreNeg
                    if self.angleDiff>0:
                        self.dincrement=1
                        for i in range(self.betaPreNeg,self.betaNeg,self.dincrement):
                            i=transform_neg_alpha(i)
                            self.widget=self.listeAngleNeg[str(i),str(self.ratioE)][0]
                            self.widget.couleur[3]=0
                    else:
                        self.dincrement=-1
                        for i in range(self.betaPreNeg,self.betaNeg,self.dincrement):
                            i=transform_neg_alpha(i)
                            self.widget=self.listeAngleNeg[str(i),str(self.ratioE)][0]
                            self.widget.couleur[3]=1

                 
    def on_changement(self,anglePre,angleCible):
        if self.nomDeProjection=='alpha':
            if self.axeY=='yPlus':
                if self.axeX=='xPlus':
                    self.flecheActuelI.fleCouleur[3]=0
                    self.flecheActuelI=self.listeFleInt[str(0),'trigo'][0]
                    self.flecheActuelI.fleCouleur[3]=1
                    ###############################################################
                    ##############################"Pour la flèche, 
                    self.flecheDirecE.canvas.ask_update()
                    #Pour la flèche intérieur
                    directionneur('alpha',self.axeY,self.angleCible,self.ratioE,
                              self.listeAngle,self.flecheDirecE)
       

                    self.angleMesureI=calcul_angle(self.nomDeProjection, False, False, self.axeY,
                                                   self.angleAxeY, self.angleAxeX)
                    self.angleMesureE=calcul_angle(self.nomDeProjection, False, True, self.axeX,
                                                   self.angleAxeX, self.angleCible)
    
                    self.dincrement=-1
    
                    for i in range(359,0,self.dincrement):
                        self.widgetI=self.listeAngle[str(i),str(self.ratioI)][0]
                        #On colorie les widgets intérieurs
                        if ((i>=self.angleAxeX) and (i<=self.angleAxeY)):
                            
                            self.widgetI.couleur[3]=1
                        else:
                            self.widgetI.couleur[3]=0
                    self.dincrement=1
                    for i in range(0,360,self.dincrement):
                        self.widgetE=self.listeAngle[str(i),str(self.ratioE)][0]
                        #On colorie les widgets extérieurs
                        if i>=self.angleCible:
                            self.widgetE.couleur[3]=0
                        else:
                            self.widgetE.couleur[3]=1
                elif self.axeX=='xMoins':
                    self.flecheActuelI.fleCouleur[3]=0
                    self.flecheActuelI=self.listeFleInt[str(180),'trigo'][0]
                    self.flecheActuelI.fleCouleur[3]=1
                    ###############################################################
                    ##############################"Pour la flèche, 
                    self.flecheDirecE.canvas.ask_update()
                    #Pour la flèche intérieur

                    directionneur('alpha',self.axeX,self.angleCible,self.ratioE,
                              self.listeAngle,self.flecheDirecE)
            
                    self.angleMesureI=calcul_angle(self.nomDeProjection, False, False, self.axeY,
                                                   self.angleAxeY, self.angleAxeX)
    
                    #pour les angles intérieures
                    self.dincrement=1
                    for i in range(self.angleAxeY,self.angleAxeX,self.dincrement):
                        self.widgetI=self.listeAngle[str(i),str(self.ratioI)][0]
                        self.widgetI.couleur[3]=1
                    for i in range(-179,self.angleAxeY,1):
                        self.widgetI=self.listeAngleNeg[str(i),str(self.ratioI)][0]
                        self.widgetI.couleur[3]=0
                    #pour les angles extérieurs
                    self.dincrement=-1
                    self.angleNeg=self.listeAngle[str(self.angleCible),str(self.ratioE)][1]
                    
                    self.angleMesureE=calcul_angle(self.nomDeProjection, False, True, self.axeX,
                                                   self.angleAxeX, self.angleNeg)
    
                    for i in range(self.angleAxeX,self.angleNeg,self.dincrement):
                        self.widgetE=self.listeAngleNeg[str(i),str(self.ratioE)][0]
                        self.widgetE.couleur[3]=1
                    if 179-abs(self.angleNeg) !=0:
                         for i in range(self.angleNeg,-180,-1):
                             self.widgetE=self.listeAngleNeg[str(i),str(self.ratioE)][0]
                             if i>=self.angleNeg:
                                 self.widgetE.couleur[3]=1
                             else:self.widgetE.couleur[3]=0

            elif self.axeY=='yMoins':
                if self.axeX=='xPlus':
                    self.flecheActuelI.fleCouleur[3]=0
                    self.flecheActuelI=self.listeFleInt[str(0),'trigo'][0]
                    self.flecheActuelI.fleCouleur[3]=1
                    ###############################################################
                    ##############################"Pour la flèche, 
                    self.flecheDirecE.canvas.ask_update()

                    directionneur('beta',self.axeX,self.angleCible,self.ratioE,
                              self.listeAngle,self.flecheDirecE)
            
                    self.angleMesureI=calcul_angle(self.nomDeProjection, False, False, self.axeY,
                                                  self.angleAxeY, self.angleAxeX)
                    self.angleCibleNeg=self.listeAngle[str(self.angleCible),str(self.ratioE)][1]
                    self.betaNeg=transform_neg_beta(self.angleCibleNeg)

                    # puis l'angle extérieur
                    self.angleAxeYBetaNeg=transform_neg_beta(-90)
                    self.angleMesureE=calcul_angle(self.nomDeProjection, False, True,
                                              self.axeY, self.angleAxeYBetaNeg, self.betaNeg)
                    self.dincrement=-1
                    ##on va s'occuper des angles intérieurs
                    for i in range(359,-1,self.dincrement):
                        self.widgetI=self.listeAngle[str(i),str(self.ratioI)][0]
                        self.widgetE=self.listeAngle[str(i),str(self.ratioE)][0]
    
                        #On colorie les widgets intérieurs
                        if (i<self.angleAxeY):
                            self.widgetI.couleur[3]=1
                        else:
                            self.widgetI.couleur[3]=0
                        self.dincrement=1
                        #On colorie les widgets extérieurs
                        if i>=self.angleCible:
                            self.widgetE.couleur[3]=0
                        else:
                            self.widgetE.couleur[3]=1
                elif self.axeX=='xMoins':
                    self.flecheActuelI.fleCouleur[3]=0
                    self.flecheActuelI=self.listeFleInt[str(180),'horaire'][0]
                    self.flecheActuelI.fleCouleur[3]=1
                    ###############################################################
                    ##############################"Pour la flèche, 
                    self.flecheDirecE.canvas.ask_update()

                    directionneur('alpha',self.axeX,self.angleCible,self.ratioE,
                              self.listeAngle,self.flecheDirecE)
            
                    #rajouter et modier self.dincrement(Iet E notamment)#################
                    self.dincrement=1
                    self.angleMesureI=calcul_angle(self.nomDeProjection, False, False, self.axeY,
                                             self.angleAxeY, self.angleAxeX)
                    self.angleCibleNeg=self.listeAngle[str(self.angleCible),str(self.ratioE)][1]
                    self.betaNeg=transform_neg_beta(self.angleCibleNeg)
                    self.angleMesureE=calcul_angle(self.nomDeProjection, False, True, self.axeX,
                                                 self.angleAxeX, self.angleCibleNeg)
                    for i in range(0,360,self.dincrement):
                        self.widgetI=self.listeAngle[str(i),str(self.ratioI)][0]
                        self.widgetE=self.listeAngle[str(i),str(self.ratioE)][0]
                        self.angleNeg=self.listeAngle[str(self.angleCible),str(self.ratioI)][1]
                        iNeg=self.listeAngle[str(i),str(self.ratioE)][1]
                        
                    #On colorie les widgets intérieurs
                        if ((i>=self.angleAxeX) and (i<=self.angleAxeY)):
                            self.widgetI.couleur[3]=1
                        else:
                            self.widgetI.couleur[3]=0
                        self.dincrement=1
                        #On colorie les widgets extérieurs
                        if iNeg>=self.angleCibleNeg:
                            self.widgetE.couleur[3]=1
                        else:
                            self.widgetE.couleur[3]=0
        #########################BETA###################################
        ################################################################
        else:
            if self.axeX=='xPlus':
                if self.axeY=='yPlus':
                    self.flecheActuelI.fleCouleur[3]=0
                    self.flecheActuelI=self.listeFleInt[str(90),'trigo'][0]
                    self.flecheActuelI.fleCouleur[3]=1
                    directionneur('beta',self.axeY,self.angleCible,self.ratioE,
                              self.listeAngle,self.flecheDirecE)
                    
                    self.angleMesureI=calcul_angle(self.nomDeProjection, False, False, self.axeX,
                                                   self.angleAxeX, self.angleAxeY)
                    
                    self.angleAxeYBeta=transform_en_beta(self.angleAxeY)
                    self.betaRef=transform_en_beta(self.angleCible)

                    self.angleMesureE=calcul_angle(self.nomDeProjection, False, True,
                                              self.axeY, self.angleAxeYBeta, self.betaRef)
                    

                    self.dincrement=1
    
                    for i in range(0,359,self.dincrement):
                        self.widgetI=self.listeAngle[str(i),str(self.ratioI)][0]
                        #On colorie les widgets intérieurs
                        if ((i>=self.angleAxeX) and (i<=self.angleAxeY)):
                            self.widgetI.couleur[3]=1
                        else:
                            self.widgetI.couleur[3]=0
                    self.dincrement=1
                    for i in range(0,359,self.dincrement):
                        i=transform_en_beta(i)
                        #On colorie les widgets extérieurs
                        if i>=self.betaRef:
                            i=transform_en_alpha(i)
                            self.widgetE=self.listeAngle[str(i),str(self.ratioE)][0]
                            self.widgetE.couleur[3]=0
                        else:
                            i=transform_en_alpha(i)
                            self.widgetE=self.listeAngle[str(i),str(self.ratioE)][0]
                            self.widgetE.couleur[3]=1
                            
                elif self.axeY=='yMoins':
                    self.flecheActuelI.fleCouleur[3]=0
                    self.flecheActuelI=self.listeFleInt[str(270),'trigo'][0]
                    self.flecheActuelI.fleCouleur[3]=1
                    directionneur('beta',self.axeY,self.angleCible,self.ratioE,
                              self.listeAngle,self.flecheDirecE)
            
                    self.angleMesureI=calcul_angle(self.nomDeProjection, False, False, self.axeX,
                                                   self.angleAxeX, self.angleAxeY)
                    self.angleNeg=self.listeAngle[str(self.angleCible),
                                                  str(self.ratioE)][1]
                    self.angleBetaNeg=transform_neg_beta(self.angleNeg)
                    #pour les angles extérieures
                    # #puis l'angle extérieur
                    self.angleAxeYBetaNeg=transform_neg_beta(-90)
                    self.angleMesureE=calcul_angle(self.nomDeProjection, False, True,
                                              self.axeY, self.angleAxeYBetaNeg, self.angleBetaNeg)
                    self.dincrement=1
                    for i in range(self.angleAxeX,self.angleAxeY,self.dincrement):
                        self.widgetI=self.listeAngle[str(i),str(self.ratioI)][0]
                        self.widgetI.couleur[3]=1
                    for i in range(self.angleAxeY,359,self.dincrement):
                        self.widgetI=self.listeAngle[str(i),str(self.ratioI)][0]
                        self.widgetI.couleur[3]=0
                    #pour les angles extérieurs
                    self.dincrement=-1

                    #On transforme l'angle Axe Y dans le référentiel négatif de Bété
                    self.angleAxeYBetaNeg=transform_neg_beta(self.listeAngle[str(self.angleAxeY),
                                                  str(self.ratioE)][1])
                    
                    # self.angleMesureE=calcul_angle(self.angleDeProjection, False, True, self.axeX,
                    #                                self.angleAxeX, self.angleNeg)
                    for i in range(self.angleAxeYBetaNeg,self.angleBetaNeg,self.dincrement):

                        i=transform_neg_alpha(i)

                        self.widgetE=self.listeAngleNeg[str(i),str(self.ratioE)][0]
                        self.widgetE.couleur[3]=1
                    if 180-self.angleBetaNeg>0:
                        
                        for i in range(self.angleBetaNeg,-180,-1):
                             j=transform_neg_alpha(i)
                             self.widgetE=self.listeAngleNeg[str(j),str(self.ratioE)][0]
                             if i>=self.angleBetaNeg:
                                 self.widgetE.couleur[3]=1
                             else:self.widgetE.couleur[3]=0
########################
            elif self.axeX=='xMoins':
                if self.axeY=='yPlus':
                    ###############################################################
                    ##############################"Pour la flèche, 
                    self.flecheDirecE.canvas.ask_update()
                    self.flecheActuelI.fleCouleur[3]=0
                    self.flecheActuelI=self.listeFleInt[str(90),'horaire'][0]
                    self.flecheActuelI.fleCouleur[3]=1
                    directionneur('beta',self.axeY,self.angleCible,self.ratioE,
                              self.listeAngle,self.flecheDirecE)

            
                    self.angleMesureI=calcul_angle(self.nomDeProjection, False, False, self.axeX,
                                                    self.angleAxeX, self.angleAxeY)
                    self.angleAxeYBeta=transform_en_beta(self.angleAxeY)
                    self.betaRef=transform_en_beta(self.angleCible)

                    self.angleMesureE=calcul_angle(self.nomDeProjection, False, True,
                                              self.axeY, self.angleAxeYBeta, self.betaRef)
                    self.angleBetaRef=transform_en_beta(self.angleCible)
                    self.dincrement=-1
                    self.angleAxeBetaY=transform_en_beta(self.angleAxeY)
                    ##on va s'occuper des angles intérieurs

                    for i in range(359,-1,self.dincrement):
                        self.widgetI=self.listeAngle[str(i),str(self.ratioI)][0]

                        #On colorie les widgets intérieurs
                        if (i>=self.angleAxeY) and (i<=self.angleAxeX):
                            self.widgetI.couleur[3]=1
                        else:

                            self.widgetI.couleur[3]=0
                        i=transform_en_beta(i)

                        self.dincrement=1
                        #On colorie les widgets extérieurs
                        if i>=self.angleBetaRef:
                            i=transform_en_alpha(i)
                            self.widgetE=self.listeAngle[str(i),str(self.ratioE)][0]
                            self.widgetE.couleur[3]=0
                        else:
                            i=transform_en_alpha(i)
                            self.widgetE=self.listeAngle[str(i),str(self.ratioE)][0]
                            self.widgetE.couleur[3]=1
                
                elif self.axeY=='yMoins':
                    self.flecheActuelI.fleCouleur[3]=0
                    self.flecheActuelI=self.listeFleInt[str(270),'trigo'][0]
                    self.flecheActuelI.fleCouleur[3]=1
                    directionneur('beta',self.axeY,self.angleCible,self.ratioE,
                              self.listeAngle,self.flecheDirecE)
            
                    #rajouter et modier self.dincrement(Iet E notamment)#################
                    self.dincrement=1
                    self.angleAxeX=180
                    self.angleMesureI=calcul_angle(self.nomDeProjection, False, False, self.axeX,
                                                   self.angleAxeX, self.angleAxeY)
                    
                    self.angleCibleNeg=self.listeAngle[str(self.angleCible),str(self.ratioE)][1]
                    self.BetaNegRef=transform_neg_beta(self.angleCibleNeg)
                    self.angleAxeYBetaNeg=transform_neg_beta(-90)
                    self.angleMesureE=calcul_angle(self.nomDeProjection, False, True,
                                              self.axeY, self.angleAxeYBetaNeg, self.BetaNegRef)
                    for i in range(0,360,self.dincrement):
                        self.widgetI=self.listeAngle[str(i),str(self.ratioI)][0]
                        self.widgetE=self.listeAngle[str(i),str(self.ratioE)][0]
                        self.angleNeg=self.listeAngle[str(self.angleCible),str(self.ratioI)][1]
                        iNeg=self.listeAngle[str(i),str(self.ratioE)][1]
                        
                    #On colorie les widgets intérieurs
                        if ((i>=self.angleAxeX) and (i<=self.angleAxeY)):
                            self.widgetI.couleur[3]=1
                        else:
                            self.widgetI.couleur[3]=0
                        self.dincrement=1
                        iNeg=transform_neg_beta(iNeg)
                        #On colorie les widgets extérieurs
                        if iNeg>=self.BetaNegRef:
                            self.widgetE.couleur[3]=1
                        else:
                            self.widgetE.couleur[3]=0

class Interpreteur(Assembleur):
    #Il récupère les données de l'orchestreur
    #Il analyse et il calcul le bon résultat en fonction de l'état des éléments
    #du cercle
    angleDirec=NumericProperty(0)
    chiffreDirec=StringProperty('')
    literalDirec=StringProperty('')
    literalDirecEq=StringProperty('')
    literalDirecEqEq=StringProperty('')

    signeNumDir=StringProperty('')
    signeNumIn=StringProperty('')
    chiffreIndirec=StringProperty('')
    signeLitDir=StringProperty('')
    signeLitIndir=StringProperty('')
    literalIndirec=StringProperty('')
    signeLitDirEq=StringProperty('')
    signeLitIndirEq=StringProperty('')
    literalIndirecEq=StringProperty('')
    literalIndirecEqEq=StringProperty('')

    angleIndirecE=NumericProperty(0)
    angleIndirecI=NumericProperty(0)
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.j=0
        self.resultatDirec=[]
        self.resultatIndirec=[]
        if self.sens=='Indirect':
            self.angleDirec=self.directProjec*(-1)
            self.angleIndirecE=self.indirectExtProjec*(-1)
            self.angleIndirecI=self.indirectIntProjec*(-1)
            self.angleIndirec=self.angleIndirecE+self.angleIndirecI
            
        else:
            self.angleDirec=self.directProjec
            self.angleIndirecE=self.indirectExtProjec
            self.angleIndirecI=self.indirectIntProjec
            self.angleIndirec=self.angleIndirecE+self.angleIndirecI

        self.resultatDirec=determineur(self.angleProjection,self.angleSup,
                        True,self.angleDirec)
        self.resultatIndirec=determineur(self.angleProjection,self.angleSup,
                                         False,self.angleIndirec,self.angleIndirecE,
                                         self.angleIndirecI)

        self.equationNumerique=Zone_texte('Equation numérique : ',self.resultatDirec[0],
                                          self.resultatDirec[1],#cos
                                          self.resultatIndirec[0],#signeIndirec
                                          self.resultatIndirec[1],7.5/100)
        self.bind(signeNumDir=self.equationNumerique.setter('signe1'))
        self.bind(signeNumIn=self.equationNumerique.setter('signe2'))
        self.bind(chiffreDirec=self.equationNumerique.setter('projecDirec'))
        self.bind(chiffreIndirec=self.equationNumerique.setter('projecIndirec'))
        self.add_widget(self.equationNumerique)
        
        self.equationLiteral=Zone_texte('Equation litérale : ',self.resultatDirec[2],
                                        self.resultatDirec[3],self.resultatIndirec[2],
                                        self.resultatIndirec[3], 10.0/100)
        self.add_widget(self.equationLiteral)

        self.bind(literalDirec=self.equationLiteral.setter('projecDirec'))
        self.bind(literalIndirec=self.equationLiteral.setter('projecIndirec'))
        self.bind(signeLitDir=self.equationLiteral.setter('signe1'))
        self.bind(signeLitIndir=self.equationLiteral.setter('signe2'))
        self.equationLiteralEq=Zone_texte('Equation litérale équivalente : ',
                                          self.resultatDirec[4],
                                          self.resultatDirec[5],self.resultatIndirec[4],
                                          self.resultatIndirec[5],12.5/100)

        self.add_widget(self.equationLiteralEq)
        self.bind(literalDirecEq=self.equationLiteralEq.setter('projecDirec'))
        self.bind(literalIndirecEq=self.equationLiteralEq.setter('projecIndirec'))
        
        self.bind(signeLitDirEq=self.equationLiteralEq.setter('signe1'))
        self.bind(signeLitIndirEq=self.equationLiteralEq.setter('signe2'))
        self.bind(angleProjection=self.on_affiche_direct)
        self.bind(angleProjection=self.on_affiche_indirect_E)
        self.bind(angleProjection=self.on_affiche_indirect_I)
        self.bind(sens=self.on_affiche_direct)
        self.bind(sens=self.on_affiche_indirect_E)
        self.bind(sens=self.on_affiche_indirect_I)
        self.bind(directProjec=self.on_affiche_direct)
        self.bind(indirectExtProjec=self.on_affiche_indirect_E)
        self.bind(indirectIntProjec=self.on_affiche_indirect_I)
    def on_affiche_direct(self,directProjec,indirecExtProjec,**kwargs):
        if self.sens=='Indirect':
            self.angleDirec=self.directProjec*(-1)
        else:
            self.angleDirec=self.directProjec
            
        self.resultatDirec=determineur(self.angleProjection,self.angleSup,
                        True,self.angleDirec)
        if self.angleProjection=='alpha':
            self.equationNumerique.couleurDirec=[1,0,0,1]
            self.equationLiteral.couleurDirec=[1,0,0,1]
            self.equationLiteralEq.couleurDirec=[1,0,0,1]
            self.signeNumDir=self.resultatDirec[0]
            self.chiffreDirec=self.resultatDirec[1]
            self.signeLitDir=self.resultatDirec[2]
            self.literalDirec=self.resultatDirec[3]
            self.signeLitDirEq=self.resultatDirec[4]
            self.literalDirecEq=self.resultatDirec[5]
        else:
            self.equationNumerique.couleurDirec=[0.18,0,0.42,1]
            self.equationLiteral.couleurDirec=[0.18,0,0.42,1]
            self.equationLiteralEq.couleurDirec=[0.18,0,0.42,1]
            self.signeNumIn=self.resultatDirec[0]
            self.chiffreIndirec=self.resultatDirec[1]
            self.signeLitIndir=self.resultatDirec[2]
            self.literalIndirec=self.resultatDirec[3]
            self.signeLitIndirEq=self.resultatDirec[4]
            self.literalIndirecEq=self.resultatDirec[5]
            
    def on_affiche_indirect_E(self,directProjec,indirectExtProjec,**kwargs):
        if self.sens=='Indirect':
            self.angleIndirecE=self.indirectExtProjec*(-1)
            self.angleIndirecI=self.indirectIntProjec*(-1)
            self.angleIndirec=self.angleIndirecE+self.angleIndirecI

        else:
            self.angleIndirecE=self.indirectExtProjec
            self.angleIndirecI=self.indirectIntProjec
            self.angleIndirec=self.angleIndirecE+self.angleIndirecI


        self.resultatIndirec=determineur(self.angleProjection,self.angleSup,
                                         False,self.angleIndirec,self.angleIndirecE,
                                         self.angleIndirecI)
        if self.angleProjection=='alpha':
            self.equationNumerique.couleurIndirec=[0.18,0,0.42,1]
            self.equationLiteral.couleurIndirec=[0.18,0,0.42,1]
            self.equationLiteralEq.couleurIndirec=[0.18,0,0.42,1]
            self.signeNumIn=self.resultatIndirec[0]
            self.chiffreIndirec=self.resultatIndirec[1]
            self.signeLitIndir=self.resultatIndirec[2]
            self.literalIndirec=self.resultatIndirec[3]
            self.signeLitIndirEq=self.resultatIndirec[4]
            self.literalIndirecEq=self.resultatIndirec[5]
        else:
            self.equationNumerique.couleurIndirec=[1,0,0,1]
            self.equationLiteral.couleurIndirec=[1,0,0,1]
            self.equationLiteralEq.couleurIndirec=[1,0,0,1]

            #En béta, l'apha de direct devient son indirect
            #et l'alpha d'indirect devient son direct
            self.signeNumDir=self.resultatIndirec[0]
            self.chiffreDirec=self.resultatIndirec[1]

            self.signeLitDir=self.resultatIndirec[2]
            self.literalDirec=self.resultatIndirec[3]

            self.signeLitDirEq=self.resultatIndirec[4]
            self.literalDirecEq=self.resultatIndirec[5]
    def on_affiche_indirect_I(self,directProjec,indirectExtProjec,**kwargs):
        if self.sens=='Indirect':
            self.angleIndirecE=self.indirectExtProjec*(-1)
            self.angleIndirecI=self.indirectIntProjec*(-1)
            self.angleIndirec=self.angleIndirecE+self.angleIndirecI

        else:
            self.angleIndirecE=self.indirectExtProjec
            self.angleIndirecI=self.indirectIntProjec
            self.angleIndirec=self.angleIndirecE+self.angleIndirecI


        self.resultatIndirec=determineur(self.angleProjection,self.angleSup,
                                         False,self.angleIndirec,self.angleIndirecE,
                                         self.angleIndirecI)
        if self.angleProjection=='alpha':
            self.equationNumerique.couleurIndirec=[0.18,0,0.42,1]
            self.equationLiteral.couleurIndirec=[0.18,0,0.42,1]
            self.equationLiteralEq.couleurIndirec=[0.18,0,0.42,1]
            self.signeNumIn=self.resultatIndirec[0]
            self.chiffreIndirec=self.resultatIndirec[1]
            self.signeLitIndir=self.resultatIndirec[2]
            self.literalIndirec=self.resultatIndirec[3]
            self.signeLitIndirEq=self.resultatIndirec[4]
            self.literalIndirecEq=self.resultatIndirec[5]
        else:
            self.equationNumerique.couleurIndirec=[1,0,0,1]
            self.equationLiteral.couleurIndirec=[1,0,0,1]
            self.equationLiteralEq.couleurIndirec=[1,0,0,1]
            #En béta, l'apha de direct devient son indirect
            #et l'alpha d'indirect devient son direct
            self.signeNumDir=self.resultatIndirec[0]
            self.chiffreDirec=self.resultatIndirec[1]
            self.signeLitDir=self.resultatIndirec[2]
            self.literalDirec=self.resultatIndirec[3]
            self.signeLitDirEq=self.resultatIndirec[4]
            self.literalDirecEq=self.resultatIndirec[5]

class Afficheur(Interpreteur):
    #L'afficheur en s'appuyant sur les données récoltées par l'interpreteur
    #affiche les différentes informations comme l'angle alpha&béta et les degrés
    #sur le cercle
    #L'afficheur agence entre eux les objets de la classe Affiche
    #La classe Affiche récupère : l'angle, le rayon et le texte à afficher
    #le rôle de l'afficheur est également de mettre à jour les données
    #lors d'une évolution sur le cercle : chgt de cercle, 
    #Toujours dans son rôle l'afficheur, il calcule la taille idéale en 
    #fonction de la police donnée par l'utilisateur

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        Window.bind(on_resize=self.on_commence)
    
    
    def on_commence(self,*largs):
        ##Cette fonction fait ## choses: 
        #-calculer la largeur à occuper
        #-la largeur totale occupée
        #-calculer la proportion de la plus grande étiquette->équationLiteralEq
        #-Calculer la largeur qu'elle devrait occuper
        #-Déterminer la police pour pouvoir respecter la largeur à occuper
        self.largeurAocc=((Window.width*0.8)-(Window.width*0.2))
        self.place=self.equationLiteralEq.ids.etiquette.size[0]

        self.equationLiteralEq.ids.etiquette.texture_update()
        self.equationLiteralEq.ids.signe1.texture_update()
        self.equationLiteralEq.ids.projecDirec.texture_update()
        self.equationLiteralEq.ids.signe2.texture_update()
        self.equationLiteralEq.ids.projecIndirec.texture_update()
        self.equationLiteral.ids.projecIndirec.texture_update()
        self.equationLiteralEq.ids.projecDirec.texture_update()
        self.equationLiteral.ids.projecDirec.texture_update()
        self.tailleProjection=0
        #Si l'angle de projection est alpha 
        if self.angleProjection=='alpha':
            self.tailleProjection=self.equationLiteral.ids.projecIndirec.size[0]
        else:
            self.tailleProjection=self.equationLiteral.ids.projecDirec.size[0]
        self.largeurOcc=0
        self.largeurOcc=self.largeurOcc+self.tailleProjection
        self.largeurOcc=self.largeurOcc+self.tailleProjection
        #Nous calculons la largeur effective quand la police est égale à 15
        self.largeurOcc=self.largeurOcc+self.equationLiteralEq.ids.etiquette.size[0]    
        self.largeurOcc=self.largeurOcc+self.equationLiteralEq.ids.signe1.size[0] 
        self.largeurOcc=self.largeurOcc+self.equationLiteralEq.ids.axeX.size[0]
        self.largeurOcc=self.largeurOcc+self.equationLiteralEq.ids.signe2.size[0]
        self.largeurOcc=self.largeurOcc+self.equationLiteralEq.ids.axeY.size[0]
        #Pour gérer l'espacement en pourcentage
        self.equationLiteralEq.espacement=1
        self.largeurOccTest=self.largeurOcc+(6*self.equationLiteralEq.espacement)


        self.proporEspacement=round((self.equationLiteralEq.espacement*6)/self.largeurOccTest,2)

        while ((self.proporEspacement >0.15) or (self.proporEspacement<0.1)):
             self.equationLiteralEq.espacement+=1
             self.largeurOccTest=self.largeurOcc+(6*self.equationLiteralEq.espacement)
             self.proporEspacement=round((self.equationLiteralEq.espacement*6)/self.largeurOccTest,2)
        self.largeurOcc=self.largeurOccTest
        #de façon unitaire
        self.proporEspacement=round((self.equationLiteralEq.espacement)/self.largeurOcc,2)
        #l'espacement ainsi que la largeur totale sont maintenant définis
        
        self.proporEtiq=round(self.equationLiteralEq.ids.etiquette.size[0]/self.largeurOcc,2)
        self.proporSign=round(self.equationLiteralEq.ids.signe1.size[0]/self.largeurOcc,2)
        self.proporAxe=round(self.equationLiteralEq.ids.axeX.size[0]/self.largeurOcc,2)
        self.proporProjec=round(self.tailleProjection/self.largeurOcc,2)
        #La largeur qu'elle devrait occuper
        self.largeurEtiquette=round(self.proporEtiq*self.largeurAocc,2)
        self.largeurSign=round(self.proporSign*self.largeurAocc,2)
        self.largeurAxe=round(self.proporAxe*self.largeurAocc,2)
        self.largeurProjec=round(self.proporProjec*self.largeurAocc,2)
        self.largeurEspace=round(self.proporEspacement*self.largeurAocc,2)
        #on initialise la boucle
        self.equationLiteralEq.fontSize=1
        while ((self.equationLiteralEq.ids.etiquette.size[0]>=1.05*self.largeurEtiquette) or
               (self.equationLiteralEq.ids.etiquette.size[0]<=0.95*self.largeurEtiquette)):
            self.equationLiteralEq.fontSize+=1
            self.equationLiteralEq.ids.etiquette.texture_update()
        self.equationLiteral.fontSize=self.equationLiteralEq.fontSize
        self.equationNumerique.fontSize=self.equationLiteralEq.fontSize
        #Nous allons maintenant fixer le départ du signe plus des autres objets
        #Le but est d'avoir quelque chose d'homogène au niveau de l'interface
        self.equationLiteralEq.ids.etiquette.texture_update()
        #Nous vérifions que la taille de la police est compatible avec la hauteur
        #Pour positionner sur la verticale
        self.hauteur=(Window.height*0.15)
        self.equationLiteralEq.hauteur=self.hauteur
        self.equationLiteral.hauteur=self.equationLiteralEq.hauteur-self.equationLiteralEq.ids.etiquette.size[1]
        self.equationNumerique.hauteur=self.equationLiteral.hauteur-self.equationLiteralEq.ids.etiquette.size[1]
        while self.equationNumerique.hauteur<0 :
            self.equationLiteralEq.fontSize-=0.5
            self.equationLiteralEq.ids.etiquette.texture_update()
            self.equationLiteralEq.hauteur=self.hauteur
            self.equationLiteral.hauteur=self.equationLiteralEq.hauteur-self.equationLiteralEq.ids.etiquette.size[1]
            self.equationNumerique.hauteur=self.equationLiteral.hauteur-self.equationLiteralEq.ids.etiquette.size[1]
        self.equationLiteral.fontSize=self.equationLiteralEq.fontSize
        self.equationNumerique.fontSize=self.equationLiteralEq.fontSize
        #Pour positionner l'étiquette
        self.equationLiteralEq.depart=0.2*Window.width
        self.equationNumerique.depart=0.2*Window.width
        self.equationLiteral.depart=0.2*Window.width
        
        self.equationLiteral.ids.signe1.texture_update()
        self.equationLiteral.ids.axeX.texture_update()
        self.equationLiteral.ids.signe2.texture_update()
        self.equationLiteral.ids.projecDirec.texture_update()
        self.equationLiteral.ids.projecIndirec.texture_update()
        #Pour positionner le signe de projectDirect
        self.place=self.largeurEtiquette+self.largeurEspace
        self.equationLiteralEq.departS=self.equationLiteralEq.depart+self.place
        self.equationNumerique.departS=self.equationLiteralEq.depart+self.place
        self.equationLiteral.departS=self.equationLiteralEq.depart+self.place
        #Pour positionner projecDirect
        self.place=self.largeurSign+self.largeurEspace
        self.equationLiteralEq.departPd=self.equationLiteralEq.departS+self.place
        self.equationNumerique.departPd=self.equationLiteralEq.departS+self.place
        self.equationLiteral.departPd=self.equationLiteralEq.departS+self.place
        #Pour l'axe X
        self.place=self.largeurProjec+self.largeurEspace
        self.equationLiteralEq.departAxeX=self.equationLiteralEq.departPd+self.place
        self.equationNumerique.departAxeX=self.equationLiteralEq.departPd+self.place
        self.equationLiteral.departAxeX=self.equationLiteralEq.departPd+self.place
        #Pour le signe de projection Indirecte
        self.place=self.largeurAxe+self.largeurEspace
        self.equationLiteralEq.departS2=self.equationLiteralEq.departAxeX+self.place
        self.equationNumerique.departS2=self.equationLiteralEq.departAxeX+self.place
        self.equationLiteral.departS2=self.equationLiteralEq.departAxeX+self.place
        #Pour la projection Indirecte
        self.place=self.largeurSign+self.largeurEspace
        self.equationLiteralEq.departPid=self.equationLiteralEq.departS2+self.place
        self.equationNumerique.departPid=self.equationLiteralEq.departS2+self.place
        self.equationLiteral.departPid=self.equationLiteralEq.departS2+self.place
        #Pour positionner l'axe Y
        self.place=self.largeurProjec+self.largeurEspace
        self.equationLiteralEq.departAxeY=self.equationLiteralEq.departPid+self.place
        self.equationNumerique.departAxeY=self.equationLiteralEq.departPid+self.place
        self.equationLiteral.departAxeY=self.equationLiteralEq.departPid+self.place

class Zone_texte(Widget):
    somme=StringProperty('')
    projecDirec=StringProperty('')
    libelle=StringProperty('')
    signe1=StringProperty('')
    signe2=StringProperty('')
    projecIndirec=StringProperty('')
    equation=StringProperty('')
    hauteur=NumericProperty(0)
    depart=NumericProperty(0)
    departS=NumericProperty(0)
    departS2=NumericProperty(0)
    departPd=NumericProperty(0)
    departPid=NumericProperty(0)
    
    departAxeX=NumericProperty(0)
    departY=NumericProperty(0)
    departAxeY=NumericProperty(0)
    couleurDirec=ListProperty([])
    couleurIndirec=ListProperty([])
    fontSize=NumericProperty(15)
    espacement=NumericProperty(8)
    def __init__(self,libelle,signe1,projecDirec,
                 signe2,projecIndirec,ratioHauteur,**kwargs):
        super().__init__(**kwargs)
        self.signe1=signe1
        self.signe2=signe2
        self.projecDirec=projecDirec
        self.couleurDirec=[1,0,0,1]
        self.couleurIndirec=[0.18,0,0.42,1]
        self.projecIndirec=projecIndirec
        self.libelle=libelle
        self.ratioHauteur=ratioHauteur
        self.hauteur=ratioHauteur*Window.height
        self.depart=Window.width*0.15



     
    #Cette fonction a pour but de calculer la longueur utilisée, la longueur à utiliser
    #et à correspondre la longueur utilisée avec la longueur à utiliser


class MyApp(App):
    def build(self):
        Window.clearcolor = (0.95, 0.94, 0.88, 0.5)
        self.a=Afficheur()
        return self.a

    def on_start(self, *args):
        print('ok')
        self.a.on_commence()

        
if __name__ == '__main__':
    MyApp().run()
  