# pip install tkcalendar
# pip install reportlab

from tkinter import *
from tkinter import ttk,messagebox
from tkinter.ttk import Notebook
from tkcalendar import Calendar, DateEntry
from datetime import datetime
import tkinter.font as tkFont
import sqlite3
import subprocess


from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm, cm
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, SimpleDocTemplate, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import  A4, landscape
from reportlab.platypus import Paragraph, Table, SimpleDocTemplate, Spacer
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer,Image
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
#Add font
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class Report3(object):
	""""""
 
	#----------------------------------------------------------------------
	def __init__(self,date='2018-05-02', dp='Maintenance', mc='Wood pallet 1'):
		"""Constructor"""
		self.width, self.height = A4
		self.styles = getSampleStyleSheet()
		self.datefromsql = date
		self.department = dp
		self.mainmc = mc
		
 
	#----------------------------------------------------------------------
	def coord(self, x, y, unit=1):
		"""
		http://stackoverflow.com/questions/4726011/wrap-text-in-a-table-reportlab
		Helper class to help position flowables in Canvas objects
		"""
		x, y = x * unit, self.height -  y * unit
		return x, y
 
	#----------------------------------------------------------------------
	def run(self,filename,data):
		"""
		Run the report
		"""
		self.doc = SimpleDocTemplate(filename,pagesize=A4, rightMargin=30,leftMargin=30, topMargin=50,bottomMargin=18)
		self.story = [Spacer(1, 1*cm)]
		self.createLineItems(data)
 
		self.doc.build(self.story, onFirstPage=self.createDocument)
		print ("finished!")
 
	#----------------------------------------------------------------------
	def createDocument(self, canvas, doc):
		"""
		Create the document
		"""
		pdfmetrics.registerFont(TTFont('chsFont', 'THSarabunNew.ttf'))

		self.c = canvas
		normal = self.styles["Title"]
 
		header_text = "<font name='chsFont'><b>THE ENERGY  CO.,LTD</b></font>"
		p = Paragraph(header_text, normal)
		p.wrapOn(self.c, self.width, self.height)
		p.drawOn(self.c, *self.coord(0, 12, mm))
 
		ptext = """<font name='chsFont'>รายการซ่อมบำรุงรักษาเชิงป้องกัน</font>"""
 
		p = Paragraph(ptext, style=normal)
		p.wrapOn(self.c, self.width, self.height)
		p.drawOn(self.c, *self.coord(0, 20, mm))

		ptext = """<font name='chsFont'>TEC-EN-MC01</font>"""
 
		p = Paragraph(ptext, style=normal)
		p.wrapOn(self.c, self.width, self.height)
		p.drawOn(self.c, *self.coord(80, 20, mm))

		ptext = """<font name='chsFont'>ชื่อเครื่องจักร : {}</font>""".format(self.mainmc)
		p = Paragraph(ptext, style=normal)
		p.wrapOn(self.c, self.width, self.height)
		p.drawOn(self.c, *self.coord(-65, 27.5, mm))

		ptext = """<font name='chsFont'>แผนก : {}</font>""".format(self.department)
 
		p = Paragraph(ptext, style=normal)
		p.wrapOn(self.c, self.width, self.height)
		p.drawOn(self.c, *self.coord(73, 27.5, mm))

	#----------------------------------------------------------------------
	def createLineItems(self,datatext):
		"""
		Create the line items
		"""
		pdfmetrics.registerFont(TTFont('chsFont', 'THSarabunNew.ttf'))
		stylesheet = getSampleStyleSheet()

		# container for the "Flowable" objects
		elements = []
		styles=getSampleStyleSheet()
		styleN = styles["Normal"]
		styleT = styles["Title"]


		style_center = ParagraphStyle(name='right', parent=styles['Normal'], fontName='chsFont',
						fontSize=13, alignment=TA_CENTER)
		# styleN.fontSize = 15
		# styleN.alignment=TA_JUSTIFY

		TH15 = ParagraphStyle(name='TH12', fontName='chsFont', fontSize=15, alignment=TA_JUSTIFY)



		a = Image("logo.png")  
		a.drawHeight = 3*cm
		a.drawWidth = 3*cm

		# Header of Table
		CH1 = Paragraph("<font size=13 name='chsFont'>ลำดับที่</font>", styleT)
		CH2 = Paragraph("<font size=13 name='chsFont'>กิจกรรม</font>", styleT)
		CH3 = Paragraph("<font size=13 name='chsFont'>จุดประสงค์</font>", styleT)
		CH4 = Paragraph("<font size=13 name='chsFont'>วิธีทำ</font>", styleT)
		CH5 = Paragraph("<font size=13 name='chsFont'>ความถี่ทำ PM</font>", styleT)
		CH6 = Paragraph("<font size=13 name='chsFont'>เวลาทำ PM</font>", styleT)
		CH7 = Paragraph("<font size=13 name='chsFont'>สภาวะเดิน/หยุด</font>", styleT)
		CH8 = Paragraph("<font size=13 name='chsFont'>ดำเนินการโดย</font>", styleT)

		data = [[CH1,CH2,CH3,CH4,CH5,CH6,CH7,CH8]]
		#data = [[CH1,CH2,CH3,a,CH5,CH6,CH7]]


		# Data of Table
		textlist = datatext
		#[['1','','/','แผ่นเจียร์ยาว 4 นิ้ว'],[2,'/','','ลวดเชื่อม']]

		count = len(textlist)

		for i in range(count):
			t1 = Paragraph("<font name='chsFont'>{}</font>".format(textlist[i][0]),styleN)
			t2 = Paragraph("<font name='chsFont'>{}</font>".format(textlist[i][1]),styleN)
			t3 = Paragraph("<font name='chsFont'>{}</font>".format(textlist[i][2]),styleN)
			t4 = Paragraph("<font name='chsFont'>{}</font>".format(textlist[i][3]),styleN)
			t5 = Paragraph("<font name='chsFont'>{}</font>".format(textlist[i][4]),styleN)
			t6 = Paragraph("<font name='chsFont'>{}</font>".format(textlist[i][5]),styleN)
			t7 = Paragraph("<font name='chsFont'>{}</font>".format(textlist[i][6]),styleN)
			t8 = Paragraph("<font name='chsFont'>{}</font>".format(textlist[i][7]),styleN)
			
			data.append([t1,t2,t3,t4,t5,t6,t7,t8])

		lineoftable = 36
		count2 = len(data)
		countf = lineoftable - count2

		for i in range(countf):
			blank = ['','','','','','','','']

			if count < lineoftable:
				data.append(blank)
			else:
				pass
 
		tableThatSplitsOverPages = Table(data, [1.4 * cm, 2.5 * cm, 2.5 * cm, 4.6 * cm, 1.3 * cm, 1.5 * cm, 2 * cm, 2.2 * cm], repeatRows=1)

		tableThatSplitsOverPages.hAlign = 'RIGHT'

		tblStyle = TableStyle([('TEXTCOLOR',(0,0),(-1,-1),colors.black),
							   ('VALIGN',(0,0),(-1,-1),'TOP'),
							   ('LINEBELOW',(0,0),(-1,-1),1,colors.black),
							   ('BOX',(0,0),(-1,-1),1,colors.black),
							   ('BOX',(0,0),(0,-1),1,colors.black)])

		style2 = TableStyle([  ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
								('VALIGN',(0,0),(0,-1),'TOP'),
							   ('ALIGN',(0,0),(-1,-1),'CENTER'),
							   ('VALIGN',(0,0),(-1,-1),'TOP'), 
							   ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
							   ('BOX', (0,0), (-1,-1), 1, colors.black),
							   ])
		# ('SPAN') is a combine (0,0),(1,1) column x=0 to x=1 y=0 to y=1 is row 0 to row 1
		# tblStyle.add('BACKGROUND',(0,0),(1,0),colors.white)
		# tblStyle.add('BACKGROUND',(0,1),(-1,-1),colors.white)

		tableThatSplitsOverPages.setStyle(style2)
 
		self.story.append(tableThatSplitsOverPages)



class Report2(object):
	""""""
 
	#----------------------------------------------------------------------
	def __init__(self,date='2018-05-02', dp='Maintenance', mc='Wood pallet 1'):
		"""Constructor"""
		self.width, self.height = landscape(A4)
		self.styles = getSampleStyleSheet()
		self.datefromsql = date
		self.department = dp
		self.mainmc = mc
		
	#----------------------------------------------------------------------
	def coord(self, x, y, unit=1):
		"""
		http://stackoverflow.com/questions/4726011/wrap-text-in-a-table-reportlab
		Helper class to help position flowables in Canvas objects
		"""
		x, y = x * unit, self.height -  y * unit
		return x, y
 
	#----------------------------------------------------------------------
	def run(self,filename,data):
		"""
		Run the report
		"""
		self.doc = SimpleDocTemplate(filename,pagesize=landscape(A4), rightMargin=30,leftMargin=30, topMargin=50,bottomMargin=18)
		self.story = [Spacer(1, 1*cm)]
		self.createLineItems(data)
 
		self.doc.build(self.story, onFirstPage=self.createDocument)
		print ("finished!")
 
	#----------------------------------------------------------------------
	def createDocument(self, canvas, doc):
		"""
		Create the document
		"""
		pdfmetrics.registerFont(TTFont('chsFont', 'THSarabunNew.ttf'))

		self.c = canvas
		normal = self.styles["Title"]
 
		header_text = "<font name='chsFont'><b>THE ENERGY CO.,LTD</b></font>"
		p = Paragraph(header_text, normal)
		p.wrapOn(self.c, self.width, self.height)
		p.drawOn(self.c, *self.coord(0, 12, mm))
 
		ptext = """<font name='chsFont'>ประวัติการบำรุงรักษาเครื่องจักร</font>"""
 
		p = Paragraph(ptext, style=normal)
		p.wrapOn(self.c, self.width, self.height)
		p.drawOn(self.c, *self.coord(0, 20, mm))

		ptext = """<font name='chsFont'>ชื่อเครื่องจักร : {}</font>""".format(self.mainmc)
		p = Paragraph(ptext, style=normal)
		p.wrapOn(self.c, self.width, self.height)
		p.drawOn(self.c, *self.coord(0, 27.5, mm))

	#----------------------------------------------------------------------
	def createLineItems(self,datatext):
		"""
		Create the line items
		"""
		pdfmetrics.registerFont(TTFont('chsFont', 'THSarabunNew.ttf'))
		stylesheet = getSampleStyleSheet()

		# container for the "Flowable" objects
		elements = []
		styles=getSampleStyleSheet()
		styleN = styles["Normal"]
		styleT = styles["Title"]


		style_center = ParagraphStyle(name='right', parent=styles['Normal'], fontName='chsFont',
						fontSize=13, alignment=TA_CENTER)
		# styleN.fontSize = 15
		# styleN.alignment=TA_JUSTIFY

		TH15 = ParagraphStyle(name='TH12', fontName='chsFont', fontSize=15, alignment=TA_JUSTIFY)



		a = Image("logo.png")  
		a.drawHeight = 3*cm
		a.drawWidth = 3*cm

		# Header of Table
		CH1 = Paragraph("<font size=13 name='chsFont'>วันที่</font>", styleT)
		CH2 = Paragraph("<font size=13 name='chsFont'>รายการที่ตรวจสอบ</font>", styleT)
		CH3 = Paragraph("<font size=13 name='chsFont'>สภาพที่ตรวจพบ</font>", styleT)
		CH4 = Paragraph("<font size=13 name='chsFont'>การซ่อมบำรุงแก้ไข</font>", styleT)
		CH5 = Paragraph("<font size=13 name='chsFont'>อะไหล่ อุปกรณ์ที่ใช้</font>", styleT)
		CH6 = Paragraph("<font size=13 name='chsFont'>ค่าใช้จ่าย</font>", styleT)
		CH7 = Paragraph("<font size=13 name='chsFont'>ผู้ปฏิบัติ</font>", styleT)

		data = [[CH1,CH2,CH3,CH4,CH5,CH6,CH7]]
		#data = [[CH1,CH2,CH3,a,CH5,CH6,CH7]]


		# Data of Table
		textlist = datatext
		#[['1','','/','แผ่นเจียร์ยาว 4 นิ้ว'],[2,'/','','ลวดเชื่อม']]

		count = len(textlist)

		for i in range(count):
			t1 = Paragraph("<font name='chsFont'>{}</font>".format(textlist[i][0]),styleN)
			t2 = Paragraph("<font name='chsFont'>{}</font>".format(textlist[i][1]),styleN)
			t3 = Paragraph("<font name='chsFont'>{}</font>".format(textlist[i][2]),styleN)
			t4 = Paragraph("<font name='chsFont'>{}</font>".format(textlist[i][3]),styleN)
			t5 = Paragraph("<font name='chsFont'>{}</font>".format(textlist[i][4]),styleN)
			t6 = Paragraph("<font name='chsFont'>{}</font>".format(textlist[i][5]),styleN)
			t7 = Paragraph("<font name='chsFont'>{}</font>".format(textlist[i][6]),styleN)
			
			data.append([t1,t2,t3,t4,t5,t6,t7])

		lineoftable = 26
		count2 = len(data)
		countf = lineoftable - count2

		for i in range(countf):
			blank = ['','','','','','','']

			if count < lineoftable:
				data.append(blank)
			else:
				pass
 
		tableThatSplitsOverPages = Table(data, [3 * cm, 5 * cm, 4.5 * cm, 4.5 * cm, 4 * cm, 3* cm, 3 * cm], repeatRows=1)

		tableThatSplitsOverPages.hAlign = 'RIGHT'

		tblStyle = TableStyle([('TEXTCOLOR',(0,0),(-1,-1),colors.black),
							   ('VALIGN',(0,0),(-1,-1),'TOP'),
							   ('LINEBELOW',(0,0),(-1,-1),1,colors.black),
							   ('BOX',(0,0),(-1,-1),1,colors.black),
							   ('BOX',(0,0),(0,-1),1,colors.black)])

		style2 = TableStyle([  ('TEXTCOLOR',(0,0),(-1,-1),colors.black),
								('VALIGN',(0,0),(0,-1),'TOP'),
							   ('ALIGN',(0,0),(-1,-1),'CENTER'),
							   ('VALIGN',(0,0),(-1,-1),'TOP'), 
							   ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
							   ('BOX', (0,0), (-1,-1), 1, colors.black),
							   ])
		# ('SPAN') is a combine (0,0),(1,1) column x=0 to x=1 y=0 to y=1 is row 0 to row 1
		# tblStyle.add('BACKGROUND',(0,0),(1,0),colors.white)
		# tblStyle.add('BACKGROUND',(0,1),(-1,-1),colors.white)

		tableThatSplitsOverPages.setStyle(style2)
 
		self.story.append(tableThatSplitsOverPages)



class Report(object):
	def __init__ (self):
		self.width, self.height = A4

	def run(self, pdfname, data1, data2,date,nb0,mc0,dmp0):
		#crete main canvas
		self.c = canvas.Canvas(pdfname, pagesize=A4)

		#call
		self.drawTest(date,nb0,mc0,dmp0)
		self.drawTable1(data1)
		self.drawTable2(data2)
		
		
		#save canvas to pdf
		self.c.save()
		print("create " + pdfname)
#--------------------------------------------------------------------------------------------------------------------------

	def drawTest(self,date,idbd,mc0,dpm0):
		#inifont
		pdfmetrics.registerFont(TTFont('nomalFont', 'THSarabunNew.ttf'))
		pdfmetrics.registerFont(TTFont('boldFont', 'THSarabunNew Bold.ttf'))
		styles=getSampleStyleSheet()
		styleN = styles["Normal"]
		styleT = styles["Title"]

		#top
		ptext = Paragraph("<font size=20 name='boldFont'>บริษัท energy จำกัด</font>", styleT)
		ptext.wrapOn(self.c, self.width, self.height)
		ptext.drawOn(self.c, 0 *mm, 280 *mm)

		ptext = Paragraph("<font size=20 name='boldFont'>energy</font>", styleT)
		ptext.wrapOn(self.c, self.width, self.height)
		ptext.drawOn(self.c, 0 *mm, 270 *mm)

		#table1
		ptext = Paragraph("<font size=15 name='boldFont'>ใบแจ้งซ่อม</font>", styleT)
		ptext.wrapOn(self.c, self.width, self.height)
		ptext.drawOn(self.c, 0 *mm, 248 *mm)

		datereport = "<font size=13 name='boldFont'>วันที่  {}  </font>".format(date)
		number = "<font size=13 name='boldFont'>เลขที่ใบแจ้ง  {}  </font>".format(idbd)
		mc = "<font size=13 name='boldFont'>เครื่องจักร  {}  </font>".format(mc0)
		dpm = "<font size=13 name='boldFont'>แผนก  {}  </font>".format(dpm0)

		ptext = Paragraph(datereport, styleT)
		ptext.wrapOn(self.c, self.width, self.height)
		ptext.drawOn(self.c, -60 *mm, 243 *mm)
		ptext = Paragraph(number, styleT)
		ptext.wrapOn(self.c, self.width, self.height)
		ptext.drawOn(self.c, 40 *mm, 243 *mm)
		
		ptext = Paragraph(mc, styleT)
		ptext.wrapOn(self.c, self.width, self.height)
		ptext.drawOn(self.c, -60 *mm, 238 *mm)
		ptext = Paragraph(dpm, styleT)
		ptext.wrapOn(self.c, self.width, self.height)
		ptext.drawOn(self.c, 40 *mm, 238 *mm)

		ptext = Paragraph("<font size=13 name='boldFont'>ผู้แจ้งซ่อม............................</font>", styleT)
		ptext.wrapOn(self.c, self.width, self.height)
		ptext.drawOn(self.c, -60 *mm, 162 *mm)
		ptext = Paragraph("<font size=13 name='boldFont'>ผู้รับผิดชอบการซ่อม..............................</font>", styleT)
		ptext.wrapOn(self.c, self.width, self.height)
		ptext.drawOn(self.c, 40 *mm, 162 *mm)

		#table2
		ptext = Paragraph("<font size=13 name='boldFont'>เพื่อใช้งาน............................</font>", styleT)
		ptext.wrapOn(self.c, self.width, self.height)
		ptext.drawOn(self.c, -60 *mm, 70 *mm)
		ptext = Paragraph("<font size=13 name='boldFont'>ผู้เบิกวัสดุ..............................</font>", styleT)
		ptext.wrapOn(self.c, self.width, self.height)
		ptext.drawOn(self.c, 40 *mm, 70 *mm)

		ptext = Paragraph("<font size=13 name='boldFont'>เครื่องจักร............................</font>", styleT)
		ptext.wrapOn(self.c, self.width, self.height)
		ptext.drawOn(self.c, -60 *mm, 63 *mm)

		ptext = Paragraph("<font size=13 name='boldFont'>แผนก............................</font>", styleT)
		ptext.wrapOn(self.c, self.width, self.height)
		ptext.drawOn(self.c, -60 *mm, 56 *mm)
		ptext = Paragraph("<font size=13 name='boldFont'>ผู้อนุมัติ..............................</font>", styleT)
		ptext.wrapOn(self.c, self.width, self.height)
		ptext.drawOn(self.c, 40 *mm, 56 *mm)

		#SUM
		ptext = Paragraph("<font size=13 name='boldFont'></font>", styleT)
		ptext.wrapOn(self.c, self.width, self.height)
		ptext.drawOn(self.c, 75 *mm, 80 *mm)
#--------------------------------------------------------------------------------------------------------------------------
	def drawTable1(self, data1):
		#inifont
		pdfmetrics.registerFont(TTFont('nomalFont', 'THSarabunNew.ttf'))
		pdfmetrics.registerFont(TTFont('boldFont', 'THSarabunNew Bold.ttf'))
		stylesheet = getSampleStyleSheet()
		styles=getSampleStyleSheet()
		styleN = styles["Normal"]
		styleT = styles["Title"]

		#Header of table
		CH1 = Paragraph("<font size=13 name='boldFont'>ปัญหาที่เจอ</font>", styleT)
		CH2 = Paragraph("<font size=13 name='boldFont'>สาเหตุ</font>", styleT)
		CH3 = Paragraph("<font size=13 name='boldFont'>แนวทางการแก้ไข</font>", styleT)
		CH4 = Paragraph("<font size=13 name='boldFont'>เวลา</font>", styleT)

		
		data = [['','','',''],['','','',''],['','','',''],
				[CH1,CH2,CH3,CH4]]

		#connect Head and Data
		textlist = data1
		count = len(textlist)
		for i in range(count):
			t1 = Paragraph("<font name='nomalFont'>{}</font>".format(textlist[i][0]),styleN)
			t2 = Paragraph("<font name='nomalFont'>{}</font>".format(textlist[i][1]),styleN)
			t3 = Paragraph("<font name='nomalFont'>{}</font>".format(textlist[i][2]),styleN)
			t4 = Paragraph("<font name='nomalFont'>{}</font>".format(textlist[i][3]),styleN)
			data.append([t1,t2,t3,t4])
			
		#line of table
		lineoftable = 15
		count2 = len(data)
		countf = lineoftable - count2
		for i in range(countf):
			blank = ['','','','']
			if count < lineoftable:
				data.append(blank)
			else:
				pass
			
		#set table
		size = 4.7
		table = Table(data,[size *cm, size*cm, size*cm, size*cm], rowHeights=18)
		table.setStyle(TableStyle([('BOX', (0,0), (-1,-1), 1, colors.black),
								   ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
								   ('ALIGN',(0,0),(-1,-1),'CENTER'),
								   ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
								   ('SPAN',(0,0),(3,2)),
								   ('SPAN',(0,13),(3,14)),
								   ]))
		table.wrapOn(self.c, self.width, self.height)
		table.drawOn(self.c, 10 *mm, 160 *mm)
#--------------------------------------------------------------------------------------------------------------------------
	def drawTable2(self, data2):
	#inifont
		pdfmetrics.registerFont(TTFont('nomalFont', 'THSarabunNew.ttf'))
		pdfmetrics.registerFont(TTFont('boldFont', 'THSarabunNew Bold.ttf'))
		stylesheet = getSampleStyleSheet()
		styles=getSampleStyleSheet()
		styleN = styles["Normal"]
		styleT = styles["Title"]

		#Header of table
		CH1 = Paragraph("<font size=13 name='boldFont'>ใบเบิกวัสดุ</font>", styleT)
		
		CH2 = Paragraph("<font size=13 name='boldFont'>ลำดับ</font>", styleT)
		CH3 = Paragraph("<font size=13 name='boldFont'>รายการ</font>", styleT)
		CH4 = Paragraph("<font size=13 name='boldFont'>หน่วย</font>", styleT)
		CH5 = Paragraph("<font size=13 name='boldFont'>จำนวน</font>", styleT)
		CH6 = Paragraph("<font size=13 name='boldFont'>ราคา/หน่วย</font>", styleT)
		CH7 = Paragraph("<font size=13 name='boldFont'>รวม</font>", styleT)

		data = [[CH1,'','','','',''],
				[CH2,CH3,CH4,CH5,CH6,CH7]]

		#connect Head and Data
		textlist = data2
		count = len(textlist)
		for i in range(count):
			t1 = Paragraph("<font name='nomalFont'>{}</font>".format(textlist[i][0]),styleN)
			t2 = Paragraph("<font name='nomalFont'>{}</font>".format(textlist[i][1]),styleN)
			t3 = Paragraph("<font name='nomalFont'>{}</font>".format(textlist[i][2]),styleN)
			t4 = Paragraph("<font name='nomalFont'>{}</font>".format(textlist[i][3]),styleN)
			t5 = Paragraph("<font name='nomalFont'>{}</font>".format(textlist[i][4]),styleN)
			t6 = Paragraph("<font name='nomalFont'>{}</font>".format(textlist[i][5]),styleN)
			data.append([t1,t2,t3,t4,t5,t6])

		#line of table
		lineoftable = 16
		count2 = len(data)
		countf = lineoftable - count2
		for i in range(countf):
			blank = ['','','','']
			if count < lineoftable:
				data.append(blank)
			else:
				pass
			
		#set table 18.8
		table = Table(data,[1.5 *cm, 7.8*cm, 2*cm, 2*cm, 2*cm, 3.5*cm], rowHeights=18)
		table.setStyle(TableStyle([('BOX', (0,0), (-1,-1), 1, colors.black),
								   ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
								   ('ALIGN',(0,0),(-1,-1),'CENTER'),
								   ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
								   ('SPAN',(0,0),(5,0)),
								   ('SPAN',(0,11),(5,15)),
								   ]))
		table.wrapOn(self.c, self.width, self.height)
		table.drawOn(self.c, 10 *mm, 50 *mm)
#--------------------------------------------------------------------------------------------------------------------------
#############################################################################
global sparelist2
def reportpdf1():

	try:
		ts = sparelist2.selection()
		x = sparelist2.item(ts)
		wd_code4export = x['values'][1]
		print('-------------------------------------')
		print(wd_code4export)

	except:
		wd_code4export = '001'
		
		

	#sparelist_mc4
	

	datatopdf = []
	
	with conn:
		c.execute("""SELECT * FROM breakdown_list WHERE bd_code = (:id)""",{'id':wd_code4export})
		wd_list = c.fetchall()
	conn.commit()
	print(wd_list)


	for i in wd_list:
		reportdata = [i[5],i[6],i[7],i[8]]
		dateofreport = i[2]
		datatopdf.append(reportdata)
		dt0 = i[1]
		nb0 = i[2]
		mc0 = i[3]
		dmp0 = i[4]
	

	print(wd_list)
	print('Success')
	data2 = [['1', 'ลูกปืน 6208 zz', 'ลูก', '1', '252', ' '],['2', 'ลูกปืน 6208', 'ลูก', '1', '194', ' '],['3', 'tc 65-90-10', 'วง', '1', '84', ' ']]
	data = [['น้ำยาหม้อน้ำ','2','ใช้เติมหม้อต้มน้ำสกิมบล็อก'],
			['เทปพันสายไฟ','3','ใช้พันสายไฟเครื่องตีน้ำ'],
			['น้ำยา sonax','2','ใช้ฉีดสนิมโซ่เครน']
	]

	dt1 = datetime.now().strftime('%Y-%m-%d %H%M%S')
	reportname = 'Breakdown-'+dt1+'.pdf'

	Report().run(reportname, datatopdf, data2,dt0,nb0,mc0,dmp0)

	messagebox.showinfo('Report Exporting',reportname + ' was Exported')


def reportpdf2():

	try:
		ts = sparelist_mc4.selection()
		x = sparelist_mc4.item(ts)
		wd_code4export = x['values'][1]
		print('-------------------------------------')
		print(wd_code4export)

	except:
		wd_code4export = '001'
		
		

	#sparelist_mc4
	

	datatopdf = []
	
	with conn:
		c.execute("""SELECT * FROM breakdown_list WHERE bd_code = (:id)""",{'id':wd_code4export})
		wd_list = c.fetchall()
	conn.commit()
	print(wd_list)


	for i in wd_list:
		reportdata = [i[5],i[6],i[7],i[8]]
		dateofreport = i[2]
		datatopdf.append(reportdata)
		dt0 = i[1]
		nb0 = i[2]
		mc0 = i[3]
		dmp0 = i[4]
	

	print(wd_list)
	print('Success')
	data2 = [['1', 'ลูกปืน 6208 zz', 'ลูก', '1', '252', ' '],['2', 'ลูกปืน 6208', 'ลูก', '1', '194', ' '],['3', 'tc 65-90-10', 'วง', '1', '84', ' ']]
	data = [['น้ำยาหม้อน้ำ','2','ใช้เติมหม้อต้มน้ำสกิมบล็อก'],
			['เทปพันสายไฟ','3','ใช้พันสายไฟเครื่องตีน้ำ'],
			['น้ำยา sonax','2','ใช้ฉีดสนิมโซ่เครน']
	]

	
	

	
	dt1 = datetime.now().strftime('%Y-%m-%d %H%M%S')
	reportname = 'Breadown-'+dt1+'.pdf'

	Report().run(reportname, datatopdf, data2,dt0,nb0,mc0,dmp0)

	messagebox.showinfo('Report Exporting',reportname + ' was Exported')

def reportpdf3():

	try:
		ts = allbreakdowntreeview.selection()
		x = allbreakdowntreeview.item(ts)
		wd_code4export = x['values'][1]
		print('-------------------------------------')
		print(wd_code4export)

	except:
		wd_code4export = '001'
		

	#sparelist_mc4
	

	datatopdf = []
	
	with conn:
		c.execute("""SELECT * FROM breakdown_list WHERE bd_code = (:id)""",{'id':wd_code4export})
		wd_list = c.fetchall()
	conn.commit()
	print(wd_list)


	for i in wd_list:
		reportdata = [i[5],i[6],i[7],i[8]]
		dateofreport = i[2]
		datatopdf.append(reportdata)
		dt0 = i[1]
		nb0 = i[2]
		mc0 = i[3]
		dmp0 = i[4]
	

	print(wd_list)
	print('Success')
	#data2 = [['1', 'ลูกปืน 6208 zz', 'ลูก', '1', '252', ' '],['2', 'ลูกปืน 6208', 'ลูก', '1', '194', ' '],['3', 'tc 65-90-10', 'วง', '1', '84', ' ']]
	data2 = [['', '', '', '', '', ' '],['', '', '', '', '', ' '],['', '', '', '', '', '']]
	data = [[' ',' ',' '],[' ',' ',' '],['   ',' ',' ']]

	
	

	
	dt1 = datetime.now().strftime('%Y-%m-%d %H%M%S')
	reportname = 'Breadown-'+dt1+'.pdf'

	Report().run(reportname, datatopdf, data2,dt0,nb0,mc0,dmp0)
	subprocess.Popen(reportname,shell=True)
	messagebox.showinfo('Report Exporting',reportname + ' was Exported')


def reportpdf4():

	try:
		ts = sparelist_mc2.selection()
		x = sparelist_mc2.item(ts)
		wd_code4export = x['values'][1]
		print('-------------------------------------')
		print(wd_code4export)

	except:
		wd_code4export = '001'
		
		

	#sparelist_mc4
	

	datatopdf = []
	
	with conn:
		c.execute("""SELECT * FROM breakdown_list WHERE bd_code = (:id)""",{'id':wd_code4export})
		wd_list = c.fetchall()
	conn.commit()
	print(wd_list)


	for i in wd_list:
		reportdata = [i[5],i[6],i[7],i[8]]
		dateofreport = i[2]
		datatopdf.append(reportdata)
		dt0 = i[1]
		nb0 = i[2]
		mc0 = i[3]
		dmp0 = i[4]
	

	print(wd_list)
	print('Success')

	#data2 = [['1', 'ลูกปืน 6208 zz', 'ลูก', '1', '252', ' '],['2', 'ลูกปืน 6208', 'ลูก', '1', '194', ' '],['3', 'tc 65-90-10', 'วง', '1', '84', ' ']]
	data2 = [['', '', '', '', '', ' '],['', '', '', '', '', ' '],['', '', '', '', '', '']]
	
	data = [['น้ำยาหม้อน้ำ','2','ใช้เติมหม้อต้มน้ำสกิมบล็อก'],
			['เทปพันสายไฟ','3','ใช้พันสายไฟเครื่องตีน้ำ'],
			['น้ำยา sonax','2','ใช้ฉีดสนิมโซ่เครน']
	]

	
	

	
	dt1 = datetime.now().strftime('%Y-%m-%d %H%M%S')
	reportname = 'Breadown-'+dt1+'.pdf'

	Report().run(reportname, datatopdf, data2,dt0,nb0,mc0,dmp0)

	messagebox.showinfo('Report Exporting',reportname + ' was Exported')
#-------------------------------------------------------------
global conn
global c





dbname = 'DB2-Maintenance2.db'
conn = sqlite3.connect(dbname)
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS breakdown_list (
			ID INTEGER PRIMARY KEY AUTOINCREMENT ,
			 bd_date text,
			 bd_code text,
			 bd_machine text,
			 bd_department text,

			 bd_problem text,
			 bd_reason text,
			 bd_method text,
			 bd_time text,

			 bd_reportby text,
			 bd_responsible text
			
			)""")

c.execute("""CREATE TABLE IF NOT EXISTS breakdown_part (
			ID INTEGER PRIMARY KEY AUTOINCREMENT ,
			 
			 bdp_code text,
			 bdp_unit text,
			 bdp_quantity integer,
			 bdp_price real,
			 bdp_total real,
			 
			 bdp_forwork text,
			 bdp_machine text,
			 bdp_department text,

			 bdp_withdrawby text,
			 bdp_approved text
			
			)""")

c.execute("""CREATE TABLE IF NOT EXISTS breakdown_work (
			ID INTEGER PRIMARY KEY AUTOINCREMENT ,
			 
			 bdw_machine text,
			 bdw_code text,
			 bdw_date text,
			 bdw_bd_problem text,
			 bdw_bd_reason text,
			 bdw_bd_method text,
			 
			 bdw_bdp_code text,
			 bdw_bdp_part text,
			 bdw_workby text
			 
			)""")

c.execute("""CREATE TABLE IF NOT EXISTS machine_part (
			ID INTEGER PRIMARY KEY AUTOINCREMENT ,
			 
			 mcp_code text,
			 mcp_machine text,
			 mcp_model text,
			 mcp_cycletime integer,
			 mcp_lastmaintenance text
			 
			)""")

c.execute("""CREATE TABLE IF NOT EXISTS stock_part (
			ID INTEGER PRIMARY KEY AUTOINCREMENT ,
			 
			 stp_mcp_code text,
			 stp_mcp_machine text,
			 stp_unit text,
			 stp_quantity integer,
			 stp_price real,
			 stp_reorderpoint integer,
			 stp_suplier text
			 
			)""")

def viewsparepart():

	VSP_GUI = Toplevel()
	VSP_GUI.title('All Sparepart')

	

	

	def update_sp():
		

		with conn:
			c.execute("""SELECT * FROM stock_part""")
			sp_list4 = c.fetchall()

		conn.commit()
		print(sp_list4)
		print('Success')

		try:
			x = sparelist_mc4.get_children()
			count = len(x)
			for z in range(count):
				sparelist_mc4.delete(x[z])
				
		except:
			pass

		print(sp_list4)

		for it in sp_list4:
			sparelist_mc4.insert('','end',values=it[1:])


	breakdown_header5= ['รหัส','ชื่ออะไหล่','หน่วย','จำนวน','ราคา', 'จุดสั่งซื้อ','ผู้ขาย']

	sparelist_width5 = [(80,100),(80,150),(80,100),(80,100),(80,100),(80,100),(80,200)]

	sparelist_mc4 = ttk.Treeview(VSP_GUI,columns=breakdown_header5, show="headings", height=20)
	for i,col in enumerate(breakdown_header5):
		sparelist_mc4.heading(col, text=col.title())
		sparelist_mc4.column(col,minwidth=sparelist_width5[i][0],width=sparelist_width5[i][1])

	sparelist_mc4.pack(fill=BOTH)


	style = ttk.Style()
	style.configure("Treeview.Heading", font=('TH Sarabun New', 13, 'bold'))
	style.configure("Treeview", font=('TH Sarabun New', 13))


	udb5 = ttk.Button(VSP_GUI, text='Update',command=update_sp).pack(pady=5,padx=5)
	


	VSP_GUI.mainloop()


def addsparepart():
	SPGUI = Toplevel()
	SPGUI.title('บันทึกอะไหล่')
	#SPGUI.geometry('3000x400')
	#-----------------------------
	ESTP_code_s = StringVar()
	BSTP_code = ttk.Label(SPGUI,text='รหัส',font=('TH Sarabun New',15)).grid(row=0,column=0,padx=10,pady=10)
	ESTP_code = ttk.Entry(SPGUI,textvariable=ESTP_code_s,font=('TH Sarabun New',15)).grid(row=0,column=1)
	#-----------------------------
	BSTP_machine_s = StringVar()
	BSTP_machine = ttk.Label(SPGUI,text='ชื่ออะไหล่',font=('TH Sarabun New',15)).grid(row=1,column=0)
	BSTP_machine = ttk.Entry(SPGUI,textvariable=BSTP_machine_s,font=('TH Sarabun New',15)).grid(row=1,column=1,padx=10,pady=10)
	#-----------------------------
	BSTP_hours_s = StringVar()
	BSTP_hours = ttk.Label(SPGUI, text='')

	#-----------------------------
	BSTP_unit_s = StringVar()
	BSTP_unit = ttk.Label(SPGUI,text='หน่วย',font=('TH Sarabun New',15)).grid(row=2,column=0)
	BSTP_unit = ttk.Entry(SPGUI,textvariable=BSTP_unit_s,font=('TH Sarabun New',15)).grid(row=2,column=1,padx=10,pady=10)
	#-----------------------------
	BSTP_price_s = StringVar()
	BSTP_price = ttk.Label(SPGUI,text='ราคา',font=('TH Sarabun New',15)).grid(row=3,column=0)
	BSTP_price = ttk.Entry(SPGUI,textvariable=BSTP_price_s,font=('TH Sarabun New',15)).grid(row=3,column=1,padx=10,pady=10)
	#-----------------------------
	BSTP_quantity_s = StringVar()
	BSTP_quantity = ttk.Label(SPGUI,text='จำนวน',font=('TH Sarabun New',15)).grid(row=4,column=0)
	BSTP_quantity = ttk.Entry(SPGUI,textvariable=BSTP_quantity_s,font=('TH Sarabun New',15)).grid(row=4,column=1,padx=10,pady=10)
	#-----------------------------
	BSTP_reorderpoint_s = StringVar()
	BSTP_reorderpoint = ttk.Label(SPGUI,text='จุดสั่งซื้อ',font=('TH Sarabun New',15)).grid(row=5,column=0)
	BSTP_reorderpoint = ttk.Entry(SPGUI,textvariable=BSTP_reorderpoint_s,font=('TH Sarabun New',15)).grid(row=5,column=1,padx=10,pady=10)
	#-----------------------------
	BSTP_suplier_s = StringVar()
	BSTP_suplier = ttk.Label(SPGUI,text='ผู้ขาย',font=('TH Sarabun New',15)).grid(row=6,column=0)
	BSTP_suplier = ttk.Entry(SPGUI,textvariable=BSTP_suplier_s,font=('TH Sarabun New',15)).grid(row=6,column=1,padx=10,pady=10)

	'''
	ID INTEGER PRIMARY KEY AUTOINCREMENT ,
				 
				 stp_mcp_code text,
				 stp_mcp_machine text,
				 stp_unit text,
				 stp_quantity integer,
				 stp_price real,
				 stp_reorderpoint integer,
				 stp_suplier text

	'''

	def Sparepart_record():

		with conn:
			c.execute("INSERT INTO stock_part VALUES(?,?,?,?,?,?,?,?)",(
				None,ESTP_code_s.get(),
				BSTP_machine_s.get(),
				BSTP_unit_s.get(),
				int(BSTP_quantity_s.get()),
				float(BSTP_price_s.get()),
				int(BSTP_reorderpoint_s.get()),
				BSTP_suplier_s.get() ))
			conn.commit()
		messagebox.showinfo('บันทึกสำเร็จ','เพิ่มอะไหล่เข้าระบบสำเร็จ')

	BSTP_Button = ttk.Button(SPGUI, text='บันทึกรายการ', command=Sparepart_record).grid(row=7,column=1,padx=10,pady=10)


	SPGUI.mainloop()


c.execute("""CREATE TABLE IF NOT EXISTS supplier (
			ID INTEGER PRIMARY KEY AUTOINCREMENT ,
			 
			 spr_code text,
			 spr_name text,
			 spr_address text,
			 spr_email text,
			 spr_tel text

			 
			)""")
conn.commit()
#-------------------------DEF-----------------------

global problemlist

problemlist = []

def insert_breakdown():

	with conn:
		c.execute("""SELECT count(DISTINCT bd_code) from breakdown_list""")
		countcode = c.fetchall()
		print("COUNT in Table",countcode)

		if countcode[0][0] < 10:
			bd_codedb = '100'+str(countcode[0][0])
		elif countcode[0][0] <100:
			bd_codedb = '10'+str(countcode[0][0])
		else:
			bd_codedb = '1'+str(countcode[0][0])

	bd_code.set(bd_codedb)

	def confirm(event=None):

		with conn:

			for i in problemlist:
				c.execute("""INSERT INTO breakdown_list VALUES (
					:ID,\
					:bd_date,\
					:bd_code,\
					:bd_machine,\
					:bd_department,\
					:bd_problem,\
					:bd_reason,\
					:bd_method,\
					:bd_time,\
					:bd_reportby,\
					:bd_responsible
					
					)""",
					{'ID':None,
					'bd_date':bd_date.get(),
					'bd_code':bd_codedb,
					'bd_machine':bd_machine.get(),
					'bd_department':bd_department.get(),
					'bd_problem':i[0],
					'bd_reason':i[1],
					'bd_method':i[2],
					'bd_time':i[3],
					'bd_reportby':bd_reportby.get(),
					'bd_responsible':bd_responsible.get()
					}
					)


		conn.commit()
		print('Success')

	def cancel():
		pass

	x = messagebox.askyesno('บันทึกข้อมูล','ต้องการบันทึกข้อมูลใช่หรือไม่')
	if x == True:
		confirm()
	else:
		messagebox.showinfo('ยังไม่บันทึก','ระบบยังไม่บันทึกข้อมูล')

def expxl():
	pass


def addproblem():

	def updateintreeview():
		data = [pb.get(),rs.get(),mt.get(),tm.get()]
		bd_list.insert('','end',values=data)
		problemlist.append(data)
		print(problemlist)

	GUI_Addproblem = Toplevel()
	GUI_Addproblem.geometry('400x400+10+10')

	LT1 = ['ปัญหาที่เจอ','สาเหตุ','แนวทางแก้ไข','เวลา']

	BDF0 = LabelFrame(GUI_Addproblem, text='ใบแจ้งซ่อม', width=20,font=('TH Sarabun New',15)) #Break down Frame1
	BDF0.pack(pady=5,padx=5)

	for i,j in enumerate(LT1):
		L1 = ttk.Label(BDF0, text=j,font=('TH Sarabun New',15))
		L1.grid(row=i, column=0,pady=5,padx=5,sticky='nw')


	pb = StringVar()
	rs = StringVar()
	mt = StringVar()
	tm = StringVar()


	Eproblem = ttk.Entry(BDF0, textvariable=pb,font=('TH Sarabun New',15)).grid(row=0, column=1,pady=5,padx=5,sticky='nw')
	Ereason = ttk.Entry(BDF0, textvariable=rs,font=('TH Sarabun New',15)).grid(row=1, column=1,pady=5,padx=5,sticky='nw')
	Emethod = ttk.Entry(BDF0, textvariable=mt,font=('TH Sarabun New',15)).grid(row=2, column=1,pady=5,padx=5,sticky='nw')
	Etime = ttk.Entry(BDF0, textvariable=tm,font=('TH Sarabun New',15)).grid(row=3, column=1,pady=5,padx=5,sticky='nw')

	Badd = ttk.Button(BDF0, text='Add', command= updateintreeview).grid(row=4, column=1,pady=5,padx=5)

	GUI_Addproblem.mainloop()


#---------------------------------------------------

GUI = Tk()
GUI.state('zoomed')
GUI.geometry('600x600+30+30')
GUI.title('energy')



f = tkFont.Font(family='TH Sarabun New', size=15)
s = ttk.Style()
s.configure('.', font=f)
combofont=('TH Sarabun New', '15')
GUI.option_add('*TCombobox*Listbox.font', combofont)
s = ttk.Style()
s.configure('my.TButton', font=('TH Sarabun New', 15))
style = ttk.Style()
style.configure("Treeview.Heading", font=('TH Sarabun New', 15, 'bold'))
style.configure("Treeview", font=('TH Sarabun New', 15))

##################3




###################

class BT:

	def __init__(self,gui,text,cm,rw,cl):
		self.text = text
		self.gui = gui
		self.cm = cm
		self.rw = rw
		self.cl = cl
		self.BT1()

	def BT1(self):
		B = ttk.Button(self.gui,text=self.text,command=eval(self.cm))
		B.grid(row=self.rw, column=self.cl,padx=5,pady=5,ipadx=10,ipady=10)


class LB:

	def __init__(self,gui,text,rw,cl,st):
		self.text = text
		self.gui = gui
		self.text = text
		self.rw = rw
		self.cl = cl
		self.st = st
		self.LB1()

	def LB1(self):
		L = ttk.Label(self.gui,text=self.text,font=('TH Sarabun New',15))
		L.grid(row=self.rw, column=self.cl,padx=5,pady=5,sticky=self.st)


class ET:

	def __init__(self,gui,textv,rw,cl,st):
		self.gui = gui
		self.text = textv
		self.rw = rw
		self.cl = cl
		self.st = st
		self.ET1()



	def ET1(self):
		self.E = ttk.Entry(self.gui,textvariable=self.text,font=('TH Sarabun New',15),width=22)
		self.E.grid(row=self.rw, column=self.cl,padx=5,pady=5,sticky=self.st)

	def focus1(self):
		self.E.focus()

class CB:

	def __init__(self,gui,itemlist,rw,cl,st):
		self.gui = gui
		self.itemlist = itemlist
		self.rw = rw
		self.cl = cl
		self.st = st
		self.sp_type = None
		self.CB1()

	

	def CB1(self):
		#SPAD_type = ['อะไหล่','วัสดุสิ้นเปลือง']
		combofont=('TH Sarabun New', '15')
		GUI.option_add('*TCombobox*Listbox.font', combofont)

		self.sp_type = ttk.Combobox(self.gui, values = self.itemlist, font=('TH Sarabun New', 15))
		self.sp_type.set(self.itemlist[0])
		self.sp_type.grid(row=self.rw, column=self.cl,padx=5,pady=5,sticky=self.st)
	
	def gets(self):
		self.sp_type.get()

# -----------------------------Create Table------------------------------

c.execute(""" CREATE TABLE IF NOT EXISTS department (

				ID INTEGER PRIMARY KEY AUTOINCREMENT,
				dep_code text,
				dep_name text

		  )	""")

c.execute(""" CREATE TABLE IF NOT EXISTS linepd (

				ID INTEGER PRIMARY KEY AUTOINCREMENT,
				line_code text,
				line_name text

		  )	""")

c.execute(""" CREATE TABLE IF NOT EXISTS machine (

				ID INTEGER PRIMARY KEY AUTOINCREMENT,
				machine_code text,
				machine_line text,
				machine_name text,
				machine_detail int,
				machine_installdate text
		  )	""")


c.execute(""" CREATE TABLE IF NOT EXISTS partlist (

				ID INTEGER PRIMARY KEY AUTOINCREMENT,
				partlist_code text,
				partlist_name text,
				partlist_model text,
				partlist_price real,
				partlist_quantity integer,
				partlist_machine text,
				partlist_supplier text
		  )	""")

c.execute(""" CREATE TABLE IF NOT EXISTS breakdown (

				ID INTEGER PRIMARY KEY AUTOINCREMENT,
				breakdown_code text,
				breakdown_title text,
				breakdown_department text,
				breakdown_machine text,
				breakdown_partlist text,
				breakdown_cost real,
				breakdown_request text,
				breakdown_responsible text,
				breakdown_date text
		  )	""")


c.execute(""" CREATE TABLE IF NOT EXISTS preventive (

				ID INTEGER PRIMARY KEY AUTOINCREMENT,
				preventive_code text,
				preventive_title text,
				preventive_department text,
				preventive_machine text,
				preventive_partlist text,
				preventive_cost real,
				preventive_responsible text,
				preventive_date text
		  )	""")

c.execute(""" CREATE TABLE IF NOT EXISTS officer (

				ID INTEGER PRIMARY KEY AUTOINCREMENT,
				officer_code text,
				officer_name text,
				officer_department text
			
		  )	""")

mach = []

try:

	with conn:
		c.execute("SELECT machine_name FROM machine")
		machs = c.fetchall()

	for i in machs:
		mach.append(i[0])
		mclist.append(i[0])
except:
	pass

menubar = Menu(GUI)
#----------------Menu File > Export to Excel > Exit---------
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label='Export to PDF', command=reportpdf1)
filemenu.add_separator()
filemenu.add_command(label='Upload to Server', command=expxl)
filemenu.add_command(label='Exit', command=GUI.quit)

menubar.add_cascade(label='File', menu=filemenu)
#----------------Menu File > Export to Excel > Exit---------
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label='Bar', command=expxl)
filemenu.add_command(label='Line', command=expxl)
filemenu.add_separator()
filemenu.add_command(label='Graph', command=GUI.quit)

menubar.add_cascade(label='Summary', menu=filemenu)

# Spare Part Menu
sparepartmenu = Menu(menubar, tearoff=0)
sparepartmenu.add_command(label='Add Spare Part', command=addsparepart, accelerator="Ctrl+Q")
sparepartmenu.add_command(label='View Spare Part', command=viewsparepart, accelerator="Ctrl+Q")
menubar.add_cascade(label='Spare Part', menu=sparepartmenu)



GUI.config(menu=menubar)
#---------End of Menubar----------

Tab = Notebook(GUI, height=700)
F0 = Frame(Tab, width=200, height=500)
F11 = Frame(Tab, width=200, height=500)
F2 = Frame(Tab, width=200, height=500)
F3 = Frame(Tab, width=200, height=500)
F4 = Frame(Tab, width=200, height=500)
F5 = Frame(Tab, width=200, height=500)
#---------ADD MORE------------
F6 = Frame(Tab, width=200, height=500)
F7 = Frame(Tab, width=200, height=500)
F8 = Frame(Tab, width=200, height=500)
F9 = Frame(Tab, width=200,height=500)

Tab.add(F0, text='บันทึกใบแจ้งซ่อม')
Tab.add(F11, text='Preventive M/T')
Tab.add(F6, text='แผนก')
Tab.add(F7, text='ไลน์ผลิต')
Tab.add(F8, text='เครื่องจักร')
Tab.add(F9, text='งานซ่อมทั้งหมด')
# Tab.add(F2, text='Wood Pellet MC1')
# Tab.add(F3, text='Wood Pellet MC2')
# Tab.add(F4, text='Wood Pellet MC3')
# Tab.add(F5, text='Wood Pellet MC4')
Tab.pack(fill=BOTH, padx=10, pady=10)

# add machine to list
mach = []
with conn:
	c.execute("SELECT machine_name FROM machine")
	machs = c.fetchall()

for i in machs:
	mach.append(i[0])



###############UPDATE DEP####################
dep = []
global prev_department
def getdepartment1():
	global dep
	dep = []
	with conn:
		c.execute("SELECT dep_name FROM department")
		deps = c.fetchall()
	
	for i in deps:
		dep.append(i[0])


def getdepartment():
	global dep
	dep = []
	with conn:
		c.execute("SELECT dep_name FROM department")
		deps = c.fetchall()
	
	for i in deps:
		dep.append(i[0])

	prev_department = ttk.Combobox(F01, values = dep, font=('TH Sarabun New', 15))
	prev_department.set('Maintenance')
	prev_department.grid(row=2, column=1,padx=5,pady=5, sticky='w')

#############################################
getdepartment1()

LT1 = ['วันที่','เลขที่ใบแจ้ง','เครื่องจักร','แผนก','ผู้แจ้งซ่อม','ผู้รับผิดชอบ','เพิ่มปัญหาที่เจอ']

BDF1 = LabelFrame(F0, text='ใบแจ้งซ่อม', width=20,font=('TH Sarabun New',15)) #Break down Frame1
BDF1.pack(pady=5,padx=5)

for i,j in enumerate(LT1):
	L1 = ttk.Label(BDF1, text=j,font=('TH Sarabun New',15))
	L1.grid(row=i, column=0,pady=5,padx=5,sticky='nw')

bd_code = StringVar()
bd_reportby = StringVar()
bd_responsible =StringVar()
# bd_machine
# bd_department


bd_date = DateEntry(BDF1, width=21, background='blue',foreground='white', borderwidth=2, font=('TH Sarabun New',15)) #*************
bd_date.grid(row=0, column=1,padx=5,pady=5, sticky='w')

BDE_code = ttk.Entry(BDF1, textvariable=bd_code,font=('TH Sarabun New',15),width=22, state='disabled')
BDE_code.grid(row=1, column=1,pady=5,padx=5, sticky='w')

mclist = ('Wood Pellet MC1','Wood Pellet MC2','Wood Pellet MC3','Wood Pellet MC4')

bd_machine = ttk.Combobox(BDF1, values = mach, font=('TH Sarabun New',15)) #*************

bd_machine.grid(row=2, column=1,padx=5,pady=5, sticky='w')

department = ('Wood Pallet','Maintenance')

bd_department = ttk.Combobox(BDF1, values = dep, font=('TH Sarabun New',15)) #*************
bd_department.set("")
bd_department.grid(row=3, column=1,padx=5,pady=5, sticky='w')

BDE_reportby = ttk.Entry(BDF1, textvariable=bd_reportby,font=('TH Sarabun New',15),width=22)
BDE_reportby.grid(row=4, column=1,pady=5,padx=5, sticky='w')

BDE_responsible = ttk.Entry(BDF1, textvariable=bd_responsible,font=('TH Sarabun New',15),width=22)
BDE_responsible.grid(row=5, column=1,pady=5,padx=5, sticky='w')

BT_problem = ttk.Button(BDF1, text='...', width=5, command=addproblem)
BT_problem.grid(row=6, column=1, pady=5,padx=5, sticky='w')

#-------------Treeview---------------
def removeitem(event=None):
	ts = bd_list.selection()
	print(ts)
	#text1 = bd_list.item(ts,'values')
	#print("Hello world", text1[0]) # select code
	try:
		bd_list.delete(ts[0])
	except:
		pass

	try:
		del problemlist[-1]
	except:
		pass
	#Remove in List



breakdown_header= ['ปัญหาที่เจอ', 'สาเหตุ','แนวทางแก้ไข','เวลา']


bd_list = ttk.Treeview(BDF1,columns=breakdown_header, show="headings", height=10)
bd_list.grid(row=1, column=2, pady=5,padx=5, sticky='w', columnspan=4, rowspan=5)
for col in breakdown_header:
	bd_list.heading(col, text=col.title())

bd_list.bind("<Double-1>",removeitem)

# sparelist.pack(fill=BOTH)

# try:
# 	sparelist.bind("<Delete>",deleteitem)
# except:
# 	pass
#sparelist2.bind("<Double-1>",deleteitem)

style = ttk.Style()
style.configure("Treeview.Heading", font=('TH Sarabun New', 13, 'bold'))
style.configure("Treeview", font=('TH Sarabun New', 13))

BD_listlabel = ttk.Label(BDF1, text='รายละเอียดปัญหา',font=('TH Sarabun New', 15,'bold'))
BD_listlabel.grid(row=0, column=2, pady=5,padx=5)

BD_add = ttk.Button(BDF1,text='Add',command=insert_breakdown)
BD_add.grid(row=6, column=5, pady=5,padx=5, sticky='w')


spa_list = []

def sparefix():
	SPF_GUI = Toplevel()
	SPF_GUI.title('เพิ่มอะไหล่สำหรับซ่อมเครื่องจักร')
	#SPF_GUI.geometry('500x500')

	def update_spf():
		

		with conn:
			c.execute("""SELECT * FROM stock_part""")
			sp_list4 = c.fetchall()

		conn.commit()
		print(sp_list4)
		print('Success')

		try:
			x = sparelist_mc4.get_children()
			count = len(x)
			for z in range(count):
				sparelist_mc4.delete(x[z])
				
		except:
			pass

		print(sp_list4)

		for it in sp_list4:
			sparelist_mc4.insert('','end',values=it[1:])


	breakdown_header5= ['รหัส','ชื่ออะไหล่','หน่วย','จำนวน','ราคา', 'จุดสั่งซื้อ','ผู้ขาย']

	sparelist_width5 = [(80,100),(80,150),(80,100),(80,100),(80,100),(80,100),(80,200)]

	sparelist_mc4 = ttk.Treeview(SPF_GUI,columns=breakdown_header5, show="headings", height=10)
	for i,col in enumerate(breakdown_header5):
		sparelist_mc4.heading(col, text=col.title())
		sparelist_mc4.column(col,minwidth=sparelist_width5[i][0],width=sparelist_width5[i][1])

	sparelist_mc4.pack(fill=BOTH)


	style = ttk.Style()
	style.configure("Treeview.Heading", font=('TH Sarabun New', 13, 'bold'))
	style.configure("Treeview", font=('TH Sarabun New', 13))


	def add_to_sparelist_mc4_add():
		quan = int(sp_quantity.get())
		countinlist = len(spa_list)
		
		ts = sparelist_mc4.selection()
		print(ts)


		#texttotv = [countinlist+1,]




	sp_quantity = StringVar()

	Famout = Frame(SPF_GUI)
	Famout.pack()
	Eudb5 = ttk.Entry(Famout,textvariable=sp_quantity).grid(row=0,column=0,pady=5,padx=5)
	udb_add = ttk.Button(Famout, text='เพิ่ม',command=add_to_sparelist_mc4_add).grid(row=0,column=1,pady=5,padx=5)

	udb5 = ttk.Button(Famout, text='Update',command=update_spf).grid(row=0,column=2,pady=5,padx=5)

	
	#-------------------------------------------------------------------

	breakdown_header_add= ['ลำดับ','รายการ','หน่วย','จำนวน','ราคา/หน่วย', 'รวม']

	sparelist_width_add = [(80,100),(80,150),(80,100),(80,100),(80,100),(80,100)]

	sparelist_mc4_add = ttk.Treeview(SPF_GUI,columns=breakdown_header_add, show="headings", height=10)
	for i,col in enumerate(breakdown_header_add):
		sparelist_mc4_add.heading(col, text=col.title())
		sparelist_mc4_add.column(col,minwidth=sparelist_width_add[i][0],width=sparelist_width_add[i][1])

	sparelist_mc4_add.pack(fill=BOTH)


	style = ttk.Style()
	style.configure("Treeview.Heading", font=('TH Sarabun New', 13, 'bold'))
	style.configure("Treeview", font=('TH Sarabun New', 13))

	def add_child():
		pass

	udb6 = ttk.Button(SPF_GUI, text='Add',command=add_child).pack(pady=5,padx=5)

	SPF_GUI.mainloop()

#----------------------------------



def update_mc1():
		with conn:
			c.execute("""SELECT * FROM breakdown_list where bd_machine = 'Wood Pellet MC1'""")
			sp_list4 = c.fetchall()

		conn.commit()
		print(sp_list4)
		print('Success')

		try:
			x = sparelist2.get_children()
			count = len(x)
			for z in range(count):
				sparelist2.delete(x[z])
				
		except:
			pass

		print(sp_list4)

		for it in sp_list4:
			sparelist2.insert('','end',values=it[1:])


breakdown_header2= ['วันที่','เลขที่ใบแจ้ง','เครื่องจักร','แผนก','ปัญหาที่เจอ', 'สาเหตุ','แนวทางแก้ไข','เวลา','ผู้แจ้งซ่อม','ผู้รับผิดชอบ']

sparelist_width2 = [(20,40),(30,50),(50,120),(50,70),(30,50),(30,50),(30,60),(30,50),(30,70),(30,70),(30,70),(30,70)]

sparelist2 = ttk.Treeview(F2,columns=breakdown_header2, show="headings", height=20)
for i,col in enumerate(breakdown_header2):
	sparelist2.heading(col, text=col.title())
	sparelist2.column(col,minwidth=sparelist_width2[i][0],width=sparelist_width2[i][1])

sparelist2.pack(fill=BOTH)


style = ttk.Style()
style.configure("Treeview.Heading", font=('TH Sarabun New', 13, 'bold'))
style.configure("Treeview", font=('TH Sarabun New', 13))


udb = ttk.Button(F2, text='Update',command=update_mc1).pack(pady=5,padx=5)


#----------------------------------

def update_mc3():
		with conn:
			c.execute("""SELECT * FROM breakdown_list where bd_machine = 'Wood Pellet MC2'""")
			sp_list4 = c.fetchall()

		conn.commit()
		print(sp_list4)
		print('Success')

		try:
			x = sparelist_mc2.get_children()
			count = len(x)
			for z in range(count):
				sparelist_mc2.delete(x[z])
				
		except:
			pass

		print(sp_list4)

		for it in sp_list4:
			sparelist_mc2.insert('','end',values=it[1:])


breakdown_header3= ['วันที่','เลขที่ใบแจ้ง','เครื่องจักร','แผนก','ปัญหาที่เจอ', 'สาเหตุ','แนวทางแก้ไข','เวลา','ผู้แจ้งซ่อม','ผู้รับผิดชอบ']

sparelist_width3 = [(20,40),(30,50),(50,120),(50,70),(30,50),(30,50),(30,60),(30,50),(30,70),(30,70),(30,70),(30,70)]

sparelist_mc2 = ttk.Treeview(F3,columns=breakdown_header3, show="headings", height=20)
for i,col in enumerate(breakdown_header3):
	sparelist_mc2.heading(col, text=col.title())
	sparelist_mc2.column(col,minwidth=sparelist_width3[i][0],width=sparelist_width3[i][1])

sparelist_mc2.pack(fill=BOTH)


style = ttk.Style()
style.configure("Treeview.Heading", font=('TH Sarabun New', 13, 'bold'))
style.configure("Treeview", font=('TH Sarabun New', 13))


udb = ttk.Button(F3, text='Update',command=update_mc3).pack(pady=5,padx=5)
udb = ttk.Button(F3, text='Report',command=reportpdf4).pack(pady=5,padx=5)

#------------------------------------------------------------------------------------------------------
def update_mc4():
		with conn:
			c.execute("""SELECT * FROM breakdown_list where bd_machine = 'Wood Pellet MC3'""")
			sp_list4 = c.fetchall()

		conn.commit()
		print(sp_list4)
		print('Success')

		try:
			x = sparelist_mc3.get_children()
			count = len(x)
			for z in range(count):
				sparelist_mc3.delete(x[z])
				
		except:
			pass

		print(sp_list4)

		for it in sp_list4:
			sparelist_mc3.insert('','end',values=it[1:])


breakdown_header4= ['วันที่','เลขที่ใบแจ้ง','เครื่องจักร','แผนก','ปัญหาที่เจอ', 'สาเหตุ','แนวทางแก้ไข','เวลา','ผู้แจ้งซ่อม','ผู้รับผิดชอบ']

sparelist_width4 = [(20,40),(30,50),(50,120),(50,70),(30,50),(30,50),(30,60),(30,50),(30,70),(30,70),(30,70),(30,70)]

sparelist_mc3 = ttk.Treeview(F4,columns=breakdown_header4, show="headings", height=20)
for i,col in enumerate(breakdown_header4):
	sparelist_mc3.heading(col, text=col.title())
	sparelist_mc3.column(col,minwidth=sparelist_width4[i][0],width=sparelist_width4[i][1])

sparelist_mc3.pack(fill=BOTH)


style = ttk.Style()
style.configure("Treeview.Heading", font=('TH Sarabun New', 13, 'bold'))
style.configure("Treeview", font=('TH Sarabun New', 13))


Fudb = Frame(F4)
Fudb.pack()

udb = ttk.Button(Fudb, text='Add Part',command=sparefix).grid(row=0,column=0,pady=5,padx=5)
udb4 = ttk.Button(Fudb, text='Update',command=update_mc4).grid(row=0,column=1,pady=5,padx=5)
udb = ttk.Button(Fudb, text='Report',command=reportpdf3).grid(row=0,column=2,pady=5,padx=5)


#------------------------------------------------------------------------------------------------------
def update_mc5():
		with conn:
			c.execute("""SELECT * FROM breakdown_list where bd_machine = 'Wood Pellet MC4'""")
			sp_list4 = c.fetchall()

		conn.commit()
		print(sp_list4)
		print('Success')

		try:
			x = sparelist_mc4.get_children()
			count = len(x)
			for z in range(count):
				sparelist_mc4.delete(x[z])
				
		except:
			pass

		print(sp_list4)

		for it in sp_list4:
			sparelist_mc4.insert('','end',values=it[1:])


breakdown_header5= ['วันที่','เลขที่ใบแจ้ง','เครื่องจักร','แผนก','ปัญหาที่เจอ', 'สาเหตุ','แนวทางแก้ไข','เวลา','ผู้แจ้งซ่อม','ผู้รับผิดชอบ']

sparelist_width5 = [(20,40),(30,50),(50,120),(50,70),(30,50),(30,50),(30,60),(30,50),(30,70),(30,70),(30,70),(30,70)]

sparelist_mc4 = ttk.Treeview(F5,columns=breakdown_header5, show="headings", height=20)
for i,col in enumerate(breakdown_header5):
	sparelist_mc4.heading(col, text=col.title())
	sparelist_mc4.column(col,minwidth=sparelist_width5[i][0],width=sparelist_width5[i][1])

sparelist_mc4.pack(fill=BOTH)


style = ttk.Style()
style.configure("Treeview.Heading", font=('TH Sarabun New', 13, 'bold'))
style.configure("Treeview", font=('TH Sarabun New', 13))


udb5 = ttk.Button(F5, text='Update',command=update_mc5).pack(pady=5,padx=5)
udb = ttk.Button(F5, text='Report',command=reportpdf2).pack(pady=5,padx=5)

###############################################################################
###############################################################################
###############################################################################

# TabF0 = Notebook(F11, height=700)

# F01 = Frame(TabF0, width=200, height=500)
# F02 = Frame(TabF0, width=200, height=500)

# TabF0.add(F02, text='แผนงาน')
# TabF0.add(F01, text='บันทึกรายการ')

# TabF0.pack(fill=BOTH, padx=10, pady=10)

#---------------GET DATA FROM DATABASE TO LIST BOX---------------

#dep = ['Maintenance','Production']

global mach_line
def getline():
	global ln
	ln = []
	with conn:
		c.execute("SELECT line_name FROM linepd")
		lines = c.fetchall()
		print(lines)
	
	for i in lines:
		ln.append(i[0])

	print(ln)

	#mach_line = ttk.Combobox(F01, values = ln, font=('TH Sarabun New', 15))
	#mach_line.set('Maintenance')
	#mach_line.grid(row=1, column=1,padx=5,pady=5, sticky='w')
	mach_line['values'] = ln




def getmachine():
	global mach
	global mclist

	mclist = ['Wood Pellet MC1','Wood Pellet MC2','Wood Pellet MC3','Wood Pellet MC4']

	mach = []
	with conn:
		c.execute("SELECT machine_name FROM machine")
		machs = c.fetchall()

	for i in machs:
		mach.append(i[0])
		mclist.append(i[0])

	prev_machine = ttk.Combobox(F01, values = mach, font=('TH Sarabun New', 15))
	prev_machine.set('Machine')
	prev_machine.grid(row=3, column=1,padx=5,pady=5, sticky='w')



	bd_machine = ttk.Combobox(BDF1, values = mach, font=('TH Sarabun New',15)) #*************
	#bd_machine.set('Wood Pellet MC1')
	bd_machine.grid(row=2, column=1,padx=5,pady=5, sticky='w')

	CBAll['values'] = mach
	

updatedropdown = Menu(menubar, tearoff = 0)
updatedropdown.add_command(label='Update Line',command=getline)
updatedropdown.add_command(label='Update Department',command=getdepartment)
updatedropdown.add_command(label='Update Machine',command=getmachine)
menubar.add_cascade(label='Update', menu=updatedropdown)






#---------------GET DATA FROM DATABASE TO LIST BOX (END)---------------
###############################################################################
###############################################################################
###############################################################################

# -----------------------------Tab0-----------------------------

TabF00 = Notebook(F11, height=700)

F01 = Frame(TabF00, width=200, height=500)
F02 = Frame(TabF00, width=200, height=500)
F011 = Frame(TabF00, width=200, height=500)
F53 = Frame(TabF00, width=200, height=500)

TabF00.add(F53, text='รายการบำรุงรักษา')
#TabF00.add(F02, text='แผนงาน')
#TabF00.add(F011, text='แผนงานซ่อมด่วน')
#TabF00.add(F01, text='บันทึกรายการ')
TabF00.pack(fill=BOTH, padx=10, pady=10)

TabF3 = Notebook(F6, height=700)

F31 = Frame(TabF3, width=200, height=500)
F32 = Frame(TabF3, width=200, height=500)

TabF3.add(F32, text='แผนก')
TabF3.add(F31, text='บันทึกรายการ')
TabF3.pack(fill=BOTH, padx=10, pady=10)
# --------------------------------------------
TabF4 = Notebook(F7, height=700)

F41 = Frame(TabF4, width=200, height=500)
F42 = Frame(TabF4, width=200, height=500)

TabF4.add(F42, text='ไลน์ผลิต')
TabF4.add(F41, text='บันทึกรายการ')
TabF4.pack(fill=BOTH, padx=10, pady=10)
# --------------------------------------------
TabF5 = Notebook(F8, height=700)

F51 = Frame(TabF5, width=200, height=500)
F52 = Frame(TabF5, width=200, height=500)

TabF5.add(F52, text='เครื่องจักร')
TabF5.add(F51, text='บันทึกรายการ')

TabF5.pack(fill=BOTH, padx=10, pady=10)

global textcheck
def on_button_3(event):
	

	if event.widget.identify(event.x, event.y) == 'label':
		index = event.widget.index('@%d,%d' % (event.x, event.y))
		textcheck = (event.widget.tab(index, 'text'))
	
	if textcheck == 'เครื่องจักร':
		print('เครื่องจักร')
		updatemach()
		
	if textcheck == 'ไลน์ผลิต':
		updateline()
		print('ไลน์ผลิต')

	if textcheck == 'แผนก':
		updatedep()
		print('แผนก')

	if textcheck == 'Preventive M/T':
		updateprev()
		print('Preventive M/T')


Tab.bind('<1>',on_button_3)

#####################   DETAIL #######################
# -----------------------------Tab0-----------------------------
getdepartment()
print(dep)



global prev_machine


	# break_machine = ttk.Combobox(F11, values = mach, font=('TH Sarabun New', 15))
	# break_machine.set('Machine')
	# break_machine.grid(row=3, column=1,padx=5,pady=5, sticky='w')

# prev_department = ttk.Combobox(F01, values = dep, font=('TH Sarabun New', 15))
# prev_department.set('Maintenance')
# prev_department.grid(row=2, column=1,padx=5,pady=5, sticky='w')


print(mach)


# ------Label and Entry------
PLB1 = LB(F01, "Preventive Code", 0, 0, 'w')
prev_code = StringVar()
PE1 = ET(F01, prev_code, 0, 1, 'w')
PLB2 = LB(F01, "Preventive Title", 1, 0, 'w')
prev_title = StringVar()
PE2 = ET(F01, prev_title, 1, 1, 'w')


PLB3 = LB(F01, "Preventive Department", 2, 0, 'w')

#prev_department = StringVar()
#PE3 = ET(F0, prev_department, 2, 1, 'w')
#gui,itemlist,rw,cl,st

prev_department = ttk.Combobox(F01, values = dep, font=('TH Sarabun New', 15))
prev_department.set('Department')
prev_department.grid(row=2, column=1,padx=5,pady=5, sticky='w')

PLB4 = LB(F01, "Preventive Machine", 3, 0, 'w')
# prev_machine = StringVar()
# PE4 = ET(F01, prev_machine, 3, 1, 'w')
prev_machine = ttk.Combobox(F01, values = mach, font=('TH Sarabun New', 15))
prev_machine.set('Machine')
prev_machine.grid(row=3, column=1,padx=5,pady=5, sticky='w')


#preventive_date
LLB3 = LB(F01, "Date Planing", 4, 0, 'w')
preventive_date = DateEntry(F01, width=18, backgroud='blue', foreground='white',borderwidth=2, font=('TH, Sarabun New',12))
preventive_date.grid(row=4, column=1, padx=5, pady=5, sticky='w')


PLB4 = LB(F01, "Preventive Partlist", 5, 0, 'w')
prev_partlist = StringVar()
PE4 = ET(F01, prev_partlist, 5, 1, 'w')
PLB5 = LB(F01, "Preventive Cost", 6, 0, 'w')
prev_cost = StringVar()
PE5 = ET(F01, prev_cost, 6, 1, 'w')
PLB6 = LB(F01, "Preventive Responsible", 7, 0, 'w')
prev_responsible = StringVar()
PE6 = ET(F01, prev_responsible, 7, 1, 'w')


def add_preventive(event=None):
	print(preventive_date.get())
	def confirm():
		with conn:
			c.execute("""INSERT INTO preventive VALUES (

				:ID,\
				:preventive_code,\
				:preventive_title,\
				:preventive_department,\
				:preventive_machine,\
				:preventive__partlist,\
				:preventive_cost,\
				:preventive_responsible,\
				:preventive_date
				)""",

					  {'ID':None,
						'preventive_code': prev_code.get(),
						'preventive_title': prev_title.get(),
						'preventive_department': prev_department.get(),
						'preventive_machine': prev_machine.get(),
						'preventive__partlist': prev_partlist.get(),
						'preventive_cost': int(prev_cost.get()),
						'preventive_responsible': prev_responsible.get(),
						'preventive_date':preventive_date.get()
					   }
					  )
		conn.commit()
		print('Success')

	def cancel():
		pass

	ok = messagebox.askyesno("ยืนยันการทำรายการ", "ต้องการบันทึกข้อมูลใช่หรือไม่?")
	if ok == True:
		confirm()
	else:
		cancel()

# ------Button------
PB1 = BT(F01, 'Add', 'add_preventive', 8, 1)

#------------------TREEVIEW Preventive--------------------
def updateprev():

	with conn:
		c.execute("""SELECT * FROM preventive""")
		tvplist = c.fetchall()
	conn.commit()
	print(tvplist)
	print('Success')

	try:
		x = TVPrev.get_children()
		count = len(x)
		for z in range(count):
			TVPrev.delete(x[z])
			
	except:
		pass
	print(tvplist)

	for it in tvplist:
		TVPrev.insert('','end',values=it[1:])
# Treview

TVFPrev = Frame(F02, width=200)
TVFPrev.grid(row=8,column=1,pady=20)

TVHPrev= ['รหัส','ชื่อแผนงาน','แผนก','ชื่อเครื่องจักร','รายการวัสดุ','ค่าใช้จ่าย','รับผิดชอบโดย','วันที่']
TVHPW = [(80,80),(200,200),(120,120),(120,120),(250,250),(70,70),(100,100),(80,80)]

#TREEVIEW----------------------

TVPrev = ttk.Treeview(TVFPrev,columns=TVHPrev, show="headings", height=20)
for i,col in enumerate(TVHPrev):
	TVPrev.heading(col, text=col.title())
	TVPrev.column(col,minwidth=TVHPW[i][0],width=TVHPW[i][1],anchor=N)

TVPrev.pack(fill=BOTH)
addtowithdraw = ttk.Button(TVFPrev,text='อัพเดต', style='my.TButton',command=updateprev)
addtowithdraw.pack(padx=5,pady=5)


#--------------WITHDRAW LIST------------------
#wd_approved = (:app) WHERE wd_id = (:code)"



# -----------------------------Tab0 End-----------------------------


# -----------------------------Tab3-----------------------------
# ------Label and Entry------
DLB1 = LB(F31, "Department Code", 0, 0, 'w')
dep_code = StringVar()
DE1 = ET(F31, dep_code, 0, 1, 'w')
DLB2 = LB(F31, "Department Name", 1, 0, 'w')
dep_name = StringVar()
DE2 = ET(F31, dep_name, 1, 1, 'w')


def add_department():
	def confirm():
		with conn:
			c.execute("""INSERT INTO department VALUES (

				:ID,\
				:dep_code,\
				:dep_name
				)""",

					  {'ID':None,
					   'dep_code': dep_code.get(),
					   'dep_name': dep_name.get(),
					   }
					  )
		conn.commit()
		print('Success')

	def cancel():
		pass

	ok = messagebox.askyesno("ยืนยันการทำรายการ", "ต้องการบันทึกข้อมูลใช่หรือไม่?")
	if ok == True:
		confirm()
	else:
		cancel()

# ------Button------
DB1 = BT(F31, 'Add', 'add_department', 2, 1)

# ------------------TREEVIEW Department--------------------
def updatedep():

	with conn:
		c.execute("""SELECT * FROM department""")
		tvdlist = c.fetchall()
	conn.commit()
	print(tvdlist)
	print('Success')

	try:
		x = TVDep.get_children()
		count = len(x)
		for z in range(count):
			TVDep.delete(x[z])

	except:
		pass
	print(tvdlist)

	for it in tvdlist:
		TVDep.insert('','end',values=it[1:])
# Treview

TVFDep = Frame(F32, width=200)
TVFDep.grid(row=8,column=1,pady=20)

TVHDep= ['รหัส','ชื่อแผนก']
TVHDW = [(80,80),(200,200)]

#TREEVIEW----------------------

TVDep = ttk.Treeview(TVFDep,columns=TVHDep, show="headings", height=20)
for i,col in enumerate(TVHDep):
	TVDep.heading(col, text=col.title())
	TVDep.column(col,minwidth=TVHDW[i][0],width=TVHDW[i][1],anchor=N)

TVDep.pack(fill=BOTH)
addtodep = ttk.Button(TVFDep,text='อัพเดต', style='my.TButton',command=updatedep)
addtodep.pack(padx=5,pady=5)
# -----------------------------Tab3 End-----------------------------

# -----------------------------Tab4-----------------------------
# ------Label and Entry------
LLB1 = LB(F41, "Line Code", 0, 0, 'w')
linepd_code = StringVar()
LE1 = ET(F41, linepd_code, 0, 1, 'w')
LLB2 = LB(F41, "Line Name", 1, 0, 'w')
linepd_name = StringVar()
LE2 = ET(F41, linepd_name, 1, 1, 'w')


def add_linepd():
	def confirm():
		with conn:
			c.execute("""INSERT INTO linepd VALUES (

				:ID,\
				:linepd_code,\
				:linepd_name
				)""",

					  {'ID':None,
					   'linepd_code': linepd_code.get(),
					   'linepd_name': linepd_name.get(),
					   }
					  )
		conn.commit()
		print('Success')

	def cancel():
		pass

	ok = messagebox.askyesno("ยืนยันการทำรายการ", "ต้องการบันทึกข้อมูลใช่หรือไม่?")
	if ok == True:
		confirm()
	else:
		cancel()

# ------Button------
LB1 = BT(F41, 'Add', 'add_linepd', 2, 1)

# ------------------TREEVIEW Linepd--------------------
def updateline():

	with conn:
		c.execute("""SELECT * FROM linepd""")
		tvllist = c.fetchall()
	conn.commit()
	print(tvllist)
	print('Success')

	try:
		x = TVLine.get_children()
		count = len(x)
		for z in range(count):
			TVLine.delete(x[z])

	except:
		pass
	print(tvllist)

	for it in tvllist:
		TVLine.insert('','end',values=it[1:])
# Treview

TVFLine = Frame(F42, width=200)
TVFLine.grid(row=8,column=1,pady=20)

TVHLine= ['รหัส','ชื่อไลน์ผลิต']
TVHLW = [(80,80),(200,200)]

#TREEVIEW----------------------

TVLine = ttk.Treeview(TVFLine,columns=TVHLine, show="headings", height=20)
for i,col in enumerate(TVHLine):
	TVLine.heading(col, text=col.title())
	TVLine.column(col,minwidth=TVHLW[i][0],width=TVHLW[i][1],anchor=N)

TVLine.pack(fill=BOTH)
addtoline = ttk.Button(TVFLine,text='อัพเดต', style='my.TButton',command=updateline)
addtoline.pack(padx=5,pady=5)
# -----------------------------Tab4 End-----------------------------


# -----------------------------Tab5-----------------------------
# ------Label and Entry------
MLB1 = LB(F51, "Machine Code", 0, 0, 'w')
mach_code = StringVar()
ME1 = ET(F51, mach_code, 0, 1, 'w')



MLB2 = LB(F51, "Machine Line", 1, 0, 'w')
#prev_line = StringVar()
#ME2 = ET(F51, mach_line, 1, 1, 'w')
mach_line = ttk.Combobox(F51, values = dep, font=('TH Sarabun New', 15))
mach_line.set('Maintenance')
mach_line.grid(row=1, column=1,padx=5,pady=5, sticky='w')


MLB3 = LB(F51, "Machine Name", 2, 0, 'w')
mach_name = StringVar()
ME3 = ET(F51, mach_name, 2, 1, 'w')
MLB4 = LB(F51, "Machine Cycle (Hours)", 3, 0, 'w')
mach_detail = StringVar()
ME4 = ET(F51, mach_detail, 3, 1, 'w')

# mach_instdate = StringVar()
# ME5 = ET(F51, mach_instdate, 4, 1, 'w')

# machine installation_date
MLB5 = LB(F51, "Machine Install Date", 4, 0, 'w')
mach_instdate = DateEntry(F51, width=18, backgroud='blue', foreground='white',borderwidth=2, font=('TH, Sarabun New',12))
mach_instdate.grid(row=4, column=1, padx=5, pady=5, sticky='w')

def add_machine():
	def confirm():
		with conn:
			c.execute("""INSERT INTO machine VALUES (

				:ID,\
				:machine_code,\
				:machine_line,\
				:machine_name,\
				:machine_detail,\
				:machine_installdate
				)""",

					  {'ID':None,
					   'machine_code': mach_code.get(),
					   'machine_line': mach_line.get(),
					   'machine_name': mach_name.get(),
					   'machine_detail': mach_detail.get(),
					   'machine_installdate': mach_instdate.get(),
					   }
					  )
		conn.commit()
		print('Success')

	def cancel():
		pass

	ok = messagebox.askyesno("ยืนยันการทำรายการ", "ต้องการบันทึกข้อมูลใช่หรือไม่?")
	if ok == True:
		confirm()
	else:
		cancel()

# ------Button------
PB1 = BT(F51, 'Add', 'add_machine', 5, 1)

getline()

# ------------------TREEVIEW Machine--------------------
def planing():
	with conn:
		c.execute("""SELECT * FROM machine""")
		tvmalist = c.fetchall()
	print(tvmalist)




def updatemach():

	with conn:
		c.execute("""SELECT * FROM machine""")
		tvmalist = c.fetchall()
	conn.commit()
	print(tvmalist)
	print('Success')

	try:
		x = TVMach.get_children()
		count = len(x)
		for z in range(count):
			TVMach.delete(x[z])

	except:
		pass
	print(tvmalist)

	for it in tvmalist:
		TVMach.insert('','end',values=it[1:])
# Treview

TVFMach = Frame(F52, width=200)
TVFMach.grid(row=8,column=1,pady=20)

TVHMach= ['รหัส','ชื่อไลน์ผลิต','ชื่อเครื่องจักร','ชั่วโมงการทำงาน','วันที่ติดตั้ง']
TVHMaW = [(80,80),(200,200),(120,120),(250,250),(80,80)]

#TREEVIEW----------------------

TVMach = ttk.Treeview(TVFMach,columns=TVHMach, show="headings", height=20)
for i,col in enumerate(TVHMach):
	TVMach.heading(col, text=col.title())
	TVMach.column(col,minwidth=TVHMaW[i][0],width=TVHMaW[i][1],anchor=N)

TVMach.pack(fill=BOTH)
addtomach = ttk.Button(TVFMach,text='อัพเดต', style='my.TButton',command=updatemach)
addtomach.pack(padx=5,pady=5)

planing = ttk.Button(TVFMach,text='แผนประจำปี', style='my.TButton',command=planing)
planing.pack(padx=5,pady=5)
# -----------------------------Tab5 End-----------------------------




###############################################################################
#################### UPDATE FRAME 9 All Breckdwon ###########################
###############################################################################


CBAll = ttk.Combobox(F9, values = mach, font=('TH Sarabun New', 15))

CBAll.pack()




def updateallbreakdown():

		Filter = CBAll.get()

		with conn:
			c.execute("""SELECT * FROM breakdown_list where bd_machine = ?""",([Filter]))
			allbreakdownlist = c.fetchall()

		conn.commit()
		print(allbreakdownlist)
		print('Success')

		try:
			x = allbreakdowntreeview.get_children()
			count = len(x)
			for z in range(count):
				allbreakdowntreeview.delete(x[z])
				
		except:
			pass

		print(allbreakdownlist)

		for it in allbreakdownlist:
			allbreakdowntreeview.insert('','end',values=it[1:])


allbreakdownheader= ['วันที่','เลขที่ใบแจ้ง','เครื่องจักร','แผนก','ปัญหาที่เจอ', 'สาเหตุ','แนวทางแก้ไข','เวลา','ผู้แจ้งซ่อม','ผู้รับผิดชอบ']

allbreakdownheader_w = [(20,40),(30,50),(50,120),(50,70),(30,50),(30,50),(30,60),(30,50),(30,70),(30,70),(30,70),(30,70)]



allbreakdowntreeview = ttk.Treeview(F9,columns=allbreakdownheader, show="headings", height=20)
for i,col in enumerate(allbreakdownheader):
	allbreakdowntreeview.heading(col, text=col.title())
	allbreakdowntreeview.column(col,minwidth=allbreakdownheader_w[i][0],width=allbreakdownheader_w[i][1])

allbreakdowntreeview.pack(fill=BOTH)


style = ttk.Style()
style.configure("Treeview.Heading", font=('TH Sarabun New', 13, 'bold'))
style.configure("Treeview", font=('TH Sarabun New', 13))


Fudb = Frame(F9)
Fudb.pack()

#udb = ttk.Button(F9, text='Add Part',command=sparefix).grid(row=0,column=0,pady=5,padx=5)
udb4 = ttk.Button(Fudb, text='Update',command=updateallbreakdown).grid(row=0,column=1,pady=5,padx=5)
udb = ttk.Button(Fudb, text='Report',command=reportpdf3).grid(row=0,column=2,pady=5,padx=5)
#sparefix
#addspare = ttk.Button(Fudb, text='Add Sparepart..',command=sparefix).grid(row=0,column=3,pady=5,padx=5)


######################Save in to F53 ########################
def updatemachineplan():

	with conn:
		c.execute("""SELECT * FROM machine_plan""")
		datatreeview = c.fetchall()

			
		print(datatreeview)
		print('Success')

	try:
		x = TVProductList.get_children()
		count = len(x)
		for z in range(count):
			TVProductList.delete(x[z])
			
	except:
		pass

	print(datatreeview)

	for it in datatreeview:
		TVProductList.insert('','end',values=it[1:])

def deletemcplan(name):
	with conn:
		c.execute("""DELETE FROM machine_plan WHERE mpm_activity = ?""",([name]))
		conn.commit()
		print('Data was deleted')

def add_machine_plan():
	def confirm():
		with conn:
			c.execute("""INSERT INTO machine_plan VALUES (

				:ID,\
				:mpm_department,\
				:mpm_mcname,\
				:mpm_activity,\
				:mpm_goal,\
				:mpm_method,\
				:mpm_every,\
				:mpm_time,\
				:mpm_status,\
				:mpm_by

				)""",

					  {'ID':None,
					  'mpm_department':mpm_department.get(),
					   'mpm_mcname':mpm_mcname.get(),
					   'mpm_activity':mpm_activity.get(),
					   'mpm_goal':mpm_goal.get(), 
					   'mpm_method':mpm_method.get(), 
					   'mpm_every':mpm_every.get(), 
					   'mpm_time':mpm_time.get(), 
					   'mpm_status':mpm_status.get(),
					   'mpm_by':mpm_by.get()
					   }
					  )
		conn.commit()
		print('Success')

	def cancel():
		pass

	ok = messagebox.askyesno("ยืนยันการทำรายการ", "ต้องการบันทึกข้อมูลใช่หรือไม่?")
	if ok == True:
		confirm()
	else:
		cancel()

	updatemachineplan()


mpm_mcname = StringVar()
mpm_activity = StringVar()
mpm_goal = StringVar()
mpm_method = StringVar()
mpm_every = StringVar()
mpm_time = StringVar()
mpm_status = StringVar()
mpm_by = StringVar()


c.execute("""CREATE TABLE IF NOT EXISTS machine_plan (
			ID INTEGER PRIMARY KEY AUTOINCREMENT ,
			mpm_department text,
			 mpm_mcname text,
			 mpm_activity text,
			 mpm_goal text,
			 mpm_method text,
			 mpm_every text,

			 mpm_time text,
			 mpm_status text,
			 mpm_by text
			
			)""")

MPV = LB(F53, "แผนก", 0, 0, 'w')
MPV0 = LB(F53, "เครื่องจักร", 1, 0, 'w')
MPV1 = LB(F53, "กิจกรรม", 2, 0, 'w')
MPV2 = LB(F53, "จุดประสงค์", 3, 0, 'w')
MPV3 = LB(F53, "วิธีทำ", 4, 0, 'w')
MPV4 = LB(F53, "ความถี่ทำ PM", 5, 0, 'w')
MPV5 = LB(F53, "เวลาทำ PM", 6, 0, 'w')
MPV6 = LB(F53, "สภาวะเดิน/หยุด", 7, 0, 'w')
MPV7 = LB(F53, "ดำเนินการโดย", 8, 0, 'w')

mpm_department = ttk.Combobox(F53, values = dep, font=('TH Sarabun New', 15))
mpm_department.set('')
mpm_department.grid(row=0, column=1,padx=5,pady=5, sticky='w')

mpm_mcname = ttk.Combobox(F53, values = mach, font=('TH Sarabun New', 15))
mpm_mcname.set('')
mpm_mcname.grid(row=1, column=1,padx=5,pady=5, sticky='w')

EMPV1 = ET(F53, mpm_activity, 2, 1, 'w')
EMPV2 = ET(F53, mpm_goal, 3, 1, 'w')
EMPV3 = ET(F53, mpm_method, 4, 1, 'w')
EMPV4 = ET(F53, mpm_every, 5, 1, 'w')
EMPV5 = ET(F53, mpm_time, 6, 1, 'w')

statusmc = ['เดิน','หยุด']

mpm_status = ttk.Combobox(F53, values = statusmc, font=('TH Sarabun New', 15))
mpm_status.set('หยุด')
mpm_status.grid(row=7, column=1,padx=5,pady=5, sticky='w')

EMPV7 = ET(F53, mpm_by, 8, 1, 'w')


MPVB = BT(F53, 'Add', 'add_machine_plan', 9, 1)
#######################3

FTV2 = Frame(F53)
FTV2.place(x=300,y=25)

TVList = LB(FTV2, "รายการซ่อมบำรุงรักษาเชิงป้องกัน", 0, 0, 'w')
#########################################

# data = [['1','เปลี่ยนลูกปืน 1','ซ่อม','ดำเนินงานตามแผน','1000','06.00','เดิน','ชรัมป์'],
	#        ['2','เปลี่ยนลูกปืน 2','ซ่อม','ดำเนินงานตามแผน','1500','12.00','เดิน','โรเบิร์ต'],
	#        ['3','เปลี่ยนลูกปืน 3','ซ่อม','ดำเนินงานตามแผน','2000','18.00','หยุด','บ็อบบี้']]

def selectallpv():
	condition = FReport_CB.get()
	with conn:
		c.execute("SELECT * FROM machine_plan WHERE mpm_mcname = ?",([condition]))
		x = c.fetchall()
		print("All Planing",x)

	data = []
	for i,j in enumerate(x):
		y = [str(i+1)]
		y.extend(list(j[3:]))
		data.append(y)
		machine_name1 = j[2]
		machine_department = j[1]

	print(data)


	dt1 = datetime.now().strftime('%Y-%m-%d %H%M%S')
	t = Report3(dt1, machine_department, machine_name1)
	reportname = 'Preventive-'+dt1+'.pdf'
	t.run(reportname,data)

	messagebox.showinfo('Report','ออก Report สำเร็จ: {}.pdf'.format(dt1))
	subprocess.Popen(reportname,shell=True)


FReport = Frame(F53)
FReport.place(x=500,y=20)

FReport_CB = ttk.Combobox(FReport, values = mach, font=('TH Sarabun New', 15))
FReport_CB.set('Select Machine')
FReport_CB.grid(row=0, column=0,padx=5,pady=5, sticky='w')

FReport_BT = ttk.Button(FReport, text='Preventive Report', command=selectallpv).grid(row=0, column=1,padx=5,pady=5, sticky='w')
#########################################
MPVHeader = ['แผนก','เครื่องจักร','กิจกรรม','จุดประสงค์','วิธีทำ','ความถี่ทำ','เวลาทำ PM','สภาวะเดิน/หยุด','ดำเนินการโดย']
MPVMaxmin = [(20,100),(20,100),(30,150),(50,150),(50,150),(30,80),(30,80),(30,100),(30,100)]

TVProductList = ttk.Treeview(FTV2, height=15, columns=MPVHeader, show='headings')
TVProductList.grid(row=1,column=0,sticky='w',padx=5, pady=5)
#---------Add MPVHeader--------------
for i,col in enumerate(MPVHeader):
	TVProductList.heading(col,text=col.title())
	TVProductList.column(col,minwidth=MPVMaxmin[i][0],width=MPVMaxmin[i][1])


def TVdelete(event=None):

	yesno = messagebox.askyesno('Are You Sure?','คุณต้องการลบข้อมูลใช่หรือไม่?')
	print(type(yesno))

	if yesno == True:

		# tvslect for delete data in treeview
		tvselect = TVProductList.selection()[0]
		# first item is 'I001'
		# why we input index 0 : ('I001',)

		# tvvalue for get values of data in current treeview
		tvvalue = TVProductList.item(TVProductList.selection(),'values')
		print("TV ID",tvselect)
		print(tvvalue)
		#TVProductList.delete('I001')
		TVProductList.delete(tvselect)
		deletemcplan(tvvalue[1])
		updatemachineplan()
	else:
		pass

TVProductList.bind('<Double-1>',TVdelete)


###############CONFIG SCROLL BAR##################
vsb = ttk.Scrollbar(F9, orient="vertical", command=allbreakdowntreeview.yview)
vsb.place(x=GUI.winfo_screenwidth()-40,y=35,height=430)
allbreakdowntreeview.configure(yscrollcommand=vsb.set)
###############CONFIG SCROLL BAR##################



# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()


##############################################################
def deleteitem2(event):
	def delitem():
		
		try:
			ts = TVPrev.selection()
			x = TVPrev.item(ts)
			print(x['values'][0])

			y = messagebox.askyesno('Delete','ลบรายการ {} ใช่หรือไม่?'.format(x['values'][0]))

			
			if y == True:
				with conn:
					c.execute("DELETE FROM preventive WHERE preventive_code = (:code)",{'code':x['values'][0]})
					conn.commit()
				messagebox.showinfo('Success','ลบรายการ {} แล้ว'.format(x['values'][0]))
			else:
				messagebox.showinfo('Cancel','ยกเลิกการลบรายการ {}'.format(x['values'][0]))
		except:
			messagebox.showinfo('Cancel','กรุณาเลือกรายการที่ต้องการลบ')
		
	delitem()
	updateprev()


TVPrev.bind('<Double-1>',deleteitem2)

##############################################################

#tvdlist

def deleteitem3(event):
	def delitem():
		
		try:
			ts = TVDep.selection()
			x = TVDep.item(ts)
			print(x['values'][0])

			y = messagebox.askyesno('Delete','ลบรายการ {} ใช่หรือไม่?'.format(x['values'][0]))

			
			if y == True:
				with conn:
					c.execute("DELETE FROM department WHERE dep_code = (:code)",{'code':x['values'][0]})
					conn.commit()
				messagebox.showinfo('Success','ลบรายการ {} แล้ว'.format(x['values'][0]))
			else:
				messagebox.showinfo('Cancel','ยกเลิกการลบรายการ {}'.format(x['values'][0]))
		except:
			messagebox.showinfo('Cancel','กรุณาเลือกรายการที่ต้องการลบ')
		
	delitem()
	updatedep()


TVDep.bind('<Double-1>',deleteitem3)

##############################################################
#TVLine
def deleteitem4(event):
	def delitem():
		
		try:
			ts = TVLine.selection()
			x = TVLine.item(ts)
			print(x['values'][0])

			y = messagebox.askyesno('Delete','ลบรายการ {} ใช่หรือไม่?'.format(x['values'][0]))

			
			if y == True:
				with conn:
					c.execute("DELETE FROM linepd WHERE line_code = (:code)",{'code':x['values'][0]})
					conn.commit()
				messagebox.showinfo('Success','ลบรายการ {} แล้ว'.format(x['values'][0]))
			else:
				messagebox.showinfo('Cancel','ยกเลิกการลบรายการ {}'.format(x['values'][0]))
		except:
			messagebox.showinfo('Cancel','กรุณาเลือกรายการที่ต้องการลบ')
		
	delitem()
	updateline()


TVLine.bind('<Double-1>',deleteitem4)

##############################################################
#TVMach

def deleteitem5(event):
	def delitem():
		
		try:
			ts = TVMach.selection()
			x = TVMach.item(ts)
			print(x['values'][0])

			y = messagebox.askyesno('Delete','ลบรายการ {} ใช่หรือไม่?'.format(x['values'][0]))

			
			if y == True:
				with conn:
					c.execute("DELETE FROM machine WHERE machine_code = (:code)",{'code':x['values'][0]})
					conn.commit()
				messagebox.showinfo('Success','ลบรายการ {} แล้ว'.format(x['values'][0]))
			else:
				messagebox.showinfo('Cancel','ยกเลิกการลบรายการ {}'.format(x['values'][0]))
		except:
			messagebox.showinfo('Cancel','กรุณาเลือกรายการที่ต้องการลบ')
		
	delitem()
	updatemach()


TVMach.bind('<Double-1>',deleteitem5)

##############################################################





updatemachineplan()

GUI.mainloop()





