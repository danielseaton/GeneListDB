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


cursor.execute("""SELECT count(*) FROM list_info WHERE list_name=%s AND description=%s AND PMID=%s""",list_info)
result_count = cursor.fetchall()[0][0]
if result_count == 0:
    list_info_sql = """INSERT INTO list_info (list_name,description,PMID) VALUES (%s,%s,%s)"""
    execute_sql_query(list_info_sql,list_info)
else:
    print "{0} already contained in database".format(list_info[0])

#get list id
cursor.execute("""SELECT list_id FROM list_info WHERE list_name=%s AND description=%s AND PMID=%s""",list_info)
result = cursor.fetchall()[0]
assert len(result)==1
list_id = result[0]

#check whether list_id is already present in database
cursor.execute("""SELECT count(*) FROM gene_lists WHERE list_id=%s""",[list_id])
result_count = cursor.fetchall()[0][0]
if result_count > 0:
    #delete previous results
    cursor.execute("""DELETE FROM gene_lists WHERE list_id=%s""",[list_id])


try:
    #add gene list
    for locus_id in gene_list:
        cursor.execute("""INSERT INTO gene_lists (locus_id,list_id) VALUES (%s,%s)""",[locus_id,list_id])
    db.commit()
except:
    db.rollback()