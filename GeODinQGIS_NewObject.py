from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from pythonmodules.pypyodbc import *
from pythonmodules.helpFunction import *
import os, sys, time, logging, win32com.client
from GeODinQGIS_Settings import Settings
from GeODinQGIS_DragShp import DragShp
from ui_Files.ui_GeODinQGIS_NewObject import Ui_NewObject

class NewObject(QDockWidget, Ui_NewObject):

	def __init__(self, iface, objecttype, project, lang_dict, lang):
		# setup UI and connect the buttons
		QDockWidget.__init__(self)
		self.iface = iface
		self.setupUi(self)
		
		# get variable references from "GeODinQGIS_Main"
		self.obj_type = objecttype.name
		self.loctype = objecttype.gen_desc
		self.path = project.parent.filepath
		self.dbtype = project.parent.options["connection"]
		self.alias = project.parent.name
		self.project_names = project.name
		self.proj_ID = project.id		
		self.plugin_dir = os.path.dirname(__file__)
		self.saveFileFolder = self.plugin_dir+"/tmp/"
		
		self.lgr = logging.getLogger('GeODinQGIS.NewObject')
		
		self.lang_dict = lang_dict
		self.lang = lang
		
		# select whole table row instead of single cell
		self.coord_tab.setSelectionBehavior(QAbstractItemView.SelectRows)
		
		# some empty lists to store coordinates from map canvas
		self.x_list = []
		self.y_list = []
		self.id_list = []
		self.rows = []
		self.attrs_list = []
		
		self.shortname = None
		self.easting = None
		self.northing = None
		
		# reference to the map canvas
		self.canvas = self.iface.mapCanvas()
		
		# define button signals for vector file management
		QObject.connect(self.btn_createshp, SIGNAL("clicked()"), self.createVector)
		QObject.connect(self.btn_openshp, SIGNAL("clicked()"), self.openVector)
		QObject.connect(self.btn_dragshp, SIGNAL("clicked()"), self.dragVector)
		
		# set behavior to load an existing vector file from layer registry to coordinate table
		self.open = False
		self.drag = False
		
		#self.btn_dragshp.setEnabled(False)
		self.btn_geodin.setEnabled(False)
		self.btn_del.setEnabled(False)
		self.btn_desel.setEnabled(False)
		self.cmb_short.setEnabled(True)
		
		# connect buttons to their functions
		QObject.connect(self.btn_geodin, SIGNAL("clicked()"),self.geodin)
		QObject.connect(self.btn_close, SIGNAL("clicked()"),self, SLOT("close()"))
		QObject.connect(self.btn_del, SIGNAL("clicked()"), self.delete)
		QObject.connect(self.btn_desel, SIGNAL("clicked()"), self.deselect)
		QObject.connect(self.cmb_short, SIGNAL("currentIndexChanged (const QString&)"), self.shortNameChoose)
		QObject.connect(self.cmb_east, SIGNAL("currentIndexChanged (const QString&)"), self.eastingChoose)
		QObject.connect(self.cmb_north, SIGNAL("currentIndexChanged (const QString&)"), self.northingChoose)
		
		# manage button icons		
		self.btn_createshp.setIcon(QIcon(":\plugins\GeODinQGIS\icons\point_create_n.png"))
		self.btn_openshp.setIcon(QIcon(":\plugins\GeODinQGIS\icons\point_add_n.png"))
		self.btn_dragshp.setIcon(QIcon(":\plugins\GeODinQGIS\icons\point_drag_n.png"))
		self.btn_del.setIcon(QIcon(":\plugins\GeODinQGIS\icons\delete.png"))
		self.btn_geodin.setIcon(QIcon(":\plugins\GeODinQGIS\icons\logo.png"))
		self.btn_desel.setIcon(QIcon(":\plugins\GeODinQGIS\icons\minus.png"))
		self.btn_del.setIconSize(QSize(24, 24))
		self.btn_geodin.setIconSize(QSize(24, 24))
		self.btn_desel.setIconSize(QSize(24, 24))
		self.btn_createshp.setIconSize(QSize(24, 24))
		self.btn_openshp.setIconSize(QSize(24, 24))
		self.btn_dragshp.setIconSize(QSize(24, 24))
	
		# manage tool tips
		createshp = self.lang_dict.getWord(self.lang,"Create new shape file")
		loadshp = self.lang_dict.getWord(self.lang,"Load shape file from file system")
		dragshp = self.lang_dict.getWord(self.lang,"Load shape file from layers panel")
		
		deleteRow = self.lang_dict.getWord(self.lang,"Delete selected rows")
		deselectRow = self.lang_dict.getWord(self.lang,"Deselect rows")
		openGeodin = self.lang_dict.getWord(self.lang,"Import to GeODin")
		
		self.btn_createshp.setToolTip(createshp)
		self.btn_openshp.setToolTip(loadshp)
		self.btn_dragshp.setToolTip(dragshp)
		
		self.btn_del.setToolTip(deleteRow)
		self.btn_desel.setToolTip(deselectRow)
		self.btn_geodin.setToolTip(openGeodin)
		
		# # set headers for child nodes
		# if self.obj_type == "All Objects":
			# self.le_obtyp.setText("All Objects")

		# else:
			# self.le_obtyp.setText(self.obj_type)
		
		self.delete = False
		self.editMode = False
		
		# clear coordinate table
		self.coord_tab.setRowCount(0)
		
		# decimal places
		self.dp = 8
		
		# 
		self.coord_tab.itemChanged.connect(self.Changed)
		#self.coord_tab.cellClicked.connect(self.clicked)
		
		self.coord_tab.itemSelectionChanged.connect(self.selectionChanged)
		
		self.root = QgsProject.instance().layerTreeRoot()	
	
	def dragVector(self):
		# open layer list table to drag shape into coordinate table
		sel = DragShp(self.iface, self.lang_dict, self.lang)
		sel.show()
		sel.exec_()
		
		# set open file name for shape (filePath)
		# add shape to coordinate table
		if sel.accepted:
			self.drag = True
			self.openName = sel.filePath
			self.loadVector()	
			
	def onremovedChildren(self, node, indexFrom, indexTo):
		# execute if a layer has been removed from QGIS layer list
		# ,ap over layer ID's in layer list
		ids = self.root.findLayerIds()
		
		# deleted, if layer ID cannot be found in layer list
		if self.layerID not in ids:
			# if layer was loaded in coordinate table, empty it
			self.coord_tab.setRowCount(0)
			
	def Started(self):
		# if editing mode has been toggled on
		self.editMode = True
		self.cmb_short.setEnabled(False)
		# table cell is only editable if has been double clicked
		if not QAbstractItemView == None:
			self.coord_tab.setEditTriggers(QAbstractItemView.DoubleClicked)
		
		# if one or more item have been selected, deletion allowed
		if len(self.coord_tab.selectedItems()) >0:
			self.btn_del.setEnabled(True)
		
	def Stopped(self):
		# turn edit triggers and deletion off
		self.editMode = False
		if not QAbstractItemView == None:
			self.coord_tab.setEditTriggers(QAbstractItemView.NoEditTriggers)
			
		self.btn_del.setEnabled(False)
		self.cmb_short.setEnabled(True)
	
		if len(self.cmb_short.currentText()) > 0:
			self.shortname = self.cmb_short.currentText()
		else:
			self.shortname = None
			
		if len(self.cmb_east.currentText()) > 0:
			self.easting = self.cmb_east.currentText()
		else:
			self.easting = None	

		if len(self.cmb_north.currentText()) > 0:
			self.northing = self.cmb_north.currentText()
		else:
			self.northing = None				
	
		# read attribute table and insert items into coordinate table
		self.insertItem()
		
		self.v_points.updateFields()
		self.selectionChanged()
		
	def Changed(self, item):
		# if item has been changed in coordinate table
		# editing mode is required
		# print self.coord_tab.currentColumn()
		# print self.coord_tab.currentRow()
		if self.v_points.isEditable():
			# print self.coord_tab.currentItem()
			# print self.coord_tab.currentColumn()
			# print self.coord_tab.currentRow()
			# coordinate which has been edited (only one at a time)
			coord_edit = float(self.coord_tab.currentItem().text())
			
			# change coordinate equals "coord_edit"
			if self.coord_tab.currentColumn() == 1:
				x = coord_edit
				y = float(self.coord_tab.item(self.rows[0],2).text())
			
			elif self.coord_tab.currentColumn() == 2:
				x = float(self.coord_tab.item(self.rows[0],1).text())
				y = coord_edit
			
			# QGIS internal functions
			# move vertex to new coordinates
			ch = QgsVectorLayerEditUtils(self.v_points)
			ch.moveVertex(x, y, self.rows[0], 0)

	def selectionChanged(self):
		#its = self.coord_tab.selectedItems()
		# write list with indices of all selected rows
		lines = self.coord_tab.selectionModel().selectedRows()
		
		self.btn_desel.setEnabled(True)
		
		# new empty list
		# loop over lines and add to rowlist
		# sort reversed
		self.rows = []
		for idx in lines:
			self.rows.append(idx.row())

		self.rows.sort(reverse=True)

		if len(self.rows) == 1:
			# get coordinates from selection
			self.coord_x = self.coord_tab.item(self.rows[0],1).text()
			self.coord_y = self.coord_tab.item(self.rows[0],2).text()
			self.name = self.coord_tab.item(self.rows[0],0).text()
			self.btn_geodin.setEnabled(True)
		else:
			self.btn_geodin.setEnabled(False)
		
		self.sel_x = []
		self.sel_y = []
		self.sel_id = []
		self.sel_attrs = []

		for i in self.rows:
			id = self.id_list[i]
			self.sel_id.append(id)
			x_coord = self.x_list[i]
			self.sel_x.append(x_coord)
			y_coord = self.y_list[i]
			self.sel_y.append(y_coord)
		
		if self.editMode:
			self.btn_del.setEnabled(True);
		
			
	def delete(self):
		self.delete = True
		
		# delete entries from coordinate list and from temporary shape file
	#	self.le_east.clear()
	#	self.le_north.clear()
		self.rows.sort(reverse=True)
		
		# map over vector layer and get attributes
		features = self.v_points.getFeatures()
		for f in features:
			fid = str(f.id())
			# map over selected ID's
			# check if feature ID matches selected ID 
			for i in self.sel_id:
				if i == fid:
					self.v_points.deleteFeature(f.id())
					self.v_points.dataProvider().forceReload()
					self.v_points.triggerRepaint()
					#delete from self.coord_tab

		for row in self.rows:
			self.coord_tab.removeRow(row)
		
		self.rows = []
		self.btn_del.setEnabled(False)	
		
		self.delete = False
		
	def openVector(self):
		# load vector file from file system
		self.open = True
		
		# get path of vector file
		self.openName = QFileDialog.getOpenFileName(self, "Load Vector Layer",".", "Shape (*.shp)")
		
		# if open dialog has been aborted
		if not self.openName:
			return
		
		# take file path and load vector file
		self.loadVector()

	def loadVector(self):
		self.v_points = None
		# name of loaded shape file equals geodin object type
		self.display_name = self.obj_type
		
		# get reference of shape 
		self.v_points = QgsVectorLayer(self.openName, self.display_name, "ogr")
		
		# vector file must be a point shape
		# important for vector drag from layer list
		if not self.v_points.wkbType() == QGis.WKBPoint:
			QMessageBox.information(None,self.lang_dict.getWord(self.lang,"Wrong Datatype"),self.lang_dict.getWord(self.lang,"You must load a Point Shape"))
			return
		
		# if vector file has been loaded from file system
		if self.open == True:
			# add file to map canvas
			QgsMapLayerRegistry.instance().addMapLayer(self.v_points)
			self.addVector()
			self.open = False
		
		# if vector file has been dragged from layer list
		elif self.drag == True:	
			self.addVector()
			self.drag = False
		
	def addVector(self):
	# get reference from layer list to loaded vector layer
	# build coordinate table
		# map over layer list
		layers = QgsMapLayerRegistry.instance().mapLayers()
		
		# split into layer ID and layer instance
		for ID, layer in layers.iteritems():
			source = layer.source()
			
			# if paths of vector layer equal each other
			# take instance of vector layer from layer list
			if self.openName == source:
				self.v_points = layer
				self.layerID = ID	
		
		# execute if layer has been removed
		self.root.removedChildren.connect(self.onremovedChildren)

		# select short name, easting and northing from attribute table
		self.cmb_short.clear()
		self.cmb_east.clear()
		self.cmb_north.clear()
		
		self.cmb_short.addItem("")	
		self.cmb_east.addItem("")	
		self.cmb_north.addItem("")	
		
		for field in self.v_points.pendingFields():
			self.cmb_short.addItem(field.name())
			self.cmb_east.addItem(field.name())
			self.cmb_north.addItem(field.name())			
		
		# fill coordinate table and update attribute table
		self.insertItem()
		
		# toggle editing modes
		self.v_points.editingStarted.connect(self.Started)
		self.v_points.editingStopped.connect(self.Stopped)

	def createVector(self):
		# name of shape file equals object type
		self.display_name = self.obj_type
		
		# create temporary shape file
		tmplayer = QgsVectorLayer("Point", self.display_name, "memory")
		
		provider = tmplayer.dataProvider()
	
		# Enter editing mode
		tmplayer.startEditing()
		
		# add attribute fields to shape
		provider.addAttributes([QgsField("INVID", QVariant.String),
								QgsField("SHORTNAME", QVariant.String),
								QgsField("LONGNAME",  QVariant.String),
								QgsField("XCOORD", QVariant.Double),
								QgsField("YCOORD", QVariant.Double),
								QgsField("DBTYPE", QVariant.String),
								QgsField("DATABASE", QVariant.String),
								QgsField("PRJNAME", QVariant.String),
								QgsField("PRJID", QVariant.String),
								QgsField("OBJECTTYPE", QVariant.String)])
		
		tmplayer.commitChanges()
		
		# get file name to be saved
		outName = QFileDialog.getSaveFileName(self, "Save Vector Layer",self.saveFileFolder+self.display_name.replace(" ", "_"), "Shape (*.shp)")
		if not outName:
			return
		self.saveFileFolder = os.path.dirname(outName)+"/"
		
		# declare options for temporary shape layer
		QgsVectorFileWriter.writeAsVectorFormat(tmplayer, outName, "CP1250", None, "ESRI Shapefile")
		
		# turn temporary layer into QGIS vector layer
		self.v_points = QgsVectorLayer(outName, self.display_name, "ogr")
		
		# add vector file to QGIS layer registry
		QgsMapLayerRegistry.instance().addMapLayer(self.v_points)
		
		# find layer ID's of all layer in layer registry
		ids = self.root.findLayerIds()
		
		# if layer registry is empty, return
		if not ids:
			return
		# if layer registry is not empty, take top level layer ID
		else:
			self.layerID = ids[0]	
		
		# exeute if layer has been removed
		self.root.removedChildren.connect(self.onremovedChildren)
		
		# toggle editing modes
		self.v_points.editingStarted.connect(self.Started)
		self.v_points.editingStopped.connect(self.Stopped)
	
	def shortNameChoose(self, shortname):
		self.shortname = shortname
		self.insertItem(True)
	
	def eastingChoose(self, easting):
		self.easting = easting
		self.insertItem(True)
	
	def northingChoose(self, northing):
		self.northing = northing
		self.insertItem(True)
	
	def insertItem(self, chooseField = False):
	
		#print shortname, easting, northing
		# create empty coordinate and ID lists
		self.x_list = []
		self.y_list = []
		self.id_list = []
		self.short_list = []
		
		# touch vector file and get feature information
		features = self.v_points.getFeatures()
		fields = self.v_points.pendingFields()

		# map over features (row in attribute table, object/point in canvas)
		for f in features:

			fid = str(f.id())
			geom = f.geometry()
			#print f.attributes() 
			
			# get feature coordinates from the map
			x = str(round(geom.asPoint().x(), self.dp))
			y = str(round(geom.asPoint().y(), self.dp))
			attrs = f.attributes()
#			a = attrs[1]
			
			# build lists with feature information
			
			if self.easting:
				if fields[fields.fieldNameIndex(self.easting)].type() == 6:
					self.x_list.append(f[self.easting])
				else:
					self.x_list.append('')
			else:
				self.x_list.append(x)
				
			if self.northing:
				if fields[fields.fieldNameIndex(self.northing)].type() == 6:
					self.y_list.append(f[self.northing])
				else:
					self.y_list.append('')
			else:
				self.y_list.append(y)

			self.id_list.append(fid)

			# short name is None, if nothing was selected, 1st column will be empty
			# if short name exists, append to list to write into table

			if self.shortname and not f[self.shortname] == None:
				self.short_list.append(f[self.shortname])
			else:
				self.short_list.append('')

		self.coord_tab.setRowCount(len(self.x_list))
		
		
		try:
		
			# insert short name into table
			for i, row in enumerate(self.short_list):
				short_input = QTableWidgetItem(row)
				self.coord_tab.setItem(i, 0, short_input)

			# insert x-coordinate into table
			for j, row in enumerate(self.x_list):
				x_input = QTableWidgetItem(str(row))
				self.coord_tab.setItem(j, 1, x_input)

			# insert y-coordinate into table
			for k, row in enumerate(self.y_list):
				y_input = QTableWidgetItem(str(row))
				self.coord_tab.setItem(k, 2, y_input)
		except TabError as te:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)
			msg.setText(str(ex))
			msg.exec_()
		except Exception as ex:
			msg = QMessageBox()
			msg.setIcon(QMessageBox.Critical)
			msg.setText(str(ex))
			msg.exec_()
			
		# touch vector file again and update attribute table
		# important if information had been changed in coordinate table
		# need to be in editing mode
		# features = self.v_points.getFeatures()

		if not chooseField:
			caps = self.v_points.dataProvider().capabilities()
			for i,f in enumerate(features):
				fid = f.id()
				
				# get coordinates from coordinate table
				x = self.coord_tab.item(i,1).text()
				y = self.coord_tab.item(i,2).text()

				# enter information into attribute table
				if caps & QgsVectorDataProvider.ChangeAttributeValues:
					attrs = { 3 : x, 4 : y, 5 : self.dbtype, 6 : self.path, 7 : self.project_names, 8 : self.proj_ID, 9 : self.obj_type }

					self.v_points.dataProvider().changeAttributeValues({ fid : attrs })

	def keyPressEvent(self, event):
		#Did the user press the Enter key?
		if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter or event.key() == Qt.Key_Tab: #QtCore.Qt.Key_Escape is a value that equates to what the operating system passes to python from the keyboard when the escape key is pressed.
		#Yes: Close the window
			print "key pressed"
		#No:  Do nothing.
		
	def clicked(self, currentRow):
		print "clicked"
		# write list with indices of all selected rows
		line = self.coord_tab.selectionModel().selectedRows()
		
		self.btn_desel.setEnabled(True)
		
		# new empty list
		# loop over lines and add to rowlist
		# sort reversed
		self.rows = []
		for idx in line:
			self.rows.append(idx.row())
		
		self.rows.sort(reverse=True)

		if len(self.rows) == 1:
			self.btn_geodin.setEnabled(True)
		
		self.sel_x = []
		self.sel_y = []
		self.sel_id = []
		self.sel_attrs = []

		# get coordinates from selection
		self.coord_x = self.coord_tab.item(self.rows[0],1).text()
		self.coord_y = self.coord_tab.item(self.rows[0],2).text()
		self.name = self.coord_tab.item(self.rows[0],0).text()
		
		for i in self.rows:
			id = self.id_list[i]
			self.sel_id.append(id)
			x_coord = self.x_list[i]
			self.sel_x.append(x_coord)
			y_coord = self.y_list[i]
			self.sel_y.append(y_coord)
		
	#	self.le_east.clear()
	#	self.le_north.clear()	

	#	self.le_east.insert(self.coord_x)
	#	self.le_north.insert(self.coord_y)
		
		if len(self.rows) != 1:
		#	self.le_east.clear()
		#	self.le_north.clear()
			self.btn_geodin.setEnabled(False)
			
		if self.editMode:
			self.btn_del.setEnabled(True);
		
	def geodin(self):
		#self.lgr.warning('GeODin COM')
		# connect to GeODin COM functions
		
		for cell in self.coord_tab.selectedItems():
			shortname = cell.text()
			break;
		
		FieldValues = ""
		features = self.v_points.getFeatures()
		for feature in features:
			if feature[self.shortname] == shortname:
				for field in feature.fields():
					#print field.name().lower()
					#if field.name() != self.shortname and field.name() != self.easting and field.name() != self.northing and field.name().lower() != 'invid' and field.name().lower() != 'objecttype':
					if not str(feature[field.name()]) == 'NULL' and not str(feature[field.name()]) == '':
						FieldValues += field.name()+"="+str(feature[field.name()])+"\n"
		
		try:
			GeODin = win32com.client.Dispatch("GeODin.GeODinApplication")
		
		#	x = self.le_east.text()
		#	y = self.le_north.text()
			short = "NAME=B101"

			if len(self.coord_x) ==0:
				QMessageBox.information(None,self.lang_dict.getWord(self.lang,"Selection Error"),self.lang_dict.getWord(self.lang,"Nothing to read. Please select the row to be written into GeODin."))
			
			else:
				# select object type in GeODin obeject manager
				Params = "[Params]\n" 
				Database = "Database="
				Username = "\nUserName="
				Password = "\nPassword="
				Objecttype = "\nObjectType=1"
				Parentnode = "\nParentNode=ProjectQueries"
				Object_ID = "\nObjectID="
				Expand = "\nExpand=true"
				
				params = Params + Database + self.alias + Username + Password + Objecttype + Parentnode + Object_ID + self.proj_ID + Expand
				print params
				#self.lgr.warning(params)
				# execute method
				GeODin.SelectObject(params)
				
				# set parameters to create a new object
				Params = "[Params]\n"
				ApplyFieldValues = "ApplyFieldValues=True"
				XCOORDS = "\nXCOORD="
				YCOORDS = "\nYCOORD="
				OBJECTTYPE = "\nOBJECTTYPE="
				NAME = "\nNAME="
				PRJID = "\nPRJID="
				FieldValueSection = "\n[FieldValues]\n"

				params = Params + ApplyFieldValues + XCOORDS + self.coord_x + YCOORDS + self.coord_y + OBJECTTYPE + self.loctype + NAME + self.name + PRJID + self.proj_ID + FieldValueSection + FieldValues
				print params
				#self.lgr.warning(params)
				# execute method to create new object
				error = GeODin.ExecuteMethodParams(39,params)
				if error:
					#print "Error ID:"+ str(GeODin.ExceptionValue)
					self.lgr.info("Error ID: "+ str(GeODin.ExceptionValue))
					#print "Error Message:"+GeODin.ExceptionMsg
					self.lgr.info("Error Message: "+GeODin.ExceptionMsg)
			
			time.sleep(3)
		except:
			print "Unexpected error:", sys.exc_info()[0]
		GeODin = None
		
	def deselect(self):
		self.rows = []
		self.sel_x = []
		self.sel_y = []
		
		selected = self.coord_tab.selectedRanges()
		for i in range(len(selected)):
			self.coord_tab.setRangeSelected(selected[i], False)
	#	self.le_east.clear()
	#	self.le_north.clear()
		
		self.btn_desel.setEnabled(False)