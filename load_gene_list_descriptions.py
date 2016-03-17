import pandas as pd
import re
import MySQLdb

db = MySQLdb.connect("localhost","root","zoomzoom","GeneListDB")
cursor = db.cursor()

def execute_sql_query(sql,parameters):
    try:
        #execute the sql command
        cursor.execute(sql,parameters)
        #commit changes
        db.commit()
    except:
        #TODO - elaborate on error information from execute statement
        print 'Failed to run query: '+sql
        # rollback if there's a problem
        db.rollback()

        
pub_columns = ['PMID','title','first_author','last_author','journal','year']
list_columns = ['list_name','description','PMID']
gene_columns = ['locus_id','list_id']

tables = ['publications','list_info','gene_lists']

with open('phyA_chip_seq_list.txt','r') as f:
    input_file = f.readlines()

pub_info = input_file[0].strip().split('\t')
list_info = input_file[1].strip().split('\t')
gene_list = [x.strip() for x in input_file[2:]]

###TODO - assert correct format and types of strings

pub_sql = """INSERT INTO publications (PMID,title,first_author,last_author,journal,year)
        VALUES (%s,%s,%s,%s,%s,%s)"""

execute_sql_query(pub_sql,pub_info)

#check whether this list_name,description,PMID already exists

#if not,add it to list_info table
list_info_sql = """INSERT INTO list_info (list_name,description,PMID) VALUES (%s,%s,%s)"""
execute_sql_query(list_info_sql,list_info)

#get list id
"""SELECT list_id FROM list_info WHERE list_name=%s AND description=%s AND PMID=%i"""

#add gene list
