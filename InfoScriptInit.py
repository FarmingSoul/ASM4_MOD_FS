#!/usr/bin/env python3
# coding: utf-8
#
# LGPL
# Copyright HUBERT Zoltán
#
# infoKeys.py


#customization file for automatic info partinfoUI

import FreeCAD as App


def infoDefault(self):
    
    ###Macro pour automatisation des Informations liées à la pièce
    ###et la compatibilité labête de l'atelier paysan [greg]
    ###Nom de la pièce
    ###Désignation
    ###Longueur
    ###Angle 1
    ###Angle 2
    ###Diamètre des troues

    ###Création de la variable de la pièce
    try :
        self.TypeId
        piece=self
    except AttributeError:
        piece=self.part
    
    print (piece.FullName)
    for i in range(len(piece.Group)):
        if piece.Group[i].TypeId == 'PartDesign::Pad' :
            corp=piece.Group[i]
            print (i, 'trouvé')
        else :
            print (i ,'cest pas' ,str(piece.Group[i].FullName))
    try :
        corp
    except NameError :
        print('recherche profonde')
        for i in range(len(piece.Group)):
            if piece.Group[i].TypeId == 'PartDesign::Body' :
                body=piece.Group[i]
                print (i, 'trouvé Body')
                for i in range(len(body.Group)):
                    print(body.FullName)
                    if body.Group[i].TypeId == 'PartDesign::Pad' :
                        corp=body.Group[i]
                        print (i, 'trouvé pad profond')
            else :
                print ('la pièce : ' ,str(piece.Group[i].FullName), "n'est pas un profile standard")
    try :
        corp
    except NameError :
        print('y a pas moyen pour : ',piece.FullName ) 
        setattr(piece,'Nom_de_la_piece',"'"+piece.Label)
        return
    print(corp.FullName)
    barre=corp
    profile=barre.Profile[0]
    ###Recuperation des variables de la pièce
    test=0
    try :
        ep=float(profile.getDatum('thickness'))
        test+=1
        temp=int(ep)
        if ep==temp:
            ep=int(ep)
        ep=str(ep)
    except NameError:
        test=test
    try :
        lar= float(profile.getDatum('width'))
        test+=1
        temp=int(lar)
        if lar==temp:
            lar=int(lar)
        lar=str(lar)
    except NameError:
        test=test
    try :
        hau= float(profile.getDatum('height'))
        test+=1
        temp=int(hau)
        if hau==temp:
            hau=int(hau)
        hau=str(hau)
    except NameError:
        test=test
    try :
        conge= float(profile.getDatum('conge'))
        test+=1
    except NameError:
        test=test
    try :
        dia= float(profile.getDatum('diaext'))
        test+=1
        temp=int(dia)
        if dia==temp:
            dia=int(dia)
        dia=str(dia)
    except NameError:
        test=test
    
    ### Déduction du profile

    if test==1:
        descri="fer rond Ø"+dia
    if test==2:
        try :
            descri="Tube rond "+dia+" x "+ep
        except NameError:
            descri="étiré plat "+lar+" x "+ep
    if test==3:
        try:
            if hau==lar:
                descri="Tube carré "+hau+" x "+ep
            else:
                descri="Tube rectangulaire "+hau+" x "+lar+" x "+ep
        except NameError:
            descri="fer plat "+lar+" x "+ep
    if test==0:
        print("le profile n'a pas était déterminé : contrainte non nomées")
        descri = "profile non déterminé"

    ###Création de la variable de percage si elle existe
    try:
        troue=App.ActiveDocument.getObject('Hole')
        sktroue=troue.OutList[0]
        troue1= str(len(App.ActiveDocument.getObject(sktroue.Name).Geometry))+" x D : "+str(troue.Diameter)
    except AttributeError:
        troue1=""
    try:
        angle1=str(App.ActiveDocument.getObject('Groove').Angle.Value)
    except AttributeError:
        angle1=""
    try:
        angle2=str(App.ActiveDocument.getObject('Groove001').Angle.Value)
    except AttributeError:
        angle2=""

    ###Recuperation des variables
    nom=str(piece.Label)
    longueur=float(barre.Length)
    temp=int(longueur)
    if longueur==temp:
        longueur=int(longueur)
    longueur=str(longueur)


    ###Ecriture des parametre dans le fichier #PARTINFO# existant
    setattr(piece,'Nom_de_la_piece',nom)
    setattr(piece,'Reference_AP',descri)
    setattr(piece,'Angle1',angle1)
    setattr(piece,'Angle2',angle2)
    setattr(piece,'percage',troue1)
    setattr(piece,'longueur',longueur)
    piece.setExpression('longueur',u''+barre.Label+'.Length')


    ###Affichage du résultat
    check=nom+" - "+descri+" - "+longueur+" mm"
    print (check)
    
    ###Actualisation
    try :
        self.getPartInfo()
        print('actualisation')
        for i,prop in enumerate(self.infoTable):
            if self.part.getGroupOfProperty(prop[0])=='PartInfo' :
                if self.part.getTypeIdOfProperty(prop[0])=='App::PropertyString' :
                    self.infos[i].setText(prop[1])
    except AttributeError:
        pass
# close