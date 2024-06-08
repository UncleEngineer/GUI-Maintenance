from tkinter import *

GUI = Tk()

GUI.title('โปรแกรมซ่อมบำรุง by Loong')
GUI.geometry('500x500+50+50')
####FONT#####
FONT1 = ('Angsana New',20)
FONT2 = ('Angsana New',15)

#############
L = Label(GUI,text='ใบแจ้งซ่อม',font=FONT1)
L.pack()

#-------------
L = Label(GUI,text='ชื่อผู้แจ้ง',font=FONT2)
L.place(x=30,y=50)
E1 = Entry(GUI,font=FONT2)
E1.place(x=150,y=50)

#-------------
L = Label(GUI,text='แผนก',font=FONT2)
L.place(x=30,y=100)
E1 = Entry(GUI,font=FONT2)
E1.place(x=150,y=100)
#-------------
L = Label(GUI,text='อุปกรณ์/เครื่อง',font=FONT2)
L.place(x=30,y=150)
E1 = Entry(GUI,font=FONT2)
E1.place(x=150,y=150)
#-------------
L = Label(GUI,text='อาการเสีย',font=FONT2)
L.place(x=30,y=200)
E1 = Entry(GUI,font=FONT2)
E1.place(x=150,y=200)
#-------------
L = Label(GUI,text='หมายเลข',font=FONT2)
L.place(x=30,y=250)
E1 = Entry(GUI,font=FONT2)
E1.place(x=150,y=250)
#-------------
L = Label(GUI,text='เบอร์โทร',font=FONT2)
L.place(x=30,y=300)
E1 = Entry(GUI,font=FONT2)
E1.place(x=150,y=300)
# L.pack()
# L.grid(row=1,column=1)
# L.place(x=20,y=100)
GUI.mainloop()
