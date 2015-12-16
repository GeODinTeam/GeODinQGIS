# -*- coding: CP1250 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import sys
	
class ShapeFromPoint:

	def __init__(self, main, queryObject):

		self.main = main
		self.shapeName = queryObject.name
		self.objects = queryObject.objects
		self.project = queryObject.parent
		self.database = queryObject.parent.parent
		
		# reference to the map canvas
		self.canvas = self.main.iface.mapCanvas()
		
		if not self.database:
			self.database = self.project
		
		self.buildLayer()

	def buildLayer(self):
		
		displayName = self.database.name+'_'+self.project.name+'_'+self.shapeName.replace('/','')
		vectorLayer = QgsVectorLayer("Point", displayName, "memory")
		provider = vectorLayer.dataProvider()
		vectorLayer.startEditing()

		# create field names for vector layer
		attributeList = [QgsField("INVID", QVariant.String),
								QgsField("SHORTNAME", QVariant.String),
								QgsField("LONGNAME",  QVariant.String),
								QgsField("XCOORD", QVariant.Double),
								QgsField("YCOORD", QVariant.Double),
								QgsField("DBTYPE", QVariant.String),
								QgsField("DATABASE", QVariant.String),
								QgsField("PRJNAME", QVariant.String),
								QgsField("PRJID", QVariant.String),
								QgsField("OBJECTTYPE", QVariant.String)]
		
		for key in self.objects[0].data.keys():
			try:
				value = float(self.objects[0].data[key])
				field = QgsField(key, QVariant.Double)
				attributeList.append(field)
			except:
				pass
			try:
				value = str(self.objects[0].data[key])
				field = QgsField(key, QVariant.String)
				attributeList.append(field)
			except:
				pass
		
		# add fields to attribute table
		provider.addAttributes(attributeList)

		for object in self.objects:
			# add feature
			feat = QgsFeature()
			feat.setGeometry( QgsGeometry.fromPoint(QgsPoint(object.coordinates[0], object.coordinates[1])) )
			attribute = [object.invid, 
							object.shortname, 
							object.name, 
							object.coordinates[0], 
							object.coordinates[1], 
							self.database.options["connection"], 
							self.database.filepath, 
							object.parent.name, 
							object.parent.id, 
							object.locname]

			for key in object.data.keys():
				attribute.append(object.data[key])
							
			feat.setAttributes(attribute)
			provider.addFeatures([feat])

			# Commit changes
			vectorLayer.commitChanges()
		
		if self.main.config.get("Options", "savelayer") == "True":
			QgsVectorFileWriter.writeAsVectorFormat(vectorLayer, self.main.tmpDirectory + '\\' + displayName.replace('/','') + '.sqlite', 'CP1250', None, 'SQLite', False, None ,['SPATIALITE=YES',])
			layer = QgsVectorLayer(self.main.tmpDirectory + '\\' + displayName.replace('/','') + '.sqlite', displayName, "ogr")
		
		else:
			QgsVectorFileWriter.writeAsVectorFormat(vectorLayer, self.main.tmpDirectory + '\\' + displayName.replace('/','') + '.shp', "CP1250", None, "ESRI Shapefile")
			layer = QgsVectorLayer(self.main.tmpDirectory + '\\' + displayName.replace('/','') + '.shp', displayName, "ogr")

		QgsMapLayerRegistry.instance().addMapLayer(layer)