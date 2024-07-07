from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import csv
from datetime import datetime
from tkcalendar import DateEntry # pip install tkcalendar
# DATABASE
from db_maintenance import *
from allpage import *

def writecsv(record_list):
    with open('data.csv','a',newline='',encoding='utf-8') as file:
        fw = csv.writer(file)
        fw.writerow(record_list)


GUI = Tk()

GUI.title('โปรแกรมซ่อมบำรุง v.0.0.1 by Loong')

#GUI.geometry('700x500')
w = 1400
h = 600

ws = GUI.winfo_screenwidth() #screen width
hs = GUI.winfo_screenheight() #screen height
#print(ws,hs)

x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

GUI.geometry(f'{w}x{h}+{x:.0f}+{y:.0f}')


def center_windows(w,h):
    ws = GUI.winfo_screenwidth() #screen width
    hs = GUI.winfo_screenheight() #screen height
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    return f'{w}x{h}+{x:.0f}+{y:.0f}'



# GUI.geometry('1400x600+50+50')
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
Tab.add(T1,text= f"{' '*5}เมนูหลัก{' '*5}")
# Tab.add(T1,text= f'{' '*10}ใบแจ้งซ่อม{' '*10}')
Tab.add(T2,text='ดูใบแจ้งซ่อม')
Tab.add(T3,text='อนุมัติให้ซ่อมแล้ว')
Tab.add(T4,text='รายการซ่อมเสร็จแล้ว')
Tab.pack(fill=BOTH,expand=1)

s = ttk.Style()
s.configure('TNotebook.Tab',font=(None,12),padding=[30,10])

##################MENU BAR#####################


#Main Menu
menubar = Menu(GUI)
GUI.config(menu=menubar)
#File Menu >
menu_file = Menu(menubar,tearoff=0)
menubar.add_cascade(label='File',menu=menu_file)

menu_file.add_command(label='Sync')
menu_file.add_command(label='Update Database')

sub_menu = Menu(menu_file,tearoff=0)
sub_menu.add_command(label='config database')
def Report():
    messagebox.showinfo('Report Menu','ตอนนี้ยังไม่พร้อมใช้งาน')
sub_menu.add_command(label='config report',command=Report)

menu_file.add_cascade(label='Config',menu=sub_menu)

menu_file.add_separator()
menu_file.add_command(label='Exit',accelerator='Ctrl+Q',command=lambda: GUI.quit())

GUI.bind('<Control-q>',lambda x: GUI.quit())

# Help

menu_help = Menu(menubar,tearoff=0)
menubar.add_cascade(label='Help',menu=menu_help)

menu_help.add_command(label='About')
menu_help.add_command(label='Update Software')
menu_help.add_command(label='Contact Developer')
menu_help.add_command(label='Donate')

################GENERAL CLASS####################
class MenuText(ttk.Label):
    def __init__(self,GUI,text='example',size=20):
        ttk.Label.__init__(self,GUI,text=text,font=('Angsana New',size,'bold'),foreground='black')

class ET(Frame):
        def __init__(self,GUI,label,textvariable,FONT=('Angsana New',15)):
            Frame.__init__(self,GUI,width=500,height=200)
            L = ttk.Label(self,text=label)
            L.place(x=0,y=0)
            self.E1 = ttk.Entry(self,textvariable=textvariable, font=FONT)
            self.E1.place(x=90,y=0)
###################################
def update_table():
    #clear ข้อมูลเก่า
    mtworkorderlist.delete(*mtworkorderlist.get_children())
    data = view_mtworkorder_status(status='new')
    # print(data)
    for d in data:
        d = list(d) #แปลง tuple เป็น list
        del d[0] # ลบ ID จาก database ออก
        mtworkorderlist.insert('','end',values=d)

#################MT WORK ORDER##################

def WindowMTWorkorder():
    GUI2 = Toplevel()
    win_size = center_windows(600,600)
    GUI2.geometry(win_size)
    GUI2.title('ใบแจ้งซ่อม')

    F1 = MTWorkorder(GUI2,insert_mtworkorder,update_table)
    F1.pack()

    GUI2.mainloop()

FBM1 = Frame(T1)
FBM1.place(x=50,y=50)
icon_bm1 = PhotoImage(file='mtworkorder.png')
BM1 = ttk.Button(FBM1,text='ใบแจ้งซ่อม',image=icon_bm1,compound='top',command=WindowMTWorkorder)
BM1.pack(ipadx=50,ipady=20)

#################DEPARTMENT##################
def WindowDepartment():
    GUI2 = Toplevel()
    win_size = center_windows(600,600)
    GUI2.geometry(win_size)
    GUI2.title('เพิ่ม/ลด แผนก')

    L = MenuText(GUI2,text='เพิ่ม/ลด แผนก')
    L.pack()

    #     (department)
    # -dep_code
    # -dep_title

    v_dep_code = StringVar() #ตัวแปรพิเศษใช้กับ GUI
    E1 = ET(GUI2,label='รหัสแผนก',textvariable=v_dep_code)
    E1.place(x=50,y=50)

    v_dep_title = StringVar() #ตัวแปรพิเศษใช้กับ GUI
    E2 = ET(GUI2,label='ชื่อแผนก',textvariable=v_dep_title)
    E2.place(x=50,y=100)

    def SaveDep():
        dep_code = v_dep_code.get()
        dep_title = v_dep_title.get()
        insert_department(dep_code,dep_title)
        v_dep_code.set('')
        v_dep_title.set('')
        E1.E1.focus()


    B = ttk.Button(GUI2,text='Save',command=SaveDep)
    B.place(x=50,y=150)
    

    GUI2.mainloop()


FBM1 = Frame(T1)
FBM1.place(x=250,y=50)
icon_bm2 = PhotoImage(file='department.png')
BM2 = ttk.Button(FBM1,text='สร้างแผนก',image=icon_bm2,compound='top',command=WindowDepartment)
BM2.pack(ipadx=50,ipady=20)

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

mtworkorderlist.column('TSID',anchor='e') #ชิดขวา ตัวเลข

# mtworkorderlist.insert('','end',values=['A','B','C','D','E','F','G'])



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


def Newnote(event):
    GUI3 = Toplevel()
    GUI3.geometry('600x600')
    GUI3.title('รายละเอียดงานซ่อม')

    select = approved_wlist.selection()
    output = approved_wlist.item(select)
    tsid = output['values'][0]

    

    FONT4 = (None,15)
    L = ttk.Label(GUI3,text='รายละเอียดงานซ่อม (tsid: {})'.format(tsid),font=FONT4)
    L.pack(pady=10)

    ###################
    L = ttk.Label(GUI3,text='แผนซ่อมในวันที่',font=FONT4)
    L.pack(pady=10)
    v_date = StringVar()
    # E1 = ttk.Entry(GUI3,textvariable=v_date,font=FONT4)
    # E1.pack()

    cal = DateEntry(GUI3, width=30, background='darkblue',foreground='white', borderwidth=2, year=2024,date_pattern='dd/MM/yyyy')
    cal.pack(padx=10, pady=10)
    ###################
    L = ttk.Label(GUI3,text='รายละเอียดงานซ่อม',font=FONT4)
    L.pack(pady=10)
    E2 = Text(GUI3,font=FONT4,width=40,height=5)
    E2.pack()
    ###################
    L = ttk.Label(GUI3,text='หมายเหตุ',font=FONT4)
    L.pack(pady=10)
    E3 = Text(GUI3,font=FONT4,width=40,height=5)
    E3.pack()
    ###################
    # get data from mtnote (1, '354858297216', '07/07/2024', 'ซ่อมได้เลย', 'ซ่อมหยุดเครื่อง')
    data = view_mtnote_tsid(tsid)
    print(data)

    GUI3.bind('<F1>',lambda x: E3.focus())

    if data != None:
        
        cal.set_date(data[2])
        E2.insert(END,data[3])
        E3.insert(END,data[4])

    ###################

    def SaveDetail():
        date_start = cal.get()
        detail = E2.get('1.0',END).strip()
        other = E3.get('1.0',END).strip()
        if data == None:
            insert_mtnote(tsid,date_start,detail,other)
        else:
            update_mtnote(tsid,'date_start',date_start)
            update_mtnote(tsid,'detail',detail)
            update_mtnote(tsid,'other',other)

        GUI3.destroy()

    B = ttk.Button(GUI3,text='Save',command=SaveDetail)
    B.pack(pady=20,ipadx=20,ipady=10)


    GUI3.mainloop()

approved_wlist.bind('<Double-1>',Newnote)

##### RIGHT CLICK MENU - อนุมัติรายละเอียดงานซ่อม #######
def Done():
    select = approved_wlist.selection()
    output = approved_wlist.item(select)
    tsid = output['values'][0]
    
    update_mtworkorder(tsid,'status','done')
    update_table()
    update_table_approved_wlist() # อัพเดตตารางที่อนุมัติแล้ว
    update_table_done_wlist()
    # อัพเดตตารางใหม่

done_menu = Menu(GUI,tearoff=0)
done_menu.add_command(label='done',command=Done)

def popup(event):
    done_menu.post(event.x_root, event.y_root)

approved_wlist.bind('<Button-3>',popup)


###################### T A B 4 ######################

# Table of Done List
L = MenuText(T4,text='ตารางแสดงรายการซ่อมเสร็จแล้ว',size=30)
L.pack()

done_wlist = WorkorderList(T4)
done_wlist.pack()

# update_table + ชื่อตาราง = ฟังชั่นสำหรับอัพเดตตารางนั้นๆ
def update_table_done_wlist():
    #clear ข้อมูลเก่า
    done_wlist.delete(*done_wlist.get_children())
    data = view_mtworkorder_status(status='done')
    # print(data)
    for d in data:
        d = list(d) #แปลง tuple เป็น list
        del d[0] # ลบ ID จาก database ออก
        done_wlist.insert('','end',values=d)

#####START UP######
GUI.wm_attributes('-transparentcolor', '#ab23ff')

update_table()
update_table_approved_wlist()
update_table_done_wlist()
GUI.mainloop()
