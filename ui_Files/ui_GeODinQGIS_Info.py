# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_Files\ui_GeODinQGIS_Info.ui'
#
# Created: Wed Aug 26 12:33:10 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_InfoDialog(object):
    def setupUi(self, InfoDialog):
        InfoDialog.setObjectName(_fromUtf8("InfoDialog"))
        InfoDialog.resize(379, 272)
        self.gridLayoutWidget = QtGui.QWidget(InfoDialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(80, 100, 297, 80))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lbl_from = QtGui.QLabel(self.gridLayoutWidget)
        self.lbl_from.setObjectName(_fromUtf8("lbl_from"))
        self.gridLayout.addWidget(self.lbl_from, 0, 2, 1, 1)
        self.lbl_date = QtGui.QLabel(self.gridLayoutWidget)
        self.lbl_date.setObjectName(_fromUtf8("lbl_date"))
        self.gridLayout.addWidget(self.lbl_date, 0, 3, 1, 1)
        self.lbl_build = QtGui.QLabel(self.gridLayoutWidget)
        self.lbl_build.setObjectName(_fromUtf8("lbl_build"))
        self.gridLayout.addWidget(self.lbl_build, 0, 0, 1, 1)
        self.lbl_buildnumb = QtGui.QLabel(self.gridLayoutWidget)
        self.lbl_buildnumb.setObjectName(_fromUtf8("lbl_buildnumb"))
        self.gridLayout.addWidget(self.lbl_buildnumb, 1, 2, 1, 1)
        self.lbl_build_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.lbl_build_2.setObjectName(_fromUtf8("lbl_build_2"))
        self.gridLayout.addWidget(self.lbl_build_2, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 1, 1, 1)
        self.lbl_buildnumb_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.lbl_buildnumb_2.setObjectName(_fromUtf8("lbl_buildnumb_2"))
        self.gridLayout.addWidget(self.lbl_buildnumb_2, 2, 0, 1, 1)

        self.retranslateUi(InfoDialog)
        QtCore.QMetaObject.connectSlotsByName(InfoDialog)

    def retranslateUi(self, InfoDialog):
        InfoDialog.setWindowTitle(_translate("InfoDialog", "GeODin QGIS Info", None))
        self.lbl_from.setText(_translate("InfoDialog", "from:", None))
        self.lbl_date.setText(_translate("InfoDialog", "1234", None))
        self.lbl_build.setText(_translate("InfoDialog", "Build number:", None))
        self.lbl_buildnumb.setText(_translate("InfoDialog", "1234", None))
        self.lbl_build_2.setText(_translate("InfoDialog", "Build number:", None))
        self.label.setText(_translate("InfoDialog", "GeODin QGIS 1.0", None))
        self.label_2.setText(_translate("InfoDialog", "GeODin QGIS 1.0", None))
        self.lbl_buildnumb_2.setText(_translate("InfoDialog", "1234", None))

