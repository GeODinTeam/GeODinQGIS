# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_Files\ui_GeODinQGIS_NewObject.ui'
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

class Ui_NewObject(object):
    def setupUi(self, NewObject):
        NewObject.setObjectName(_fromUtf8("NewObject"))
        NewObject.resize(395, 360)
        NewObject.setMinimumSize(QtCore.QSize(395, 360))
        NewObject.setAcceptDrops(False)
        NewObject.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setAcceptDrops(False)
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.btn_close = QtGui.QPushButton(self.dockWidgetContents)
        self.btn_close.setGeometry(QtCore.QRect(260, 300, 125, 23))
        self.btn_close.setObjectName(_fromUtf8("btn_close"))
        self.coord_tab = QtGui.QTableWidget(self.dockWidgetContents)
        self.coord_tab.setGeometry(QtCore.QRect(10, 69, 375, 221))
        self.coord_tab.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.coord_tab.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.coord_tab.setDragDropOverwriteMode(True)
        self.coord_tab.setDragDropMode(QtGui.QAbstractItemView.NoDragDrop)
        self.coord_tab.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.coord_tab.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.coord_tab.setColumnCount(3)
        self.coord_tab.setObjectName(_fromUtf8("coord_tab"))
        self.coord_tab.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.coord_tab.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.coord_tab.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.coord_tab.setHorizontalHeaderItem(2, item)
        self.coord_tab.horizontalHeader().setDefaultSectionSize(100)
        self.coord_tab.verticalHeader().setDefaultSectionSize(28)
        self.btn_createshp = QtGui.QPushButton(self.dockWidgetContents)
        self.btn_createshp.setGeometry(QtCore.QRect(10, 300, 25, 25))
        self.btn_createshp.setText(_fromUtf8(""))
        self.btn_createshp.setCheckable(False)
        self.btn_createshp.setObjectName(_fromUtf8("btn_createshp"))
        self.btn_openshp = QtGui.QPushButton(self.dockWidgetContents)
        self.btn_openshp.setGeometry(QtCore.QRect(40, 300, 25, 25))
        self.btn_openshp.setText(_fromUtf8(""))
        self.btn_openshp.setCheckable(False)
        self.btn_openshp.setObjectName(_fromUtf8("btn_openshp"))
        self.btn_dragshp = QtGui.QPushButton(self.dockWidgetContents)
        self.btn_dragshp.setGeometry(QtCore.QRect(70, 300, 25, 25))
        self.btn_dragshp.setText(_fromUtf8(""))
        self.btn_dragshp.setCheckable(False)
        self.btn_dragshp.setObjectName(_fromUtf8("btn_dragshp"))
        self.btn_del = QtGui.QPushButton(self.dockWidgetContents)
        self.btn_del.setGeometry(QtCore.QRect(100, 300, 25, 25))
        self.btn_del.setText(_fromUtf8(""))
        self.btn_del.setCheckable(False)
        self.btn_del.setObjectName(_fromUtf8("btn_del"))
        self.btn_desel = QtGui.QPushButton(self.dockWidgetContents)
        self.btn_desel.setGeometry(QtCore.QRect(130, 300, 25, 25))
        self.btn_desel.setText(_fromUtf8(""))
        self.btn_desel.setCheckable(False)
        self.btn_desel.setObjectName(_fromUtf8("btn_desel"))
        self.btn_geodin = QtGui.QPushButton(self.dockWidgetContents)
        self.btn_geodin.setGeometry(QtCore.QRect(160, 300, 25, 25))
        self.btn_geodin.setText(_fromUtf8(""))
        self.btn_geodin.setCheckable(False)
        self.btn_geodin.setObjectName(_fromUtf8("btn_geodin"))
        self.cmb_short = QtGui.QComboBox(self.dockWidgetContents)
        self.cmb_short.setGeometry(QtCore.QRect(100, 5, 285, 22))
        self.cmb_short.setObjectName(_fromUtf8("cmb_short"))
        self.lbl_short = QtGui.QLabel(self.dockWidgetContents)
        self.lbl_short.setGeometry(QtCore.QRect(10, 10, 91, 16))
        self.lbl_short.setObjectName(_fromUtf8("lbl_short"))
        self.lbl_east = QtGui.QLabel(self.dockWidgetContents)
        self.lbl_east.setGeometry(QtCore.QRect(10, 40, 91, 16))
        self.lbl_east.setObjectName(_fromUtf8("lbl_east"))
        self.lbl_north = QtGui.QLabel(self.dockWidgetContents)
        self.lbl_north.setGeometry(QtCore.QRect(220, 40, 91, 16))
        self.lbl_north.setObjectName(_fromUtf8("lbl_north"))
        self.cmb_east = QtGui.QComboBox(self.dockWidgetContents)
        self.cmb_east.setGeometry(QtCore.QRect(100, 40, 100, 22))
        self.cmb_east.setObjectName(_fromUtf8("cmb_east"))
        self.cmb_north = QtGui.QComboBox(self.dockWidgetContents)
        self.cmb_north.setGeometry(QtCore.QRect(285, 40, 100, 22))
        self.cmb_north.setObjectName(_fromUtf8("cmb_north"))
        NewObject.setWidget(self.dockWidgetContents)

        self.retranslateUi(NewObject)
        QtCore.QMetaObject.connectSlotsByName(NewObject)

    def retranslateUi(self, NewObject):
        NewObject.setWindowTitle(_translate("NewObject", "New Object", None))
        self.btn_close.setText(_translate("NewObject", "Close", None))
        item = self.coord_tab.horizontalHeaderItem(0)
        item.setText(_translate("NewObject", "Short name", None))
        item = self.coord_tab.horizontalHeaderItem(1)
        item.setText(_translate("NewObject", "Easting", None))
        item = self.coord_tab.horizontalHeaderItem(2)
        item.setText(_translate("NewObject", "Northing", None))
        self.lbl_short.setText(_translate("NewObject", "Short name", None))
        self.lbl_east.setText(_translate("NewObject", "Easting", None))
        self.lbl_north.setText(_translate("NewObject", "Northing", None))

