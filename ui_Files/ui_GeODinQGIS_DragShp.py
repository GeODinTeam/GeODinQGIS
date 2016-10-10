# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_Files\ui_GeODinQGIS_DragShp.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_DragShape(object):
    def setupUi(self, DragShape):
        DragShape.setObjectName(_fromUtf8("DragShape"))
        DragShape.setWindowModality(QtCore.Qt.ApplicationModal)
        DragShape.resize(620, 435)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DragShape.sizePolicy().hasHeightForWidth())
        DragShape.setSizePolicy(sizePolicy)
        DragShape.setMaximumSize(QtCore.QSize(620, 16777215))
        self.verticalLayout = QtGui.QVBoxLayout(DragShape)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.shape_tab = QtGui.QTableWidget(DragShape)
        self.shape_tab.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.shape_tab.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.shape_tab.setColumnCount(2)
        self.shape_tab.setObjectName(_fromUtf8("shape_tab"))
        self.shape_tab.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.shape_tab.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.shape_tab.setHorizontalHeaderItem(1, item)
        self.shape_tab.horizontalHeader().setDefaultSectionSize(300)
        self.verticalLayout.addWidget(self.shape_tab)
        self.buttonBox = QtGui.QDialogButtonBox(DragShape)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(DragShape)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DragShape.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DragShape.reject)
        QtCore.QMetaObject.connectSlotsByName(DragShape)

    def retranslateUi(self, DragShape):
        DragShape.setWindowTitle(_translate("DragShape", "Dialog", None))
        item = self.shape_tab.horizontalHeaderItem(0)
        item.setText(_translate("DragShape", "Name", None))
        item = self.shape_tab.horizontalHeaderItem(1)
        item.setText(_translate("DragShape", "Filepath", None))

