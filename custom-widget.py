from tkinter import *
from tkinter import ttk

GUI = Tk()
GUI.geometry('500x500')


L1 = ttk.Label(GUI,text='Hello',font=('Angsana New',20,'bold'),foreground='red')
L1.pack()

class RedText(ttk.Label):
    def __init__(self,GUI,text='example',size=20):
        ttk.Label.__init__(self,GUI,text=text,font=('Angsana New',size,'bold'),foreground='red')

L2 = RedText(GUI,text='สวัสดีจ้าาา',size=40)
L2.pack()


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
t.pack()
t.insertdata(['X','Y','Z'])
# # t.insert('','end',values=['A','B','C'])


GUI.mainloop()