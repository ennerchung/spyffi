"""
This module aims to create the database used for All Small Molecules
Blunt way of processing is to treat all data as strings.

The database management system consists of 
    create, update and delete
for
    database(db), table, column and data

some functions are not implemented as of now because there is currently no need for them.


"""

import os,sys
import sqlite3
import numpy as np

IMPLEMENT = True
VERBOSE = True


def access_db(db_name):
    
    conn = sqlite3.connect(db_name)
    conn.text_factory = str  #retrieve DB strings in UTF-8 format? is this useful?
    c = conn.cursor()

    return c,conn

def create_db(db_name, remove):
    """
    Database initiation function, creates the database called db_name and 
    return the database controlling mechanism c and conn.
    If remove is true, will overwrite the database.
    """

    if remove:
        if IMPLEMENT == True:
            os.remove(db_name) if os.path.exists(db_name) else None     
        else:    
            while True:
                next = str(raw_input("Are you sure about removing database: %s(Y/N)?"%db_name))
                if next == "Y":
                    os.remove(db_name) if os.path.exists(db_name) else None
                    break
                elif next == "N":
                    break
                else:
                    continue
    
    conn = sqlite3.connect(db_name)
    conn.text_factory = str  #retrieve DB strings in UTF-8 format? is this useful?
    c = conn.cursor()

    return c,conn
    
def update_db(db_name, new_db_name):
    """
    not really needed to be implemented at the moment
    """
    pass

def delete_db(db_name):
    """
    not really needed to be implemented at the moment
    """
    pass

def return_table_name(db_name, conn, c):
    pass


    
    
def create_table_prime(table_name,primary,column,conn,c):    
    """
    Table initiation function, creates the table called table_name
    and column which contain a list of tuples. Each tuples consist the data and data type.
    Remove is boolean. 
    """
    # creating the data creation command to execute
    command = "CREATE TABLE %s ("%table_name
    tag = True
    for i in column:
        if tag:
            command = command+"%s %s"%(i[0],i[1])
            tag = False
        else:
            command = command+", %s %s"%(i[0],i[1])
        if i[0] == primary:
            command = command+" PRIMARY KEY"
    command = command+")"
    print command
    c.execute(command)
    
    conn.commit()
    
def create_table_noprime(table_name,column,conn,c):    
    """
    Table initiation function, creates the table called table_name
    and column which contain a list of tuples. Each tuples consist the data and data type.
    Remove is boolean. 
    """
    # creating the data creation command to execute
    command = "CREATE TABLE %s (%s %s PRIMARY KEY"%(table_name, column[0][0],column[0][1])
    for i in column[1:]:
        command = command+", %s %s"%(i[0],i[1])
    command = command+")"
    c.execute(command)
    
    conn.commit()
    
def update_table(table_name,new_table_name, conn, c):

    command = "ALTER TABLE %s RENAME TO %s"%(table_name,new_table_name)
    c.execute(command)
    conn.commit()

def delete_table(table_name,conn,c):
    
    while True:
        try:
            if IMPLEMENT:
                command = "DROP TABLE %s"%(table_name)
                c.execute(command)
                conn.commit()
                break
            
            response = str(raw_input("Execute: "+command+"? (Y/N)"))
            if response == "Y":
                c.execute(command)
                conn.commit()
                break
            elif response == "N":
                print "table remove cancelled"
                break
            else:
                continue
        except sqlite3.OperationalError:
            print "Table not exist, no remove needed"
            break




def add_column(table_name,column_name, conn, c):
    """
    add a column to the table
    
    """
    command = "ALTER TABLE %s ADD COLUMN %s %s"%(table_name,column_name[0],column_name[1])
    
    c.execute(command)
    conn.commit()    

def update_column(table_name,column_name, conn, c):
    """
    The idea is to create a new table with the column and drop the old table
    There are heavy work arounds available.
    """
    pass

def delete_column(table_name,column_name, conn, c):
    """
    The idea is to create a new table with the column and drop the old table.
    There are heavy work arounds available.
    """
    pass

def return_column_name(table_name, conn, c):
    pass


def insert_single_data_nc(table_name, data, conn, c):
    """
    insert into table_name a tuple called data,
    does not handle conflicts. please use update_data for existing cases
    
    command should look like 
    'INSERT INTO table_name VALUES (?,?,?,?,?)'   
    
    not committed version for faster processing. Should commit outside of loop
    """
    
    inserts = 'INSERT INTO %s VALUES (?'
    for _ in range(len(data)-1):
        inserts = inserts+",?"
    inserts = inserts+")"
    
    try:
        c.execute(inserts%table_name, data)
    except sqlite3.IntegrityError as s:
        print "insert error"
        print data
        for _ in s:
            print s
    

def insert_single_data(table_name, data, conn, c):
    """
    insert into table_name a tuple called data,
    does not handle conflicts. please use update_data for existing cases
    
    command should look like 
    'INSERT INTO table_name VALUES (?,?,?,?,?)'   
    """
    
    inserts = 'INSERT INTO %s VALUES (?'
    for _ in range(len(data)-1):
        inserts = inserts+",?"
    inserts = inserts+")"
    
    try:
        c.execute(inserts%table_name, data)
    except sqlite3.IntegrityError as s:
        print "insert error"
        print data
        for _ in s:
            print s
    
    conn.commit()

def insert_single_data_unguard(table_name, data, conn, c):
    """
    insert into table_name a tuple called data,
    does not handle conflicts. please use update_data for existing cases
    
    command should look like 
    'INSERT INTO table_name VALUES (?,?,?,?,?)'  
    
    will return error if failed 
    """
    
    inserts = 'INSERT INTO %s VALUES (?'
    for _ in range(len(data)-1):
        inserts = inserts+",?"
    inserts = inserts+")"
    
    
    c.execute(inserts%table_name, data)
    
    conn.commit()


def insert_multi_data(table_name, data, conn, c):
    """
    insert into table_name a list of tuples called data,
    does not handle conflicts. please use update_data for existing cases
    
    command should look like 
    'INSERT INTO table_name VALUES (?,?,?,?,?)'   
    """
    
    inserts = 'INSERT INTO %s VALUES (?'
    for _ in range(len(data)-1):
        inserts = inserts+",?"
    inserts = inserts+")"
    
    try:
        c.executemany(inserts%table_name, data)
    except sqlite3.IntegrityError as s:
        print "insert error"
        print data
        for _ in s:
            print s
    
    conn.commit()








    
def update_single_data(table_name, data, conditions, conn, c):
    """
    updates the data in table_name
    datas and conditions must each be a list of two items
    """
    if len(data) !=2 and len(conditions)!=2:
        print "Update Failed due to data entry error or condition error"
        return 
    
    c.execute('UPDATE %s SET %s="%s" WHERE %s="%s"'%(table_name,data[0],data[1],conditions[0],conditions[1]))
    conn.commit()

def delete_single_data(table_name, conditions, conn, c):
    
    command = 'DELETE FROM %s WHERE %s="%s"'%(table_name, conditions[0],conditions[1])
    
    while True:
        try:
            if IMPLEMENT == True:
                c.execute(command)
                conn.commit()
                break
            
            response = str(raw_input("Execute: "+command+"? (Y/N)"))
            if response == "Y":
                c.execute(command)
                conn.commit()
                break
            elif response == "N":
                print "data remove cancelled"
                break
            else:
                continue
            
        except sqlite3.OperationalError:
            print "Column doesn't exist"
            break



def return_single_data_single_condition(table_name, target, conditions, conn, c):
    """
    look up the target value in the database using one condition
    ["name","john"]
    """
    
    cmd = "SELECT %s FROM %s Where %s='%s'"%(target, table_name, conditions[0],conditions[1])
    c.execute(cmd)
    result = c.fetchone()
    
    return result
    
def return_single_data_multi_condition(table_name, target, conditions, conn, c):
    """
    look up the target value in the database using multiple condition
    [["name","john],["Age","50]]
    """
    
    
    count = len(conditions)    
    
    cmd = "SELECT %s FROM %s Where "%(table_name,target)
    
    for i in range(count - 1):
        cmd = cmd+"%s = %s AND"%(conditions[i][0],conditions[i][1])
    cmd = cmd+"%s = %s"%(conditions[count-1][0],conditions[count-1][1])
    
    
    c.excute(cmd)
    
    
    
    pass
    
def return_all_from_table(table_name,conn,c):
    """
    Return everything in this table
    """
    cmd = "SELECT * FROM %s"%(table_name)
    c.execute(cmd)
    result = c.fetchall()
    
    return result

def return_column_from_table(table_name, column, conn,c):
    """
    Return everything in a selected column
    """
    cmd = "SELECT %s FROM %s"%(column, table_name)
    c.execute(cmd)
    result = c.fetchall()
    
    return result

def return_all_from_condition(table_name,conditions,conn,c):
    """
    Return everything under this condition
    """
    cmd = "SELECT * FROM %s where %s='%s'"%(table_name,conditions[0],conditions[1])
    c.execute(cmd)
    result = c.fetchall()
    
    return result




def data_process(filename,splitter=""):
    """
    process data files into numpy arrays that can be plotted.
    input files are arbitrary columns.
    """
    ndata = []
    for line in open(filename, 'r'):
        init = line.split(splitter)
        data = np.array(init,ndmin=2)  # convert data into numpy array         
        if ndata == []:     
            ndata = data
        else:
            ndata = np.concatenate((ndata,data))      # data stitching
    ndata = np.transpose(ndata)
    return ndata    

if __name__ =="__main__":
    
    
    
    # test cases to understand how the database works.
    remove = True
    db_name = "../database/demoDatabase.db"
    c,conn = create_db(db_name, remove)

    table_name = "ID"
    columns = [("InChiKey","text"),("Inchi","text"),("Common_Name","text"),("Formula","text"),("Smiles","text")]
    primary = "InChiKey"
    control = create_table_prime(table_name,primary,columns,conn,c)
    
    data = ["Test1","Nob","Sob","Dob","Nob"]
    insert_single_data(table_name, data, conn, c)
    data = ["Test2","Nob","Sob","Kob","bob"]
    insert_single_data(table_name, data, conn, c)
    
    for row in c.execute('SELECT * FROM %s'%table_name):
        print row


    update_single_data(table_name,["Inchi","Joe"],["Smiles","Nob"],conn,c)

    for row in c.execute('SELECT * FROM %s'%table_name):
        print row


    delete_single_data(table_name, ["InChiKey","Test1"], conn, c)
    
    for row in c.execute('SELECT * FROM %s'%table_name):
        print row














    """
    molecules = ["water","Methane","Ethane","Joe"]
    
    filename = "Light_Gas.csv"
    data = data_process(filename,"\n")
    for i in data[0]:
        print i.split(",")
        
    moremolecules = ["water","Methane","Ethane","John","something"]
    moreorigin = "there"    
    
    insert_data(moremolecules, moreorigin, conn, c)
    
    for row in c.execute('SELECT * FROM molecules ORDER BY name'):
        print row    
    """
    
