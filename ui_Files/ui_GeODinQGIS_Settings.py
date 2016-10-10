# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_Files\ui_GeODinQGIS_Settings.ui'
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

class Ui_Settings(object):
    def setupUi(self, Settings):
        Settings.setObjectName(_fromUtf8("Settings"))
        Settings.setWindowModality(QtCore.Qt.ApplicationModal)
        Settings.resize(440, 221)
        self.buttonBox = QtGui.QDialogButtonBox(Settings)
        self.buttonBox.setGeometry(QtCore.QRect(260, 186, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.checkBox = QtGui.QCheckBox(Settings)
        self.checkBox.setGeometry(QtCore.QRect(20, 10, 20, 20))
        self.checkBox.setText(_fromUtf8(""))
        self.checkBox.setIconSize(QtCore.QSize(20, 20))
        self.checkBox.setChecked(False)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.lbl_del = QtGui.QLabel(Settings)
        self.lbl_del.setGeometry(QtCore.QRect(20, 44, 331, 16))
        self.lbl_del.setObjectName(_fromUtf8("lbl_del"))
        self.btn_del_tmp = QtGui.QPushButton(Settings)
        self.btn_del_tmp.setGeometry(QtCore.QRect(396, 40, 25, 25))
        self.btn_del_tmp.setText(_fromUtf8(""))
        self.btn_del_tmp.setObjectName(_fromUtf8("btn_del_tmp"))
        self.lbl_surpress = QtGui.QLabel(Settings)
        self.lbl_surpress.setGeometry(QtCore.QRect(40, 11, 381, 16))
        self.lbl_surpress.setObjectName(_fromUtf8("lbl_surpress"))
        self.lbl_err = QtGui.QLabel(Settings)
        self.lbl_err.setGeometry(QtCore.QRect(20, 73, 251, 16))
        self.lbl_err.setObjectName(_fromUtf8("lbl_err"))
        self.lbl_size = QtGui.QLabel(Settings)
        self.lbl_size.setGeometry(QtCore.QRect(140, 73, 91, 16))
        self.lbl_size.setText(_fromUtf8(""))
        self.lbl_size.setObjectName(_fromUtf8("lbl_size"))
        self.btn_mail = QtGui.QPushButton(Settings)
        self.btn_mail.setGeometry(QtCore.QRect(346, 70, 75, 23))
        self.btn_mail.setObjectName(_fromUtf8("btn_mail"))
        self.le_dir = QtGui.QLineEdit(Settings)
        self.le_dir.setGeometry(QtCore.QRect(20, 130, 401, 20))
        self.le_dir.setObjectName(_fromUtf8("le_dir"))
        self.lbl_dir = QtGui.QLabel(Settings)
        self.lbl_dir.setGeometry(QtCore.QRect(20, 100, 211, 16))
        self.lbl_dir.setObjectName(_fromUtf8("lbl_dir"))
        self.btn_dir = QtGui.QPushButton(Settings)
        self.btn_dir.setGeometry(QtCore.QRect(240, 100, 31, 23))
        self.btn_dir.setObjectName(_fromUtf8("btn_dir"))
        self.lbl_lyr = QtGui.QLabel(Settings)
        self.lbl_lyr.setGeometry(QtCore.QRect(20, 160, 121, 16))
        self.lbl_lyr.setObjectName(_fromUtf8("lbl_lyr"))
        self.rbtn_sql = QtGui.QRadioButton(Settings)
        self.rbtn_sql.setGeometry(QtCore.QRect(150, 160, 82, 17))
        self.rbtn_sql.setCheckable(True)
        self.rbtn_sql.setChecked(True)
        self.rbtn_sql.setObjectName(_fromUtf8("rbtn_sql"))
        self.rbtn_shp = QtGui.QRadioButton(Settings)
        self.rbtn_shp.setGeometry(QtCore.QRect(230, 160, 82, 17))
        self.rbtn_shp.setObjectName(_fromUtf8("rbtn_shp"))
        self.btn_defdir = QtGui.QPushButton(Settings)
        self.btn_defdir.setGeometry(QtCore.QRect(280, 100, 141, 23))
        self.btn_defdir.setObjectName(_fromUtf8("btn_defdir"))
        self.btn_info = QtGui.QPushButton(Settings)
        self.btn_info.setGeometry(QtCore.QRect(230, 190, 23, 23))
        self.btn_info.setText(_fromUtf8(""))
        self.btn_info.setObjectName(_fromUtf8("btn_info"))

        self.retranslateUi(Settings)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Settings.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Settings.reject)
        QtCore.QMetaObject.connectSlotsByName(Settings)

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(_translate("Settings", "GeODinQGIS Settings", None))
        self.lbl_del.setText(_translate("Settings", "Delete temporary files", None))
        self.lbl_surpress.setText(_translate("Settings", "Suppress attribute form pop-up after feature creation", None))
        self.lbl_err.setText(_translate("Settings", "Error Log:", None))
        self.btn_mail.setText(_translate("Settings", "Send Email", None))
        self.lbl_dir.setText(_translate("Settings", "Directory to save vector layers", None))
        self.btn_dir.setText(_translate("Settings", "...", None))
        self.lbl_lyr.setText(_translate("Settings", "Save Layer as", None))
        self.rbtn_sql.setText(_translate("Settings", "SQLite", None))
        self.rbtn_shp.setText(_translate("Settings", "Shape", None))
        self.btn_defdir.setText(_translate("Settings", "Restore Default", None))

