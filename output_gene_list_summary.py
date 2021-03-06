import re
from connect_to_db import connect_to_db
import os
import pandas as pd

db = connect_to_db()
cursor = db.cursor()


#gene_list = ['AT1G09570','AT1G09570']

#directory = '/home/daniel/Dropbox/Work/Other projects/Toledo-Ortiz - RNA binding proteins/'
#filename = 'Atg cpRNPs.csv'
#write_filename = '
#df = pd.read_csv(directory+filename,header=None)
#gene_list = [x.upper() for x in df[0].tolist()]


#directory = '/home/daniel/Dropbox/Work/Circadian/Other projects/Phytocal/'
#filename='2016-04-13 genes for list name lookup_1.xlsx'
#write_filename = 'gene_lists_for_Johanna.tsv'
#df = pd.read_excel(directory+filename,sheetname='list of only accessions')
#gene_list = [x.upper() for x in df['accession'].tolist()]


#with open(directory+write_filename,'w') as f:
#    f.write('\t'.join(['locus_id','list_name','description','PMID'])+'\n')
#    for gene_name in gene_list:
#        
#        ##check whether list has already been added
#        #cursor.execute("""SELECT list_name FROM gene_lists WHERE locus_id=%s""",[gene_name])
#        #result = [x[0] for x in cursor.fetchall()]
#        #cursor.execute("""SELECT description,PMID FROM list_info WHERE list_name=%s""",result[:1])
#        #result = cursor.fetchall()
#                
#        sql_query="""SELECT list_name,description,PMID 
#             FROM list_info
#             WHERE list_name IN (SELECT list_name 
#                          FROM gene_lists
#                          WHERE locus_id=%s)"""
#        cursor.execute(sql_query,[gene_name])
#        result = cursor.fetchall()
#        for r in result:
#            f.write('\t'.join([gene_name]+list(r))+'\n')





####Modified code to include gene name

directory = '/home/daniel/Dropbox/Work/Circadian/Other projects/Phytocal/'
filename='2016-04-13 genes for list name lookup_1.xlsx'
write_filename = 'gene_lists_for_Johanna.tsv'
df = pd.read_excel(directory+filename,sheetname='with explanations')
df.dropna(subset=['accession'],inplace=True)
gene_list = df['accession'].tolist()
gene_symbols = df['name'].tolist()

with open(directory+write_filename,'w') as f:
    f.write('\t'.join(['symbol','locus_id','list_name','description','PMID'])+'\n')
    for gene_symbol,gene_name in zip(gene_symbols,gene_list):
        
        if re.search(u'\xdf',gene_symbol):
            gene_symbol = u'unicode error - unable to print'

        sql_query="""SELECT list_name,description,PMID 
             FROM list_info
             WHERE list_name IN (SELECT list_name 
                          FROM gene_lists
                          WHERE locus_id=%s)"""
        cursor.execute(sql_query,[gene_name])
        result = cursor.fetchall()
        for r in result:
            f.write('\t'.join([gene_symbol,gene_name]+list(r))+'\n')






db.close()