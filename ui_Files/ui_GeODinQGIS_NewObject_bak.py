# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_Files\ui_GeODinQGIS_NewObject.ui'
#
# Created: Tue Mar 29 11:37:28 2016
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
        self.lbl_obtyp = QtGui.QLabel(self.dockWidgetContents)
        self.lbl_obtyp.setGeometry(QtCore.QRect(10, 10, 80, 25))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(8)
        font.setKerning(True)
        self.lbl_obtyp.setFont(font)
        self.lbl_obtyp.setFrameShape(QtGui.QFrame.Box)
        self.lbl_obtyp.setObjectName(_fromUtf8("lbl_obtyp"))
        self.btn_close = QtGui.QPushButton(self.dockWidgetContents)
        self.btn_close.setGeometry(QtCore.QRect(260, 200, 125, 23))
        self.btn_close.setObjectName(_fromUtf8("btn_close"))
        self.btn_ok = QtGui.QPushButton(self.dockWidgetContents)
        self.btn_ok.setGeometry(QtCore.QRect(260, 170, 125, 23))
        self.btn_ok.setObjectName(_fromUtf8("btn_ok"))
        self.btn_del = QtGui.QPushButton(self.dockWidgetContents)
        self.btn_del.setGeometry(QtCore.QRect(260, 110, 125, 23))
        self.btn_del.setObjectName(_fromUtf8("btn_del"))
        self.coord_tab = QtGui.QTableWidget(self.dockWidgetContents)
        self.coord_tab.setGeometry(QtCore.QRect(10, 79, 244, 201))
        self.coord_tab.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.coord_tab.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.coord_tab.setDragDropOverwriteMode(True)
        self.coord_tab.setDragDropMode(QtGui.QAbstractItemView.NoDragDrop)
        self.coord_tab.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.coord_tab.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.coord_tab.setColumnCount(2)
        self.coord_tab.setObjectName(_fromUtf8("coord_tab"))
        self.coord_tab.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.coord_tab.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.coord_tab.setHorizontalHeaderItem(1, item)
        self.coord_tab.horizontalHeader().setDefaultSectionSize(100)
        self.coord_tab.verticalHeader().setDefaultSectionSize(28)
        self.le_obtyp = QtGui.QLineEdit(self.dockWidgetContents)
        self.le_obtyp.setGeometry(QtCore.QRect(105, 10, 280, 25))
        self.le_obtyp.setAcceptDrops(False)
        self.le_obtyp.setObjectName(_fromUtf8("le_obtyp"))
        self.lbl_east = QtGui.QLabel(self.dockWidgetContents)
        self.lbl_east.setGeometry(QtCore.QRect(10, 40, 80, 25))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(8)
        font.setKerning(True)
        self.lbl_east.setFont(font)
        self.lbl_east.setFrameShape(QtGui.QFrame.Box)
        self.lbl_east.setObjectName(_fromUtf8("lbl_east"))
        self.le_east = QtGui.QLineEdit(self.dockWidgetContents)
        self.le_east.setGeometry(QtCore.QRect(105, 40, 87, 25))
        self.le_east.setAcceptDrops(False)
        self.le_east.setObjectName(_fromUtf8("le_east"))
        self.lbl_north = QtGui.QLabel(self.dockWidgetContents)
        self.lbl_north.setGeometry(QtCore.QRect(206, 40, 80, 25))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(8)
        font.setKerning(True)
        self.lbl_north.setFont(font)
        self.lbl_north.setFrameShape(QtGui.QFrame.Box)
        self.lbl_north.setObjectName(_fromUtf8("lbl_north"))
        self.le_north = QtGui.QLineEdit(self.dockWidgetContents)
        self.le_north.setGeometry(QtCore.QRect(298, 40, 87, 25))
        self.le_north.setAcceptDrops(False)
        self.le_north.setObjectName(_fromUtf8("le_north"))
        self.btn_desel = QtGui.QPushButton(self.dockWidgetContents)
        self.btn_desel.setGeometry(QtCore.QRect(260, 140, 125, 23))
        self.btn_desel.setObjectName(_fromUtf8("btn_desel"))
        self.btn_createshp = QtGui.QPushButton(self.dockWidgetContents)
        self.btn_createshp.setGeometry(QtCore.QRect(260, 80, 25, 25))
        self.btn_createshp.setText(_fromUtf8(""))
        self.btn_createshp.setCheckable(False)
        self.btn_createshp.setObjectName(_fromUtf8("btn_createshp"))
        self.btn_openshp = QtGui.QPushButton(self.dockWidgetContents)
        self.btn_openshp.setGeometry(QtCore.QRect(290, 80, 25, 25))
        self.btn_openshp.setText(_fromUtf8(""))
        self.btn_openshp.setCheckable(False)
        self.btn_openshp.setObjectName(_fromUtf8("btn_openshp"))
        self.btn_dragshp = QtGui.QPushButton(self.dockWidgetContents)
        self.btn_dragshp.setGeometry(QtCore.QRect(320, 80, 25, 25))
        self.btn_dragshp.setText(_fromUtf8(""))
        self.btn_dragshp.setCheckable(False)
        self.btn_dragshp.setObjectName(_fromUtf8("btn_dragshp"))
        NewObject.setWidget(self.dockWidgetContents)

        self.retranslateUi(NewObject)
        QtCore.QMetaObject.connectSlotsByName(NewObject)

    def retranslateUi(self, NewObject):
        NewObject.setWindowTitle(_translate("NewObject", "New Object", None))
        self.lbl_obtyp.setText(_translate("NewObject", "Object type", None))
        self.btn_close.setText(_translate("NewObject", "Close", None))
        self.btn_ok.setText(_translate("NewObject", "GeODin", None))
        self.btn_del.setText(_translate("NewObject", "Delete Selected", None))
        item = self.coord_tab.horizontalHeaderItem(0)
        item.setText(_translate("NewObject", "Easting", None))
        item = self.coord_tab.horizontalHeaderItem(1)
        item.setText(_translate("NewObject", "Northing", None))
        self.lbl_east.setText(_translate("NewObject", "Easting", None))
        self.le_east.setPlaceholderText(_translate("NewObject", "Empty", None))
        self.lbl_north.setText(_translate("NewObject", "Northing", None))
        self.le_north.setPlaceholderText(_translate("NewObject", "Empty", None))
        self.btn_desel.setText(_translate("NewObject", "Deselect", None))

