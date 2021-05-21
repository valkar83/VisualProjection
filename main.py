from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.togglebutton import ToggleButton
from kivy.properties import NumericProperty,StringProperty,BooleanProperty,ListProperty
from kivy.core.window import Window
from kivy.weakproxy import WeakProxy

from math import cos,sin,radians

from cadreur import Cadreur
from bouton import Bouton_centre,Boutons_cercle,points_du_cercle
from fleche import Fleche,IndicSens
from projection import ProjectionDirect,ProjectionIndirect
from fleche import longueur

    
def points_cardinaux(centrex,centrey,r,angle):
    xpos=round(centrex+r*cos(radians(angle)),2)
    ypos=round(centrey+r*sin(radians(angle)),2)
    #La coordonnée y de xPdroit se confond avec la coordonnée y du centre
    #Si x position est supérieure à centre x, alors x Plus, 
    #Le même raisonnement est appliqué pour les autres conditions
    if ((centrey*0.99<ypos)and(ypos<centrey*1.01)) and xpos>centrex:
        if ((angle>= 358.5) and (angle <= 360)) or  ((angle >=0) and (angle <= 1.5)):
            angle=0
        return True,"xPdroit",xpos,ypos,angle
    elif ypos>centrey and ((xpos<1.01*centrex) and (xpos>0.99*centrex)):
        if angle <= 91.5 and angle >= 88.5:
            angle=90
        return True,"yPhaut",xpos,ypos,angle
    elif ((centrey*0.99<ypos)and(ypos<centrey*1.01)) and xpos<centrex:
        if angle <= 181.5 and angle >= 178.5:
            angle=180
        return True,"xPgauche",xpos,ypos,angle
    elif ypos<centrey and ((xpos<1.01*centrex) and (xpos>0.99*centrex)):
        if angle <= 271.5 and angle >= 268.5:
            angle=270
        return True,"yPbas",xpos,ypos,angle
    else:
        return False,""
    


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
        #Si l'angle complémentaire est activé
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
        #Si l'angle complémentaire n'est pas activé
        else:
            if angle1>=0:
                signeLiteralDirecEqEq=' + '
                literalDirecEqEq='cos('+lettreAngle+'/)'
                if angle1==0:
                    signeLiteralDirecEq=' + '
                    literalDirecEq='cos('+lettreAngle+') = +1'
                elif angle1==90:
                    signeLiteralDirecEq=' + '
                    literalDirecEq='cos('+lettreAngle+') = 0'
                elif angle1==180:
                    signeLiteralDirecEq=' + '
                    literalDirecEq='cos('+lettreAngle+') = -1'
                elif angle1==270:
                    signeLiteralDirecEq=' + '
                    literalDirecEq='cos('+lettreAngle+') = 0'
                else:
                    signeLiteralDirecEq=' + '
                    literalDirecEq='cos('+lettreAngle+')'
            else:
                signeLiteralDirecEqEq=' + '
                literalDirecEqEq='cos('+lettreAngle+')'
                if angle1==-90:
                    signeLiteralDirecEq=' + '
                    literalDirecEq='cos(-'+lettreAngle+') = 0'
                elif angle1==-180:
                    signeLiteralDirecEq=' + '
                    literalDirecEq='cos(-'+lettreAngle+') = -1'
                elif angle1==-270:
                    signeLiteralDirecEq=' + '
                    literalDirecEq='cos(-'+lettreAngle+') = 0'
                elif angle1==270:
                    signeLiteralDirecEq=' + '
                    literalDirecEq='cos(-'+lettreAngle+') = 0'
                else:
                    signeLiteralDirecEq=' + '
                    literalDirecEq='cos(-'+lettreAngle+')'
                
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
    
                elif angleI==-90:
                    
                    signeIndirec='+'
                    chiffreIndirec='cos('+str(angle1)+')'
                    signeLiteral='+'
                    literalIndirec='cos('+lettreAngle+'-π/2)'
                    if angleE==270:
                        signeLiteralEq='+'
                        literalIndirecEq='sin('+lettreAngle+')=-1'
                    else:
                        signeLiteralEq='+'
                        literalIndirecEq='sin('+lettreAngle+')'
  

            #L'angle E est négatif
            else:
                if angleI==-90:
                    signeIndirec='+'
                    chiffreIndirec='cos('+str(angle1)+')'
                    signeLiteral='+'
                    literalIndirec='cos(-'+lettreAngle+'-π/2)'
                    if angleE==-270:
                        signeLiteralEq='-'
                        literalIndirecEq='sin('+lettreAngle+') = +1'
                    else:
                        signeLiteralEq='-'
                        literalIndirecEq='sin('+lettreAngle+')'
                    
                #forcément +270
                elif angleI==270:
                    signeIndirec='+'
                    chiffreIndirec='cos('+str(angle1)+')'
                    signeLiteral='+'
                    literalIndirec='cos(-'+lettreAngle+'+3π/2)'
                    if angleE==-90:
                        signeLiteralEq='+'
                        literalIndirecEq='sin('+lettreAngle+') = -1'
                    elif angleE==-180:
                        signeLiteralEq='+'
                        literalIndirecEq='sin('+lettreAngle+') = +1'            
                    else:
                        signeLiteralEq='+'
                        literalIndirecEq='sin('+lettreAngle+')'
                
                else:
                    if angleE==-180:
                        signeIndirec='+'
                        chiffreIndirec='cos('+str(angle1)+')'
                        signeLiteral='+'
                        literalIndirec='cos(π/2-'+lettreAngle+')'
                        if angleI==90:
                            signeLiteralEq='+'
                            literalIndirecEq='sin('+lettreAngle+') = 0'
                        else:
                            print(angle1)
                            print(angleE)
                            print(angleI)
                            print('bizarre1')
                    else:
                        print(angle1)
                        print(angleE)
                        print(angleI)
                        print('bizarre2')


            return signeIndirec,chiffreIndirec,signeLiteral,literalIndirec,signeLiteralEq,literalIndirecEq

        else:
            print('ok')
            #L'angle est positif
            if angleE>=0:
                if angleI==-90:
                    signeIndirec='+'
                    chiffreIndirec='cos('+str(angle1)+')'
                    signeLiteral='+'
                    literalIndirec='cos('+lettreAngle+'-π/2)'
                    if angleE==90: 
                        signeLiteralEq='+'
                        literalIndirecEq='sin('+lettreAngle+') = +1'
                    elif angleE==270:
                        signeLiteralEq='+'
                        literalIndirecEq='sin('+lettreAngle+') = -1'
                    else:
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


#####################                         ################################
#Créer les classes de type Widget

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
    changePtsSpeciaux=BooleanProperty(False)
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
                self.etatActuel="xPdroit"
                self.etatChange="xPgauche"
                self.ptPlusx=self.ptsSpeciaux[self.etatActuel][0]
                self.ptPlusy=self.ptsSpeciaux[self.etatActuel][1]
                self.angleAxe=self.ptsSpeciaux[self.etatActuel][2]
                self.ptxVirtuel=self.ptPlusx
                self.ptyVirtuel=self.ptPlusy
                self.hauteurWidget=self.largeurCanva*2
                self.largeurWidget=longueur(self.centrex, self.centrey,
                                            self.ptPlusx,self.ptPlusy)
            else:
                self.etatActuel='yPhaut'
                self.etatChange='yPbas'
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

                    if self.etatChange=='xPgauche':
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
                    if self.etatChange=='yPbas':
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
                if self.etatActuel=='xPgauche':
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
                if self.etatActuel=='yPbas':
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
        #Cette variable est un indicateur de changement
        #Quand sa valeur change, cela enclenche des changements
        self.changePtsSpeciaux=True
class Choix_angle(Cadreur,ToggleButton):
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
#ex et ey sont les 2 points de coordonnées de la barre utilisateur

    ex=NumericProperty(0)
    ey=NumericProperty(0)
    sens=StringProperty('')
    directProjec=NumericProperty(0)
    indirectIntProjec=NumericProperty(0)
    indirectExtProjec=NumericProperty(0)
    angleProjection=StringProperty('')
    angleSup=BooleanProperty(False)
    
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.listAngleSpeciaux=[]
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
            #Pour constituer la liste des angles spéciaux : la liste des angles
            #associés à des textes
            if (i%30==0) and (i!=360):
                self.listAngleSpeciaux.append(self.chaine)
        self.boutonCentre=Bouton_centre()

        self.flecheBarreX=Fleche(self.bxPlus,self.boutonCentre,20.0,'axeX')
        self.flecheBarreX.fleCouleur=self.gris
        self.add_widget(self.flecheBarreX)
        #On associe la flèche à by
        self.flecheBarreY=Fleche(self.byPlus,self.boutonCentre,20.0,'axeY')
        self.flecheBarreY.fleCouleur=self.gris
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
        if ((self.axeX=='xPdroit') and (self.axeY=='yPhaut')) or ((self.axeX=='xPgauche') and (self.axeY=='yPbas')):
            self.sens='Direct'
        else:
            self.sens='Indirect'   
        self.bind(r=self.on_chgt)
        self.angleProjection='alpha'
        self.pjx=ProjectionDirect('xPdroit','alpha',self.bx.etatActuel,self.bx.angleAxe,
                                  self.by.etatActuel,self.by.angleAxe,self.cible.angle)
        self.pjx=WeakProxy(self.pjx)
        self.add_widget(self.pjx)
        #Le sens du repère        
        self.pjy=ProjectionIndirect('yPhaut','alpha',self.bx.etatActuel,self.bx.angleAxe,
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


        
        #Ici nous créons la classe qui représente graphiquement le sens
        self.indication=IndicSens(self.sens)
        self.add_widget(self.indication)
        #on lie la propriété de sens Assembleur à la propriété sens IndicSens
        self.bind(sens=self.indication.setter('sens'))

        self.btd=Choix_angle('δ',self.ratioH*0.5,0.11)
        ##On crééer les boutons pour le choix des angles
        self.bta=Choix_angle('α',self.ratioH*0.7,0.07)
        self.btb=Choix_angle('ß',self.ratioH*0.7,0.15)
        
        self.add_widget(self.bta)
        self.add_widget(self.btb)
        self.add_widget(self.btd)
        self.bta.bind(state=self.on_angle)
        self.btb.bind(state=self.on_angle)

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


class Interpreteur(Assembleur):
    #Il récupère les données de l'assembleur
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
   
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.labelDegre=[]
        self.lxPdroit=Label_x('xPdroit','+',self.gris)
        self.lxPgauche=Label_x('xPgauche','-',self.gris)
        self.lyPhaut=Label_y('yPhaut','+',self.gris)
        self.lyPbas=Label_y('yPbas','-',self.gris)
        
        
        #Au tour des labels maintenant
        self.angleAffiche=Label_angle('α',self.marron)
        if self.sens=='Direct':
            self.indicSensAffiche=Label_angle('sens trigonomètrique',[0,1,0,1])
        else:
            self.indicSensAffiche=Label_angle('sens horaire',[0,1,0,1])
        for i in range(12):
            self.angleDegre=Label_angle(str(i*30)+'°',self.marron)
            self.add_widget(self.angleDegre)
            self.labelDegre.append(self.angleDegre)
        self.add_widget(self.lxPdroit)
        self.add_widget(self.lxPgauche)
        self.add_widget(self.lyPhaut)
        self.add_widget(self.lyPbas)
        self.add_widget(self.angleAffiche)
        
        self.add_widget(self.indicSensAffiche)

        self.bx.bind(etatActuel=self.on_direction)
        self.by.bind(etatActuel=self.on_direction)
        Window.bind(on_resize=self.on_commence)
        self.flecheBarreX.bind(aMaj=self.on_replacement)
        #On relie l'indicateur de changement des axes spéciaux aux fonctions
        #suivantes
        self.bx.bind(changePtsSpeciaux=self.on_com_bx)
        self.by.bind(changePtsSpeciaux=self.on_com_by)
        #Quand le cercle change de direction : horaire <> trigo
        self.pjx.bind(angleMesure=self.on_mouv_angle)

        self.bind(r=self.on_commenceLabel)
        #Changement lorsque angle de projection change de valeur
        self.bind(angleProjection=self.on_commenceLabel)
    def on_direction(self,bx,by):#On surcharge la méthode de la classe parent
        #Cette fonction ne gère que la position des flèches sur les barres
        #Il peut envoyer un signal au sens flèche qui modifiera la position 
        #de la flèche

        self.axeX=self.bx.etatActuel
        self.axeY=self.by.etatActuel
        if self.axeX=='xPdroit':
            self.flecheBarreX.ctr=self.bxPlus
            self.lxPdroit.signe='+'
            self.lxPgauche.signe='-'
        else:
            self.flecheBarreX.ctr=self.bxMoins
            self.lxPdroit.signe='-'
            self.lxPgauche.signe='+'
        if self.axeY=='yPhaut':
            self.flecheBarreY.ctr=self.byPlus
            self.lyPhaut.signe='+'
            self.lyPbas.signe='-'
        else:
            self.flecheBarreY.ctr=self.byMoins
            self.lyPhaut.signe='-'
            self.lyPbas.signe='+'
        if ((self.axeX=='xPdroit') and (self.axeY=='yPhaut')) or ((self.axeX=='xPgauche') and (self.axeY=='yPbas')):
            self.sens='Direct'
            self.indicSensAffiche.nom='Sens trigonomètrique'
        else:
            self.sens='Indirect'
            self.indicSensAffiche.nom='Sens horaire'

        self.on_commenceLabel()
        
    #Pour mettre à jour la position de la flèche
    def on_replacement(self,*largs):
        if self.flecheBarreX.aMaj==True:
            self.pjy.flecheDirecE.on_maj(*largs)
            self.pjx.flecheDirec.on_maj(*largs)
            self.flecheBarreX.aMaj=False
            
    def on_commence(self,*largs):
        ##Cette méthode fait ## choses: 
        #-calculer la largeur à occuper
        #-la largeur totale occupée
        #-calculer la proportion de la plus grande étiquette->équationLiteralEq
        #-Calculer la largeur qu'elle devrait occuper
        #-Déterminer la taille de police pour pouvoir respecter la largeur à occuper
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
        self.on_commenceAxe()

    def on_commenceAxe(self,*largs):
        #pour gérer xLabel et yLabel
        #Taille police&image x_label et y_label
        self.lxPdroit.ids.signeX.font_size=self.equationLiteralEq.fontSize
        self.lxPgauche.ids.signeX.font_size=self.equationLiteralEq.fontSize
        self.lyPhaut.ids.signeY.font_size=self.equationLiteralEq.fontSize
        self.lyPbas.ids.signeY.font_size=self.equationLiteralEq.fontSize
        #Positionnement x et y des 4 widgets axes
        #Pour x à droite
        self.lxPdroit.ids.vectxGris.texture_update()   
        self.lxPdroit.ids.signeX.texture_update()   
        self.lxPdroit.ids.signeX.pos[0]=self.bx.ptsSpeciaux['xPdroit'][0]-\
            (self.btLCercl*1.2)-self.largeurEspace-self.lxPdroit.ids.vectxGris.size[0]
        self.lxPdroit.ids.vectxGris.pos[0]=self.lxPdroit.ids.signeX.pos[0]+\
            self.lxPdroit.ids.signeX.size[0]+self.largeurEspace*(2/10)
        self.lxPdroit.ids.signeX.pos[1]=self.bx.ptsSpeciaux['xPdroit'][1]+(self.largeurEspace*1.7)
        self.lxPdroit.ids.vectxGris.pos[1]=self.lxPdroit.ids.signeX.pos[1]
        #pour x à gauche
        self.lxPgauche.ids.vectxGris.texture_update()   
        self.lxPgauche.ids.signeX.texture_update()   

        self.lxPgauche.ids.signeX.pos[0]=self.bx.ptsSpeciaux['xPgauche'][0]+\
            self.btLCercl
       

        self.lxPgauche.ids.vectxGris.pos[0]= self.lxPgauche.ids.signeX.pos[0]+ \
            self.lxPgauche.ids.signeX.size[0]+(self.largeurEspace*1/2)

        self.lxPgauche.ids.signeX.pos[1]=self.bx.ptsSpeciaux['xPgauche'][1]+self.largeurEspace
        self.lxPgauche.ids.vectxGris.pos[1]=self.lxPgauche.ids.signeX.pos[1]
        #pour y en haut
        self.lyPhaut.ids.vectyGris.texture_update()   
        self.lyPhaut.ids.signeY.texture_update()   
        self.lyPhaut.ids.signeY.pos[1]=self.by.ptsSpeciaux['yPhaut'][1]-\
            self.btHCercl-self.lyPhaut.ids.signeY.size[1]
        self.lyPhaut.ids.vectyGris.pos[1]=self.lyPhaut.ids.signeY.pos[1]
        self.lyPhaut.ids.signeY.pos[0]=self.by.ptsSpeciaux['yPhaut'][0] -\
            self.largeurEspace-self.lyPhaut.ids.signeY.size[0]-2.5*self.btLCercl

        self.lyPhaut.ids.vectyGris.pos[0]=self.lyPhaut.ids.signeY.pos[0] +\
            self.lyPhaut.ids.signeY.size[0]+(self.largeurEspace*0.4)

        #pour y en bas
        self.lyPbas.ids.vectyGris.texture_update()   
        self.lyPbas.ids.signeY.texture_update()      

        self.lyPbas.ids.signeY.pos[1]=self.by.ptsSpeciaux['yPbas'][1]+\
            self.btHCercl
        self.lyPbas.ids.vectyGris.pos[1]=self.lyPbas.ids.signeY.pos[1]
        self.lyPbas.ids.signeY.pos[0]=self.by.ptsSpeciaux['yPbas'][0] +\
            self.largeurEspace+self.btLCercl

        self.lyPbas.ids.vectyGris.pos[0]=self.lyPbas.ids.signeY.pos[0] +\
            self.lyPbas.ids.signeY.size[0]+(self.largeurEspace)
        self.on_commenceLabel()
    def on_commenceLabel(self,*largs):
        #Cette méthode est une fonction qui affiche les degrés ainsi que

        #Nous allons calculer le rayon de l'angle à afficher
        self.rayonAA=self.pjx.ratioP*self.r-((self.pjx.ratioP*self.r)-(self.pjy.ratioE*self.r))/1.8
        #Pour initialiser la position de l'angle alpha ou béta
        if self.angleProjection =='alpha':
            if self.bx.etatActuel=='xPdroit':
                self.angleMoit=self.pjx.angleCible/2
                #S'il est trop faible
                if self.angleMoit<15:
                    self.angleMoit=345

                self.angleAffiche.ids.label.pos[0],self.angleAffiche.ids.label.pos[1]=points_du_cercle(self.centrex,self.centrey,self.rayonAA,self.angleMoit)


        #On calcule les positions du label
        self.hauteurAA=self.rayonAA*1.1-self.rayonAA
        self.angleAffiche.ids.label.texture_size[1]=self.hauteurAA
        self.angleAffiche.ids.label.texture_update()
        ##########################################################
        ##########################################################
        ##Maintenant, nous allons le faire pour afficher les étiquettes en degrés
        self.hauteurED=(self.r)-(self.pjx.ratioC*self.r)
        self.rayonED=self.r*1.1
        if self.angleProjection=='alpha':
            if self.bx.etatActuel=='xPdroit':
                    
                for i in range(len(self.labelDegre)):
                    self.degreW=self.labelDegre[i]
                    self.degreW.ids.label.texture_size[1]=self.hauteurED*0.9
                    self.degreW.ids.label.pos[0],self.degreW.ids.label.pos[1]=points_du_cercle(self.centrex,self.centrey,self.rayonED,i*30)
                    self.degreW.ids.label.texture_update()
        
                    
                    if (self.degreW.ids.label.pos[0]>self.listAngleSpeciaux[i].pos[0]):
                        self.degreW.ids.label.pos[0]=self.listAngleSpeciaux[i].pos[0]+\
                            self.largeurEspace+self.btLCercl
                    elif self.degreW.ids.label.pos[0]==self.listAngleSpeciaux[i].pos[0]:
                        if self.degreW.ids.label.pos[1]>self.listAngleSpeciaux[i].pos[1]:
                            pass
                        else:
                            self.degreW.ids.label.pos[1]=self.degreW.ids.label.pos[1]-\
                                -self.degreW.ids.label.size[1]-2.5*self.btHCercl
                    else:
                        self.degreW.ids.label.pos[0]=self.listAngleSpeciaux[i].pos[0]-\
                            self.largeurEspace-self.degreW.ids.label.size[0]-self.btLCercl
        
                self.angleAffiche.ids.label.texture_size[0]=self.angleAffiche.ids.label.texture_size[1]*0.686
            if self.bx.etatActuel=='xPgauche':
                self.compteur1=120
                self.compteur2=180
                for i in range(len(self.labelDegre)):
                    self.degreW=self.labelDegre[i]
                    self.degreW.ids.label.texture_size[1]=self.hauteurED*0.9
                    i=i*30

                    if i <180:
                        j=i+self.compteur2
                        self.compteur2 -=60
                    elif i==180:
                        j=i-180
                    else:
                        j=i+self.compteur1
                        self.compteur1 -=60
                    self.degreW.ids.label.pos[0],self.degreW.ids.label.pos[1]=points_du_cercle(self.centrex,self.centrey,self.rayonED,j)
                    self.degreW.ids.label.texture_update()
                    j=int(j/30)
                    if (self.degreW.ids.label.pos[0]>self.listAngleSpeciaux[j].pos[0]):
                        self.degreW.ids.label.pos[0]=self.listAngleSpeciaux[j].pos[0]+\
                            self.largeurEspace+self.btLCercl
                    elif self.degreW.ids.label.pos[0]==self.listAngleSpeciaux[j].pos[0]:
                        if self.degreW.ids.label.pos[1]>self.listAngleSpeciaux[j].pos[1]:
                            pass
                        else:
                            self.degreW.ids.label.pos[1]=self.degreW.ids.label.pos[1]-\
                                -self.degreW.ids.label.size[1]-2.5*self.btHCercl
                    else:
                        self.degreW.ids.label.pos[0]=self.listAngleSpeciaux[j].pos[0]-\
                            self.largeurEspace-self.degreW.ids.label.size[0]-self.btLCercl
        
                self.angleAffiche.ids.label.texture_size[0]=self.angleAffiche.ids.label.texture_size[1]*0.686
        #Si c'est béta
        else:
            if self.by.etatActuel=='yPhaut':
                for i in range(len(self.labelDegre)):
                    self.degreW=self.labelDegre[i]
                    self.degreW.ids.label.texture_size[1]=self.hauteurED*0.9
                    i=i*30

                    if i <270:
                        j=i+90
                    else:
                        j=i-270
                    self.degreW.ids.label.pos[0],self.degreW.ids.label.pos[1]=points_du_cercle(self.centrex,self.centrey,self.rayonED,j)
                    self.degreW.ids.label.texture_update()
                    j=int(j/30)
                    if (self.degreW.ids.label.pos[0]>self.listAngleSpeciaux[j].pos[0]):
                        self.degreW.ids.label.pos[0]=self.listAngleSpeciaux[j].pos[0]+\
                            self.largeurEspace+self.btLCercl
                    elif self.degreW.ids.label.pos[0]==self.listAngleSpeciaux[j].pos[0]:
                        if self.degreW.ids.label.pos[1]>self.listAngleSpeciaux[j].pos[1]:
                            pass
                        else:
                            self.degreW.ids.label.pos[1]=self.degreW.ids.label.pos[1]-\
                                -self.degreW.ids.label.size[1]-2.5*self.btHCercl
                    else:
                        self.degreW.ids.label.pos[0]=self.listAngleSpeciaux[j].pos[0]-\
                            self.largeurEspace-self.degreW.ids.label.size[0]-self.btLCercl
        
                self.angleAffiche.ids.label.texture_size[0]=self.angleAffiche.ids.label.texture_size[1]*0.686
            else:
                self.compteur1=30

                for i in range(len(self.labelDegre)):
                    self.degreW=self.labelDegre[i]
                    self.degreW.ids.label.texture_size[1]=self.hauteurED*0.9
                    i=i*30
                    if i>270:
                        j=i+self.compteur1
                        self.compteur1-=60
                    else:
                        j=270-i
                    self.degreW.ids.label.pos[0],self.degreW.ids.label.pos[1]=points_du_cercle(self.centrex,self.centrey,self.rayonED,j)
                    self.degreW.ids.label.texture_update()
                    j=int(j/30)
                    if (self.degreW.ids.label.pos[0]>self.listAngleSpeciaux[j].pos[0]):
                        self.degreW.ids.label.pos[0]=self.listAngleSpeciaux[j].pos[0]+\
                            self.largeurEspace+self.btLCercl
                    elif self.degreW.ids.label.pos[0]==self.listAngleSpeciaux[j].pos[0]:
                        if self.degreW.ids.label.pos[1]>self.listAngleSpeciaux[j].pos[1]:
                            pass
                        else:
                            self.degreW.ids.label.pos[1]=self.degreW.ids.label.pos[1]-\
                                -self.degreW.ids.label.size[1]-2.5*self.btHCercl
                    else:
                        self.degreW.ids.label.pos[0]=self.listAngleSpeciaux[j].pos[0]-\
                            self.largeurEspace-self.degreW.ids.label.size[0]-self.btLCercl
        
                self.angleAffiche.ids.label.texture_size[0]=self.angleAffiche.ids.label.texture_size[1]*0.686
        self.on_commenceIndicSens()
    def on_commenceIndicSens(self,*largs):

        self.indicSensAffiche.ids.label.font_size=self.equationLiteralEq.fontSize
        self.indicSensAffiche.ids.label.texture_update()
        self.indicSensAffiche.ids.label.pos[0]=self.indication.crclIndicSens.ctrIndicX-(self.indicSensAffiche.ids.label.texture_size[0]/2.3)
        self.indicSensAffiche.ids.label.pos[1]=self.indication.crclIndicSens.ctrIndicY+self.indication.crclIndicSens.rIndicSens*1.2


    def on_angle(self,*largs):
         if (self.bta.state=='down') and (self.btb.state=='normal'):
             self.angleProjection='alpha'
             self.pjx.nomDeProjection=self.angleProjection
             self.pjy.nomDeProjection=self.angleProjection
             self.angleAffiche.nom='α'
         elif (self.bta.state=='normal') and (self.btb.state=='down'):
             self.angleProjection='beta'
             self.angleAffiche.nom='ß'
             self.pjx.nomDeProjection=self.angleProjection

             self.pjy.nomDeProjection=self.angleProjection
         self.on_mouv_angle()
            #Désactivation des barres avec les propriétés des projections
            
    def on_mouv_angle(self,*largs):
        #Ce n'est que pour afficher l'angle
        #Cette méthode est appelée quand l'utilisateur modifie la position de la barre
        #utilisateur (voir classe Assembleur)
        if self.angleProjection =='alpha':
            if self.bx.etatActuel=='xPdroit':
                self.angleMoit=self.pjx.angleCible/2
                #S'il est trop faible
                if self.angleMoit<15:
                    self.angleMoit=345

                self.angleAffiche.ids.label.pos[0],self.angleAffiche.ids.label.pos[1]=points_du_cercle(self.centrex,self.centrey,self.rayonAA,self.angleMoit)
            else:
                self.angleMoit=int((360+self.pjx.angleMesure)/2)
                self.angleMoit=self.pjx.listeAngleNeg[str(self.angleMoit),str(self.pjx.ratioP)][0].angle
                self.angleAffiche.ids.label.pos[0],self.angleAffiche.ids.label.pos[1]=points_du_cercle(self.centrex,self.centrey,self.rayonAA,self.angleMoit)
        #Si c'est béta
        else:
            if self.by.etatActuel=='yPhaut':
                self.angleMoit=int(self.pjx.angleMesure/2)
                self.angleMoit=self.pjx.listeAngleBeta[str(self.angleMoit),str(self.pjx.ratioP)][0].angle
                self.angleAffiche.ids.label.pos[0],self.angleAffiche.ids.label.pos[1]=points_du_cercle(self.centrex,self.centrey,self.rayonAA,self.angleMoit)  
            else:
                self.angleMoit=int((360+self.pjx.angleMesure)/2)
                self.angleMoit=self.pjx.listeAngleBetaNeg[str(self.angleMoit),str(self.pjx.ratioP)][0].angle
                self.angleAffiche.ids.label.pos[0],self.angleAffiche.ids.label.pos[1]=points_du_cercle(self.centrex,self.centrey,self.rayonAA,self.angleMoit)
    def on_com_bx(self,*largs):
        if self.bx.changePtsSpeciaux:
            #Pour x à droite
            self.lxPdroit.ids.vectxGris.texture_update()   
            self.lxPdroit.ids.signeX.texture_update()   
            self.lxPdroit.ids.signeX.pos[0]=self.bx.ptsSpeciaux['xPdroit'][0]-\
                (self.btLCercl*1.2)-self.largeurEspace-self.lxPdroit.ids.vectxGris.size[0]
            self.lxPdroit.ids.vectxGris.pos[0]=self.lxPdroit.ids.signeX.pos[0]+\
                self.lxPdroit.ids.signeX.size[0]+self.largeurEspace*(2/10)
            self.lxPdroit.ids.signeX.pos[1]=self.bx.ptsSpeciaux['xPdroit'][1]+(self.largeurEspace*1.7)
            self.lxPdroit.ids.vectxGris.pos[1]=self.lxPdroit.ids.signeX.pos[1]
            #pour x à gauche
            self.lxPgauche.ids.vectxGris.texture_update()   
            self.lxPgauche.ids.signeX.texture_update()   
            
            self.lxPgauche.ids.signeX.pos[0]=self.bx.ptsSpeciaux['xPgauche'][0]+\
            self.btLCercl    
            self.lxPgauche.ids.vectxGris.pos[0]= self.lxPgauche.ids.signeX.pos[0]+ \
                self.lxPgauche.ids.signeX.size[0]+(self.largeurEspace*1/2)    
            self.lxPgauche.ids.signeX.pos[1]=self.bx.ptsSpeciaux['xPgauche'][1]+self.largeurEspace
            self.lxPgauche.ids.vectxGris.pos[1]=self.lxPgauche.ids.signeX.pos[1]

            self.bx.changePtsSpeciaux=False
    def on_com_by(self,*largs):
        if self.by.changePtsSpeciaux:
            #pour y en haut
            self.lyPhaut.ids.vectyGris.texture_update()   
            self.lyPhaut.ids.signeY.texture_update()   
            self.lyPhaut.ids.signeY.pos[1]=self.by.ptsSpeciaux['yPhaut'][1]-\
                self.btHCercl-self.lyPhaut.ids.signeY.size[1]
            self.lyPhaut.ids.vectyGris.pos[1]=self.lyPhaut.ids.signeY.pos[1]
            self.lyPhaut.ids.signeY.pos[0]=self.by.ptsSpeciaux['yPhaut'][0] -\
                self.largeurEspace-self.lyPhaut.ids.signeY.size[0]-2.5*self.btLCercl
            self.lyPhaut.ids.vectyGris.pos[0]=self.lyPhaut.ids.signeY.pos[0] +\
                self.lyPhaut.ids.signeY.size[0]+(self.largeurEspace*0.4)
    
            #pour y en bas
            self.lyPbas.ids.vectyGris.texture_update()   
            self.lyPbas.ids.signeY.texture_update()      
    
            self.lyPbas.ids.signeY.pos[1]=self.by.ptsSpeciaux['yPbas'][1]+\
                self.btHCercl
            self.lyPbas.ids.vectyGris.pos[1]=self.lyPbas.ids.signeY.pos[1]
            self.lyPbas.ids.signeY.pos[0]=self.by.ptsSpeciaux['yPbas'][0] +\
                self.largeurEspace+self.btLCercl    
            self.lyPbas.ids.vectyGris.pos[0]=self.lyPbas.ids.signeY.pos[0] +\
                self.lyPbas.ids.signeY.size[0]+(self.largeurEspace)

            self.by.changePtsSpeciaux=False
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

class Label_angle(Widget):
    nom=StringProperty('')
    couleurLabel=ListProperty()
    def __init__(self,nom,couleurLabel,**kwargs):
        super().__init__(**kwargs)
        self.nom=nom
        self.couleurLabel=couleurLabel

class Label_x(Widget):
    espaceX=NumericProperty(0)
    xPos=NumericProperty(0)
    yPos=NumericProperty(0)
    signe=StringProperty('')
    couleurAxeX=ListProperty()
    def __init__(self,nom,signe,couleurAxeX,**kwargs):
        super().__init__(**kwargs)
        self.nom=nom
        self.signe=signe
        self.couleurAxeX=couleurAxeX

        
class Label_y(Widget):
    espaceY=NumericProperty(0)
    xPos=NumericProperty(0)
    yPos=NumericProperty(0)
    signe=StringProperty('')
    couleurAxeY=ListProperty()
    def __init__(self,nom,signe,couleurAxeY,**kwargs):
        super().__init__(**kwargs)
        self.nom=nom
        self.signe=signe
        self.couleurAxeY=couleurAxeY



class MyApp(App):
    def build(self):
        Window.clearcolor = (0.95, 0.94, 0.88, 0.5)
        self.a=Afficheur()
        return self.a
    
    def on_start(self, *args):
        #on_commenc() est une méthode qui calcule la taille de la police
        self.a.on_commence()

if __name__ == '__main__':
    MyApp().run()
  
