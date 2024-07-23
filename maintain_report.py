from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm, mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.pdfgen import canvas

# Add font
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from subprocess import Popen

class Report(object):
    # Constructor
    def __init__(self):
        self.width, self.height = A4
        self.styles = getSampleStyleSheet()
    
    # create PDF file
    def createPDF(self, filename, data):
        self.doc = SimpleDocTemplate(filename, pagesize=A4, leftMargin=30,
                                     rightMargin=30, topMargin=50, bottomMargin=10)
        self.story = [Spacer(1, 1*cm)]
        self.createTable(data)
        self.doc.build(self.story, onFirstPage=self.createDocument)
        print(f"create file : {filename}" )

    def createCoord(self, x, y, unit=1):
        x, y = x * unit, self.height - y * unit
        return x, y
    
    def createDocument(self, canvas, doc):
        pdfmetrics.registerFont(TTFont('normalFont', 'THSarabunNew.ttf'))
        pdfmetrics.registerFont(TTFont('boldFont', 'THSarabunNew Bold.ttf'))

        self.c = canvas
        normal = self.styles["Title"]

        htext = "<font size=18 name='boldFont'>บริษัท อังเคิล เมนเทนแนนซ์ จำกัด</font>"
        h = Paragraph(htext, normal)
        h.wrapOn(self.c, self.width, self.height)
        h.drawOn(self.c, *self.createCoord(0, 12, mm))

        htext = "<font size=18 name='boldFont'>UNCLE MAINTENANCE CO.,LTD</font>"
        h = Paragraph(htext, normal)
        h.wrapOn(self.c, self.width, self.height)
        h.drawOn(self.c, *self.createCoord(0, 18, mm))

        htext = "<font size=15 name='boldFont'>ตารางแสดงรายการซ่อมบำรุงรักษา</font>"
        h = Paragraph(htext, normal)
        h.wrapOn(self.c, self.width, self.height)
        h.drawOn(self.c, *self.createCoord(0, 28, mm))

    def createTable(self, datatext):
        pdfmetrics.registerFont(TTFont('normalFont', 'THSarabunNew.ttf'))
        pdfmetrics.registerFont(TTFont('boldFont', 'THSarabunNew Bold.ttf'))

        styles = getSampleStyleSheet()
        styleNormal = styles["Normal"]
        styleTitle = styles["Title"]

        # Header of Table
        CH1 = Paragraph("<font size=13 name='boldFont'>TSID</font>", styleTitle)
        CH2 = Paragraph("<font size=13 name='boldFont'>ชื่อ</font>", styleTitle)
        CH3 = Paragraph("<font size=13 name='boldFont'>แผนก</font>", styleTitle)
        CH4 = Paragraph("<font size=13 name='boldFont'>อุปกรณ์</font>", styleTitle)
        CH5 = Paragraph("<font size=13 name='boldFont'>อาการเสีย</font>", styleTitle)
        CH6 = Paragraph("<font size=13 name='boldFont'>หมายเลข</font>", styleTitle)
        CH7 = Paragraph("<font size=13 name='boldFont'>เบอร์โทรศัพท์ผู้แจ้ง</font>", styleTitle)
        CH8 = Paragraph("<font size=13 name='boldFont'>สถานะ</font>", styleTitle)

        data = [
            ['หน้า 1','','','','','','',''],
            [CH1,CH2,CH3,CH4,CH5,CH6,CH7,CH8]
        ]

        # Data of table
        textlist = datatext
        count = len(textlist)

        for i in range(count):
            t1 = Paragraph("<font name='normalFont'>{}</font>".format(textlist[i][0]), styleNormal)
            t2 = Paragraph("<font name='normalFont'>{}</font>".format(textlist[i][1]), styleNormal)
            t3 = Paragraph("<font name='normalFont'>{}</font>".format(textlist[i][2]), styleNormal)
            t4 = Paragraph("<font name='normalFont'>{}</font>".format(textlist[i][3]), styleNormal)
            t5 = Paragraph("<font name='normalFont'>{}</font>".format(textlist[i][4]), styleNormal)
            t6 = Paragraph("<font name='normalFont'>{}</font>".format(textlist[i][5]), styleNormal)
            t7 = Paragraph("<font name='normalFont'>{}</font>".format(textlist[i][6]), styleNormal)
            t8 = Paragraph("<font name='normalFont'>{}</font>".format(textlist[i][7]), styleNormal)

            data.append([t1,t2,t3,t4,t5,t6,t7,t8])

        # table line full A4
        lineoftable = 38
        count2 = len(data)
        countf = lineoftable - count2

        for i in range(countf):
            blank = ['','','','','','','','']

            if count < lineoftable:
                data.append(blank)

        tableThatSplitsOverPages = Table(data, [2 * cm, 2.5 * cm, 2.5 * cm, 4 * cm, 1.8 * cm, 1.8 * cm, 2.2 * cm, 1.5 * cm], repeatRows=1)
        tableStyle = TableStyle(
            [
                ('BOX', (0,0), (-1,-1), 1, colors.black),
                ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
                ('FONTNAME', (0,0), (-1,0), 'boldFont'),
                ('SPAN', (0,0), (-1,0))
            ]
        )

        tableThatSplitsOverPages.setStyle(tableStyle)
        self.story.append(tableThatSplitsOverPages)

if __name__ == '__main__':
    pdffile = 'Maintenance-Report.pdf'
    data = [
        ['123456789012','ขาว', 'ช่าง', 'ลำโพง', 'ไม่ดัง', 'A111', '0987654321', 'done'],
        ['123456789012','ขาว', 'ช่าง', 'ลำโพง', 'ไม่ดัง', 'A111', '0987654321', 'done'],
        ['123456789012','ขาว', 'ช่าง', 'ลำโพง', 'ไม่ดัง', 'A111', '0987654321', 'done'],
    ]
    Report().createPDF(pdffile, data)
    Popen(pdffile, shell=True)