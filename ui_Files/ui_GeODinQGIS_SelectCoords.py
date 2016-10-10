# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_Files\ui_SelectCoords.ui'
#
# Created: Thu Jul 30 09:36:26 2015
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

class Ui_SelectCoords(object):
    def setupUi(self, SelectCoords):
        SelectCoords.setObjectName(_fromUtf8("SelectCoords"))
        SelectCoords.setWindowModality(QtCore.Qt.ApplicationModal)
        SelectCoords.resize(400, 300)
        self.buttonBox = QtGui.QDialogButtonBox(SelectCoords)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.lbl_xcol = QtGui.QLabel(SelectCoords)
        self.lbl_xcol.setGeometry(QtCore.QRect(50, 30, 60, 13))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lbl_xcol.setFont(font)
        self.lbl_xcol.setObjectName(_fromUtf8("lbl_xcol"))
        self.lbl_ycol = QtGui.QLabel(SelectCoords)
        self.lbl_ycol.setGeometry(QtCore.QRect(50, 70, 60, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lbl_ycol.setFont(font)
        self.lbl_ycol.setObjectName(_fromUtf8("lbl_ycol"))
        self.cmb_xcol = QtGui.QComboBox(SelectCoords)
        self.cmb_xcol.setGeometry(QtCore.QRect(120, 30, 141, 22))
        self.cmb_xcol.setObjectName(_fromUtf8("cmb_xcol"))
        self.cmb_ycol = QtGui.QComboBox(SelectCoords)
        self.cmb_ycol.setGeometry(QtCore.QRect(120, 70, 141, 22))
        self.cmb_ycol.setObjectName(_fromUtf8("cmb_ycol"))

        self.retranslateUi(SelectCoords)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SelectCoords.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SelectCoords.reject)
        QtCore.QMetaObject.connectSlotsByName(SelectCoords)

    def retranslateUi(self, SelectCoords):
        SelectCoords.setWindowTitle(_translate("SelectCoords", "Dialog", None))
        self.lbl_xcol.setText(_translate("SelectCoords", "X column:", None))
        self.lbl_ycol.setText(_translate("SelectCoords", "Y column:", None))

