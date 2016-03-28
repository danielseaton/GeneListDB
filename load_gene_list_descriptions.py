import pandas as pd
import re
from connect_to_db import connect_to_db
import os
import string

#load all genelists
home_dir = os.getenv('HOME')
genelist_file_list = []
for root, dirs, files in os.walk(home_dir+"/Dropbox/Work/Circadian/Data/"):
    for file in files:
        if file.endswith(".genelist"):
             genelist_file_list.append(os.path.join(root, file))

db = connect_to_db()
cursor = db.cursor()

def execute_sql_command(sql,parameters):
    try:
        #execute the sql command
        cursor.execute(sql,parameters)
        #commit changes
        db.commit()
    except:
        #TODO - elaborate on error information from execute statement
#        print 'Failed to run SQL command: '+sql  #don't worry about this for now
        # rollback if there's a problem
        db.rollback()


added_lists = []
already_present_lists = []
failed_to_load_lists = []

for filename in genelist_file_list:
    with open(filename,'r') as f:
        input_file = f.readlines()
    
    pub_info = input_file[0].strip().split('\t')
    list_info = input_file[1].strip().split('\t')
    list_name = list_info[0]
    gene_list = list(set([x.strip() for x in input_file[2:]]))
    #convert any lowercase agi codes to uppercase
    gene_list = [string.upper(x) for x in gene_list]
    
    pmid,year = pub_info[0],pub_info[5]
    assert(re.match('[0-9]{4}',year))
    assert(re.match('[0-9]+',pmid))
    
    pub_sql = """INSERT INTO publications (PMID,title,first_author,last_author,journal,year)
            VALUES (%s,%s,%s,%s,%s,%s)"""
    execute_sql_command(pub_sql,pub_info)
    
    #check whether list has already been added
    cursor.execute("""SELECT count(*) FROM list_info WHERE list_name=%s AND description=%s AND PMID=%s""",list_info)
    result_count = cursor.fetchall()[0][0]
    if result_count == 0:
        try:
            #insert list into list info
            cursor.execute("""INSERT INTO list_info (list_name,description,PMID) VALUES (%s,%s,%s)""",list_info)
            for locus_id in gene_list:
                cursor.execute("""INSERT INTO gene_lists (locus_id,list_name) VALUES (%s,%s)""",[locus_id,list_name])
            db.commit()
            added_lists.append(list_name)
        except:
            failed_to_load_lists.append(list_name)
            db.rollback()
    else:
        already_present_lists.append(list_name)

print 'Added lists:'
for x in added_lists:
    print x
print ''
print 'Failed to load:'
for x in failed_to_load_lists:
    print x
print ''
print 'Already present:'
for x in already_present_lists:
    print x

db.close()