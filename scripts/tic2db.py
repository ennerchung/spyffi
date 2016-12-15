"""
This module reads in TIC data from txt or csv files and convert it into database format

#execute many is possible to insert all data at once. look into this.


"""
import numpy as np
import general_functions as gf
import db_management as dbm
import os
import time
from astropy.table import Table


def read_file_txt(filename, scan=None):
    """
    reads in a data file and return a 2d list of the data
    """
    if scan < 0 and scan !=None:
        print "invalid scan parameter"
        return []
    

    f = open(filename).read().split("\n")
    
    data = []
    
    ct = 0
    for i in f:
        data.append(i.split(","))
        ct+=1
        if ct == scan:
            break

    return np.array(data)


def load_into_db(filename,remove):

    data = gf.read_file_txt(filename,None)
    #subject to change
    db_name = "../input/TIC_db.db"
    table_name = "Data"
    
    if remove:
        try:
            os.remove(db_name)
            print "File removed"
        except OSError:
            pass
    
    if not os.path.isfile(db_name):
        c,conn = dbm.create_db(db_name, remove)
        columns = [("ID","text"),("TMAG","FLOAT"),("TEFF","FLOAT"),("PMRA","FLOAT"),
                   ("PMDEC","FLOAT"),("RA","FLOAT"),("DEC","FLOAT"),("OBJTYPE","text")]
        primary = "ID"
        control = dbm.create_table_prime(table_name,primary,columns,conn,c)
    else:
        c,conn = dbm.access_db(db_name)


    """
    Skip_Header = True
    for i in data:
        if Skip_Header:
            Skip_Header = False
            continue
        try:
            item = [i[0],i[1],i[4],i[7],i[9],i[16],i[17],i[20]]
            dbm.insert_single_data_nc(table_name, item, conn, c)
        except IndexError:
            pass 
    """
    
    data = data[1:]
    insert = []
    # implement the data manipulation for execute many
    
    
    conn.commit()
    
    
def main():

    start = time.time()    
    
    filename = "../input/sample_tic.txt"
    remove = True
    load_into_db(filename,remove)
    
    
    print time.time()- start







if __name__ == "__main__":
    main()
    
    
    