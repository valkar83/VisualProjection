# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 19:51:21 2021

@author: valkar
"""
from kivy.properties import NumericProperty,StringProperty,BooleanProperty
from kivy.uix.widget import Widget
from bouton import Boutons_angle
from fleche import Fleche

###########################   FONCTIONS    ###################################
def calcul_angle(angleDeProjection,complementaire,exterieur,nomAxe,angleAxe,angleciAxe):
    #Pour le calcul des angles comme par exemple pour la variable angleMesure,
    #le sens direct est pris par défaut =>
    #dans le sens horaire = angle négatif
    #dans le sens trigo = angle positif
    #et ceux, même si le sens effectif est indirect
    #ça sera à l'intérpréteur de trancher sur le signe réel (voir main.py)
    if angleDeProjection=='alpha':
        if complementaire==False:
            if exterieur:
                #AngleAxe correspond à l'angle xPgauche et xPdroit
                return angleciAxe-angleAxe
            #Dans le cas des angles intérieures
            else:
                if nomAxe=='yPhaut':
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
                #AngleAxe correspond à l'angle yPbas et yPhaut
                return angleciAxe-angleAxe
            else:
                if nomAxe=='xPdroit':
                    return angleciAxe-angleAxe
                else:
                    #Ici on cible yPhaut
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
def directionneur(angleProjection,nomAxe,angleCible,ratioAngle,listeAngle,nomFleche):
    #Fonction utilisée pour mettre à jour les flèches lorsqu'on les touche
    #AInsi, un signal sera produit pour la méthode on_chgt des flèches

    if nomAxe=='xPdroit' or nomAxe=='yPhaut':
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
    if nomAxe=='xPgauche' or nomAxe=='yPbas':
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
def projecteurDP(initialisation,anglePre, angleCible,angleDiff,angleSupp,listeAngle,
                 dincrementP,dincrementO,ratioP,ratioC,angleAxe=0):
    if initialisation:
        if angleCible>180:
            dincrementP=1
            dincrementO=1
            for i in range(angleAxe,angleCible,dincrementP):
                widgetP=listeAngle[str(i),str(ratioP)][0]
                widgetD=listeAngle[str(i),str(ratioC)][0]
                widgetP.couleur[3]=1
                widgetD.couleur[3]=0
                #QUe les boutons qui sont supérieurs à 180°
                if angleSupp:
                    if i>180:
                        widgetD.couleur[3]=1
        else:
            dincrementP=1
            for i in range(angleAxe,angleCible,dincrementP):
                widgetP=listeAngle[str(i),str(ratioP)][0]
                widgetD=listeAngle[str(i),str(ratioC)][0]
                widgetP.couleur[3]=1
                widgetD.couleur[3]=0

        if (359-angleCible)>0:
            for i in range(angleCible,359):
                widgetP=listeAngle[str(i),str(ratioP)][0]
                widgetD=listeAngle[str(i),str(ratioC)][0]
                widgetD.couleur[3]=0
                widgetP.couleur[3]=0          
    else:
        #Il y a 4 conditions afin d'optimiser le traitement des angles deltas
        if (angleCible>180) and (anglePre>180):
            #Afficher les autres angles
            if angleDiff>=0:
                dincrementP=1
                dincrementO=1
                for i in range(anglePre,angleCible,dincrementP):
                    widgetP=listeAngle[str(i),str(ratioP)][0]
                    widgetP.couleur[3]=1
                    if angleSupp:
                        widgetD=listeAngle[str(i),str(ratioC)][0]
                        widgetD.couleur[3]=1

            else:
                dincrementO=-1
                dincrementP=-1
                for i in range(anglePre,angleCible,dincrementP):
                    widgetP=listeAngle[str(i),str(ratioP)][0]
                    widgetP.couleur[3]=0
                    if angleSupp:
                        widgetD=listeAngle[str(i),str(ratioC)][0]
                        widgetD.couleur[3]=0
        
        elif (angleCible>180) and (anglePre<=180):
            dincrementO=1
            #Pour colorier les angles deltas
            for i in range(181,angleCible+1,dincrementO):
                if angleSupp:
                    angleDelta=listeAngle[str(i),str(ratioC)][0]
                    angleDelta.couleur[3]=1
            if angleDiff>=0:
                dincrementP=1
                #Pour les angles normaux
                for i in range(anglePre,angleCible,dincrementP):
                    widgetP=listeAngle[str(i),str(ratioP)][0]
                    widgetP.couleur[3]=1
            else:
                dincrementP=-1
                for i in range(anglePre,angleCible,dincrementP):
                    widgetP=listeAngle[str(i),str(ratioP)][0]
                    widgetP.couleur[3]=0
        elif (angleCible<=180) and (anglePre>180):
            dincrementO=-1
            for i in range(anglePre,180,dincrementO):
                if angleSupp:
                    angleDelta=listeAngle[str(i),str(ratioC)][0]
                    angleDelta.couleur[3]=0
            if angleDiff>=0:
                dincrementP=1
                #Pour les angles normaux
                for i in range(anglePre,angleCible,dincrementP):
                    widgetP=listeAngle[str(i),str(ratioP)][0]
                    widgetP.couleur[3]=1
            else:
                dincrementP=-1
                for i in range(anglePre,angleCible,dincrementP):
                    widgetP=listeAngle[str(i),str(ratioP)][0]
                    widgetP.couleur[3]=0
        elif (angleCible<=180) and (anglePre<=180):
            
            if angleDiff>=0:
                dincrementP=1
                #Pour les angles normaux
                for i in range(anglePre,angleCible,dincrementP):
                    widgetP=listeAngle[str(i),str(ratioP)][0]
                    widgetP.couleur[3]=1
            else:
                dincrementP=-1
                for i in range(anglePre,angleCible,dincrementP):
                    widgetP=listeAngle[str(i),str(ratioP)][0]
                    widgetP.couleur[3]=0
def projecteurDN(initialisation,anglePreNeg, angleNeg,angleDiff,angleSupp,listeAngleNeg,
                 dincrementP,dincrementO,ratioP,ratioC,angleAxe=0,angleCible=0):
    if initialisation:
        if angleNeg<0:
            dincrementP=-1
            dincrementO=-1
            for i in range(angleAxe,angleNeg,dincrementP):
                widgetP=listeAngleNeg[str(i),str(ratioP)][0]
                widgetD=listeAngleNeg[str(i),str(ratioC)][0]
                widgetD.couleur[3]=0
                widgetP.couleur[3]=1
                
                if angleSupp:
                    if i<0:
                        widgetD.couleur[3]=1
        else:
            dincrementP=-1
            for i in range(angleAxe,angleNeg,dincrementP):
                widgetP=listeAngleNeg[str(i),str(ratioP)][0]
                widgetD=listeAngleNeg[str(i),str(ratioC)][0]
                widgetP.couleur[3]=1
                widgetD.couleur[3]=0
        if (-179-angleCible)<0:
            for i in range(angleNeg,-180,-1):
                widgetP=listeAngleNeg[str(i),str(ratioP)][0]
                widgetD=listeAngleNeg[str(i),str(ratioC)][0]
                widgetD.couleur[3]=0
                widgetP.couleur[3]=0  
    else:
        #Il y a 4 conditions afin d'optimiser le traitement des angles deltas
        if (angleNeg<0) and (anglePreNeg<0):
            #Afficher les autres angles
            if angleDiff<=0:
                dincrementP=-1
                dincrementO=-1
                for i in range(anglePreNeg,angleNeg,dincrementP):
                    widgetP=listeAngleNeg[str(i),str(ratioP)][0]
                    widgetP.couleur[3]=1
                    if angleSupp:
                        widgetD=listeAngleNeg[str(i),str(ratioC)][0]
                        widgetD.couleur[3]=1

            else:
                dincrementO=1
                dincrementP=1
                for i in range(anglePreNeg,angleNeg,dincrementP):
                    widgetP=listeAngleNeg[str(i),str(ratioP)][0]
                    widgetP.couleur[3]=0
                    if angleSupp:
                        widgetD=listeAngleNeg[str(i),str(ratioC)][0]
                        widgetD.couleur[3]=0
        elif (angleNeg<0) and (anglePreNeg>=0):
            dincrementO=-1
            if angleSupp:
                #Pour colorier les angles deltas
                for i in range(-1,angleNeg,dincrementO):
                    widgetD=listeAngleNeg[str(i),str(ratioC)][0]
                    widgetD.couleur[3]=1
    
            if angleDiff<=0:
                dincrementP=-1
                for i in range(anglePreNeg,angleNeg,dincrementP):
                    widget=listeAngleNeg[str(i),str(ratioP)][0]
                    widget.couleur[3]=1
            else:
                dincrementP=1
                for i in range(anglePreNeg,angleNeg,dincrementP):
                   widget=listeAngleNeg[str(i),str(ratioP)][0]
                   widget.couleur[3]=0
                   
        elif (angleNeg>=0) and (anglePreNeg<0):
            dincrementO=1
            if angleSupp:
            #Pour colorier les angles deltas
                for i in range(anglePreNeg,1,dincrementO):
                    widgetD=listeAngleNeg[str(i),str(ratioC)][0]
                    widgetD.couleur[3]=0
            if angleDiff<=0:
                dincrementP=-1
                for i in range(anglePreNeg,angleNeg,dincrementP):
                    widget=listeAngleNeg[str(i),str(ratioP)][0]
                    widget.couleur[3]=1
            else:
                dincrementP=1
                for i in range(anglePreNeg,angleNeg,dincrementP):
                   widget=listeAngleNeg[str(i),str(ratioP)][0]
                   widget.couleur[3]=0
                   
        elif (angleNeg>=0) and (anglePreNeg>=0):
            if angleDiff<=0:
                dincrementP=-1
                for i in range(anglePreNeg,angleNeg,dincrementP):
                    widget=listeAngleNeg[str(i),str(ratioP)][0]
                    widget.couleur[3]=1
            else:
                dincrementP=1
                for i in range(anglePreNeg,angleNeg,dincrementP):
                   widget=listeAngleNeg[str(i),str(ratioP)][0]
                   widget.couleur[3]=0
class ProjectionDirect(Widget):
    #Pour le calcul des angles comme par exemple pour la variable angleMesure,
    #le sens direct est pris par défaut =>
    #dans le sens horaire = angle négatif
    #dans le sens trigo = angle positif
    #et ceux, même si le sens effectif est indirect
    #ça sera à l'intérpréteur de trancher sur le signe réel (voir main.py)
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
            if self.axeX=='xPdroit':
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
                    self.flecheDirec=Fleche(self.centre, self.ptRef, 10.0,'Fleche Direct')
                    self.add_widget(self.flecheDirec)

                else:
                    j=self.angleCible-1
                    self.centre=self.listeAngle[str(self.angleCible),str(self.ratioP)][0]
                    self.ptRef=self.listeAngle[str(j),str(self.ratioP)][0]
                    #fleche sens trigo
                    self.flecheDirec=Fleche(self.centre, self.ptRef, 10.0,'Fleche Direct')
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
            if self.axeX=='xPdroit':
                directionneur('alpha',self.axeX,self.angleCible,self.ratioP,
                              self.listeAngle,self.flecheDirec)
          
                #On récupère la mesure de l'angle
                self.angleMesure=calcul_angle(self.nomDeProjection, False, True, self.axeX, self.angleAxeX, self.angleCible)
                #on récupére la différence à colorier
                self.angleDiff=self.angleCible-self.anglePre
                projecteurDP(False,self.anglePre,self.angleCible,self.angleDiff,
                             self.angleSupp,self.listeAngle,self.dincrementP,
                             self.dincrementO,self.ratioP,self.ratioC)

            elif self.axeX=='xPgauche':
                #Cela signifie ice que l'axe positif a la direction gauche

                self.angleNeg=self.listeAngle[str(self.angleCible),str(self.ratioP)][1]
                directionneur('alpha',self.axeX,self.angleNeg,self.ratioP,
                              self.listeAngleNeg,self.flecheDirec)

                #Si c'est xPgauche, nous allons utiliser les angles négatifs
                self.angleNeg=self.listeAngle[str(self.angleCible),str(self.ratioP)][1]
                ###Calcul angleMesure avec xPgauche
                self.angleMesure=calcul_angle(self.nomDeProjection, False, True, self.axeX, self.angleAxeX, self.angleNeg)
                self.anglePreNeg=self.listeAngle[str(self.anglePre),str(self.ratioP)][1]
                self.angleDiff=self.angleNeg-self.anglePreNeg
                projecteurDN(False, self.anglePreNeg, self.angleNeg, self.angleDiff,
                             self.angleSupp, self.listeAngleNeg, self.dincrementP,
                             self.dincrementO, self.ratioP, self.ratioC)
                
#############################################################################################◘
#############################################################################################  
        #angleBeta
        else:
            if self.axeY=='yPhaut':
                #On récupère la mesure de l'angle par rapport au béta référence
                ###############################################################
                directionneur('beta',self.axeY,self.angleCible,self.ratioP,
                              self.listeAngle,self.flecheDirec)
                
                self.angleCibleBeta=self.listeAngle[str(self.angleCible),
                                                 str(self.ratioP)][2]
                self.anglePreBeta=self.listeAngle[str(self.anglePre),
                                                str(self.ratioP)][2]
                #on récupére la différence à colorier
                self.angleDiff=self.angleCibleBeta-self.anglePreBeta
                self.angleAxeYBeta=transform_en_beta(self.angleAxeY)
 
                projecteurDP(False,self.anglePreBeta,self.angleCibleBeta,self.angleDiff,
                             self.angleSupp,self.listeAngleBeta,self.dincrementP,
                             self.dincrementO,self.ratioP,self.ratioC)
                self.angleMesure=calcul_angle(self.nomDeProjection, False, True,
                                              self.axeY, self.angleAxeYBeta, self.angleCibleBeta)

        #yPbas
            elif self.axeY=='yPbas':
                #Si c'est yBas, nous allons utiliser les angles négatifs
                self.angleNeg=self.listeAngle[str(self.angleCible),str(self.ratioP)][1]
                self.angleBetaNeg=transform_neg_beta(self.angleNeg)
                  ###############################################################
                ##############################"Pour la flèche, 
                directionneur('beta',self.axeY,self.angleCible,self.ratioP,
                              self.listeAngle,self.flecheDirec)

                ##AngleRef pour le béta positif et ainsi le mettre dans la fonction
                self.anglePreBetaNeg=self.listeAngle[str(self.anglePre),str(self.ratioP)][3]
                ###Calcul angleMesure avec xPgauches
                self.angleAxeYBeta=transform_neg_beta(-90)
                self.angleMesure=calcul_angle(self.nomDeProjection, False, True,
                                              self.axeY, self.angleAxeYBeta, self.angleBetaNeg)
                
                self.angleDiff=self.angleBetaNeg-self.anglePreBetaNeg
                projecteurDN(False, self.anglePreBetaNeg, self.angleBetaNeg, self.angleDiff,
                             self.angleSupp, self.listeAngleBetaNeg, self.dincrementP,
                             self.dincrementO, self.ratioP, self.ratioC)
               
    def on_changement(self,anglePre,angleCible):
        if self.nomDeProjection=='alpha':

            if self.axeX=='xPdroit':
                directionneur('alpha',self.axeX,self.angleCible,self.ratioP,
                              self.listeAngle,self.flecheDirec)
                projecteurDP(True, self.anglePre, self.angleCible, 0, self.angleSupp,
                            self.listeAngle, self.dincrementP, self.dincrementO,
                            self.ratioP, self.ratioC,self.angleAxeX)
                #On récupère la mesure de l'angle
                #On récupère la mesure de l'angle
                self.angleMesure=calcul_angle(self.nomDeProjection, False, True, self.axeX, self.angleAxeX, self.angleCible)
          
            elif self.axeX=='xPgauche':
                self.angleNeg=self.listeAngle[str(self.angleCible),str(self.ratioC)][1]

                directionneur('alpha',self.axeX,self.angleNeg,self.ratioP,
                              self.listeAngleNeg,self.flecheDirec)
                self.flecheDirec.canvas.ask_update()
  
                ###Calcul angleMesure avec xPgauche
                self.angleMesure=calcul_angle(self.nomDeProjection, False, True, self.axeX, self.angleAxeX, self.angleNeg)

                self.anglePreNeg=self.listeAngle[str(self.angleCible),str(self.ratioC)][1]
                self.angleDiff=self.angleNeg-self.anglePreNeg
                projecteurDN(True, self.anglePreNeg, self.angleNeg, self.angleDiff,
                             self.angleSupp, self.listeAngleNeg, self.dincrementP, 
                             self.dincrementO, self.ratioP, self.ratioC,self.angleAxeX,
                             self.angleCible)

    ###################################################################################
    ###################################################################################
    #BETA
        else:
            if self.axeY=='yPhaut':
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
 
                projecteurDP(True, self.anglePreBeta, self.angleCibleBeta, 0, self.angleSupp,
                            self.listeAngleBeta, self.dincrementP, self.dincrementO,
                            self.ratioP, self.ratioC,self.angleAxeYBeta)
                self.angleMesure=calcul_angle(self.nomDeProjection, False, True,
                                              self.axeY, self.angleAxeYBeta, self.angleCibleBeta)
               
            elif self.axeY=='yPbas':
                self.angleNeg=self.listeAngle[str(self.angleCible),str(self.ratioP)][1]
                self.angleBetaNeg=transform_neg_beta(self.angleNeg)
                directionneur('beta',self.axeY,self.angleCible,self.ratioP,
                              self.listeAngle,self.flecheDirec)
                self.angleAxeYBeta=transform_neg_beta(-90)
                self.angleMesure=calcul_angle(self.nomDeProjection, False, True,
                                              self.axeY, self.angleAxeYBeta, self.angleBetaNeg)
                projecteurDN(True, 0, self.angleBetaNeg, 0,
                             self.angleSupp, self.listeAngleBetaNeg, self.dincrementP, 
                             self.dincrementO, self.ratioP, self.ratioC,self.angleAxeYBeta,
                             self.angleCible)
 

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
    
    angleChange=NumericProperty(0)
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
            if self.nomAxe=='yPhaut':
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
                    self.flecheDirecE=Fleche(self.centre, self.ptRef, 10.0,'Fleche Indirect E')
                    self.flecheDirecE.fleCouleur=self.indigo

                    self.add_widget(self.flecheDirecE)

                else:
                    j=self.angleCible-1
                    self.centre=self.listeAngle[str(self.angleCible),str(self.ratioE)][0]
                    self.ptRef=self.listeAngle[str(j),str(self.ratioE)][0]
                    #fleche sens trigo
                    self.flecheDirecE=Fleche(self.centre, self.ptRef, 10.0,'Fleche Indirect E')
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
                        self.flecheDirecH=Fleche(self.centre,self.ptRefH,10.0,
                                                 'horaire'+str(h))
                        self.flecheDirecT=Fleche(self.centre,self.ptRefT,10.0,
                                                 'trigo'+str(t))
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
                        self.flecheDirecH=Fleche(self.centre,self.ptRefH,10.0,
                                                 'horaire'+str(h))
                        self.flecheDirecT=Fleche(self.centre,self.ptRefT,10.0,
                                                 'trigo'+str(t))
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
            if self.axeY=='yPhaut' or self.axeY=='yPbas':
                if self.axeX=='xPdroit':
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
                elif self.axeX=='xPgauche':
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
            if self.axeX=='xPdroit'or self.axeX=='xPgauche':
                if self.axeY=='yPhaut':
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
                
                elif self.axeY=='yPbas':
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
        self.angleChange+=1
    def on_changement(self,anglePre,angleCible):
        if self.nomDeProjection=='alpha':
            if self.axeY=='yPhaut':
                if self.axeX=='xPdroit':
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
                elif self.axeX=='xPgauche':
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

            elif self.axeY=='yPbas':
                if self.axeX=='xPdroit':
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

                    
                    self.angleMesureE=calcul_angle(self.nomDeProjection, False, True,
                                              self.axeX, self.angleAxeX, self.angleCible)
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
                elif self.axeX=='xPgauche':
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
            
            if self.axeX=='xPdroit':
                if self.axeY=='yPhaut':
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
                            
                elif self.axeY=='yPbas':
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
            elif self.axeX=='xPgauche':
                if self.axeY=='yPhaut':
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
                
                elif self.axeY=='yPbas':
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
        self.angleChange+=1