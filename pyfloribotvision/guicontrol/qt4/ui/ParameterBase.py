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
from Ui_ParameterBase import Ui_ParameterBase as UiBase


class ParameterBase(QtGui.QWidget, UiBase):

    def __init__(self, **kwargs):
        QtGui.QWidget.__init__(self, **kwargs)
        self.setupUi(self)


