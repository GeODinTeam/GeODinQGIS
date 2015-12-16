from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from pythonmodules.pypyodbc import *
from ui_Files.ui_GeODinQGIS_DragShp import Ui_DragShape

class DragShp(QDialog, Ui_DragShape):

	def __init__(self, iface, new_dict, lang):
		# setup UI and connect the buttons
		QDockWidget.__init__(self)
		self.iface = iface
		self.setupUi(self)
		self.plugin_dir = os.path.dirname(__file__)
		self.filePath = ""
		self.new_dict = new_dict
		self.lang = lang
		self.canvas = self.iface.mapCanvas()
		
		self.LayerScan()
		self.shape_tab.cellClicked.connect(self.clicked)
		
	def LayerScan(self):
		# scan through QGIS layer list
		layerlist = self.iface.mapCanvas().layers()
		self.shape_tab.setRowCount(len(layerlist))
		
		# insert name and shape file path into table
		for i, row in enumerate(layerlist):
			row.name()
			try:
				source = row.dataProvider().dataSourceUri()
				path_shp, b = source.split("|")
			except:
				continue
			name_input = QTableWidgetItem(row.name())
			self.shape_tab.setItem(i, 0, name_input)
			
			path_input = QTableWidgetItem(path_shp)
			self.shape_tab.setItem(i, 1, path_input)

		
	def clicked(self, currentRow):
		# get shape file path from table
		try:
			self.filePath = self.shape_tab.item(currentRow, 1).text()
		except:
			QMessageBox.information(None,self.new_dict.getWord(self.lang,"No Datatype"),self.new_dict.getWord(self.lang,"Cannot read from vector file. Maybe it's volatile."))
			pass