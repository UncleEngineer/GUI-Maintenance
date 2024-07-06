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
    # READ
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