from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from pythonmodules.helpFunction import *


from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import smtplib, shutil, ConfigParser, win32api

from ui_Files.ui_GeODinQGIS_Settings import Ui_Settings

class Settings(QDialog, Ui_Settings):

	def __init__(self, main):
		# setup UI and connect the buttons
		QDialog.__init__(self)

		self.setupUi(self)
		
		self.main = main

		# connect buttons to their functions
		QObject.connect(self.btn_del_tmp, SIGNAL("clicked()"), self.deleteTmp)
		QObject.connect(self.btn_mail, SIGNAL("clicked()"), self.sendMail)
		self.connect(self.btn_dir, SIGNAL("clicked()"), self.Tmp_Dir)
		self.connect(self.btn_defdir, SIGNAL("clicked()"), self.Def_Dir)
		self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.okClick)
		QObject.connect(self.btn_info, SIGNAL("clicked()"), self.openInfo)

		# manage button icons
		self.btn_info.setIcon(QIcon(":\plugins\GeODinQGIS\icons\info.png"))
		self.btn_del_tmp.setIcon(QIcon(":\plugins\GeODinQGIS\icons\i_102F.png"))
		self.btn_del_tmp.setIconSize(QSize(24, 24))

		# path of tmp folder in home directory
		self.tmpDirectory = main.tmpDirectory

		self.dict = main.dictionary
		self.lang = main.lang
		self.errorLog = main.logDirectory+"\\error.log"
		
		self.setWindowTitle(self.dict.getWord(self.lang,"Settings"))
		self.lbl_del.setText(self.dict.getWord(self.lang,"Delete temporary files"))
		self.lbl_surpress.setText(self.dict.getWord(self.lang,"Suppress attribute form pop-up after feature creation"))
		self.btn_mail.setText(self.dict.getWord(self.lang,"Send Email"))
		self.lbl_dir.setText(self.dict.getWord(self.lang,"Directory to save vector layers"))
		self.lbl_lyr.setText(self.dict.getWord(self.lang,"Save Layer as"))
		self.btn_defdir.setText(self.dict.getWord(self.lang,"Restore Default"))
		
		self.logFile()
		
		self.configFile = main.configFile
		self.config = main.config
		self.readConfigFile()

		self.exec_()
		
	def Tmp_Dir(self):
		# enter custom directory for temporary files
		tmpDirectory = QFileDialog.getExistingDirectory(self)
		self.le_dir.setText(tmpDirectory)
		
	def Def_Dir(self):
		# restore default directory for temporary files
		self.le_dir.setText(self.main.def_tmp_dir)
		
	def readConfigFile(self):
		self.le_dir.setText(self.config.get('Options', 'tmpdirectory'))
		
		if self.config.get("Options", "suppressattribute") == "True":
			self.checkBox.setChecked(True)
		else:
			self.checkBox.setChecked(False)
			
		if self.config.get("Options", "savelayer") == "True":
			self.rbtn_sql.setChecked(True)
#			self.rbtn_sql.setChecked(False)
			print self.rbtn_shp.isChecked()
			print self.rbtn_sql.isChecked()
		else:
			self.rbtn_shp.setChecked(True)
#			self.rbtn_shp.setChecked(False)

		
	def okClick(self):
		self.main.tmpDirectory = self.le_dir.text()
		if self.checkBox.isChecked():
			self.config.set('Options', "suppressattribute", "True")
			QSettings().setValue( '/qgis/digitizing/disable_enter_attribute_values_dialog', True )
		else:
			self.config.set('Options', "suppressattribute", "False")
			QSettings().setValue( '/qgis/digitizing/disable_enter_attribute_values_dialog', False )
			
		if self.rtbn_sql.isChecked():
			self.config.set('Options', "savelayer", "True")
		else:
			self.config.set('Options', "savelayer", "False")
		
		self.config.set('Options', 'tmpdirectory', self.main.tmpDirectory)
			
		self.saveConfig()			
			
	def saveConfig(self):
		with open(self.configFile, 'wb') as configFile:
			self.config.write(configFile)
			
	def deleteTmp(self):
		# delete files in tmp-directory
		try:
			for subFile in os.listdir(self.tmpDirectory):
				subFilePath = os.path.join(self.tmpDirectory, subFile)
				if os.path.isfile(subFilePath):
					try:
						os.unlink(subFilePath)
					except:
						pass
				elif os.path.isdir(subFilePath): 
					try:
						shutil.rmtree(subFilePath)
					except:
						pass
			QMessageBox.information(None,self.dict.getWord(self.lang,"Deletion"),self.dict.getWord(self.lang,"Temporary files deleted successfully"))
		except Exception,e:
			print str(e)
			return
			
	def logFile(self):
		# print size of error log file in kb
		size = str(round(float(os.path.getsize(self.errorLog))/1000)) + " kb"
		self.lbl_size.setText(size)
		
	def sendMail(self):
		# send email to GeODin support team
		# email browser is automatically openend
		# error log file must be attached manually
		# text from error message is appreciated
		email = "mailto:"
		receiver = "support@geodin.com"
		cc = [""]
		bcc = [""]
		subject = "Fehlermeldung GeODin QGIS"
		body = "Es ist ein Fehler bei der Arbeit mit GeODinQGIS aufgetreten.\n\nDas Fehlerprotokoll befindet sich im Anhang."
		
		body = body.replace(' ', '%20').replace('\n', '%0D%0A').replace('=',':').replace('"',"'")
		email += receiver +'&SUBJECT='+subject+'&BODY='+body
		win32api.ShellExecute(0, 'open', email, None, None, 0)

	def attrsDialog(self):
		# get user defined current setting
		disableDialog = QSettings().value( '/qgis/digitizing/disable_enter_attribute_values_dialog')
		# override setting
		QSettings().setValue( '/qgis/digitizing/disable_enter_attribute_values_dialog', True )
		# restore setting
		QSettings().setValue( '/qgis/digitizing/disable_enter_attribute_values_dialog', disableDialog )
		
	def openInfo(self):
		print "Info"
		info = Info()