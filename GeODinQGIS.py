# -*- coding: utf-8 -*-
"""
/***************************************************************************
GeODinQGIS
							 A QGIS plugin
This plugin connects GeODin with QGIS
						  -------------------
	begin                : 2015-02-16
	git sha              : $Format:%H$
	copyright            : (C) 2015 by Fugro Consult GmbH
	email                : www.fugro.de
***************************************************************************/

/***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************/
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from win32api import GetSystemMetrics
import sys

import resources_rc, os.path

from GeODinQGIS_Main import GeODinQGISMain
from GeODinQGIS_Settings import Settings
from ui_Files.ui_GeODinQGIS_Help import Ui_HelpDialog
from pythonmodules.helpFunction import *
from extras.layout import ImageLayout

class GeODinQGIS:

	def __init__(self, iface):
		# Save reference to the QGIS interface
		self.iface = iface
		# locate main function in "GeODinQGIS_Main"
		self.main = GeODinQGISMain(iface)
		if self.main.error:
			return

		#initialize plugin directory
		self.plugin_dir = os.path.dirname(__file__)
		
		# create language and dictionary
		self.language = self.main.lang
		self.dictionary = self.main.dictionary

	def initGui(self):
		if self.main.error:
			return
		# Create actionmain that will start plugin configuration
		self.actionmain = QAction(QIcon(":\plugins\GeODinQGIS\icons\logo.png"), u"Main", self.iface.mainWindow())
		
		# connect the actionmain to the run method
		QObject.connect(self.actionmain, SIGNAL("triggered()"), self.openMain)
		
		# Add Plugin to toolbar
		self.toolBar = self.iface.addToolBar("GeODin")
		self.toolBar.addAction(self.actionmain)
		
		# manage language icons
		lang_en = QAction(QIcon(":\plugins\GeODinQGIS\icons\i_371F.png"), u"English", self.toolBar)
		lang_de = QAction(QIcon(":\plugins\GeODinQGIS\icons\i_370F.png"), u"Deutsch", self.toolBar)
		lang_fr = QAction(QIcon(":\plugins\GeODinQGIS\icons\i_372F.png"), u"Fran\u00E7ais", self.toolBar)
		lang_ru = QAction(QIcon(":\plugins\GeODinQGIS\icons\i_373F.png"), u"русский", self.toolBar)
		
		# manage menu to set operating language
		self.languageMenu = QMenu(self.dictionary.getWord(self.language,"Language"), self.toolBar )
		self.languageMenu.setIcon(self.main.activeIcon)
		self.languageMenu.addAction( lang_en )
		self.languageMenu.addAction( lang_de )
		self.languageMenu.addAction( lang_fr )
		self.languageMenu.addAction( lang_ru )
		
		# french and russian are currently not available
		lang_fr.setEnabled(False)
		lang_ru.setEnabled(False)
		
		# enable language change, connect to functions
		QObject.connect(lang_en, SIGNAL("triggered()"), self.changeToEn)
		QObject.connect(lang_de, SIGNAL("triggered()"), self.changeToDe)
		QObject.connect(lang_fr, SIGNAL("triggered()"), self.changeToFr)
		QObject.connect(lang_ru, SIGNAL("triggered()"), self.changeToRu)
		
		# add settings menu to manage plugin settings and operating language
		self.preferenceMenu = QMenu(self.toolBar)
		self.preferenceMenu.addMenu(self.languageMenu)
		self.preferenceButton = QToolButton()
		self.preferenceButton.setIcon(QIcon(":\plugins\GeODinQGIS\icons\system_run.png"))
		self.preferenceButton.setMenu(self.preferenceMenu)
		self.preferenceButton.setPopupMode( QToolButton.InstantPopup)
		self.toolBar.addWidget(self.preferenceButton)
		
		# add layer refresh button
		self.refreshButton = QAction(QIcon(":\plugins\GeODinQGIS\icons\system_refresh.png"), u"Refresh", self.iface.mainWindow())
		QObject.connect(self.refreshButton, SIGNAL("triggered()"), self.refresh)
		self.toolBar.addAction(self.refreshButton)
		
		# add plugin documentation button
		self.helpButton = QAction(QIcon(":\plugins\GeODinQGIS\icons\system_help.png"), u"Help", self.iface.mainWindow())
		QObject.connect(self.helpButton, SIGNAL("triggered()"), self.openHelp)
		self.toolBar.addAction(self.helpButton)
		
		# add settings button
		self.settingsButton = QAction(QIcon(""), self.dictionary.getWord(self.language,"Settings"), self.toolBar)
		self.settingsButton.setIcon(QIcon(":\plugins\GeODinQGIS\icons\settings.png"))
		self.preferenceMenu.addAction(self.settingsButton)
		QObject.connect(self.settingsButton, SIGNAL("triggered()"), self.openSettings)
	
	def openSettings(self):
		# open extra file "GeODinQGIS_Settings" and execute class "Settings" with variables from "GeODinQGIS_Main"
		settings = Settings(self.main)
		self.main.tmpDirectory = settings.le_dir.text()

	def unload(self):
		# unload plugin
		if not self.main.error:
			# Remove the buttons
			self.iface.removeToolBarIcon(self.actionmain)
			self.iface.removeToolBarIcon(self.helpButton)

			# remove tool bar
			del self.toolBar
			
		self.main = None
		self.plugin_dir = None
		self.language = None

	def openMain(self):
		# show main functions in a right docked widget
		self.iface.addDockWidget(Qt.RightDockWidgetArea, self.main)
		self.main.getBuild()
		self.main.checkVersion()
		
	def openHelp(self):
		if self.language == 'en':
			path = self.plugin_dir + "\help\help_en.pdf"
		elif self.language == 'de':
			path = self.plugin_dir + "\help\help_de.pdf"
		
		ImageLayout(path, "GeODinQGIS Help")


		
	def refresh(self):
		#Warning message box with two buttons
		msgBox = QMessageBox()
		msgBox.setInformativeText(self.main.dictionary.getWord(self.main.lang,"Do you want to accept the changes and discard all layer informations?"))
		msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
		msgBox.setDefaultButton(QMessageBox.Cancel)
		msgBox.setWindowTitle('Warning')
		canvas = self.iface.mapCanvas()
		allLayers = canvas.layers()
		for layerid, layer in enumerate(allLayers):
			databases = []
			try:
				for feature in layer.getFeatures():
					database = Database(feature["database"]+str(layerid), feature["database"])
					database.options["connection"] = feature["dbtype"]
					if not database in databases:
						databases.append(database)
					else:
						database = databases[databases.index(database)]
					project = Project(feature["prjname"], database)
					project.id = feature["prjid"]
					if not project in database.projects:
						database.projects.append(project)
					else:
						project = database.projects[database.projects.index(project)]

					object = Object(feature["longname"], project)
					object.shortname = feature["shortname"]
					object.locname = feature["objecttype"]
					object.invid = feature["invid"]
					object.coordinates = (feature["xcoord"], feature["ycoord"])
					object.data = []
					for i in range(10, len(feature.attributes())):
						object.data.append(feature.attributes()[i])
					project.objects.append(object)
			except Exception,e :
				print str(e)
			
			changes = False
			features = []
			for database in databases:
				
				for project in database.projects:
					query = """SELECT GEODIN_LOC_LOCREG.INVID, GEODIN_LOC_LOCREG.SHORTNAME, GEODIN_LOC_LOCREG.LONGNAME, GEODIN_LOC_LOCREG.XCOORD, GEODIN_LOC_LOCREG.YCOORD, GEODIN_SYS_LOCTYPES.Gen_name
								FROM GEODIN_LOC_LOCREG INNER JOIN GEODIN_SYS_LOCTYPES ON GEODIN_LOC_LOCREG.LOCTYPE = GEODIN_SYS_LOCTYPES.GEN_DESC
								WHERE GEODIN_LOC_LOCREG.PRJ_ID = '{0}';""".format(project.id)

					result = self.main.connectToDatabase(database, query)

					for row in result:
						#get the data from database and check if something has changed
						if project.getObject(row[0]):
							object = project.getObject(row[0])
							if row[1] != object.shortname or row[2] != object.name or row[3] != object.coordinates[0] or row[4] != object.coordinates[1] or row[5] != object.locname:
								changes = True
						else:
							changes = True
						feat = QgsFeature()
						feat.setGeometry(QgsGeometry.fromPoint(QgsPoint(row[3], row[4])))
						attributes = [row[0], row[1], row[2], row[3], row[4], database.options["connection"], database.filepath, project.name, project.id, row[5]]
						attributes += object.data
						feat.setAttributes(attributes)
						features.append(feat)
			if changes:
				#if something has changed, open message box and ask for changing
				msgBox.setText(layer.name().split('_')[0]+self.main.dictionary.getWord(self.main.lang," has been modified."))
				if msgBox.exec_() == 1024:
					provider = layer.dataProvider()
					provider.deleteFeatures([f.id() for f in layer.getFeatures()])
					provider.addFeatures(features)
					layer.commitChanges()
		canvas.refresh()
			
	def changeToEn(self):
		# change language to English and set the activeIcon from self.main
		self.main.changeLang('en')
		self.language = 'en'
		self.languageMenu.setIcon(self.main.activeIcon)
		self.languageMenu.setTitle(self.dictionary.getWord(self.language,"Language"))
		self.settingsButton.setText(self.dictionary.getWord(self.language,"Settings"))
	def changeToDe(self):
		# change language to German and set the activeIcon from self.main
		self.main.changeLang('de')
		self.language = 'de'
		self.languageMenu.setIcon(self.main.activeIcon)
		self.languageMenu.setTitle(self.dictionary.getWord(self.language,"Language"))
		self.settingsButton.setText(self.dictionary.getWord(self.language,"Settings"))
	def changeToFr(self):
		# change language to French and set the activeIcon from self.main
		self.main.changeLang('fr')
		self.language = 'fr'
		self.languageMenu.setIcon(self.main.activeIcon)
		self.languageMenu.setTitle(self.dictionary.getWord(self.language,"Language"))
		self.settingsButton.setText(self.dictionary.getWord(self.language,"Settings"))
	def changeToRu(self):
		# change language to Russian and set the activeIcon from self.main
		self.main.changeLang('ru')
		self.language = 'ru'
		self.languageMenu.setIcon(self.main.activeIcon)
		self.languageMenu.setTitle(self.dictionary.getWord(self.language,"Language"))
		self.settingsButton.setText(self.dictionary.getWord(self.language,"Settings"))

class HelpObject(QDialog):
	def __init__(self, page, title):
		QDialog.__init__(self)
		self.ui = Ui_HelpDialog()
		self.ui.setupUi(self)
		self.setWindowTitle(title)
		self.load(page)

		self.show()
		self.exec_()

	def load(self, page):
		self.ui.webView.load(QUrl(page))#"file:///C:/Users/.../.qgis2/python/plugins/GeODinQGIS/help/index.html?language=en"))
		
