from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import os, sys, time

from ui_Files.ui_GeODinQGIS_SelectCoords import Ui_SelectCoords

class SelectCoords(QDialog, Ui_SelectCoords):

	def __init__(self, iface, new_dict, lang, v_points):
		# setup UI and connect the buttons
		QDockWidget.__init__(self)
		self.iface = iface
		self.setupUi(self)
		self.plugin_dir = os.path.dirname(__file__)
		
		self.new_dict = new_dict
		self.lang = lang
		self.v_points = v_points
		self.canvas = self.iface.mapCanvas()
		self.ok = False		
		self.buttonBox.button(QDialogButtonBox.Ok).clicked.connect(self.okClick)

		fields = self.v_points.pendingFields()
		self.fields_list = []
		
		for f in fields:
			#print f.name()
			self.fields_list.append(f.name())
		
		self.cmb_xcol.addItems(self.fields_list)
		self.cmb_ycol.addItems(self.fields_list)
		

		
		
	def okClick(self):
		self.ok = True
		
		x_text = self.cmb_xcol.currentText()
		y_text = self.cmb_ycol.currentText()
		
		self.x_index = self.fields_list.index(x_text)
		self.y_index = self.fields_list.index(y_text)