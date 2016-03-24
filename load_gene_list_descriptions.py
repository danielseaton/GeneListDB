import pandas as pd
import re
import MySQLdb
import os

#load all genelists
home_dir = os.getenv('HOME')
genelist_file_list = []
for root, dirs, files in os.walk(home_dir+"/Dropbox/Work/Circadian/Data/"):
    for file in files:
        if file.endswith(".genelist"):
             genelist_file_list.append(os.path.join(root, file))

db = MySQLdb.connect("localhost","root","zoomzoom","GeneListDB")
cursor = db.cursor()

def execute_sql_command(sql,parameters):
    try:
        #execute the sql command
        cursor.execute(sql,parameters)
        #commit changes
        db.commit()
    except:
        #TODO - elaborate on error information from execute statement
        print 'Failed to run SQL command: '+sql
        # rollback if there's a problem
        db.rollback()


for filename in genelist_file_list:
    with open(filename,'r') as f:
        input_file = f.readlines()
    
    pub_info = input_file[0].strip().split('\t')
    list_info = input_file[1].strip().split('\t')
    gene_list = list(set([x.strip() for x in input_file[2:]]))
    
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
            list_name = list_info[0]
            for locus_id in gene_list:
                cursor.execute("""INSERT INTO gene_lists (locus_id,list_name) VALUES (%s,%s)""",[locus_id,list_name])
            db.commit()
        except:
            print 'Failed to add list to DB: {0}'.format(*list_info)
            db.rollback()
    else:
        print "{0} already contained in database".format(list_info[0])