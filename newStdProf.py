#!/usr/bin/env python3
# coding: utf-8
#
# LGPL
#
# newStdProf.py 




import os

from PySide import QtGui, QtCore
import FreeCADGui as Gui
import FreeCAD as App
import Part
import Sketcher
import PartDesign

import Asm4_libs as Asm4



"""
    +-----------------------------------------------+
    |                  The command                  |
    +-----------------------------------------------+
"""
class stdProfCrea():
    def __init__(self):
        self.menutext    = "Standard Profile Creator"
        self.tooltip     = "To make a standard profile with auto-filling partInfo"
        self.icon        = os.path.join( Asm4.iconPath , 'Asm4_SPC.png')

    def GetResources(self):
        return {"MenuText"   : self.menutext,
                "ToolTip"    : self.tooltip,
                "Pixmap"     : self.icon 
                }

    def IsActive(self):
        # return active if you have a new file with Assembly
        if Asm4.getAssembly() is None:
            return False
        else: 
            return True
        

    def Activated(self):
        Gui.Control.showDialog( profileUI() )
    

"""
    +-----------------------------------------------+
    |    The UI and functions in the Task panel     |
    +-----------------------------------------------+
"""
class profileUI():

    def __init__(self):
        #init of widget
        self.base = QtGui.QWidget()
        self.form = self.base        
        iconFile = os.path.join( Asm4.iconPath , 'Asm4_SPC.png')
        self.form.setWindowIcon(QtGui.QIcon( iconFile ))
        self.form.setWindowTitle("Standard Profile Creator")
        
        # the GUI objects are defined later down
        self.drawUI()
    # close
    def finish(self):
        Gui.Control.closeDialog()

    # standard panel UI buttons
    def getStandardButtons(self):
        return int(0)

    # Cancel
    def reject(self):
        self.finish()

    # OK
    def accept(self):
        self.finish()
        
    def proreset(self):
        self.qledit[0].setEnabled(1)
        self.qledit[1].setEnabled(0)
        self.qledit[2].setEnabled(0)
        self.qledit[3].setEnabled(0)
        self.qledit[4].setEnabled(0)
        self.qledit[5].setEnabled(1)
        
    def on_currentIndexChanged(self):
        print(self.profileType.currentText(), self.profileForm.currentText() )
        self.proreset()
        if self.profileType.currentText()!= 'choisir' and self.profileForm.currentText() != 'choisir':
            if self.profileType.currentText() == 'Tube':
                self.qledit[4].setEnabled(1)
            if self.profileType.currentText() == 'Fer':
                self.qledit[4].clear()
            if self.profileForm.currentText() == 'Rond':
                self.qledit[1].clear()
                self.qledit[2].clear()
                self.qledit[3].setEnabled(1)
            if self.profileForm.currentText() == 'Carre':
                self.qledit[2].clear()
                self.qledit[3].clear()
                self.qledit[1].setEnabled(1)
            if self.profileForm.currentText() == 'Rectangulaire_Plat':
                self.qledit[3].clear()
                self.qledit[1].setEnabled(1)
                self.qledit[2].setEnabled(1)
                

    # Define the iUI, only static elements
    def drawUI(self):
        #init Profile
        self.Profile=[]
        # Place the widgets with layouts
        self.mainLayout = QtGui.QVBoxLayout(self.form)
        self.formLayout = QtGui.QFormLayout()
        
        #profile type data
        checkLayout = QtGui.QHBoxLayout()
        self.profileType = QtGui.QComboBox()
        self.profileType.addItem("choisir")
        self.profileType.addItem("Tube")
        self.profileType.addItem("Fer")
        self.profileType.addItem("Etire")
        checkLayout.addWidget(self.profileType)
        self.formLayout.addRow(QtGui.QLabel('Type'),checkLayout)
        self.profileType.currentIndexChanged.connect(self.on_currentIndexChanged)
        
        #profile form data
        self.buttonsLayout = QtGui.QHBoxLayout()
        self.profileForm = QtGui.QComboBox()
        self.profileForm.addItem("choisir")
        self.profileForm.addItem("Rond")
        self.profileForm.addItem("Carre")
        self.profileForm.addItem("Rectangulaire_Plat")
        checkLayout.addWidget(self.profileForm)
        self.formLayout.addRow(None,checkLayout)
        self.profileForm.currentIndexChanged.connect(self.on_currentIndexChanged)
        
        # profile constraints
        self.proconst=[('hauteur',''),('largeur',''),('diametre',''),('epaisseur',''),('longueur','')]
        self.qledit=[]
        checkLayout = QtGui.QHBoxLayout()
        propValue = QtGui.QLineEdit()
        checkLayout.addWidget(propValue)
        self.formLayout.addRow(QtGui.QLabel('nom de la piece'),checkLayout)
        propValue.setEnabled(1)
        self.qledit.append(propValue)
        for i,prop in enumerate(self.proconst):
            checkLayout = QtGui.QHBoxLayout()
            propValue = QtGui.QLineEdit()
            lala = QtGui.QIntValidator ()
            propValue.setValidator(lala)
            checkLayout.addWidget(propValue)
            self.formLayout.addRow(QtGui.QLabel(prop[0]),checkLayout)
            propValue.setEnabled(0)
            self.qledit.append(propValue)

        self.mainLayout.addLayout(self.formLayout)
        self.mainLayout.addWidget(QtGui.QLabel())
        
        # Buttons
        #self.buttonsLayout = QtGui.QHBoxLayout()
        self.Config = QtGui.QPushButton('Config')
        self.Close = QtGui.QPushButton('Close')
        self.Make = QtGui.QPushButton('Make Part')
        self.buttonsLayout.addWidget(self.Config)
        self.buttonsLayout.addWidget(self.Close)
        self.buttonsLayout.addStretch()
        self.buttonsLayout.addWidget(self.Make)

        self.mainLayout.addLayout(self.buttonsLayout)
        self.form.setLayout(self.mainLayout)

        # Actions
        self.Make.clicked.connect(self.makeProfile)
        self.Config.clicked.connect(self.config)
        self.Close.clicked.connect(self.reject)
        
    def config(self):
        print('Building fonction in progress')
    
    def initBody(self,partname,bodyname):
        # init doc
        doc = App.ActiveDocument
        #init name of part
        partName = partname ### self.qledit[0].text()
        partNamet=''
        i=1
        if doc.getObject(partName):
            while partName != partNamet :
                n=str(i)		
                partNamet = partName  + n
                if not doc.getObject(partNamet) :
                    partName = partNamet
                i=i+1
        #make part
        newPart = doc.addObject('App::Part',partName)
        # add LCS if appropriate
        # add an LCS at the root of the Part, and attach it to the 'Origin'
        lcs0 = newPart.newObject('PartDesign::CoordinateSystem','LCS_0')
        lcs0.Support = [(newPart.Origin.OriginFeatures[0],'')]
        lcs0.MapMode = 'ObjectXY'
        lcs0.MapReversed = False
        # If the 'Part' group exists, move it there:
        #init partsGroup
        partsGroup = doc.getObject('Parts')
        if partsGroup.TypeId == 'App::DocumentObjectGroup':
            if newPart.Name != 'Assembly':
                partsGroup.addObject(newPart)
                    # recompute
        newPart.recompute()
        App.ActiveDocument.recompute()
        #init part
        part = doc.getObject(partName)

        #init name of body
        bodyName = bodyname ###'bodytest'
        bodyNamet=''
        i=1
        if doc.getObject(bodyName):
            while bodyName != bodyNamet :
                n=str(i)		
                bodyNamet = bodyName  + n
                print(bodyNamet)
                if not doc.getObject(bodyNamet) :
                    bodyName = bodyNamet
                i=i+1
        #make body
        newBody =doc.addObject('PartDesign::Body',bodyName)
        # add LCS if appropriate
        # add an LCS at the root of the Part, and attach it to the 'Origin'
        lcs0 = newBody.newObject('PartDesign::CoordinateSystem','LCS_0')
        lcs0.Support = [(newBody.Origin.OriginFeatures[0],'')]
        lcs0.MapMode = 'ObjectXY'
        lcs0.MapReversed = False
        # move the body in the part:
        part.addObject(newBody)
        # recompute
        newPart.recompute()
        App.ActiveDocument.recompute()
        #init body
        body = doc.getObject(bodyName)
        return body
        
    def makeRound(self,body,sketchname,diameter,thickness):
        #init sketch
        doc=body.Document
        sketchName = sketchname ###'sketchtest'
        sketchNamet=''
        i=1
        n=1
        if doc.getObject(sketchName):
            while sketchName != sketchNamet :
                n=str(i)		
                sketchNamet = sketchName  + n
                print(sketchNamet)
                if not doc.getObject(sketchNamet) :
                    sketchName = sketchNamet
                i=i+1
        #init support
        support = body.Origin.OriginFeatures[5].Name
        #make sketch
        body.newObject('Sketcher::SketchObject',sketchName)
        #init sketch
        sketch = doc.getObject(sketchName)
        sketch.Support = (doc.getObject(support),[''])
        sketch.MapMode = 'FlatFace'
        #make ext circle
        sketch.addGeometry(Part.Circle(App.Vector(0.000000,-0.000000,0),App.Vector(0,0,1),2.000000),False)
        sketch.addConstraint(Sketcher.Constraint('Coincident',0,3,-1,1)) 
        sketch.addConstraint(Sketcher.Constraint('Diameter',0,diameter))
        sketch.renameConstraint(1, u'diaext')
        #make int circle
        if thickness == None:
            #recompute
            App.ActiveDocument.recompute()
            return sketch
        else :
            diaint = diameter - thickness * 2
            sketch.addGeometry(Part.Circle(App.Vector(0.000000,-0.000000,0),App.Vector(0,0,1),2.000000),False)
            sketch.addConstraint(Sketcher.Constraint('Coincident',1,3,0,3)) 
            sketch.addConstraint(Sketcher.Constraint('Diameter',1,diaint)) 
            sketch.renameConstraint(3, u'diaint')
            #recompute
            App.ActiveDocument.recompute()
            return sketch

    def makeSquare(self,body,sketchname,height,width,thickness,speprof):
        #init sketch
        doc=body.Document
        sketchName = sketchname ###'sketchtest'
        sketchNamet=''
        i=1
        n=1
        if doc.getObject(sketchName):
            while sketchName != sketchNamet :
                n=str(i)		
                sketchNamet = sketchName  + n
                print(sketchNamet)
                if not doc.getObject(sketchNamet) :
                    sketchName = sketchNamet
                i=i+1
        #init support
        support = body.Origin.OriginFeatures[5].Name
        #make sketch
        body.newObject('Sketcher::SketchObject',sketchName)
        #init sketch
        sketch = doc.getObject(sketchName)
        sketch.Support = (doc.getObject(support),[''])
        sketch.MapMode = 'FlatFace'
        #make ext Square
        #make etire profile
        geoList = []
        geoList.append(Part.LineSegment(App.Vector(-2,-2,0),App.Vector(2,-2,0)))
        geoList.append(Part.LineSegment(App.Vector(2,-2,0),App.Vector(2,2,0)))
        geoList.append(Part.LineSegment(App.Vector(2,2,0),App.Vector(-2,2,0)))
        geoList.append(Part.LineSegment(App.Vector(-2,2,0),App.Vector(-2,-2,0)))
        geoList.append(Part.Point(App.Vector(0,0,0)))
        sketch.addGeometry(geoList,False)
        conList = []
        conList.append(Sketcher.Constraint('Coincident',0,2,1,1))
        conList.append(Sketcher.Constraint('Coincident',1,2,2,1))
        conList.append(Sketcher.Constraint('Coincident',2,2,3,1))
        conList.append(Sketcher.Constraint('Coincident',3,2,0,1))
        conList.append(Sketcher.Constraint('Horizontal',1))
        conList.append(Sketcher.Constraint('Horizontal',3))
        conList.append(Sketcher.Constraint('Vertical',0))
        conList.append(Sketcher.Constraint('Vertical',2))
        conList.append(Sketcher.Constraint('Symmetric',1,2,0,1,4,1))
        conList.append(Sketcher.Constraint('Coincident',-1,1,4,1))
        sketch.addConstraint(conList)
        conWidth = sketch.addConstraint(Sketcher.Constraint('DistanceX',1,1,1,2,width))
        conHeight = sketch.addConstraint(Sketcher.Constraint('DistanceY',2,2,2,1,height))
        sketch.renameConstraint(conWidth, u'width')
        sketch.renameConstraint(conHeight, u'height')
        App.ActiveDocument.recompute()
        #make Fer profile
        if speprof != None:
            print (speprof)
            App.ActiveDocument.recompute()
            return sketch
        sketch.fillet(0,1,height/10,True,True)
        sketch.fillet(0,2,height/10,True,True)
        sketch.fillet(1,2,height/10,True,True)
        sketch.fillet(2,2,height/10,True,True)
        App.ActiveDocument.recompute()
        sketch.addConstraint(Sketcher.Constraint('Equal',7,9)) 
        sketch.addConstraint(Sketcher.Constraint('Equal',9,11)) 
        sketch.addConstraint(Sketcher.Constraint('Equal',11,5)) 
        conFillet = sketch.addConstraint(Sketcher.Constraint('Radius',7,height/10))
        sketch.setExpression('Constraints['+str(conFillet)+']', u'.Constraints.height / 10')
        sketch.renameConstraint(conFillet, u'fillet')
        App.ActiveDocument.recompute()
        #make Tube profile
        if thickness == None:
            #recompute
            App.ActiveDocument.recompute()
            return sketch
        else :
            geoList = []
            geoList.append(Part.LineSegment(App.Vector(-2,-2,0),App.Vector(2,-2,0)))
            geoList.append(Part.LineSegment(App.Vector(2,-2,0),App.Vector(2,2,0)))
            geoList.append(Part.LineSegment(App.Vector(2,2,0),App.Vector(-2,2,0)))
            geoList.append(Part.LineSegment(App.Vector(-2,2,0),App.Vector(-2,-2,0)))
            geoList.append(Part.Point(App.Vector(0,0,0)))
            sketch.addGeometry(geoList,False)
            conList = []
            conList.append(Sketcher.Constraint('Coincident',13,2,14,1))
            conList.append(Sketcher.Constraint('Coincident',14,2,15,1))
            conList.append(Sketcher.Constraint('Coincident',15,2,16,1))
            conList.append(Sketcher.Constraint('Coincident',16,2,13,1))
            conList.append(Sketcher.Constraint('Horizontal',14))
            conList.append(Sketcher.Constraint('Horizontal',16))
            conList.append(Sketcher.Constraint('Vertical',13))
            conList.append(Sketcher.Constraint('Vertical',15))
            conList.append(Sketcher.Constraint('Symmetric',14,2,13,1,17,1))
            conList.append(Sketcher.Constraint('Coincident',17,1,-1,1))
            sketch.addConstraint(conList)
            conThicknessY = sketch.addConstraint(Sketcher.Constraint('DistanceY',14,2,10,1,thickness))
            conThicknessX = sketch.addConstraint(Sketcher.Constraint('DistanceX',14,2,10,1,thickness))
            sketch.renameConstraint(conThicknessY, u'thickness')
            sketch.setExpression('Constraints[39]', u'.Constraints.thickness')
            #recompute
            App.ActiveDocument.recompute()
            return sketch
        

    def makePad(self,body,sketch,length):
        doc=sketch.Document
        #init name
        padName = 'pad'
        padNamet=''
        i=1
        if doc.getObject(padName):
            while padName != padNamet :
                n=str(i)		
                padNamet = padName  + n
                print(padNamet)
                if not doc.getObject(padNamet) :
                    padName = padNamet
                i=i+1    
        #make pad
        body.newObject('PartDesign::Pad',padName)
        #init pad
        pad = doc.getObject(padName)
        #use sketck for pad
        pad.Profile = sketch
        #length of pad
        pad.Length = length
        #recompute
        App.ActiveDocument.recompute()
        
    def makeProfile(self):
        # init var
        partName = self.qledit[0].text()
        bodyName = str(self.profileType.currentText() + self.profileForm.currentText())
        sketchname = bodyName
        # init body
        body = self.initBody(partName,bodyName)
        print (partName,bodyName,body)
        # inti length
        length = int (self.qledit[5].text())
        #test type of profile
        if self.profileForm.currentText() == 'Rond' :
            # init var
            diameter = int(self.qledit[3].text())
            if self.profileType.currentText() == 'Tube':
                thickness = int(self.qledit[4].text())
            else :
                thickness = None
            # make sketch
            sketch = self.makeRound(body,sketchname,diameter,thickness)
            self.makePad(body,sketch,length)
        if self.profileForm.currentText() == 'Carre' or self.profileForm.currentText() == 'Rectangulaire_Plat' :
            # init var
            height = int(self.qledit[1].text())
            if self.profileForm.currentText() == 'Rectangulaire_Plat' :
                width = int (self.qledit[2].text())
            else:
                width = height
            if self.profileType.currentText() == 'Tube':
                thickness = int(self.qledit[4].text())
            else :
                thickness = None
            if self.profileType.currentText() != 'Tube' and self.profileType.currentText() != 'Fer':
                speprof = self.profileType.currentText()
            else :
                speprof = None
            
            # make sketch
            sketch = self.makeSquare(body,sketchname,height,width,thickness,speprof)
            self.makePad(body,sketch,length)
        

# add the command to the workbench
Gui.addCommand( 'Asm4_stdProf',  stdProfCrea() )
