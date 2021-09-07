#-----------------------------------------------------------
# Copyright (C) 2015 Martin Dobias
#-----------------------------------------------------------
# Licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#---------------------------------------------------------------------

## 🐦 ##

from PyQt5.QtWidgets import QAction, QLineEdit
from qgis.PyQt.QtGui import QIcon
from qgis.core import (QgsProject, QgsExpressionContextUtils,
                       QgsCoordinateReferenceSystem, QgsCoordinateTransform, QgsPointXY)

def classFactory(iface):
    return BirdyPlugin(iface)


class BirdyPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.setDefaults()
        # assumed all inputs are geographic for now
        self.input_crs = QgsCoordinateReferenceSystem("EPSG:4326")

    def initGui(self):
        self.action = QAction("🐦", self.iface.mainWindow())
        self.reset = QAction("0", self.iface.mainWindow())
        '''self.action = QAction(QIcon(":/plugins/birdy/icon.png"),
                                    "Birdy",
                                    self.iface.mainWindow())'''
        self.toolbar = self.iface.addToolBar(u'Birdy')
        self.toolbar.setObjectName(u'Birdy')
        #self.iface.addToolBarIcon(self.action)
        # Add XY textboxes
        self.textbox_x = QLineEdit(self.iface.mainWindow())
        self.textbox_y = QLineEdit(self.iface.mainWindow())
        self.textbox_scale = QLineEdit(self.iface.mainWindow())
        self.textbox_x.setFixedWidth(80)
        self.textbox_y.setFixedWidth(80)
        self.textbox_scale.setFixedWidth(80)
        self.textbox_x.setText(str(self.x))
        self.textbox_y.setText(str(self.y))
        self.textbox_scale.setText(str(self.scale))
        self.txtAction_x = self.toolbar.addWidget(self.textbox_x)
        self.txtAction_y = self.toolbar.addWidget(self.textbox_y)
        self.txtAction_scale = self.toolbar.addWidget(self.textbox_scale)
        # callback
        self.textbox_x.textChanged.connect(self.runUpdateX)
        self.textbox_y.textChanged.connect(self.runUpdateY)
        self.textbox_scale.textChanged.connect(self.runUpdateS)
        # Add reset button
        self.toolbar.addAction(self.reset)
        self.reset.triggered.connect(self.resetDefaults)
        # Add the do the thing button
        self.toolbar.addAction(self.action)
        self.action.triggered.connect(self.run)

    def runUpdateX(self):
        position = self.textbox_x.text()
        if not position or position == '' or float(position) == 0:
            self.x = 0
        else:
            self.x = float(position)
    
    def runUpdateY(self):
        position = self.textbox_y.text()
        if not position or position == '' or float(position) == 0:
            self.y = 0
        else:
            self.y = float(position)
    
    def runUpdateS(self):
        scale = self.textbox_scale.text()
        if not scale or scale == '' or float(scale) == 0:
            self.scale = 15000
        else:
            self.scale = float(scale)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def setDefaults(self):
        if QgsExpressionContextUtils.projectScope(QgsProject.instance()).variable('birdy_x'):
            self.x = QgsExpressionContextUtils.projectScope(QgsProject.instance()).variable('birdy_x')
        else:
            self.x = 29.9
        if QgsExpressionContextUtils.projectScope(QgsProject.instance()).variable('birdy_y'):
            self.y = QgsExpressionContextUtils.projectScope(QgsProject.instance()).variable('birdy_y')
        else:
            self.y = -30.1
        if QgsExpressionContextUtils.projectScope(QgsProject.instance()).variable('birdy_scale'):
            self.scale = QgsExpressionContextUtils.projectScope(QgsProject.instance()).variable('birdy_scale')
        else:
            self.scale = 1000000

    def resetDefaults(self):
        if QgsExpressionContextUtils.projectScope(QgsProject.instance()).variable('birdy_x'):
            self.x = QgsExpressionContextUtils.projectScope(QgsProject.instance()).variable('birdy_x')
        else:
            self.x = 29.9
        if QgsExpressionContextUtils.projectScope(QgsProject.instance()).variable('birdy_y'):
            self.y = QgsExpressionContextUtils.projectScope(QgsProject.instance()).variable('birdy_y')
        else:
            self.y = -30.1
        if QgsExpressionContextUtils.projectScope(QgsProject.instance()).variable('birdy_scale'):
            self.scale = QgsExpressionContextUtils.projectScope(QgsProject.instance()).variable('birdy_scale')
        else:
            self.scale = 1000000
        self.textbox_x.setText(str(self.x))
        self.textbox_y.setText(str(self.y))
        self.textbox_scale.setText(str(self.scale))

    def run(self):
        # define geographic and non-geographic projections
        map_crs = QgsCoordinateReferenceSystem(self.iface.mapCanvas().mapSettings().destinationCrs().authid())
        # Define the transform
        trm = QgsCoordinateTransform(self.input_crs, map_crs, QgsProject.instance())
        # Transform XY from geographic to planar
        self.iface.mapCanvas().setCenter(trm.transform(QgsPointXY(self.x,self.y)))
        self.iface.mapCanvas().zoomScale(self.scale)
