# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from win32api import GetSystemMetrics
from PIL import Image

import win32com.client
import time
import json, os
import datetime
import md5
import sys


class DisplayLayout(QDialog):

	def __init__(self, main, object):
		QDialog.__init__(self)

		self.main = main
		self.tmp = main.tmpDirectory
		self.object = object
		self.layoutList = []
		self.setWindowTitle('Layout')
		
		self.resize(650, 500)
		self.setMinimumSize(QSize(0, 500))
		self.setMaximumSize(QSize(16777215, 500))

		horizontalLayout = QHBoxLayout(self)

		formLayout = QFormLayout()
		formLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
		formLayout.setFormAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

		
		addLabel = QLabel(self)
		addLabel.setMinimumSize(QSize(23, 23))
		addLabel.setMaximumSize(QSize(23, 23))
		addLabel.setPixmap(QPixmap(self.main.pluginDirectory+"/icons/addLayout.png"))

		removeLabel = QLabel(self)
		removeLabel.setMinimumSize(QSize(23, 23))
		removeLabel.setMaximumSize(QSize(23, 23))
		removeLabel.setPixmap(QPixmap(self.main.pluginDirectory+"/icons/remove.png"))
		
		addLayout = QHBoxLayout()
		addLayout.setSizeConstraint(QLayout.SetFixedSize)
		addLayout.addWidget(addLabel)
		addLayout.addWidget(removeLabel)
		formLayout.setLayout(0, QFormLayout.LabelRole, addLayout)
		
		
		self.layoutFoldersList = QTableWidget(0, 1, self)
		self.layoutFoldersList.setMinimumSize(QSize(300, 400))
		self.layoutFoldersList.setColumnWidth(0, 300)
		self.layoutFoldersList.setHorizontalHeaderLabels(["Layout-Ordner"])
		self.layoutFoldersList.setEditTriggers(QAbstractItemView.NoEditTriggers)
		self.layoutFoldersList.setSelectionMode(QAbstractItemView.SingleSelection)
		self.layoutsList = QTableWidget(0, 1, self)
		self.layoutsList.setMinimumSize(QSize(300, 400))
		self.layoutsList.setColumnWidth(0, 300)
		self.layoutsList.setHorizontalHeaderLabels(["Layouts"])
		self.layoutsList.setSelectionMode(QAbstractItemView.SingleSelection)
		self.layoutsList.setEditTriggers(QAbstractItemView.NoEditTriggers)

		layoutLayout = QHBoxLayout()
		layoutLayout.setSizeConstraint(QLayout.SetMaximumSize)		
		layoutLayout.addWidget(self.layoutFoldersList)
		layoutLayout.addWidget(self.layoutsList)
		formLayout.setLayout(1, QFormLayout.SpanningRole, layoutLayout)
		buttonBox = QDialogButtonBox(self)
		buttonBox.setStandardButtons(QDialogButtonBox.Close|QDialogButtonBox.Apply)
		formLayout.setWidget(2, QFormLayout.FieldRole, buttonBox)
		
		horizontalLayout.addLayout(formLayout)

		buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.show)
		buttonBox.button(QDialogButtonBox.Close).clicked.connect(self.cancel)
		QObject.connect(self.layoutFoldersList, SIGNAL("itemClicked (QTableWidgetItem*)"), self.getLayouts)
		addLabel.mouseReleaseEvent = self.newFolder
		removeLabel.mouseReleaseEvent = self.delFolder
		
		self.layoutFoldersList.keyPressEvent = self.keyPress
		
		for layout in self.main.config.options('Layouts'):
			l = self.main.config.get('Layouts', layout)
			self.layoutList.append(layout)
			self.layoutFoldersList.setRowCount(self.layoutFoldersList.rowCount()+1)
			self.layoutFoldersList.setItem(self.layoutFoldersList.rowCount()-1, 0, QTableWidgetItem(l))
			
		self.exec_()

	def show(self):
		now = datetime.datetime.now()
		a = str(now.year) + str(now.strftime('%m')) + str(now.strftime('%d'))

		GeODin = win32com.client.Dispatch("GeODin.GeODinApplication")
		info = GeODin.LicenceInfo.split('\r\n')
		#print "Licence Info: ", info
		
		dongle = [t for t in info if 'Dongle' in t][0].split(': ')[1]
		m = md5.new()
		m.update(a+'-'+dongle)
		new_hash = m.hexdigest()
		selected = self.layoutsList.selectedItems()
		#layout = self.folderpath + '\\' + str(selected[0].text())
		layout = self.folderpath + '\\' + selected[0].text()
		database = self.object.parent.parent
		invid = self.object.invid
		image = 41
		#image = 12
		
		Params = "[Params]\n"
		exe = "EXECUTE=ProducePortalImage\n"
		Layout = "LAYOUT="
		pagenumber = "\nPageNumber=20\n"
		scale = "Scale=0\n"
		version = "VersionName=\n"
		ArcGeODin = "ArcGeODin="
		dbName = "\n[Database]\n"
		name = "Name="
		username = "\nUsername= \n"
		password = "Password= \n"
		objects = "[Objects]\n"
		objectID = "ObjectID1="
		Image = "\n[Image]\n"
		imageType = "ImageType="
		resolution = "\nResolution=3000"
		
		
		params = Params + exe + Layout + layout + pagenumber + scale + version + ArcGeODin + new_hash + dbName + name + str(database) + username + password + objects + objectID + invid + Image + imageType + str(image) + resolution

		pic = GeODin.ProduceData(params)
		if GeODin.ExceptionValue != 0: 
			print "Error ID:"+ str(GeODin.ExceptionValue)
			print "Error Message:"+GeODin.ExceptionMsg
			
		f = open(self.tmp + "\\out.pdf", 'wb')
		if isinstance(pic[0], unicode):
			f.write(pic[0].encode('utf-8'))
		else:
			f.write(pic[0])
		#f.write(pic[0])
		f.close()

		GeODin = None
		
		ImageLayout(self.tmp + "\\out.pdf", selected[0].text())
		
	def cancel(self):
		self.main = None
		self.object = None
		self.layoutFoldersList = None
		self.accept()
		
	def newFolder(self, event):
		# get path for GeODin data
		path_data = str(self.main.config.get('Options', 'programdata'))
		# get layout directory
		directory = QFileDialog.getExistingDirectory(self, "Select Directory", path_data)
		#print type(directory)
		#print directory
#		directory = directory.encode('utf-8')
		
		# if layout directory has been specified
		if directory:
			i=0
			# map over layout folders
			self.layoutFoldersList.setRowCount(self.layoutFoldersList.rowCount() + 1)
			self.layoutFoldersList.setItem(self.layoutFoldersList.rowCount()-1, 0, QTableWidgetItem(directory))
			
			# write layout folder to config file
			while self.main.config.has_option('Layouts','L' + str(i)):
				i  =1
			self.main.config.set('Layouts', 'L'+str(i), directory)
			self.main.saveConfig()
			
			# append layouts to tableview
			self.layoutList.append('L' + str(i))
			
	def delFolder(self, event):
		# delete layout folder from list
		selected = self.layoutFoldersList.selectedItems()
		if selected:
			for s in reversed(selected):
				pos = self.layoutFoldersList.row(s)
				self.main.config.remove_option('Layouts', self.layoutList[pos])
				self.main.saveConfig()
				self.layoutList.pop(pos)
				self.layoutFoldersList.removeRow(pos)
	
	def reloadLayouts(self):
		selected = self.layoutFoldersList.selectedItems()
		if selected:
			self.getLayouts(selected[0])
	
	def getLayouts(self, item):
		path = item.text()
		self.folderpath = path
		layouts = [ l for l in os.listdir(path) if os.path.isfile(os.path.join(path,l)) and l.lower().endswith(".glo")]
		self.layoutsList.clearContents()
		self.layoutsList.setRowCount(0)
		if layouts:
			for l in layouts:
				self.layoutsList.setRowCount(self.layoutsList.rowCount()+1)
				self.layoutsList.setItem(self.layoutsList.rowCount()-1, 0, QTableWidgetItem(l))

	def keyPress(self, event):
		pass

class ImageLayout(QDialog):
	def __init__(self, path, title):
		QDialog.__init__(self)
		
		offset = 100#px
		windowsSize = [GetSystemMetrics(0)-offset, GetSystemMetrics(1)-offset]
		self.setWindowTitle(title)
		self.horizontalLayout = QHBoxLayout(self)
		self.horizontalLayout.setMargin(0)

		self.webView = QWebView(self)
		sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		sizePolicy.setHeightForWidth(self.webView.sizePolicy().hasHeightForWidth())
		self.webView.setSizePolicy(sizePolicy)

		self.horizontalLayout.addWidget(self.webView)
		

		self.webView.settings().setAttribute(QWebSettings.PluginsEnabled, True)
		self.webView.show()		
		self.webView.load(QUrl(path)) # Change path to actual file.

		self.exec_()
		