# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from _winreg import *
import json, os, codecs


#different types of TreeWidgetItems
DATABASEITEM = 0
PROJECTITEM = 1
OBJECTTYPEITEM = 2
OBJECTITEM = 3
DOCUMENTITEM = 4
CHILDITEM = 5
QUERYITEM = 6
DBQUERYITEM = 7

#columns of geodin_loc_locreg table and description
def locreg(column):
	columns = ["PRJ_ID", "LOCTYPE", "INVID", "OPT_PARAM", "XCOORD", "YCOORD", "ZCOORDB", "ZCOORDE", "SHORTNAME", "LONGNAME", "PHYSFILE", "LOCKINFO"]
	description = ["GeODin Project ID", "Object type", "Monitoring point ID", "Optional parameter", "X-coordinate", "Y-coordinate", "Ground Level", "End depth", "Short name", "Object name", "File", "Locked data record"]
	if column in columns:
		return description[columns.index(column)]
	else:
		return ""

def unique(seq):
	# not order preserving
	set = {}
	map(set.__setitem__, seq, [])
	return set.keys()

def firstLastIndices(seq, item):
	ind = [i for i, x in enumerate(seq) if x == item]
	if ind:
		return [min(ind), max(ind)]
	else:
		return []
	
def unique_order(seq): 
	# order preserving
	checked = []
	for e in seq:
		if e not in checked:
			checked.append(e)
	return checked
	
def searchItem(parentItem, item_name):
	for i in range(parentItem.childCount()):
		if parentItem.child(i).extraInformation == item_name:
			return parentItem.child(i)
	return None

class Dict:

	def __init__(self, path):
		self.__path = path
		self.__dict = self.load()

	def getLang(self, lang):
		return self.__dict[lang][0]

	def load(self):
		with open(self.__path) as dictfile:
			pyjson = json.load(dictfile)
		return pyjson

	def getWord(self, lang, word):
		language = self.__dict[lang][0]
		return language[word]
		
	def getLanguages(self):
		return self.__dict.keys()
		
	def getDictionary(self):
		return self.__dict

class DatabaseObjects:

	def __init__(self, name=None):
		self.name = name
		self.parent = None
		
	def __repr__(self):
		#>>> a = Database('Test','Path to test')
		#>>> print a
		#Test
		return self.name

	def __str__(self):
		#>>> a = Database('Test','Path to test')
		#>>> b=str(a)
		#>>> print b
		#Test
		return self.name

	def __eq__(self, other):
		return self.name == other

class Database(DatabaseObjects):

	def __init__(self, name=None, filepath=None):
		DatabaseObjects.__init__(self, name)
		self.filepath = filepath
		self.options = {}

		self.projects = []
		self.queries = []

	def deleteData(self):
		self.projects = []
		self.queries = []

	def setOption(self, key, value):
		#Adds an new option to dictionary
		self.options[key] = value

	def delOption(self, key):
		#Deletes an option from dictionary and returns true if it was possible,
		#flase otherwise
		try:
			del self.options[key]
			return True
		except KeyError:
			return False

	def getOption(self, key):
		#Returns the ordered option value
		try:
			return self.options[key]
		except KeyError:
			print key + ' not found in options.'

	def getProject(self, prjid):
		for project in self.projects:
			if project.id == prjid:
				return project
		return None
			
class Project(DatabaseObjects):

	def __init__(self, name=None, parent=None):
		DatabaseObjects.__init__(self, name)
		self.parent = parent
		self.id = ''
		self.user = ''
		self.date = ''
		self.alias = ''

		self.objects = []
		self.queries = []

	def getObject(self, invid):
		for object in self.objects:
			if object.invid == invid:
				return object
		return None

	def deleteData(self):
		self.objects = []
		self.queries = []
		
	def __eq__(self, other):
		return self.id == other
		
class Object(DatabaseObjects):

	def __init__(self, name=None, parent=None):
		DatabaseObjects.__init__(self, name)
		self.shortname = ""
		self.parent = parent
		self.locname = ""
		self.invid = ""
		self.coordinates = ()
		self.data = {}
		
	def __eq__(self, other):
		return self.invid == other

class Query(DatabaseObjects):

	def __init__(self, name=None, parent=None):
		DatabaseObjects.__init__(self, name)
		self.parent = parent
		self.sql = ""
		self.objects = []
		
	def delObjects(self):
		self.objects = []

class ObjectType(DatabaseObjects):

	def __init__(self, name=None, parent=None):
		DatabaseObjects.__init__(self, name)
		self.parent = parent
		self.objects = []

class TreeWidgetItem(QTreeWidgetItem):

	def __init__(self, args):
		QTreeWidgetItem.__init__(self, args)
		self.extraInformation = u''
		self.normalString = u''
	
		#default type
		self.itemType = CHILDITEM
		
class UserChooser(QDialog):

	def __init__(self, headLabel):
		QDialog.__init__(self)

		self.buttonBox = QDialogButtonBox(self)
		self.buttonBox.setGeometry(QRect(10, 120, 360, 25))
		self.buttonBox.setOrientation(Qt.Horizontal)
		self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
		self.headLabel = QLabel(self)
		self.headLabel.setGeometry(QRect(10, 30, 360, 25))
		self.headLabel.setText(headLabel)
		self.userBox = QComboBox(self)
		self.userBox.setGeometry(QRect(10, 80, 360, 25))
		
		layout = QVBoxLayout(self)
		layout.addWidget(self.headLabel)
		layout.addWidget(self.userBox)
		layout.addWidget(self.buttonBox)
		
		
		self.okPressed = False
		self.user = ''
		self.fillCombobox()
		
		QObject.connect(self.buttonBox, SIGNAL("accepted()"), self.accept)
		QObject.connect(self.buttonBox, SIGNAL("rejected()"), self.reject)		
		self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.ok)
		self.connect(self.userBox, SIGNAL("activated (const QString&)"), self.newItem)
		self.show()
		self.exec_()

	def fillCombobox(self):
		users = next(os.walk("C:\\Users"))[1]
		self.user = users[0]
		self.userBox.addItems(users)
		#for user in users:
		#	self.userBox.addItem(user)

	def ok(self):
		self.okPressed = True
		
	def newItem(self, item):
		self.user = str(item)
		
class Login(QDialog):
	def __init__(self, name, pw):
		QDialog.__init__(self)
		
		self.textName = QLineEdit(self)
		self.textName.setText(name)
		
		self.textPass = QLineEdit(self)
		self.textPass.setText(pw)
		self.textPass.setEchoMode(QLineEdit.Password)
		
		buttonLogin = QPushButton('Login', self)
		buttonLogin.clicked.connect(self.handleLogin)
		
		layout = QVBoxLayout(self)
		layout.addWidget(QLabel("Username"))
		layout.addWidget(self.textName)
		layout.addWidget(QLabel("Password"))
		layout.addWidget(self.textPass)
		layout.addWidget(buttonLogin)
		
		self.uname = ""
		self.upassword = ""
		
		self.exec_()

	def handleLogin(self):
		self.uname = self.textName.text()
		self.upassword = self.textPass.text()
		self.accept()
		
class QueryDialog(QDialog):
	def __init__(self, name="", query=""):
		QDialog.__init__(self)
		self.setWindowTitle("Query")
		self.accepted = False
		self.queryName = ""
		self.sqlCommand = ""
		
		self.nameText = QLineEdit(self)
		self.nameText.setText(name)
		
		self.queryText = QTextEdit(self)
		self.queryText.setText(query)
		
		self.buttonBox = QDialogButtonBox(self)
		self.buttonBox.setOrientation(Qt.Horizontal)
		self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.NoButton|QDialogButtonBox.Ok)
		self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.ok)
		self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.cancel)
		
		layout = QVBoxLayout(self)
		layout.addWidget(QLabel("Name der Abfrage"))
		layout.addWidget(self.nameText)
		layout.addWidget(QLabel("SQL-Befehl"))
		layout.addWidget(self.queryText)
		layout.addWidget(self.buttonBox)
		
		self.exec_()

	def ok(self):
		self.accepted = True
		self.queryName = self.nameText.text()
		self.sqlCommand = self.queryText.toPlainText()
		self.accept()
		
	def cancel(self):
		self.close()
		
class ParameterizedQueryDialog(QDialog):
	def __init__(self, name, parameters = None, connections=None):
		QDialog.__init__(self)
		
		self.result = []		
		
		self.setWindowTitle("Define query parameters")
		self.setWindowIcon(QIcon(":\plugins\GeODinQGIS\icons\transparent.png"))
		
		self.buttonBox = QDialogButtonBox(self)
		self.buttonBox.setOrientation(Qt.Horizontal)
		self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.NoButton|QDialogButtonBox.Ok)
		self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.ok)
		self.buttonBox.button(QDialogButtonBox.Cancel).clicked.connect(self.cancel)
		
		layout = QVBoxLayout(self)

		l1 = QLabel("Parameters in red are required entries.")
		l1.setStyleSheet('color: red')
		l2 = QLabel("Parameters in blue are optional (empty entry fields are not evaluated in the query).")
		l2.setStyleSheet('color: blue')

		self.w = QWidget()
		self.w.setAutoFillBackground(True)
		p = self.w.palette()
		p.setColor(self.w.backgroundRole(), QColor(255, 221, 161))
		self.w.setPalette(p)

		tableLayout = QGridLayout(self.w)
		j=0
		for i, parameter in enumerate(parameters):
			label = QLabel(parameter[0])
			le1 = QLineEdit(parameter[1])
			le1.setFixedSize(50, 25)
			le2 = QLineEdit()
			le2.setFixedSize(250, 25)
			tableLayout.addWidget(QLabel(connections[i]), i+j, 0)
			tableLayout.addWidget(label, i+j+1, 1)
			tableLayout.addWidget(le1, i+j+1, 2)
			tableLayout.addWidget(le2, i+j+1, 3)
			j+=1
			
			
		layout.addWidget(QLabel("Enter the required values of the query '"+name+"'"))
		layout.addWidget(QLabel(""))
		#layout.addWidget(l1)
		#layout.addWidget(l2)
		layout.addWidget(QLabel("This operators are available:  <  <=  =  >=  >  <>  like"))
		layout.addWidget(self.w)
		layout.addWidget(self.buttonBox)
		
		
		self.exec_()

	def ok(self):
		for i in range(1, len(self.w.children()),4):
			if not self.w.children()[i+3].text().isdigit():
				self.w.children()[i+3].setText("'"+self.w.children()[i+3].text()+"'")
			self.result.append([self.w.children()[i+1].text(), self.w.children()[i+2].text(), self.w.children()[i+3].text()])
		self.accept()
		
	def cancel(self):
		self.close()
		
class Info(QDialog):
	def __init__(self):
		QDialog.__init__(self)
		self.resize(230, 150)
		self.setWindowTitle("Info")
		
		main_grid = QGridLayout(self)
		build_grid = QGridLayout(self)
		link_grid = QGridLayout(self)
		version_grid = QGridLayout(self)
		
		# Title
		lbl_title = QLabel(self)
		font = QFont()
		font.setPointSize(16)
		lbl_title.setFont(font)		
		lbl_title.setText("GeODin QGIS 1.0")
		
		# GeODin Icon
		i_geodin = QLabel(self)
		i_geodin.setPixmap(QPixmap(":\plugins\GeODinQGIS\icons\logo.png").scaled(40,40))


		# Fugro Icon
		i_fugro = QLabel(self)
		i_fugro.setPixmap(QPixmap(":\plugins\GeODinQGIS\icons\fugro.png").scaled(70,70))

		# enter registry and get GeODin build number
		key = OpenKey(HKEY_CURRENT_USER, r"Software\GeODin-System\System", 0, KEY_READ)
		build, dummy = QueryValueEx(key, 'Build')
		CloseKey(key)
		
		lbl_build = QLabel(self)
		lbl_build.setText("Build number:")
		
		lbl_number = QLabel(self)
		lbl_number.setText(build)
		
		# add URL's to GeODin and Fugro websites
		link_geodin = QLabel(self)
		link_geodin.setText('''<a href='http://www.geodin.com'>http://www.geodin.com</a>''')
		link_geodin.setOpenExternalLinks(True)

		link_fugro = QLabel(self)
		link_fugro.setText('''<a href='http://www.fugro.de'>http://www.fugro.de</a>''')
		link_fugro.setOpenExternalLinks(True)
		
		lbl_version1 = QLabel(self)
		lbl_version1.setText("Full functionality only with GeODin 8.2")
		lbl_version2 = QLabel(self)
		lbl_version2.setText("Will be released soon")
		
		# Ok-Button to exit
		buttonBox = QDialogButtonBox(self)
		buttonBox.setOrientation(Qt.Horizontal)
		buttonBox.setStandardButtons(QDialogButtonBox.Ok)
		buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.ok)

		main_grid.addWidget(i_geodin, 0, 0)
		main_grid.addWidget(lbl_title, 0, 1)
		main_grid.addWidget(QLabel(self), 1, 0)
		main_grid.addWidget(i_fugro, 2, 0)
		main_grid.addWidget(buttonBox, 4, 1)
		
		build_grid.addWidget(lbl_build, 0, 0)
		build_grid.addWidget(lbl_number, 0, 1)
		
		link_grid.addWidget(link_geodin, 0, 0)
		link_grid.addWidget(link_fugro, 1, 0)
		
		version_grid.addWidget(lbl_version1, 0, 0)
		version_grid.addWidget(lbl_version2, 1, 0)
		
		main_grid.addLayout(build_grid, 1, 1)
		main_grid.addLayout(link_grid, 2, 1)
		main_grid.addLayout(version_grid, 3, 1)		
		
		self.exec_()

	def ok(self):
		self.accept()
		
class ConfigParser:

	def __init__(self):
		self.__path = ""
		self.__dict = {}

	def add_section(self, section):
		self.__dict[section] = {}

	def set(self, section, key, value):
		self.__dict[section][key]=value

	def read(self, path):
		self.__path = path
		with codecs.open(path, 'r', encoding='utf-8') as f:
			section = ""
			config = f.read()

		for line in config.split('\n'):
			line = line.replace('\r','')
			if (len(line)) and (line[0]=='[') and (line[-1]==']'):
				section = line[1:-1]
				self.add_section(section)

			elif (len(line)) and ('=' in line):
				self.set(section, line.split('=')[0], line.split('=')[1])
						
	def get(self, section, key):
		return self.__dict[section][key]
		
	def has_option(self, section, key):
		try:
			self.get(section, key)
			return True
		except:
			return False

	def options(self, section):
		return self.__dict[section].keys()

	def remove_option(self, section, key):
		del self.__dict[section][key]

	def write(self, configFile):
		for section in self.__dict.keys():
			configFile.write("["+section+"]\n")
			for key in self.__dict[section].keys():
				print key, self.get(section, key)
				configFile.write(key+"="+self.get(section, key)+"\n")
			
	def sections(self):
		return self.__dict.keys()
		
	def items(self, section):
		array = []
		for key in self.options(section):
			array.append((key, self.get(section, key)))
		return array