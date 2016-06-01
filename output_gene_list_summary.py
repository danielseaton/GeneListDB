import re
from connect_to_db import connect_to_db
import os
import pandas as pd

db = connect_to_db()
cursor = db.cursor()


gene_list = ['AT1G09570','AT1G09570']

with open('test_output.csv','w') as f:
    f.write('\t'.join(['locus_id','list_name','description','PMID'])+'\n')
    for gene_name in gene_list:
        
        ##check whether list has already been added
        #cursor.execute("""SELECT list_name FROM gene_lists WHERE locus_id=%s""",[gene_name])
        #result = [x[0] for x in cursor.fetchall()]
        #cursor.execute("""SELECT description,PMID FROM list_info WHERE list_name=%s""",result[:1])
        #result = cursor.fetchall()
                
        sql_query="""SELECT list_name,description,PMID 
             FROM list_info
             WHERE list_name IN (SELECT list_name 
                          FROM gene_lists
                          WHERE locus_id=%s)"""
        cursor.execute(sql_query,[gene_name])
        result = cursor.fetchall()
        for r in result:
            f.write('\t'.join([gene_name]+list(r))+'\n')


db.close()