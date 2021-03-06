#!/usr/bin/env python2
#-*- coding: utf-8 -*-
#
#Author: Björn Eistel
#Contact: <eistel@gmail.com>
#
# THIS SOURCE-CODE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED. IN NO 
# EVENT WILL THE AUTHOR BE HELD LIABLE FOR ANY DAMAGES ARISING FROM THE USE OF THIS SOURCE-CODE. 
# USE AT YOUR OWN RISK.


from PyQt4 import QtGui
from Ui_MainWindow import Ui_MainWindow as UiBase
from ConfigControl import ConfigControl
from PluginList import PluginList
from ParameterBase import ParameterBase
from IntParameter import IntParameter
from PyQt4 import QtCore
from pyfloribotvision.manager.ContextManager import ContextManager
from pyfloribotvision.types.BaseType import BaseType
from pyfloribotvision.types.StringType import StringType
from StringParameter import StringParameter
from pyfloribotvision.types.FloatType import FloatType
from FloatParameter import FloatParameter
from pyfloribotvision.types.ImageType import ImageType
from ImageParameter import ImageParameter
from pyfloribotvision.types.IntType import IntType
from pyfloribotvision.types.NameType import NameType
from pyfloribotvision.types.BoolType import BoolType
from BoolParameter import BoolParameter
from pyfloribotvision.types.IntListType import IntListType
from IntListParameter import IntListParameter
from pyfloribotvision.types.IntNestedListType import IntNestedListType
from IntNestedListParameter import IntNestedListParameter


class MainWindow(QtGui.QMainWindow, UiBase):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)

        self.typeHandleList = self.initTypeHandleDict()
        self.activeParameters = dict()

        css = ''
        #with open('./config/dark.css', 'r') as f:
        with open('./config/light.css', 'r') as f:
            css = ' '.join(f.readlines())
        self.setStyleSheet(css)
        self.cc = ConfigControl()
        self.tab1Content.addWidget(self.cc)

        self.parameterBase = ParameterBase()
        self.tab1Content.addWidget(self.parameterBase)
        self.pluginList = PluginList()
        self.tab1Content.addWidget(self.pluginList)

        # beware.. the timer is needed due to the IMHO  python loading concept
        # the contextManager is not available in the startup process (__init__-stuff)
        self._timer = QtCore.QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.loadList)
        self._timer.start(1)
        #self.connect(self.pluginList.btnUpdate, QtCore.SIGNAL('clicked()'), self.loadList)
        self.connect(self.pluginList.listWidget, QtCore.SIGNAL('itemClicked(QListWidgetItem*)'), self.itemClicked)

        self.cm = ContextManager()


    def loadList(self):
        self.conf = self.cm.configController.getConfig()
        for x in self.conf:
            self.pluginList.listWidget.addItem(x)

    def cleanParameterBase(self):
        for i in reversed(range(self.parameterBase.verticalLayout.count())):
             self.parameterBase.verticalLayout.itemAt(i).widget().setParent(None)
        self.activeParameters = dict()

    def itemClicked(self, item):
        assert isinstance(item, QtGui.QListWidgetItem)
        self.cleanParameterBase()
        secconf = self.conf[str(item.text())]
        print '-'*50
        #print secconf
        for k, v in secconf.items():
            print k,
            if issubclass(type(v), BaseType):
                vclass = v.__class__
                if vclass in self.typeHandleList:
                    self.typeHandleList[vclass](v)
                else:
                    print 'NOT IMPLEMENTED', type(v)
                #print v.__class__, StringType,



    def initTypeHandleDict(self):
        thl = dict()

        thl[StringType] = self.handleStringType
        thl[IntType] = self.handleIntType
        thl[FloatType] = self.handleFloatType
        thl[NameType] = self.handleStringType
        thl[ImageType] = self.handleImageType
        thl[BoolType] = self.handleBoolType
        thl[IntListType] = self.handleIntListType
        thl[IntNestedListType] = self.handleIntNestedListType

        return thl

    def handleStringType(self, parameter):
        print 'handle invoked STRING-TYPE for name <%s> and parameter-value <%s>' % (parameter.name, str(parameter.value))

    def handleIntType(self, parameter):
        print 'handle invoked INT-TYPE for name <%s> and parameter-value <%s>' % (parameter.name, str(parameter.value))

        itg = IntParameter()

        itg.horizontalSlider.setMinimum(0)
        itg.horizontalSlider.setMaximum(1000)
        itg.horizontalSlider.setSingleStep(1)
        itg.horizontalSlider.setPageStep(10)

        itg.label.setText(parameter.name)
        itg.lineEdit.setText(str(parameter.value))
        itg.horizontalSlider.setValue(parameter.value)


        itg.registerNotify(self.widgetValueChanged)
        self.parameterBase.verticalLayout.addWidget(itg)
        self.activeParameters[itg] = parameter

    def widgetValueChanged(self, caller, value):
        for widget, parameter in self.activeParameters.items():
            if widget is caller:
                parameter.value = value

    def handleImageType(self, parameter):
        widget = ImageParameter()
        widget.parameter = parameter
        widget.label.setText(parameter.name)
        widget.lineEdit.setText(parameter.value)
        widget.lineEdit.setDisabled(True)
        self.parameterBase.verticalLayout.addWidget(widget)
        self.activeParameters[widget] = parameter

    def handleName(self, parameter):
        print 'handle invoked NAME-TYPE for name <%s> and parameter-value <%s>' % (parameter.name, str(parameter.value))

    def handleFloatType(self, parameter):
        print 'handle invoked FLOAT-TYPE for name <%s> and parameter-value <%s>' % (parameter.name, str(parameter.value))

        ftg = FloatParameter()

        ftg.horizontalSlider.setMinimum(0)
        ftg.horizontalSlider.setMaximum(500)
        ftg.horizontalSlider.setSingleStep(1)
        ftg.horizontalSlider.setPageStep(10)

        ftg.label.setText(parameter.name)
        ftg.lineEdit.setText(str(parameter.value))
        ftg.horizontalSlider.setValue(parameter.value)

        ftg.registerNotify(self.widgetValueChanged)
        self.parameterBase.verticalLayout.addWidget(ftg)
        self.activeParameters[ftg] = parameter

    def handleBoolType(self, parameter):

        btg = BoolParameter()

        btg.label.setText(parameter.name)
        btg.checkBox.setCheckState(QtCore.Qt.Checked) if parameter.value \
            else btg.checkBox.setCheckState(QtCore.Qt.Unchecked)

        self.parameterBase.verticalLayout.addWidget(btg)
        self.activeParameters[btg] = parameter
        btg.registerNotify(self.widgetValueChanged)

    def handleIntListType(self, parameter):

        ilp = IntListParameter()
        ilp.setContent(parameter.value)
        ilp.groupBox.setTitle(parameter.name)

        self.parameterBase.verticalLayout.addWidget(ilp)
        self.activeParameters[ilp] = parameter
        ilp.registerNotify(self.widgetValueChanged)

    def handleIntNestedListType(self, parameter):

        inlp = IntNestedListParameter()

        inlp.setBaseContent(parameter.value)
        inlp.groupBox.setTitle(parameter.name)

        self.parameterBase.verticalLayout.addWidget(inlp)
        self.activeParameters[inlp] = parameter
        inlp.registerNotify(self.widgetValueChanged)



