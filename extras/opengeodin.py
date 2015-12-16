# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import sys
from win32api import GetSystemMetrics
from PIL import Image

import win32com.client
import time
import json, os
import datetime
import md5


class GeODinFromObject:

	def __init__(self, main, item):

		self.main = main
		self.item = item
		
		# get variable references from "GeODinQGIS_Main"
		self.alias = item.parent.parent.name	

#		self.objectName = queryObject.name
#		self.objects = queryObject.objects
#		self.project = queryObject.parent
#		self.database = queryObject.parent.parent
		
#		if not self.database:
#			self.database = self.project

		self.GeODin = win32com.client.Dispatch("GeODin.GeODinApplication")
		
		self.geodin()
		
	def geodin(self):
		#self.lgr.warning('GeODin COM')
		# connect to GeODin COM functions
#		self.GeODin = win32com.client.Dispatch("GeODin.GeODinApplication")
		
		# select object type in GeODin obeject manager
		Params = "[Params]\n" 
		Database = "Database="
		Username = "\nUserName="
		Password = "\nPassword="
		Objecttype = "\nObjectType=1"
		Parentnode = "\nParentNode=ProjectQueries"
		Object_ID = "\nObjectID="
		Expand = "\nExpand=true"
		
		params = Params + Database + self.alias + Username + Password + Objecttype + Parentnode + Object_ID + self.item.invid + Expand
		#self.lgr.warning(params)
		# execute method
		self.GeODin.SelectObject(params)	
		
		# set parameters to create a new object
		# Params = "[Params]\n"
		# FieldValues = "ApplyFieldValues=True"
		# XCOORDS = "\nXCOORD="
		# YCOORDS = "\nYCOORD="
		# PRJID = "\nPRJID="

		# params = Params + FieldValues + XCOORDS + x + YCOORDS + y + PRJID + self.proj_ID
		# #self.lgr.warning(params)
		# # execute method to create new object
		# error = GeODin.ExecuteMethodParams(39,params)
		# if error:
			# #print "Error ID:"+ str(GeODin.ExceptionValue)
			# self.lgr.info("Error ID: "+ str(GeODin.ExceptionValue))
			# #print "Error Message:"+GeODin.ExceptionMsg
			# self.lgr.info("Error Message: "+GeODin.ExceptionMsg)
			
		self.GeODin.ExecuteMethod(1)	
		
		time.sleep(3)
#		GeODin = None
		

		