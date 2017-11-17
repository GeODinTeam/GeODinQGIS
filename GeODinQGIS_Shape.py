# -*- coding: CP1250 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import sys, os
	
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
								QgsField("OBJECTTYPE", QVariant.String),
								QgsField("EPSG", QVariant.Int)]
		
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
		epsg = 0

		for object in self.objects:
			epsg = object.epsg
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
							object.locname,
							object.epsg]
			for key in object.data.keys():
				attribute.append(object.data[key])
		
			feat.setAttributes(attribute)
			provider.addFeatures([feat])

			# Commit changes
			vectorLayer.commitChanges()
		#http://qgis.org/api/2.18/classQgsVectorFileWriter.html#ab566ed2016352c37d9a4a6900614eac2
		error = ""
		fileName = displayName.replace('\\','').replace(':','').replace('*','').replace('?','').replace('"','').replace('<','').replace('>','').replace('|','').replace('/','').strip().replace(' ','_')
		
		if self.main.config.get("Options", "savelayer") == "True":
			fileName = os.path.join(self.main.tmpDirectory, fileName+'.sqlite')
			error = QgsVectorFileWriter.writeAsVectorFormat(vectorLayer, fileName, 'CP1250', QgsCoordinateReferenceSystem(epsg, QgsCoordinateReferenceSystem.EpsgCrsId), 'SpatiaLite', False, None ,['SPATIALITE=YES'])
			layer = QgsVectorLayer(fileName, displayName, "ogr")
			layer.setCrs(QgsCoordinateReferenceSystem(epsg, QgsCoordinateReferenceSystem.EpsgCrsId))
		else:
			fileName = os.path.join(self.main.tmpDirectory, fileName+'.shp')
			error = QgsVectorFileWriter.writeAsVectorFormat(vectorLayer, fileName, "CP1250", QgsCoordinateReferenceSystem(epsg, QgsCoordinateReferenceSystem.EpsgCrsId), 'ESRI Shapefile')
			layer = QgsVectorLayer(fileName, displayName, "ogr")
			layer.setCrs(QgsCoordinateReferenceSystem(epsg, QgsCoordinateReferenceSystem.EpsgCrsId))

		if error == QgsVectorFileWriter.NoError:
			print "NoError"
		elif error == QgsVectorFileWriter.ErrDriverNotFound :
			print "ErrDriverNotFound "
		elif error == QgsVectorFileWriter.ErrCreateDataSource :
			print "ErrCreateDataSource "
		elif error == QgsVectorFileWriter.ErrCreateLayer :
			print "ErrCreateLayer "
		elif error == QgsVectorFileWriter.ErrAttributeTypeUnsupported :
			print "ErrAttributeTypeUnsupported "
		elif error == QgsVectorFileWriter.ErrAttributeCreationFailed :
			print "ErrAttributeCreationFailed "
		elif error == QgsVectorFileWriter.ErrProjection :
			print "ErrProjection "
		elif error == QgsVectorFileWriter.ErrFeatureWriteFailed :
			print "ErrFeatureWriteFailed "
		elif error == QgsVectorFileWriter.ErrInvalidLayer :
			print "ErrInvalidLayer "
		elif error == QgsVectorFileWriter.Canceled :
			print "Canceled "
		
		QgsMapLayerRegistry.instance().addMapLayer(layer)