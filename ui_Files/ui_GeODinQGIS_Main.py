# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_Files\ui_GeODinQGIS_Main.ui'
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

class Ui_GeODinQGISMain(object):
    def setupUi(self, GeODinQGISMain):
        GeODinQGISMain.setObjectName(_fromUtf8("GeODinQGISMain"))
        GeODinQGISMain.resize(380, 636)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GeODinQGISMain.sizePolicy().hasHeightForWidth())
        GeODinQGISMain.setSizePolicy(sizePolicy)
        GeODinQGISMain.setMinimumSize(QtCore.QSize(380, 300))
        GeODinQGISMain.setMaximumSize(QtCore.QSize(400, 1000))
        GeODinQGISMain.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.gridLayout_9 = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(15)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.multipleImportButton = QtGui.QPushButton(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.multipleImportButton.sizePolicy().hasHeightForWidth())
        self.multipleImportButton.setSizePolicy(sizePolicy)
        self.multipleImportButton.setMaximumSize(QtCore.QSize(200, 16777215))
        self.multipleImportButton.setObjectName(_fromUtf8("multipleImportButton"))
        self.horizontalLayout.addWidget(self.multipleImportButton)
        self.singleImportButton = QtGui.QPushButton(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.singleImportButton.sizePolicy().hasHeightForWidth())
        self.singleImportButton.setSizePolicy(sizePolicy)
        self.singleImportButton.setMaximumSize(QtCore.QSize(200, 16777215))
        self.singleImportButton.setObjectName(_fromUtf8("singleImportButton"))
        self.horizontalLayout.addWidget(self.singleImportButton)
        self.gridLayout_9.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.treeWidget = QtGui.QTreeWidget(self.dockWidgetContents)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.horizontalLayout_2.addWidget(self.treeWidget)
        self.gridLayout_9.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        GeODinQGISMain.setWidget(self.dockWidgetContents)

        self.retranslateUi(GeODinQGISMain)
        QtCore.QMetaObject.connectSlotsByName(GeODinQGISMain)

    def retranslateUi(self, GeODinQGISMain):
        GeODinQGISMain.setWindowTitle(_translate("GeODinQGISMain", "GeODin QGIS", None))
        self.multipleImportButton.setText(_translate("GeODinQGISMain", "Load Database", None))
        self.singleImportButton.setText(_translate("GeODinQGISMain", "Import Databases", None))
        self.treeWidget.headerItem().setText(0, _translate("GeODinQGISMain", "GeODin Databases", None))

