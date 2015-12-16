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
import codecs
from ui_Files.ui_GeODinQGIS_Main import Ui_GeODinQGISMain

import os, sys, time, logging, datetime, locale, ctypes, binascii, win32com.client
try:
	import pyodbc
except:
	from pythonmodules import pypyodbc
	print "Main: Can not import pyodbc maybe it is needed."
try:
	import psycopg2
except:
	print "Main: Can not import psycopg2 maybe it is needed."

from pythonmodules import _mysql
from pythonmodules.helpFunction import *
from _winreg import *

from GeODinQGIS_NewObject import NewObject
from GeODinQGIS_Shape import *
from GeODinQGIS_DragShp import DragShp
from GeODinQGIS_Settings import Settings

try:
	from extras.layout import *
	from extras.opengeodin import *
except Exception,e:
	print str(e)

class GeODinQGISMain(QDockWidget, Ui_GeODinQGISMain):

	def __init__(self, iface):
		# setup UI and connect the buttons
		QDockWidget.__init__(self)
		self.iface = iface
		self.setupUi(self)

		# local path for plugin
		self.pluginDirectory = os.path.dirname(__file__)
		if "Users" in self.pluginDirectory:
			self.userPluginDirectory = self.pluginDirectory
		else:
			self.userPluginDirectory = 'C:\\Users\\'+os.environ.get( "USERNAME" )+'\\.qgis2\\python\\plugins\\GeODinQGIS'
			
		# path of tmp folder in home directory
		self.tmpDirectory = self.userPluginDirectory+'\\tmp'
		self.GeODin = None
		
		# path of log folder in home directory
		self.logDirectory = self.userPluginDirectory+'\\logs'
		# path of config file in home directory
		self.configFile = self.userPluginDirectory+'\\config.cfg'

		# store NewObject object
		self.crd = None
		# actual language icon
		self.activeIcon = ''
		self.error = 0
		
		self.config = ConfigParser()
		
		# set plugin icons
		self.geodinicon = QIcon(":\plugins\GeODinQGIS\icons\logo.png")
		self.dbicon = QIcon(":\plugins\GeODinQGIS\icons\i_484F.png")
		self.dbicon_open = QIcon(":\plugins\GeODinQGIS\icons\i_485F.png")
		self.dbicon_del = QIcon(":\plugins\GeODinQGIS\icons\i_102F.png")
		
		self.prjicon = QIcon(":\plugins\GeODinQGIS\icons\i_099F.png")
		self.prjicon_open = QIcon(":\plugins\GeODinQGIS\icons\i_101F.png")
		
		self.objicon = QIcon(":\plugins\GeODinQGIS\icons\i_126F.png")
		self.objicon_type = QIcon(":\plugins\GeODinQGIS\icons\i_222F.png")
		self.objicon_single = QIcon(":\plugins\GeODinQGIS\icons\i_232F.png")
		
		self.new_obj = QIcon(":\plugins\GeODinQGIS\icons\i_100F.png")
		self.docicon = QIcon(":\plugins\GeODinQGIS\icons\i_157F.png")
		self.shpicon = QIcon(":\plugins\GeODinQGIS\icons\i_246F.png")
		self.queryIcon = QIcon(":\plugins\GeODinQGIS\icons\i_090F.png")
		self.ownQueryIcon = QIcon(":\plugins\GeODinQGIS\icons\i_0815F.png")
		
		# set button signals
		QObject.connect(self.singleImportButton, SIGNAL("clicked()"), self.loadMultipleDatabases)
		QObject.connect(self.multipleImportButton, SIGNAL("clicked()"), self.loadSingleDatabase)
		QObject.connect(self.iface, SIGNAL("currentLayerChanged(QgsMapLayer *)"), self.layerActivationChanged)
		
		# tool tips
		self.singleImportButton.setToolTip('Import Databases')
		self.singleImportButton.setFont(QFont('OldEnglish', 10))
		self.multipleImportButton.setToolTip('Load Databases')
		self.multipleImportButton.setFont(QFont('OldEnglish', 10))

		# set treeWidget signals
		self.connect(self.treeWidget, SIGNAL("itemExpanded(QTreeWidgetItem*)"), self.expanded)
		self.connect(self.treeWidget, SIGNAL("itemCollapsed(QTreeWidgetItem*)"), self.collapsed)
		self.connect(self.treeWidget, SIGNAL("itemDoubleClicked(QTreeWidgetItem*, int)"), self.buildTree)
		self.connect(self.treeWidget, SIGNAL("itemSelectionChanged ()"), self.activateItem)
		self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
		self.treeWidget.customContextMenuRequested.connect(self.treeMenu)
		self.treeWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
		
		#self.treeWidget.setDragEnabled(True)
		
		# connect to dictionary, English language by default
		self.dictionary = Dict(os.path.join(self.pluginDirectory, 'lang/all.lang'))
		#self.givenObj = ''
		
		# use language of operating system, if possible
		# if not use english as default
		osLanguage = locale.windows_locale[ctypes.windll.kernel32.GetUserDefaultUILanguage()].split('_')[0]
		if osLanguage in self.dictionary.getLanguages():
			self.lang = osLanguage
		else:
			self.lang = 'en'
		
		# if plugin directory of QGIS is not set, create it
		try:
			if not os.path.isdir(self.userPluginDirectory):
				os.makedirs(self.userPluginDirectory)
		except WindowsError as e:
			if e.errno == 13:
				uc = UserChooser(self.dictionary.getWord(self.lang,"Choose your home directory."))
				if uc.okPressed:
					self.userPluginDirectory = 'C:\\Users\\'+uc.user+'\\.qgis2\\python\\plugins\\GeODinQGIS'
					uc = None
					try:
						if not os.path.isdir(self.userPluginDirectory):
							os.makedirs(self.userPluginDirectory)
					except Exception,e:
						QMessageBox.information(None,self.dictionary.getWord(self.lang,"Error"),str(e))
						self.error = 1
						return

		# path of tmp folder in home directory
		self.tmpDirectory = self.userPluginDirectory+'\\tmp'
		# path of tmp directory for restoring it, if lost
		self.def_tmp_dir = self.tmpDirectory
		# path of log folder in home directory
		self.logDirectory = self.userPluginDirectory+'\\logs'
		# path of config file in home directory
		self.configFile = self.userPluginDirectory+'\\config.cfg'

		# if log directory not available, create it
		if not os.path.isdir(self.logDirectory):
			os.makedirs(self.logDirectory)
			open(self.logDirectory+'\\error.log', 'a').close()
			
		# create error logger
		self.lgr = logging.getLogger('GeODinQGIS')
		if not len(self.lgr.handlers):
			self.lgr.setLevel(logging.DEBUG)
			# add a file handler
			fh = logging.FileHandler(self.logDirectory+'\\error.log')
			fh.setLevel(logging.DEBUG)
			# create a formatter and set the formatter for the handler.
			frmt = logging.Formatter('%(asctime)s %(levelname)-8s %(filename)s:%(lineno)-4d: %(message)s', "%Y-%m-%d %H:%M:%S")
			fh.setFormatter(frmt)
			# add the Handler to the logger
			self.lgr.addHandler(fh)
		
		
		# if tmp directory not set, create it
		if not os.path.isdir(self.tmpDirectory):
			os.makedirs(self.tmpDirectory)
			
		# if config file not available, create it
		# set sections and default settings in config file
		if not os.path.isfile(self.configFile):
			self.config.add_section('Databases')
			self.config.add_section('Options')
			self.config.set('Options', 'lang', self.lang)
			print "hier 1"
			self.config.set('Options', 'project', 'tmp.qgs')
			self.config.set('Options', 'geodinrootdir', self.getGeodinPath())
			self.config.set('Options', 'programdata', self.getProgramData())
			self.config.set('Options', 'suppressattribute', 'False')
			self.config.set('Options', 'savelayer', 'True')
			self.config.set('Options', 'tmpdirectory', self.tmpDirectory)
			self.config.add_section('Layouts')
			self.saveConfig()
			self.changeLang(self.lang)
	
		self.config.read(self.configFile)
#		self.config.readfp(codecs.open(self.configFile, "r", "utf-8"))
		
		# call config file checker
		self.configChecker()
		
		# get language option from config file
		self.lang = self.config.get('Options', 'lang')
		# change language according to config file
		self.changeLang(self.lang)
		# get root directory of GeODin installation
		self.geodin_dir = self.config.get('Options', 'geodinrootdir')
		self.dbs = []
		
		# map over databases written to config file
		for db in self.config.options('Databases'):
			fn = self.config.get('Databases', db)
			alias = fn.split('/')[-1][:-4]
			if os.path.exists(fn):
				options = {}
				options["uname"] = ""
				options["upassword"] = ""
				options["connection"] = "ODBC"
				database = Database(alias, fn)
				database.options = options
				self.newTopLevelItem(database)
			else:
				self.config.remove_option('Databases', db)
		
		# check if config has the sections "Databases" and "Options"
		# add content to sections
		if "Databases" not in self.config.sections():
			self.config.add_section('Databases')
		if "Options" not in self.config.sections():
			self.config.add_section('Options')
			self.config.set('Options', 'lang', self.lang)
			print "hier 2"
			self.config.set('Options', 'project', 'tmp.qgs')
			self.config.set('Options', 'geodinrootdir', self.getGeodinPath())
			self.config.set('Options', 'programdata', self.getProgramData())
			self.config.set('Options', 'suppressattribute', 'False')
			self.config.set('Options', 'savelayer', 'True')
			self.config.set('Options', 'tmpdirectory', self.tmpDirectory)
			
		if "Layouts" not in self.config.sections():
			self.config.add_section('Layouts')
			self.saveConfig()
			self.changeLang(self.lang)
			
		self.saveConfig()
		
		
		self.deny = 0

		self.inProcess = False
		
	def configChecker(self):
		# set default config array to check
		configArray = {"Databases":{}, "Options":{"lang":self.lang, "project":'tmp.qgs', "geodinrootdir":self.getGeodinPath(), "programdata":self.getProgramData(), "suppressattribute":"False", "savelayer":"True", "tmpdirectory":self.tmpDirectory}, "Layouts":{}}
		
		# map over config array
		# check config consistency and restore if necessary
		for f in configArray.keys():
			if f in self.config.sections():
				for i in configArray[f].keys():
					if i not in configArray[f].keys():
						self.config.set(f, i, configArray[f][i])
						
			else:
				self.config.add_section(f)
				for i in configArray[f]:
					self.config.set(f, i, configArray[f][i])
						
		self.saveConfig()
		
	def loadMultipleDatabases(self):
		# access key from Windows Registry
		# open main database folder
		key = None
		try:
			key = OpenKey(HKEY_CURRENT_USER, r"Software\GeODin-System\Database", 0, KEY_READ)
		except WindowsError as e:
			self.lgr.info('{0}: {1}'.format(e, r"Computer\HKEY_CURRENT_USER\Software\GeODin-System\System"))
			QMessageBox.information(None,self.dictionary.getWord(self.lang,"Connection Error"),self.dictionary.getWord(self.lang,"No GeODin database connections found."))
			return
		
		# loop through subkeys
		i=0
		while True:
			database = Database()
			options = None
			path = None
			try:
				asubkey_name = EnumKey(key,i)					# numerate through folder, get subkeys (folder name = database name)
			except:
				break
			try:
				asubkey = OpenKey(key,asubkey_name)				# open subkeys (database folders)
				try:
					options, path = self.getConnectionOptions(QueryValueEx(asubkey, "ADOConnection")[0], "ADOConnection", asubkey_name)
				except AttributeError as e:
					self.lgr.error(e)
				except KeyError as e:
					self.lgr.error(asubkey_name+": "+str(e))
				except IndexError as e:
					pass
				except Exception,e:
					self.lgr.error(e)
					pass
				try:
					if not options:
						options, path = self.getConnectionOptions(QueryValueEx(asubkey, "FireDACConnection")[0], "FireDACConnection", asubkey_name)
				except WindowsError as e:
					self.lgr.error(e)
				except AttributeError as e:
					self.lgr.error(e)
				except KeyError as e:
					self.lgr.error(e)
				except Exception,e:
					self.lgr.error(e)
					pass

				database.name = asubkey_name
				database.filepath = path
				database.options = options

				if path not in [db.filepath for db in self.dbs]:
					self.newTopLevelItem(database)
				else:
					# if database has been loaded yet, check if listed in Config and delete from there
					# because it's also located in the registry
					for db in self.config.options('Databases'):
						fn = self.config.get('Databases', db)
						if fn == path:
							self.config.remove_option('Databases', db)
							self.saveConfig()
			except TypeError as e:
				self.lgr.error(e)
				pass
			except UnicodeEncodeError as e:
				self.lgr.error(e)
				pass
			except UnicodeDecodeError as e:
				self.lgr.error(e)
				pass
			except NameError as e:
				self.lgr.error(e)
				pass
			except AttributeError as e:
				self.lgr.error(e)
				pass
			except Exception,e:
				self.lgr.error(e)
				pass
			i+=1
		if key:
			CloseKey(key)

	def getConnectionOptions(self, connectionString, key, name):
		#transforms the option string from registry to dictionary
		#returns a options dictionary and a file path to the database
		options = {}
		options["ip"] = "127.0.0.1"
		options["uname"] = ""
		options["upassword"] = ""
		path = ""
		for option in connectionString.split(';'):
			options[option.split('=')[0]]=option.split('=')[1]
		
		if key == "ADOConnection":
			if "Provider" in options.keys():
				options["connection"] = options.pop("Provider")
				if "OLEDB" in options["connection"]:
					options["connection"] = "ODBC"
				elif "SQLOLEDB" in options["connection"]:
					options["connection"] = "MSQL"
				elif "MSDAORA" in options["connection"]:
					options["connection"] = "Oracle"
				elif "SQLSERVER" in options["connection"]:
					options["connection"] = "SQLCE"
				elif "MSDASQL" in options["connection"]:
					options["connection"] = "DSNConnection"
			if "Data Source" in options.keys():
				if options["connection"] == "MSQL":
					options["ip"] = options.pop("Data Source")
				elif options["connection"] == "ODBC" or options["connection"] == "SQLCE":
					path = options["Data Source"]
				elif options["connection"] == "Oracle":
					options["ip"] = options["Data Source"].split('/')[0]
					options["database"] = options["Data Source"].split('/')[1]
				elif options["connection"] == "DSNConnection":
					options["DSN"] = options.pop("Data Source")
			if "Initial Catalog" in options.keys():
				options["database"] = options.pop("Initial Catalog")
			if "User ID" in options.keys():
				options["uname"] = options.pop("User ID")
			if "Password" in options.keys():
				options["upassword"] = options.pop("Password")
		elif key == "FireDACConnection":
			if "DriverID" in options.keys():
				options["connection"] = options.pop("DriverID")
				if "MSAcc" in options["connection"]:
					options["connection"] = "ODBC"
					path = options["Database"]
					del options["Database"]
				elif "MSSQL" in options["connection"]:
					options["connection"] = "MSSQL"
					options["database"] = options.pop("Database")
				elif "Ora" in options["connection"]:
					options["connection"] = "Oracle"
					options["ip"] = options["Database"].split('/')[0]
					options["database"] = options["Database"].split('/')[1]
				elif "MySQL" in options["connection"]:
					options["connection"] = "MySQL"
					options["database"] = options.pop("Database")
				elif "PG" in options["connection"]:
					options["connection"] = "PostgreSQL"
					options["database"] = options.pop("Database")
			if "Server" in options.keys():
				options["ip"] = options.pop("Server")
			if "User_Name" in options.keys():
				options["uname"] = options.pop("User_Name")
			if "Password" in options.keys():
				options["upassword"] = options.pop("Password")
		
		if not len(path) and "database" in options.keys():
			#if it is no local database, create a pseudo path
			path = options["ip"]+'/'+name
		else:
			del options["ip"]
		return options, path.replace('\\','/')
		
	def saveConfig(self):
		# write settings to config file to save them
		with codecs.open(self.configFile, 'wb', encoding='utf-8') as configfile:
			self.config.write(configfile)
#			self.config.write(codecs.open(self.configFile,'wb+','utf-8'))
		
	def loadSingleDatabase(self, database=None):
		#load a local access database
		try:
			fileName = QFileDialog.getOpenFileName(None, self.dictionary.getWord(self.lang,"Open database"), "C:\\", "Microsoft Access(*.accdb;*.mdb)")
			if fileName and fileName not in [db.filepath for db in self.dbs]:
				if database == None:
					database = Database(fileName.split('/')[-1][:-4])
					options = {}
					options["uname"] = ""
					options["upassword"] = ""
					options["connection"] = "ODBC"
					database.options = options
				
				self.config.set('Databases', database.name, fileName)
				self.saveConfig()
				database.filepath = fileName
				self.newTopLevelItem(database)
				return 1
		except Exception,e:
			self.lgr.error(e)
			return 0
		return 0
			
	def getGeodinPath(self):
		#get the GeODin installation path from registry
		#return path or empty string
		try:
			key = OpenKey(HKEY_CURRENT_USER, r"Software\GeODin-System\System", 0, KEY_READ)
			path, regtype = QueryValueEx(key, 'RootDir')
			CloseKey(key)
		except WindowsError as e:
			self.lgr.info('{0}: {1}'.format(e, r"Computer\HKEY_CURRENT_USER\Software\GeODin-System\System"))
			QMessageBox.information(None,self.dictionary.getWord(self.lang,"Connection Error"),self.dictionary.getWord(self.lang,"No GeODin installation found."))
			return ''

		return path		
		
	def getProgramData(self):
		# get the geodin program information from geodin.ini
		# return path
		
#		try:
#			geodin_path = self.getGeodinPath()
#			# locate geodin.ini in installation folder
#			ini = geodin_path + "\\GEODIN.INI"
#			
#			# read geodin.ini and get path to program data
#			geodinConfig = ConfigParser()
#			geodinConfig.read(ini)
#			path_data = geodinConfig.get('SYSTEM', 'ProgramData')
#			
#		except:
#			print "Fehler: Program Data"
#			return
#			
#		return path_data
		
		
		#get the GeODin installation path from registry
		#return path or empty string
		try:
			key = OpenKey(HKEY_CURRENT_USER, r"Software\GeODin-System\ChildWindows\GRFMAIN\QVLayoutFolders", 0, KEY_READ)
			path_data, regtype = QueryValueEx(key, 'E0')
			CloseKey(key)
		except WindowsError as e:
			self.lgr.info('{0}: {1}'.format(e, r"Computer\HKEY_CURRENT_USER\Software\GeODin-System\ChildWindows\GRFMAIN\QVLayoutFolders"))
			return ''		
		
		return path_data

	def load_db(self, database, level, project = None):
		# execute queries in GeODin database
		if level == 0:
			#load only project names and description
			query = '''SELECT DISTINCT LOCPRMGR.PRJ_ID, LOCPRMGR.PRJ_USER, LOCPRMGR.PRJ_DATE, LOCPRMGR.PRJ_ALIAS, LOCPRMGR.PRJ_NAME
						FROM GEODIN_LOC_LOCREG INNER JOIN LOCPRMGR ON GEODIN_LOC_LOCREG.PRJ_ID = LOCPRMGR.PRJ_ID
						ORDER BY LOCPRMGR.PRJ_NAME;
						'''			

		elif level == 1:
			#load information of specific project
			query = """SELECT GEODIN_LOC_LOCREG.LONGNAME, GEODIN_SYS_LOCTYPES.GEN_NAME, GEODIN_LOC_LOCREG.INVID, GEODIN_LOC_LOCREG.SHORTNAME, GEODIN_LOC_LOCREG.XCOORD, GEODIN_LOC_LOCREG.YCOORD
						FROM GEODIN_SYS_LOCTYPES INNER JOIN (GEODIN_LOC_LOCREG INNER JOIN LOCPRMGR ON GEODIN_LOC_LOCREG.PRJ_ID = LOCPRMGR.PRJ_ID) ON GEODIN_SYS_LOCTYPES.GEN_DESC = GEODIN_LOC_LOCREG.LOCTYPE
						WHERE LOCPRMGR.PRJ_ID='{0}'
						ORDER BY LOCPRMGR.PRJ_NAME, GEODIN_SYS_LOCTYPES.GEN_NAME;
					""".format(project.id)
		try:
			result = None
			if database.options["connection"] == "ODBC":
				#connect to local Microsoft database files (*.mdb, *.accdb)
				if 'pyodbc' in sys.modules.keys():
					connection = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ="+database.filepath+";")
				else:
					connection = pypyodbc.win_connect_mdb(database.filepath)
				cursor = connection.cursor()
				cursor.execute(query)
				result = cursor.fetchall()
				cursor.close()
				connection.close()
			
			elif database.options["connection"] == "DSNConnection":
				#connect to DSN connection
				try:
					if 'pyodbc' in sys.modules.keys():
						connection = pyodbc.connect("DSN="+database.options["DSN"])
					else:
						connection = pypyodbc.connect("DSN="+database.options["DSN"])
				except Exception,e:
					QMessageBox.warning(self, 'Error', str(e))
					self.lgr.error('path='+database.filepath+', name='+database.name + ', error=' +str(e))
					return 1
				cursor = connection.cursor()
				cursor.execute(query)
				result = cursor.fetchall()		
				cursor.close()
				connection.close()
			elif database.options["connection"] == "MSSQL":
				#connect to DSN connection
				if not database.options["uname"] or not database.options["upassword"]:
					login = Login(database.options["uname"], database.options["upassword"])
					try:
						database.options["uname"] = login.uname
						database.options["upassword"] = login.upassword
						if 'pyodbc' in sys.modules.keys():
							connection = pyodbc.connect("DRIVER={SQL Server};SERVER="+database.options["ip"]+";DATABASE="+database.options["database"]+";UID="+database.options["uname"]+";PWD="+database.options["upassword"])
						else:
							return 1
						del login
					except:
						del login
						QMessageBox.warning(self, 'Error', 'Bad user or password')
						database.options["upassword"] = ""
						return 1
				else:
					if 'pyodbc' in sys.modules.keys():
						connection = pyodbc.connect("DRIVER={SQL Server};SERVER="+database.options["ip"]+";DATABASE="+database.options["database"]+";UID="+database.options["uname"]+";PWD="+database.options["upassword"])
					else:
						return 1
				cursor = connection.cursor()
				cursor.execute(query)
				result = cursor.fetchall()		
				cursor.close()
				connection.close()
			elif database.options["connection"] == "MySQL":
				#connect to MySQL databases
				if not database.options["uname"] or not database.options["upassword"]:
					login = Login(database.options["uname"], database.options["upassword"])
					try:
						database.options["uname"] = login.uname
						database.options["upassword"] = login.upassword
						connection = _mysql.connect(database.options["ip"], database.options["uname"], database.options["upassword"], database.options["database"])
						login.close()
						del login
					except:
						login.close()
						del login
						QMessageBox.warning(self, 'Error', 'Bad user or password')
						database.options["upassword"] = ""
						return 1
				else:
					try:
						connection = _mysql.connect(database.options["ip"], database.options["uname"], database.options["upassword"], database.options["database"])
					except Exception,e:
						QMessageBox.warning(self, 'Error', str(e))
						return 1

				connection.query(query)
				r = connection.use_result()
				row = r.fetch_row()
				result=[]
				while row:
					result.append(row)
					row = r.fetch_row()
				connection.close()
			elif database.options["connection"] == "PostgreSQL":
				#connect to PostgreSQL databases
				if 'psycopg2' in sys.modules.keys():
					if not database.options["uname"] or not database.options["upassword"]:
						#if no user name or password in registry open a login dialog
						login = Login(database.options["uname"], database.options["upassword"])
						try:
							database.options["uname"] = login.uname
							database.options["upassword"] = login.upassword
							connection = psycopg2.connect("dbname={0} user={1} host={2} password={3}".format(database.options["database"], database.options["uname"], database.options["ip"], database.options["upassword"]))
							del login
						except:
							del login
							QMessageBox.warning(self, 'Error', 'Bad user or password')
							database.options["upassword"] = ""
							return 1
					else:
						#otherwise login with given data
						connection = psycopg2.connect("dbname={0} user={1} host={2} password={3}".format(database.options["database"], database.options["uname"], database.options["ip"], database.options["upassword"]))

				else:
					return 1
				cursor = connection.cursor()
				cursor.execute(query)
				result = cursor.fetchall()
				cursor.close()
				connection.close()
			
			if level == 0:
				for row in result:
					#store the results in the specific arrays
					project = Project(None, database)
					project.id = row[0]
					project.user = row[1]
					project.date = row[2]
					project.alias = row[3]
					project.name = row[4]
					database.projects.append(project)

			elif level == 1:
				for row in result:
					#store the results in the specific arrays
					object = Object(None, project)
					object.name = row[0]
					object.locname = row[1]
					object.invid = row[2]
					object.shortname = row[3]
					object.coordinates = (row[4], row[5])
					project.objects.append(object)
			result = None
		except NameError as e:
			self.lgr.error('path={0}, alias={1}, error={2}'.format(database.filepath, database.name, str(e)))
			return 1
		except KeyError as e:
			self.lgr.error('path={0}, alias={1}, error={2}'.format(database.filepath, database.name, str(e)))
			return 1
		except psycopg2.ProgrammingError as e:
			self.lgr.error('path={0}, alias={1}, error={2}'.format(database.filepath, database.name, str(e)))
			return 1
		except:
			self.lgr.error('path='+database.filepath+', alias='+database.name + ', error=' +str(sys.exc_info()[0]))
			return 1
		return 0
		#return 0

		
	def newTopLevelItem(self, database):
		#create a TopLevelItem in QTreeWidget (database item)
		self.dbs.append(database)
		item = TreeWidgetItem([database.name])
		item.setIcon(0, self.dbicon)
		item.setToolTip(0, database.filepath)
		item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
		item.itemType = DATABASEITEM
		item.extraInformation = database
		item.normalString = database.name
		self.treeWidget.addTopLevelItem(item)
		
	def buildTree(self, clickedItem = None, clickedColumn = None):
		#build the QTreeWidget:
		#1. possibility: the clicked item is a database item and has currently no child items
		#2. possibility: the clicked item is a project item and has currently no child items
		#3. possibility: the clicked item is a query item and has currently no child items
		
		if not clickedItem:
			#expand database item with right click menu
			try:
				clickedItem = self.treeWidget.itemFromIndex(self.treeWidget.selectedIndexes()[0])
			except Exception,e:
				print str(e)
			
		if clickedItem and clickedItem.itemType == DATABASEITEM and clickedItem.childCount() == 0:
			#load projects and documents
			try:
				#get database with the name of the TreeWidgetItem
				database = clickedItem.extraInformation
			except:
				return
			
			if self.load_db(database, 0):
				#if loading database returns with errors
				self.error = 1
				return
			self.error = 0
			
			for prj in database.projects:
				#add all projects to tree

				item_prj = TreeWidgetItem([prj.name])			
				item_prj.setIcon(0, self.prjicon)
				item_prj.setData(0, Qt.WhatsThisRole, prj.id)
				item_prj.extraInformation = prj
				item_prj.itemType = PROJECTITEM
				item_prj.normalString = prj.name
				item_prj.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
				
				try:
					if prj.alias != None:
						proj_tip = prj.id  + "\n" + prj.user + "\n" + str(prj.date) + "\n" + prj.alias
					else:
						proj_tip = prj.id  + "\n" + prj.user + "\n" + str(prj.date)
					item_prj.setToolTip(0, proj_tip)
				except Exception,e :
					self.lgr.error('name='+prj.name+', id='+prj.id+ ', user='+prj.user+', alias='+prj.alias+', error=' +str(e))
				clickedItem.addChild(item_prj)


				clickedItem.sortChildren(0,Qt.AscendingOrder)
	
			query_name = self.getDBQueries(database)
			if query_name:
				for query in query_name:
					queryObject = Query(query, database)
					item_query = TreeWidgetItem([query])
					item_query.setIcon(0, self.queryIcon)
					item_query.extraInformation = queryObject
					item_query.itemType = DBQUERYITEM
					item_query.normalString = query
					clickedItem.addChild(item_query)
					database.queries.append(queryObject)

			data_name, data_path = self.getDBLayer(database)
			if data_name:
			
				item_doc = TreeWidgetItem([self.dictionary.getWord(self.lang,"Documents")])
				item_doc.setIcon(0, self.docicon)
				item_doc.extraInformation = "Documents"
				item_doc.itemType = DOCUMENTITEM
				item_doc.normalString = "Documents"
				clickedItem.addChild(item_doc)
				
				
				for i, shape_path in enumerate(data_path):
					try:
						shape_path = shape_path.split('\\')
						children = [item_doc]
						for j in range(1,len(shape_path)):
							if children[j-1].child(0)!= None and children[j-1].child(0).text(0)==shape_path[j]:
								#if the last item already has a child node and the text of this child is equal to the current element add it to list
								children.append(children[j-1].child(0))
							else:
								#if not: create a new item and add it as child to the last node
								item_shp = TreeWidgetItem([shape_path[j]])
								item_shp.setIcon(0, self.shpicon)
								item_shp.normalString = ("/").join(database.filepath.split("/")[:-1]+shape_path[1:])
								item_shp.itemType = DOCUMENTITEM
								children.append(item_shp)
								children[j-1].addChild(children[j])
					except Exception,e:
						p = ("/").join(database.filepath.split("/")[:-1]+shape_path[1:])
						self.lgr.error('path='+p+', name='+data_name[i] + ', error=' +str(e[1]))

		elif clickedItem and clickedItem.itemType == PROJECTITEM and clickedItem.childCount() == 0:
			#add all objects of selected project to tree
			try:
				#get database with the name of the TreeWidgetItem
				database=self.dbs[[db.name for db in self.dbs].index(clickedItem.parent().text(0))]
			except:
				return
			if self.load_db(database, 1, clickedItem.extraInformation):
				#if loading database returns without errors 
				clickedItem.setExpanded(False)
				return
			self.buildProjects(database, clickedItem)
		elif clickedItem and clickedItem.itemType == QUERYITEM and clickedItem.childCount() == 0:
			self.runQuery()
		else:
			return
			
		if clickedColumn==None:
			clickedItem.setExpanded(True)
		
	def buildProjects(self, database, item_prj):
		project = item_prj.extraInformation
		item_obj = TreeWidgetItem([self.dictionary.getWord(self.lang,"Objects")])
		item_obj.setIcon(0, self.objicon)
		item_obj.extraInformation = "Objects"
		item_obj.normalString = "Objects"
		item_obj.itemType = 999
		item_prj.addChild(item_obj)

		item_all = TreeWidgetItem([self.dictionary.getWord(self.lang,"All Objects")])
		item_all.setIcon(0, self.objicon_type)
		item_all.extraInformation = ObjectType("All Objects", project)
		item_all.itemType = OBJECTTYPEITEM
		item_all.normalString = "All Objects"

		thisObjectType = project.objects[0].locname
		objectType = ObjectType(project.objects[0].locname, project)
		objectType.objects.append(project.objects[0])
		
		item_loc = TreeWidgetItem([project.objects[0].locname])
		item_loc.setIcon(0, self.objicon_type)
		item_loc.itemType = OBJECTTYPEITEM
		item_loc.normalString = project.objects[0].locname
		item_loc.extraInformation = objectType
		item_obj.addChild(item_loc)
				
		for i in range(len(project.objects)):
			item_new_obj = TreeWidgetItem([project.objects[i].name])
			item_new_obj.setIcon(0, self.objicon_single)
			item_new_obj.normalString = project.objects[i].name
			item_new_obj.extraInformation = project.objects[i]
			item_new_obj.itemType = OBJECTITEM
			
			item_all_obj = TreeWidgetItem([project.objects[i].name])
			item_all_obj.setIcon(0, self.objicon_single)
			item_all_obj.normalString = project.objects[i].name
			item_all_obj.extraInformation = project.objects[i]
			item_all.extraInformation.objects.append(project.objects[i])
			item_all_obj.itemType = OBJECTITEM
			item_all.addChild(item_all_obj)

			if (project.objects[i].locname==thisObjectType):
				item_loc.addChild(item_new_obj)
				item_loc.setToolTip(0, str(item_loc.childCount()) + " " + self.dictionary.getWord(self.lang,"Objects"))
				objectType.objects.append(project.objects[i])
				
			else:
				thisObjectType = project.objects[i].locname
				objectType = ObjectType(project.objects[i].locname, project)
				objectType.objects.append(project.objects[i])
				
				item_loc = TreeWidgetItem([project.objects[i].locname])
				item_loc.setIcon(0, self.objicon_type)
				item_loc.itemType = OBJECTTYPEITEM
				item_loc.normalString = project.objects[i].locname
				item_loc.extraInformation = objectType
				
				item_obj.addChild(item_loc)
				item_loc.addChild(item_new_obj)
				
				item_loc.setToolTip(0, str(item_loc.childCount()) + " " + self.dictionary.getWord(self.lang,"Objects"))
			
		item_prj.sortChildren(0,Qt.AscendingOrder)
		item_obj.sortChildren(0,Qt.AscendingOrder)
		item_obj.insertChild(0,item_all)
		
		for i in range(item_obj.childCount()):
			item_obj.child(i).sortChildren(0,Qt.AscendingOrder)
		
		try:
			query = """SELECT GEODIN_SYS_PRJDEFS.OBJ_NAME
						FROM GEODIN_SYS_PRJDEFS
						WHERE GEODIN_SYS_PRJDEFS.PRJ_ID = '{0}' AND GEODIN_SYS_PRJDEFS.OBJ_DESC = 'LOCQUERY' """.format(item_prj.extraInformation.id)
			result = self.connectToDatabase(database, query)
			
			for row in result:
				queryObject = Query(row[0], project)
				project.queries.append(queryObject)
				
				queryItem = TreeWidgetItem([row[0]])			
				queryItem.setIcon(0, self.queryIcon)
				queryItem.extraInformation = queryObject
				queryItem.itemType = DBQUERYITEM
				queryItem.normalString = row[0]
				item_obj.addChild(queryItem)
		except:
			pass
		
		try:
			query = """SELECT * 
						FROM GEODIN_QGIS_QUERY 
						WHERE GEODIN_QGIS_QUERY.PRJ_ID = '{0}'
						ORDER BY GEODIN_QGIS_QUERY.QUERY_NAME;""".format(item_prj.extraInformation.id)
			result = self.connectToDatabase(database, query)
			
			for row in result:
				queryObject = Query(row[2], project)
				queryObject.sql = row[3]
				project.queries.append(queryObject)
				
				queryItem = TreeWidgetItem([row[2]])			
				queryItem.setIcon(0, self.ownQueryIcon)
				queryItem.extraInformation = queryObject
				queryItem.itemType = QUERYITEM
				queryItem.normalString = row[2]
				item_obj.addChild(queryItem)
		except:
			pass
	def deleteTree(self):
		#remove database connection from tree
		selectedItem = self.treeWidget.itemFromIndex(self.treeWidget.selectedIndexes()[0])
		selectedItem.setExpanded(False)
		selectedItem.takeChildren()
		selectedItem.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
		
		if selectedItem.itemType == DATABASEITEM:
			selectedItem.setIcon(0, self.dbicon)
			selectedItem.extraInformation.deleteData()
		elif selectedItem.itemType == PROJECTITEM:
			selectedItem.setIcon(0, self.prjicon)
			selectedItem.extraInformation.deleteData()
			
	def treeMenu(self, position):
		#right click menu
		selectedItem = self.treeWidget.itemFromIndex(self.treeWidget.selectedIndexes()[0])

		menu = QMenu()
		if selectedItem.itemType == DATABASEITEM:
			openDB = menu.addAction(self.dbicon_open, self.dictionary.getWord(self.lang,"Open database"))
			closeDB = menu.addAction(self.dbicon, self.dictionary.getWord(self.lang,"Close database"))
			delDB = menu.addAction(self.dbicon_del, self.dictionary.getWord(self.lang,"Delete database connection"))
			recDB = menu.addAction(self.new_obj, self.dictionary.getWord(self.lang,"Edit database connection"))
			QObject.connect(openDB, SIGNAL("triggered()"), self.buildTree)
			QObject.connect(closeDB, SIGNAL("triggered()"), self.deleteTree)
			QObject.connect(delDB, SIGNAL("triggered()"), self.deleteDB)
			QObject.connect(recDB, SIGNAL("triggered()"), self.reconnectDB)

		elif selectedItem.itemType == DOCUMENTITEM:
			if selectedItem.childCount():
				newLayer = menu.addAction(self.new_obj, self.dictionary.getWord(self.lang,"Add all layers to QGIS"))
				QObject.connect(newLayer, SIGNAL("triggered()"), self.addLayer)
			else:
				newLayer = menu.addAction(self.new_obj, self.dictionary.getWord(self.lang,"Add layer to QGIS"))
				QObject.connect(newLayer, SIGNAL("triggered()"), self.addLayer)

		elif selectedItem.itemType == OBJECTTYPEITEM:
			newObject = menu.addAction(self.new_obj, self.dictionary.getWord(self.lang,"New object"))
			createShape = menu.addAction(self.new_obj, self.dictionary.getWord(self.lang,"Add Points to QGIS"))
			
			QObject.connect(newObject, SIGNAL("triggered()"), self.createObj)
			QObject.connect(createShape, SIGNAL("triggered()"), self.createShape)

		elif selectedItem.itemType == PROJECTITEM:
		
			openProject = menu.addAction(self.prjicon_open, self.dictionary.getWord(self.lang,"Open project"))
			closeProject = menu.addAction(self.prjicon, self.dictionary.getWord(self.lang,"Close project"))
		
			QObject.connect(openProject, SIGNAL("triggered()"), self.buildTree)
			QObject.connect(closeProject, SIGNAL("triggered()"), self.deleteTree)
			
			if selectedItem.childCount() > 0:
				createQuery = menu.addAction(self.ownQueryIcon, self.dictionary.getWord(self.lang,"New query"))
				QObject.connect(createQuery, SIGNAL("triggered()"), self.createQuery)
		
		elif selectedItem.itemType == QUERYITEM:
			editQuery = menu.addAction(self.ownQueryIcon, self.dictionary.getWord(self.lang,"Edit query"))
			runQuery = menu.addAction(self.ownQueryIcon, self.dictionary.getWord(self.lang,"Run query"))
			deleteQuery = menu.addAction(self.ownQueryIcon, self.dictionary.getWord(self.lang,"Delete query"))
			createShape = menu.addAction(self.new_obj, self.dictionary.getWord(self.lang,"Add Points to QGIS"))

			QObject.connect(editQuery, SIGNAL("triggered()"), self.editQuery)
			QObject.connect(runQuery, SIGNAL("triggered()"), self.runQuery)
			QObject.connect(deleteQuery, SIGNAL("triggered()"), self.deleteQuery)
			QObject.connect(createShape, SIGNAL("triggered()"), self.createShape)
			
		elif selectedItem.itemType == DBQUERYITEM:
			runQuery = menu.addAction(self.queryIcon, self.dictionary.getWord(self.lang,"Run query"))
			createShape = menu.addAction(self.new_obj, self.dictionary.getWord(self.lang,"Add Points to QGIS"))

			QObject.connect(runQuery, SIGNAL("triggered()"), self.runDBQuery)
			QObject.connect(createShape, SIGNAL("triggered()"), self.createShape)
		
		elif selectedItem.itemType == OBJECTITEM:
			if "GeODinQGIS.extras.layout" in sys.modules.keys():
				showLayout = menu.addAction(self.new_obj, self.dictionary.getWord(self.lang,"Show layout"))
				QObject.connect(showLayout, SIGNAL("triggered()"), self.showLayout)
				
			openGeODin = menu.addAction(self.geodinicon, self.dictionary.getWord(self.lang,"open GeODin"))
			
			QObject.connect(openGeODin, SIGNAL("triggered()"), self.openGeODin)	
			
		menu.exec_(self.treeWidget.viewport().mapToGlobal(position))

	def showLayout(self):
		item = self.treeWidget.itemFromIndex(self.treeWidget.selectedIndexes()[0])
		layout = DisplayLayout(self, item.extraInformation)
	
	def runDBQuery(self):
		try:
			item = self.treeWidget.itemFromIndex(self.treeWidget.selectedIndexes()[0])
			databaseItem = item
			projectItem = None
			while databaseItem.parent() != None:
				databaseItem = databaseItem.parent()
				if databaseItem.itemType == PROJECTITEM:
					projectItem = databaseItem
			
			a = databaseItem.extraInformation.name
			b = databaseItem.extraInformation.options["uname"]
			c = databaseItem.extraInformation.options["upassword"]
			d = item.extraInformation.name
			
			if projectItem:
				e = projectItem.extraInformation.id
				
				print "ObjectID: ", e
				
				params = "[Params]\nDatabase={0}\nUserName={1}\nPassword={2}\nObjectType=1\nParentNode=ProjectQueries\nQuery={3}\nObjectID={4}\nExpand=false".format(a, b, c, d, e)
			else:
				params = "[Params]\nDatabase={0}\nUserName={1}\nPassword={2}\nObjectType=1\nParentNode=DatabaseQueries\nQuery={3}\nObjectID=\nExpand=false".format(a, b, c, d)
			
			GeODin = win32com.client.Dispatch("GeODin.GeODinApplication")
			GeODin.SelectObject(params)

			params = "[Params]\nMethod=FeatureCollection\nFilename={0}\n".format(self.tmpDirectory+"\query.json")
			GeODin.ExecuteMethodParams(60,params)

			if GeODin.ExceptionValue:
				print "Error ID:"+ str(GeODin.ExceptionValue)
				print "Error Message:"+GeODin.ExceptionMsg

			time.sleep(3)
			GeODin = None
		except Exception,e:
			self.lgr.error("runDBQueryCOMFunction= {0}".format(str(e)))

		try:
			result = Dict(self.tmpDirectory+"\query.json").getDictionary()
			item.takeChildren()
			item.extraInformation.objects = []
			
			msgBox = QMessageBox()
			msgBox.setInformativeText(u"Möchten Sie das Projekt laden?")
			msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
			msgBox.setDefaultButton(QMessageBox.Cancel)
			msgBox.setWindowTitle('Warning')

			database =  databaseItem.extraInformation
			for queryObject in result["features"]:
				project = database.getProject(queryObject["properties"]["INVID"][0:6])
				if not project.objects:
					msgBox.setText(u"Projekt '{0}' muss geöffnet werden.".format(project.name))
					if msgBox.exec_() == 1024:
						projectItem = searchItem(databaseItem, project.id)
						self.buildTree(projectItem)

				obj = project.getObject(queryObject["properties"]["INVID"])
				
				if not obj:
					break
				info = queryObject["properties"]
				del info["INVID"]
				del info["XCOORD"]
				del info["YCOORD"]
				obj.data = info

				objectItem = TreeWidgetItem([obj.name])			
				objectItem.setIcon(0, self.objicon_single)
				objectItem.itemType = OBJECTITEM
				objectItem.extraInformation = obj
				objectItem.normalString = obj.name
				item.addChild(objectItem)
				item.extraInformation.objects.append(obj)

			item.sortChildren(0,Qt.AscendingOrder)
			item.setExpanded(True)
			os.unlink(self.tmpDirectory+"\query.json")
			if os.path.isfile(self.tmpDirectory+"\query.~json"):
				os.unlink(self.tmpDirectory+"\query.~json")
		except Exception,e:
			self.lgr.error("runDBQueryLoadObjects: {0}".format(str(e)))
		
	def runQuery(self):
		item = self.treeWidget.itemFromIndex(self.treeWidget.selectedIndexes()[0])
		database = item.extraInformation.parent.parent
		sqlStatement = item.extraInformation.sql.upper().replace(',','').split(' ')

		parameters=[]
		connections = ['If']
		whereStart = False
		for i, element in enumerate(sqlStatement):
			if 'WHERE' in element:
				whereStart = True
				
			if whereStart and 'AND' in element:
				connections.append('and')
			elif whereStart and 'OR' in element:
				connections.append('or')
				
			if ':?' in element:
				if '>=' in element:
					parameters.append([sqlStatement[i-1].replace('(',''), '>='])
				elif '>=' in sqlStatement[i-1]:
					parameters.append([sqlStatement[i-2].replace('(',''), '>='])
					
				elif '<=' in element:
					parameters.append([sqlStatement[i-1].replace('(',''), '<='])
				elif '<=' in sqlStatement[i-1]:
					parameters.append([sqlStatement[i-2].replace('(',''), '<='])

				elif '<>' in element:
					parameters.append([sqlStatement[i-1].replace('(',''), '<>'])
				elif '<>' in sqlStatement[i-1]:
					parameters.append([sqlStatement[i-2].replace('(',''), '<>'])

				elif '=' in element:
					parameters.append([sqlStatement[i-1].replace('(',''), '='])
				elif '=' in sqlStatement[i-1]:
					parameters.append([sqlStatement[i-2].replace('(',''), '='])
					
				elif '<' in element:
					parameters.append([sqlStatement[i-1].replace('(',''), '<'])
				elif '<' in sqlStatement[i-1]:
					parameters.append([sqlStatement[i-2].replace('(',''), '<'])
					
				elif '>' in element:
					parameters.append([sqlStatement[i-1].replace('(',''), '>'])
				elif '>' in sqlStatement[i-1]:
					parameters.append([sqlStatement[i-2].replace('(',''), '>'])
				
				elif 'like' in element.lower():
					parameters.append([sqlStatement[i-1].replace('(',''), 'like'])
				elif 'like' in sqlStatement[i-1].lower():
					parameters.append([sqlStatement[i-2].replace('(',''), 'like'])

		try:
			for parameter in parameters:
				if 'locreg' in parameter[0].lower():
					parameter[0] = self.dictionary.getWord(self.lang,locreg(parameter[0].split('.')[1]))
				elif 'loc' in parameter[0].lower():
					longQuery = "SELECT FIELD_LONG FROM GEODIN_SYS_LOCSTRS WHERE TAB_DESC = '"+parameter[0].split('.')[0].split('_')[2]+"' AND FIELD_NAME = '"+parameter[0].split('.')[1]+"';"
					parameter[0] = self.connectToDatabase(database, longQuery)[0][0]
				elif 'mes' in parameter[0].lower():
					longQuery = "SELECT FIELD_LONG FROM GEODIN_SYS_MESSTRS WHERE TAB_DESC = '"+parameter[0].split('.')[0].split('_')[2]+"' AND FIELD_NAME = '"+parameter[0].split('.')[1]+"';"
					parameter[0] = self.connectToDatabase(database, longQuery)[0][0]
		except Exception, e:
			print str(e)
			return


		if parameters:
			parameterWindow = ParameterizedQueryDialog(item.normalString, parameters, connections)
			if parameterWindow.accepted and parameterWindow.result:
				i=0
				for j, element in enumerate(sqlStatement):
					if ':?' in element:
						if len(sqlStatement[j-1])<=4:
							sqlStatement[j-1] = parameterWindow.result[i][1]
							sqlStatement[j] = sqlStatement[j].replace(":?", parameterWindow.result[i][2])
						else:
							sqlStatement[j] = parameterWindow.result[i][1] + sqlStatement[j][sqlStatement[j].index(':?'):] 
							sqlStatement[j] = sqlStatement[j].replace(":?", parameterWindow.result[i][2])
						i+=1
		
		sqlStatement = [x.upper() for x in sqlStatement]
		if 'DISTINCT' in sqlStatement:
			select = sqlStatement[2:sqlStatement.index('FROM')]
		else:
			select = sqlStatement[1:sqlStatement.index('FROM')]

		if "GEODIN_LOC_LOCREG.INVID" in select:
			select.remove("GEODIN_LOC_LOCREG.INVID")
		if "GEODIN_LOC_LOCREG.LONGNAME" in select:
			select.remove("GEODIN_LOC_LOCREG.LONGNAME")

		if select:
			sqlStatement = ' '.join([sqlStatement[0]] + ["GEODIN_LOC_LOCREG.INVID, GEODIN_LOC_LOCREG.LONGNAME,"] + [", ".join(select)] + sqlStatement[sqlStatement.index('FROM'):])
		else:
			sqlStatement = ' '.join([sqlStatement[0]] + ["GEODIN_LOC_LOCREG.INVID, GEODIN_LOC_LOCREG.LONGNAME"] + sqlStatement[sqlStatement.index('FROM'):])

		if "$PRJID" in sqlStatement:
			sqlStatement = sqlStatement.replace("$PRJID", item.extraInformation.parent.id)
		try:
			result = self.connectToDatabase(database, sqlStatement)
		except Exception, e:
			print sqlStatement
			print str(e[1])
			return

		item.takeChildren()
		for row in result:
			objectItem = TreeWidgetItem([row[1]])			
			objectItem.setIcon(0, self.objicon_single)
			objectItem.itemType = OBJECTITEM
			objectItem.extraInformation = item.extraInformation.parent.getObject(row[0])
			objectItem.normalString = row[1]
			if not objectItem.extraInformation:
				continue
			objectItem.extraInformation.data={}
			for column in range(2,len(row)):
				#add columns to object
				try:
					objectItem.extraInformation.data[select[column-2].split('.')[1]] = row[column]
				except:
					objectItem.extraInformation.data["F"+str(column-2)] = row[column]

			item.addChild(objectItem)
			item.extraInformation.objects.append(objectItem.extraInformation)
		
		if item.childCount() > 0 and not item.isExpanded():
			item.setExpanded(True)
		
	def createQuery(self):
		# get instance from mouse click position
		item = self.treeWidget.itemFromIndex(self.treeWidget.selectedIndexes()[0])
		
		newQuery = QueryDialog()
		if newQuery.accepted:
			#Create a new table in the GeODin database
			query = """CREATE TABLE GEODIN_QGIS_QUERY (id AUTOINCREMENT PRIMARY KEY, PRJ_ID varchar(6), QUERY_NAME varchar(255) UNIQUE , QUERY longtext);"""
			database=self.dbs[[db.name for db in self.dbs].index(item.parent().normalString)]
			print "Database for Query: ", database
			self.connectToDatabase(database, query, True)
			query = """INSERT INTO GEODIN_QGIS_QUERY(PRJ_ID, QUERY_NAME, QUERY) values (?, ?, ?);"""
			#try:
			self.connectToDatabase(database, query, True, [item.extraInformation.id, newQuery.queryName, newQuery.sqlCommand])
			
			queryObject = Query(newQuery.queryName, item.extraInformation)
			queryObject.sql = newQuery.sqlCommand
			item.extraInformation.queries.append(queryObject)
			
			queryItem = TreeWidgetItem([newQuery.queryName])			
			queryItem.setIcon(0, self.ownQueryIcon)
			queryItem.extraInformation = queryObject
			queryItem.itemType = QUERYITEM
			queryItem.normalString = newQuery.queryName
			item.child(0).addChild(queryItem)
			
			#except:
			#	QMessageBox.warning(self, 'Error', u"Die von Ihnen gewünschten Änderungen an der Tabelle konnten nicht vorgenommen werden, da der Index, der Primärschlüssel oder die Beziehung mehrfach vorkommende Werte enthalten würde. Ändern Sie die Daten in den Feldern, die gleiche Daten enthalten, entfernen Sie den Index, oder definieren Sie den Index neu, damit doppelte Einträge möglich sind, und versuchen Sie es erneut.")
			
	def editQuery(self):
		item = self.treeWidget.itemFromIndex(self.treeWidget.selectedIndexes()[0])
		database=self.dbs[[db.name for db in self.dbs].index(item.extraInformation.parent.parent.name)]
		query = """SELECT id FROM GEODIN_QGIS_QUERY WHERE QUERY_NAME='{0}';""".format(item.normalString)
		id = self.connectToDatabase(database, query)
		if not id:
			return
		id = id[0][0]
		
		queryObject = QueryDialog(item.extraInformation.name, item.extraInformation.sql)
		if queryObject.accepted:
			query = """UPDATE GEODIN_QGIS_QUERY SET QUERY_NAME=?, QUERY=? WHERE id=?;"""
			parameter = [queryObject.queryName, queryObject.sqlCommand, id]
			try:
				self.connectToDatabase(database, query, True, parameter)
				item.setText(0, queryObject.queryName)
				item.extraInformation.sql = queryObject.sqlCommand
				item.extraInformation.name = queryObject.queryName
				item.normalString = queryObject.queryName
				item.takeChildren()
			except:
				QMessageBox.warning(self, 'Error', u"Die von Ihnen gewünschten Änderungen an der Tabelle konnten nicht vorgenommen werden, da der Index, der Primärschlüssel oder die Beziehung mehrfach vorkommende Werte enthalten würde. Ändern Sie die Daten in den Feldern, die gleiche Daten enthalten, entfernen Sie den Index, oder definieren Sie den Index neu, damit doppelte Einträge möglich sind, und versuchen Sie es erneut.")
		
	def deleteQuery(self):
		item = self.treeWidget.itemFromIndex(self.treeWidget.selectedIndexes()[0])

		database=self.dbs[[db.name for db in self.dbs].index(item.extraInformation.parent.parent.name)]
		query = """SELECT id FROM GEODIN_QGIS_QUERY WHERE QUERY_NAME='{0}';""".format(item.normalString)
		id = self.connectToDatabase(database, query)
		if not id:
			return
		id = id[0][0]
		
		query = """DELETE FROM GEODIN_QGIS_QUERY WHERE id=?;"""
		try:
			self.connectToDatabase(database, query, True, [id])
			item.takeChildren()
			item.parent().removeChild(item)
			del item
		except:
			QMessageBox.warning(self, 'Error', u"Die von Ihnen gewünschten Änderungen an der Tabelle konnten nicht vorgenommen werden, da der Index, der Primärschlüssel oder die Beziehung mehrfach vorkommende Werte enthalten würde. Ändern Sie die Daten in den Feldern, die gleiche Daten enthalten, entfernen Sie den Index, oder definieren Sie den Index neu, damit doppelte Einträge möglich sind, und versuchen Sie es erneut.")
	
	def createShape(self):
		item = self.treeWidget.itemFromIndex(self.treeWidget.selectedIndexes()[0])
		try:
			QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
			ShapeFromPoint(self, item.extraInformation)
			QApplication.restoreOverrideCursor()
		except Exception,e:
			print str(e)
			QApplication.restoreOverrideCursor()
	
	def expanded(self, item):
		#called if TreeWidgetItem is expanded
		if (item.itemType == DATABASEITEM or item.itemType== PROJECTITEM) and item.childCount() == 0 and not self.error:
			self.buildTree(item)
		if item.itemType == DATABASEITEM:
			item.setIcon(0, self.dbicon_open)
		if item.itemType == PROJECTITEM:
			item.setIcon(0, self.prjicon_open)
		self.error = 0
					
	def collapsed(self, item):
		#called if TreeWidgetItem is collapsed
		if item.itemType == DATABASEITEM:
			item.setIcon(0, self.dbicon)
		if item.itemType == PROJECTITEM:
			item.setIcon(0, self.prjicon)


	def changeLang(self, language):

		self.lang = language

		self.singleImportButton.setText(self.dictionary.getWord(self.lang,"Import Databases"))
		self.multipleImportButton.setText(self.dictionary.getWord(self.lang,"Load Database"))
		self.treeWidget.setHeaderLabels([self.dictionary.getWord(self.lang,"GeODin Databases")])
		
		self.singleImportButton.setToolTip(self.dictionary.getWord(self.lang,"Import Databases"))
		self.singleImportButton.setFont(QFont('OldEnglish', 10))
		
		self.multipleImportButton.setToolTip(self.dictionary.getWord(self.lang,"Load Database"))
		self.multipleImportButton.setFont(QFont('OldEnglish', 10))

		if self.crd:
			self.crd.btn_del.setText(self.dictionary.getWord(self.lang,"Delete Entries"))
			self.crd.btn_desel.setText(self.dictionary.getWord(self.lang,"Deselect Entries"))
			self.crd.btn_close.setText(self.dictionary.getWord(self.lang,"Close"))
			
			self.crd.setWindowTitle(self.dictionary.getWord(self.lang,"New object"))
			self.crd.lbl_obtyp.setText(self.dictionary.getWord(self.lang,"Object type"))

			self.crd.coord_tab.horizontalHeaderItem(0).setText(self.dictionary.getWord(self.lang,"Easting"))
			self.crd.coord_tab.horizontalHeaderItem(1).setText(self.dictionary.getWord(self.lang,"Northing"))
			
			self.crd.lbl_east.setText(self.dictionary.getWord(self.lang,"Easting"))
			self.crd.lbl_north.setText(self.dictionary.getWord(self.lang,"Northing"))
			self.crd.le_east.setPlaceholderText(self.dictionary.getWord(self.lang,"Empty"))
			self.crd.le_north.setPlaceholderText(self.dictionary.getWord(self.lang,"Empty"))
			self.crd.lang = language

		self.config.set('Options', 'lang', language)
		self.saveConfig()
		
		for i in range(self.treeWidget.topLevelItemCount()):
			self.renameChildren(self.treeWidget.topLevelItem(i))
			
		if language == 'en':
			self.activeIcon = QIcon(":\plugins\GeODinQGIS\icons\i_371F.png")
		elif language == 'de':
			self.activeIcon = QIcon(":\plugins\GeODinQGIS\icons\i_370F.png")
		elif language == 'fr':
			self.activeIcon = QIcon(":\plugins\GeODinQGIS\icons\i_372F.png")
		elif language == 'ru':
			self.activeIcon = QIcon(":\plugins\GeODinQGIS\icons\i_373F.png")
		
	def renameChildren(self, item):
		for i in range(0, item.childCount()):
			try:
				item.child(i).setText(0,self.dictionary.getWord(self.lang,item.child(i).extraInformation))
			except:
				pass
			if item.child(i).childCount()>0:
				self.renameChildren(item.child(i))
		
	def deleteDB(self):
		item = self.treeWidget.itemFromIndex(self.treeWidget.selectedIndexes()[0])
		delDB = item.extraInformation.name
		index = self.treeWidget.indexOfTopLevelItem(item)
		self.treeWidget.takeTopLevelItem(index)

		self.dbs.remove(item.extraInformation)

		if delDB.lower() in self.config.options('Databases'):
			self.config.remove_option('Databases', delDB.lower())
			self.saveConfig()
		del item

	def reconnectDB(self):
		item = self.treeWidget.itemFromIndex(self.treeWidget.selectedIndexes()[0])
		database = item.extraInformation
		try:
			result = self.loadSingleDatabase(database)
		except:
			return
			
		if result:
			self.treeWidget.removeItemWidget(item, 0)
	
	def createObj(self):
		if self.deny == 1:
			print "Permission denied"
		
		else:
			item = self.treeWidget.itemFromIndex(self.treeWidget.selectedIndexes()[0])						# coded name of current item (at mouse click position)
			
			# open Method "New Object" in a right docked window
			self.crd = NewObject(self.iface, item.extraInformation.name, item.parent().parent().extraInformation, self.dictionary, self.lang)

			# buttons
			self.crd.btn_del.setText(self.dictionary.getWord(self.lang,"Delete Entries"))
			self.crd.btn_desel.setText(self.dictionary.getWord(self.lang,"Deselect Entries"))
			self.crd.btn_close.setText(self.dictionary.getWord(self.lang,"Close"))
			
			# labels and tables
			self.crd.setWindowTitle(self.dictionary.getWord(self.lang,"New object"))
			self.crd.lbl_obtyp.setText(self.dictionary.getWord(self.lang,"Object type"))
			
			self.crd.coord_tab.horizontalHeaderItem(0).setText(self.dictionary.getWord(self.lang,"Easting"))
			self.crd.coord_tab.horizontalHeaderItem(1).setText(self.dictionary.getWord(self.lang,"Northing"))

			self.crd.lbl_east.setText(self.dictionary.getWord(self.lang,"Easting"))
			self.crd.lbl_north.setText(self.dictionary.getWord(self.lang,"Northing"))
			self.crd.le_east.setPlaceholderText(self.dictionary.getWord(self.lang,"Empty"))
			self.crd.le_north.setPlaceholderText(self.dictionary.getWord(self.lang,"Empty"))
			
			self.iface.addDockWidget(Qt.RightDockWidgetArea, self.crd)
			
	def getDBLayer(self, database):
		name = []
		file = []
		try:
			query = """SELECT GEODIN_ADC_ADCDATA.ADC_NAME, GEODIN_ADC_ADCDATA.ADC_FILE
						FROM GEODIN_ADC_ADCDATA
						WHERE GEODIN_ADC_ADCDATA.ADC_TYPE = 'SHP' """
						
			result = self.connectToDatabase(database, query)

			for row in result:
				
				name.append(row[0])
				file.append(row[1])
			
		except SystemError as e:
			self.lgr.error('path={0}, error={1}'.format(database.filepath, str(e[1])))
			pass	
		except Exception,e:
			self.lgr.error('path={0}, error={1}'.format(database.filepath, str(e[1])))
			pass
		return name, file

	def getDBQueries(self, database):
		name = []
		try:
			query = """SELECT GEODIN_SYS_PRJDEFS.OBJ_NAME
						FROM GEODIN_SYS_PRJDEFS
						WHERE GEODIN_SYS_PRJDEFS.PRJ_ID = 'DBDEF' AND GEODIN_SYS_PRJDEFS.OBJ_DESC = 'LOCQUERY' """
						
			result = self.connectToDatabase(database, query)
			
			for row in result:
				name.append(row[0])
		except SystemError as e:
			self.lgr.error('path={0}, error={1}'.format(database.filepath, e))
			pass	
		except Exception,e:
			self.lgr.error('path={0}, error={1}'.format(database.filepath, str(e)))
			pass
		return name
		
	def connectToDatabase(self, database, query, create = False, param=None):
		result = []
		print "Database for Connection: ", database
		if not len(database.options.keys()) or database.options["connection"] == "ODBC":
			if 'pyodbc' in sys.modules.keys():
				connection = pyodbc.connect("Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ="+database.filepath+";")
			else:
				connection = pypyodbc.win_connect_mdb(database.filepath)
			cursor = connection.cursor()

			if create:
				# Does table 'GEODIN_QGIS_QUERY' exist?
				if cursor.tables(table='GEODIN_QGIS_QUERY').fetchone():
					if "CREATE" in query:
						return
					cursor.execute(query, param)
				else:
					query = """CREATE TABLE GEODIN_QGIS_QUERY (id AUTOINCREMENT PRIMARY KEY, PRJ_ID varchar(6), QUERY_NAME varchar(255) UNIQUE , QUERY longtext);"""
					cursor.execute(query)
				connection.commit()
			else:
				cursor.execute(query)
				result = cursor.fetchall()
			cursor.close()
			connection.close()
		elif database.options["connection"] == "DSNConnection":
			connection = pyodbc.connect("DSN="+database.options["DSN"])
			cursor = connection.cursor()

			if create:
				# Does table 'GEODIN_QGIS_QUERY' exist?
				if cursor.tables(table='GEODIN_QGIS_QUERY').fetchone():
					if "CREATE" in query:
						return
					cursor.execute(query, param)
				else:
					cursor.execute(query)
				connection.commit()
			else:
				cursor.execute(query)
				result = cursor.fetchall()
			cursor.close()
			connection.close()
			
		elif database.options["connection"] == "MSSQL":
			#connect to DSN connection
			connection = pyodbc.connect("DRIVER={SQL Server};SERVER="+database.options["ip"]+";DATABASE="+database.options["database"]+";UID="+database.options["uname"]+";PWD="+database.options["upassword"])
			cursor = connection.cursor()

			if create:
				# Does table 'GEODIN_QGIS_QUERY' exist?
				if cursor.tables(table='GEODIN_QGIS_QUERY').fetchone():
					if "CREATE" in query:
						return
					cursor.execute(query, param)
				else:
					query = """CREATE TABLE GEODIN_QGIS_QUERY (id int IDENTITY(1,1) PRIMARY KEY, PRJ_ID varchar(6), QUERY_NAME varchar(255) UNIQUE , QUERY varchar(max));"""
					cursor.execute(query)
				connection.commit()
			else:
				cursor.execute(query)
				result = cursor.fetchall()
			cursor.close()
			connection.close()
		elif database.options["connection"] == "MySQL":
			connection = _mysql.connect(database.options["ip"], database.options["uname"], database.options["upassword"], database.options["database"])
			connection.query(query)
			r = connection.use_result()
			row = r.fetch_row()
			while row:
				result.append(row)
				row = r.fetch_row()
			connection.close()
		elif database.options["connection"] == "PostgreSQL":
			connection = psycopg2.connect("dbname={0} user={1} host={2} password={3}".format(database.options["database"], database.options["uname"], database.options["ip"], database.options["upassword"]))
			cursor = connection.cursor()
			if create:
				# Does table 'GEODIN_QGIS_QUERY' exist?
				if "CREATE" in query:
					query = """CREATE TABLE IF NOT EXISTS GEODIN_QGIS_QUERY (id serial PRIMARY KEY, PRJ_ID varchar(6), QUERY_NAME varchar(255) UNIQUE , QUERY text);"""
					cursor.execute(query)
				else:
					i=0
					while '?' in query:
						query=query[:query.index('?')]+"'{"+str(i)+"}'"+query[query.index('?')+1:]
						i+=1
					query = query.format(param[0], param[1], param[2])
					cursor.execute(query)
				
				connection.commit()
			else:
				cursor.execute(query)
				result = cursor.fetchall()
			cursor.close()
			connection.close()
		return result
		
	def addLayer(self, item=None):
		item = self.treeWidget.itemFromIndex(self.treeWidget.selectedIndexes()[0])
		addItems = []
		if item.childCount() == 0:
			addItems.append(item)
		else:
			for i in range(0, item.childCount()):
				addItems.append(item.child(i))
	
		for item in addItems:
			layer = QgsVectorLayer(item.normalString, item.normalString.split('/')[-1].split('.')[0], 'ogr')
			if not layer.isValid():
				print self.dictionary.getWord(self.lang,"Layer failed to load!")
				continue
			QgsMapLayerRegistry.instance().addMapLayer(layer)

	def closeEvent(self, event):
		#close event handler of the main window
		if self.crd:
			#close NewObject window if open
			self.crd.close()
		event.accept()
		
	#A key has been pressed!
	def keyPressEvent(self, event):
		pass
		#Did the user press the Enter key?
		#if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter or event.key() == Qt.Key_Tab: #Qt.Key_Enter is a value that equates to what the operating system passes to python from the keyboard when the escape key is pressed.
			#Yes: Delete database
		#	self.treeWidget.takeTopLevelItem(0)
		#No:  Do nothing.
		
	def activateItem(self):
	
		if self.inProcess:
			return
		self.inProcess = True
		try:
			selectedTreeItems = self.treeWidget.selectedItems()
			allLayers = self.iface.mapCanvas().layers()
			for layer in allLayers:
				selectFeatures = []
				for feature in layer.getFeatures():
					idx = layer.fieldNameIndex('INVID')
					for item in selectedTreeItems:
						if item.itemType == OBJECTITEM and item.extraInformation.invid == feature.attributes()[idx]:
							selectFeatures.append(feature.id())
				layer.setSelectedFeatures(selectFeatures)
		except Exception,e:
			print e
		self.inProcess = False
			
	def layerActivationChanged(self, layer):
		try:
			self.activeLayer = layer
			self.activeLayer.selectionChanged.connect(self.selectfromCanvas)
		except:
			return
	
	def selectfromCanvas(self, selFeatures):

		if self.inProcess:
			return
		self.inProcess = True
		selectedTreeItems = self.treeWidget.selectedItems()
		selectTreeItems = []
		
		database_paths = [db.filepath for db in self.dbs]
		###selection are the features of the current layer
		#selection = self.activeLayer.selectedFeatures()
		
		###selection are the features of all layers
		selection = []
		for layer in self.iface.mapCanvas().layers():
			selection+= layer.selectedFeatures()
		
		for feature in selection:
			try:
				if feature["database"] in database_paths:
					try:
						db = self.dbs[database_paths.index(feature["database"])]
						#search and expand for top level item with database alias as text
						databaseItem = self.treeWidget.findItems(db.name, Qt.MatchExactly)[0]
						if databaseItem.childCount() == 0:
							self.buildTree(databaseItem)
						databaseItem.setExpanded(True)
					
						#search and expand project item 
						projectItem = searchItem(databaseItem, feature["prjid"])
						if projectItem.childCount() == 0:
							self.buildTree(projectItem)
						projectItem.setExpanded(True)
					
						#search and expand objects item
						objectsItem = searchItem(projectItem, "Objects")
						objectsItem.setExpanded(True)

						#search and expand object type item
						objectTypeItem = searchItem(objectsItem, feature["objecttype"])
						objectTypeItem.setExpanded(True)

						#search and select item
						selectItem = searchItem(objectTypeItem, feature["invid"])
						selectTreeItems.append(selectItem)
					except Exception,e:
						print str(e)
						continue
			
			except KeyError:
				continue
		
		try:
			for item in selectedTreeItems:
				if not item in selectTreeItems:
					item.setSelected(False)
			for item in selectTreeItems:
				if not item.isSelected():
					item.setSelected(True)
		except:
			pass
			
		self.inProcess = False
		
	def openGeODin(self):
		item = self.treeWidget.itemFromIndex(self.treeWidget.selectedIndexes()[0])
		try:
			QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
			self.GeODin = GeODinFromObject(self, item.extraInformation)
			QApplication.restoreOverrideCursor()
		except Exception,e:
			print str(e)
			QApplication.restoreOverrideCursor()