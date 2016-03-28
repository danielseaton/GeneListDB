import MySQLdb
import os

def connect_to_db():
    with open(os.getenv('HOME')+'/Dropbox/config/mysqlrootpassword.txt') as f:
        mysqlpassword = f.readlines()[0].strip()
    db = MySQLdb.connect("localhost","root",mysqlpassword,"GeneListDB")
    return db