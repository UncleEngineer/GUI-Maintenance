import sqlite3
conn = sqlite3.connect('maintenance.sqlite3')
c = conn.cursor()

c.execute(""" CREATE TABLE IF NOT EXISTS mt_workorder (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    tsid TEXT,
                    name TEXT,
                    department TEXT,
                    machine TEXT,
                    problem TEXT,
                    number TEXT,
                    tel TEXT,
                    status TEXT ) """)

# -tsid 
# - วัน (date_start)
# - รายละเอียดการซ่อม (detail)
# - หมายเหตุ (Other)

c.execute("""CREATE TABLE IF NOT EXISTS mt_note (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                tsid TEXT,
                date_start TEXT,
                detail TEXT,
                other TEXT )""")




def insert_mtworkorder(tsid,name,department,machine,problem,number,tel):
    #CREATE
    with conn:
        command = 'INSERT INTO mt_workorder VALUES (?,?,?,?,?,?,?,?,?)'
        c.execute(command,(None,tsid,name,department,machine,problem,number,tel,'new'))
    conn.commit()
    #print('saved')


def view_mtworkorder():
    # READ
    with conn:
        command = 'SELECT * FROM mt_workorder'
        c.execute(command)
        result = c.fetchall()
    #print(result)
    return result

def view_mtworkorder_status(status='approved'):
    
    with conn:
        command = 'SELECT * FROM mt_workorder WHERE status=(?)'
        c.execute(command,([status]))
        result = c.fetchall()
    #print(result)
    return result


def update_mtworkorder(tsid,field,newvalue):
    # UPDATE
    with conn:
        command = 'UPDATE mt_workorder SET {} = (?) WHERE tsid=(?)'.format(field)
        c.execute(command,(newvalue,tsid))
    conn.commit()
    #print('updated')


def delete_mtworkorder(tsid):
    # DELETE
    with conn:
        command = 'DELETE FROM mt_workorder WHERE tsid=(?)'
        c.execute(command,([tsid]))
    conn.commit()
    #print('deleted')

#########################################
def insert_mtnote(tsid,date_start,detail,other):
    with conn:
        command = 'INSERT INTO mt_note VALUES (?,?,?,?,?)'
        c.execute(command,(None,tsid,date_start,detail,other))
    conn.commit()

def view_mtnote():
    with conn:
        command = 'SELECT * FROM mt_note'
        c.execute(command)
        result = c.fetchall()
    return result

def view_mtnote_tsid(tsid):
    with conn:
        command = 'SELECT * FROM mt_note WHERE tsid=(?)'
        c.execute(command,([tsid]))
        result = c.fetchone()
    return result

def update_mtnote(tsid,field,newvalue):
    with conn:
        command = 'UPDATE mt_note SET {} = (?) WHERE tsid=(?)'.format(field)
        c.execute(command,(newvalue,tsid))
    conn.commit()

def delete_mtnote(tsid):
    with conn:
        command = 'DELETE FROM mt_note WHERE tsid=(?)'
        c.execute(command,([tsid]))
    conn.commit()
#########################################
'''
(department)
-dep_code
-dep_title

(machine_equipment)
-mc_code
-mc_title
-mc_detail
-dep_code

(sparepart)
-sp_code
-sp_title
-sp_detail
-sp_quantity
-sp_reorderpoint
'''

## DEPARTMENT
c.execute("""CREATE TABLE IF NOT EXISTS department (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                dep_code TEXT,
                dep_title TEXT)""")

def insert_department(dep_code,dep_title):
    with conn:
        command = 'INSERT INTO department VALUES (?,?,?)'
        c.execute(command,(None,dep_code,dep_title))
    conn.commit()

def view_department():
    with conn:
        command = 'SELECT * FROM department'
        c.execute(command)
        result = c.fetchall()
    return result

def update_department(dep_code,field,newvalue):
    with conn:
        command = 'UPDATE department SET {} = (?) WHERE dep_code=(?)'.format(field)
        c.execute(command,(newvalue,dep_code))
    conn.commit()

def delete_department(dep_code):
    with conn:
        command = 'DELETE FROM department WHERE dep_code=(?)'
        c.execute(command,([dep_code]))
    conn.commit()

## MACHINE_EQUIPMENT
c.execute("""CREATE TABLE IF NOT EXISTS machine_equipment (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                mc_code TEXT,
                mc_title TEXT,
                mc_detail TEXT,
                dep_code TEXT)""")

def insert_machine_equipment(mc_code,mc_title,mc_detail,dep_code):
    with conn:
        command = 'INSERT INTO machine_equipment VALUES (?,?,?,?,?)'
        c.execute(command,(None,mc_code,mc_title,mc_detail,dep_code))
    conn.commit()

def view_machine_equipment():
    with conn:
        command = 'SELECT * FROM machine_equipment'
        c.execute(command)
        result = c.fetchall()
    return result

def update_machine_equipment(mc_code,field,newvalue):
    with conn:
        command = 'UPDATE machine_equipment SET {} = (?) WHERE mc_code=(?)'.format(field)
        c.execute(command,(newvalue,mc_code))
    conn.commit()

def delete_machine_equipment(mc_code):
    with conn:
        command = 'DELETE FROM machine_equipment WHERE mc_code=(?)'
        c.execute(command,([mc_code]))
    conn.commit()

## SPAREPART
c.execute("""CREATE TABLE IF NOT EXISTS sparepart (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                sp_code TEXT,
                sp_title TEXT,
                sp_detail TEXT,
                sp_quantity INTEGER,
                sp_reorderpoint INTEGER)""")

def insert_sparepart(sp_code,sp_title,sp_detail,sp_quantity,sp_reorderpoint):
    with conn:
        command = 'INSERT INTO sparepart VALUES (?,?,?,?,?,?)'
        c.execute(command,(None,sp_code,sp_title,sp_detail,sp_quantity,sp_reorderpoint))
    conn.commit()

def view_sparepart():
    with conn:
        command = 'SELECT * FROM sparepart'
        c.execute(command)
        result = c.fetchall()
    return result

def update_sparepart(sp_code,field,newvalue):
    with conn:
        command = 'UPDATE sparepart SET {} = (?) WHERE sp_code=(?)'.format(field)
        c.execute(command,(newvalue,sp_code))
    conn.commit()

def delete_sparepart(sp_code):
    with conn:
        command = 'DELETE FROM sparepart WHERE sp_code=(?)'
        c.execute(command,([sp_code]))
    conn.commit()