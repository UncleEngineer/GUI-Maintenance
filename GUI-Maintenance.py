from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import csv
from datetime import datetime
# DATABASE
from db_maintenance import *

def writecsv(record_list):
    with open('data.csv','a',newline='',encoding='utf-8') as file:
        fw = csv.writer(file)
        fw.writerow(record_list)



GUI = Tk()

GUI.title('โปรแกรมซ่อมบำรุง v.0.0.1 by Loong')
GUI.geometry('1400x600+50+50')
####FONT#####
FONT1 = ('Angsana New',20,'bold')
FONT2 = ('Angsana New',15)
FONT3 = ('Angsana New',13)

#######TAB#######
# s = ttk.Style()
# s.theme_create('MyStyle',settings={
#     'TNotebook.Tab':{'configure':{'padding':[10,10],'font':(None,'14','bold')}}
# })
# s.theme_use('MyStyle')




Tab = ttk.Notebook(GUI)
T1 = Frame(Tab)
T2 = Frame(Tab)
T3 = Frame(Tab)
T4 = Frame(Tab)
Tab.add(T1,text= f'{' '*5}ใบแจ้งซ่อม{' '*5}')
# Tab.add(T1,text= f'{' '*10}ใบแจ้งซ่อม{' '*10}')
Tab.add(T2,text='ดูใบแจ้งซ่อม')
Tab.add(T3,text='อนุมัติให้ซ่อมแล้ว')
Tab.add(T4,text='รายการซ่อมเสร็จแล้ว')
Tab.pack(fill=BOTH,expand=1)

s = ttk.Style()
s.configure('TNotebook.Tab',font=(None,12),padding=[30,10])


#############
L = Label(T1,text='ใบแจ้งซ่อม',font=FONT1)
L.place(x=80,y=10)

#-------------
L = Label(T1,text='ชื่อผู้แจ้ง',font=FONT2)
L.place(x=30,y=50)
v_name = StringVar() #ตัวแปรพิเศษใช้กับ GUI
E1 = ttk.Entry(T1,textvariable=v_name, font=FONT2)
E1.place(x=150,y=50)

#-------------
L = Label(T1,text='แผนก',font=FONT2)
L.place(x=30,y=100)
v_department =StringVar()
E2 = ttk.Entry(T1,textvariable=v_department,font=FONT2)
E2.place(x=150,y=100)
#-------------
L = Label(T1,text='อุปกรณ์/เครื่อง',font=FONT2)
L.place(x=30,y=150)
v_machine =StringVar()
E3 = ttk.Entry(T1,textvariable=v_machine,font=FONT2)
E3.place(x=150,y=150)
#-------------
L = Label(T1,text='อาการเสีย',font=FONT2)
L.place(x=30,y=200)
v_problem =StringVar()
E4 = ttk.Entry(T1,textvariable=v_problem ,font=FONT2)
E4.place(x=150,y=200)
#-------------
L = Label(T1,text='หมายเลข',font=FONT2)
L.place(x=30,y=250)
v_number =StringVar()
E5 = ttk.Entry(T1,textvariable=v_number,font=FONT2)
E5.place(x=150,y=250)
#-------------
L = Label(T1,text='เบอร์โทร',font=FONT2)
L.place(x=30,y=300)
v_tel =StringVar()
E6 = ttk.Entry(T1,textvariable=v_tel,font=FONT2)
E6.place(x=150,y=300)

def save():
    name = v_name.get() # .get คือการดึงออกมาจาก StringVar
    department = v_department.get()
    machine = v_machine.get()
    problem = v_problem.get()
    number = v_number.get()
    tel = v_tel.get()

    text = 'ชื่อผู้แจ้ง: ' + name + '\n' # \n คือขึ้นบรรทัดใหม่
    text = text + 'แผนก: ' + department + '\n'
    text = text + 'อุปกรณ์/เครื่อง: ' + machine + '\n'
    text = text + 'อาการเสีย: ' + problem + '\n'
    text = text + 'หมายเลข: ' + number + '\n'
    text = text + 'โทร: ' + tel + '\n'
    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Generate Transaction
    tsid = str(int(datetime.now().strftime('%y%m%d%H%M%S')) + 114152147165)
    insert_mtworkorder(tsid,name,department,machine,problem,number,tel)
    v_name.set('')
    v_department.set('')
    v_machine.set('')
    v_problem.set('')
    v_number.set('')
    v_tel.set('')
    update_table()


    # datalist = [dt,name,department,machine,problem,number,tel]
    # writecsv(datalist)
    # messagebox.showinfo('กำลังบันทึกข้อมูล...',text)    
B = ttk.Button(T1, text='บันทึกใบแจ้งซ่อม',command=save)
B.place(x=200,y=350)


################TAB2################
header = ['TSID','ชื่อ','แผนก','อุปกรณ์','อาการเสีย','หมายเลข','เบอร์โทรผู้แจ้ง','สถานะ']
headerw = [100,150,150,200,250,150,150,150]

mtworkorderlist = ttk.Treeview(T2,columns=header,show='headings',height=20)
mtworkorderlist.pack()

#ปรับขนาดฟอนต์และตารางให้ใหญ่ขึ้น
style = ttk.Style()
style.configure('Treeview.Heading',font=('Angsana New',20,'bold'))
style.configure('Treeview',rowheight=25,font=('Angsana New',15))

for h,w in zip(header,headerw):
    # h='TSID', w=50 ---> h='ชื่อ' w=100
    mtworkorderlist.heading(h,text=h)
    mtworkorderlist.column(h,width=w,anchor='center')

mtworkorderlist.column('TSID',anchor='e')

# mtworkorderlist.insert('','end',values=['A','B','C','D','E','F','G'])

def update_table():
    #clear ข้อมูลเก่า
    mtworkorderlist.delete(*mtworkorderlist.get_children())
    data = view_mtworkorder_status(status='new')
    # print(data)
    for d in data:
        d = list(d) #แปลง tuple เป็น list
        del d[0] # ลบ ID จาก database ออก
        mtworkorderlist.insert('','end',values=d)


## หน้าสำหรับแก้ไขข้อความ

def EditPage_mtworkorder(event=None):
    select = mtworkorderlist.selection()
    output = mtworkorderlist.item(select)
    op = output['values']
    print('OP:',op)
    tsid = op[0]
    t_name = op[1]
    t_department = op[2]
    t_machine = op[3]
    t_problem = op[4]
    t_number = op[5]
    t_tel = '0{}'.format(op[6])
    


    GUI2 = Toplevel()
    GUI2.title('หน้าแก้ไขข้อมูลใบแจ้งซ่อม')
    GUI2.geometry('500x500')

    L = Label(GUI2,text='ใบแจ้งซ่อม',font=FONT1)
    L.place(x=80,y=10)

    #-------------
    L = Label(GUI2,text='ชื่อผู้แจ้ง',font=FONT2)
    L.place(x=30,y=50)
    v_name2 = StringVar() #ตัวแปรพิเศษใช้กับ GUI
    v_name2.set(t_name)
    E1 = ttk.Entry(GUI2,textvariable=v_name2, font=FONT2)
    E1.place(x=150,y=50)

    #-------------
    L = Label(GUI2,text='แผนก',font=FONT2)
    L.place(x=30,y=100)
    v_department2 =StringVar()
    v_department2.set(t_department)
    E2 = ttk.Entry(GUI2,textvariable=v_department2,font=FONT2)
    E2.place(x=150,y=100)
    #-------------
    L = Label(GUI2,text='อุปกรณ์/เครื่อง',font=FONT2)
    L.place(x=30,y=150)
    v_machine2 =StringVar()
    v_machine2.set(t_machine)
    E3 = ttk.Entry(GUI2,textvariable=v_machine2,font=FONT2)
    E3.place(x=150,y=150)
    #-------------
    L = Label(GUI2,text='อาการเสีย',font=FONT2)
    L.place(x=30,y=200)
    v_problem2 =StringVar()
    v_problem2.set(t_problem)
    E4 = ttk.Entry(GUI2,textvariable=v_problem2 ,font=FONT2)
    E4.place(x=150,y=200)
    #-------------
    L = Label(GUI2,text='หมายเลข',font=FONT2)
    L.place(x=30,y=250)
    v_number2 =StringVar()
    v_number2.set(t_number)
    E5 = ttk.Entry(GUI2,textvariable=v_number2,font=FONT2)
    E5.place(x=150,y=250)
    #-------------
    L = Label(GUI2,text='เบอร์โทร',font=FONT2)
    L.place(x=30,y=300)
    v_tel2 =StringVar()
    v_tel2.set(t_tel)
    E6 = ttk.Entry(GUI2,textvariable=v_tel2,font=FONT2)
    E6.place(x=150,y=300)

    def edit_save():
        name = v_name2.get() # .get คือการดึงออกมาจาก StringVar
        department = v_department2.get()
        machine = v_machine2.get()
        problem = v_problem2.get()
        number = v_number2.get()
        tel = v_tel2.get()
       
        update_mtworkorder(tsid,'name',name)
        update_mtworkorder(tsid,'department',department)
        update_mtworkorder(tsid,'machine',machine)
        update_mtworkorder(tsid,'problem',problem)
        update_mtworkorder(tsid,'number',number)
        update_mtworkorder(tsid,'tel',tel)

        
        update_table()
        GUI2.destroy()
  
    B = ttk.Button(GUI2, text='บันทึกใบแจ้งซ่อม',command=edit_save)
    B.place(x=200,y=350)

    GUI2.mainloop()

mtworkorderlist.bind('<Double-1>',EditPage_mtworkorder)

def Delete_mtworkorder(event=None):
    select = mtworkorderlist.selection()
    output = mtworkorderlist.item(select)
    tsid = output['values'][0] # get only ts id

    check = messagebox.askyesno('ยืนยันการลับ','คุณต้องการลบข้อมูลใช่หรือไม่?')
    #print(check)

    if check == True:
        delete_mtworkorder(tsid)
        update_table()

mtworkorderlist.bind('<Delete>',Delete_mtworkorder)

##### RIGHT CLICK MENU #######
def Approved():
    select = mtworkorderlist.selection()
    output = mtworkorderlist.item(select)
    tsid = output['values'][0]
    
    update_mtworkorder(tsid,'status','approved')
    update_table()
    update_table_approved_wlist() # อัพเดตตารางที่อนุมัติแล้ว

approved_menu = Menu(GUI,tearoff=0)
approved_menu.add_command(label='approved',command=Approved)
approved_menu.add_command(label='delete',command=Delete_mtworkorder)

def popup(event):
    approved_menu.post(event.x_root, event.y_root)

mtworkorderlist.bind('<Button-3>',popup)

###################### T A B 3 ######################


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

class MenuText(ttk.Label):
    def __init__(self,GUI,text='example',size=20):
        ttk.Label.__init__(self,GUI,text=text,font=('Angsana New',size,'bold'),foreground='black')



# Table of Approved List
L = MenuText(T3,text='ตารางแสดงรายการอนุมัติให้ซ่อม',size=30)
L.pack()

approved_wlist = WorkorderList(T3)
approved_wlist.pack()

# update_table + ชื่อตาราง = ฟังชั่นสำหรับอัพเดตตารางนั้นๆ
def update_table_approved_wlist():
    #clear ข้อมูลเก่า
    approved_wlist.delete(*approved_wlist.get_children())
    data = view_mtworkorder_status(status='approved')
    # print(data)
    for d in data:
        d = list(d) #แปลง tuple เป็น list
        del d[0] # ลบ ID จาก database ออก
        approved_wlist.insert('','end',values=d)


#####START UP######
update_table()
update_table_approved_wlist()

GUI.mainloop()
