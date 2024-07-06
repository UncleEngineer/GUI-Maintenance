from tkinter import *
from tkinter import ttk

GUI = Tk()
GUI.geometry('500x500')

class WorkorderList(ttk.Treeview):
    def __init__(self,GUI):
        header = ['TSID','ชื่อ','แผนก','อุปกรณ์','อาการเสีย','หมายเลข','เบอร์โทรผู้แจ้ง','สถานะ']
        headerw = [100,150,150,200,250,150,150,150]
        ttk.Treeview.__init__(self,GUI,columns=header,show='headings',height=20)
        for h,w in zip(header,headerw):
            self.heading(h,text=h)
            self.column(h,width=w,anchor='center')
    
    def insertdata(self,values):
        self.insert('','end',values=values)

        
t = WorkorderList(GUI)
t.place(x=50,y=50)
t.insertdata(['X','Y','Z'])
# t.insert('','end',values=['A','B','C'])


GUI.mainloop()