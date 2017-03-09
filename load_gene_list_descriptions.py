import re
import sqlite3
import os
import string


##### USER INPUT STARTS

#Specify the path to the data directory - this will be recursively searched
# for all files with the ".genelist" suffix.
home_dir = os.getenv('HOME')
data_directory = home_dir+"/Dropbox/Work/Circadian/Data/"

#Specify the path to the database file
database_file = 'GeneListDB.db'


##### USER INPUT ENDS




#Find genelists
genelist_file_list = []
for root, dirs, files in os.walk(data_directory):
    for file in files:
        if file.endswith(".genelist"):
             genelist_file_list.append(os.path.join(root, file))

#Connect to database
db = sqlite3.connect(database_file)
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
    
    #check where gene list starts
    if re.match('[Aa][tT][0-9CM][Gg][0-9]{5}',input_file[1].strip()):
        #only one header entry
        start_idx = 1
    else:
        #two header entries, so first entry is publication info
        pub_info = input_file[0].strip().split('\t')
        pmid,year = pub_info[0],pub_info[5]
        assert(re.match('[0-9]{4}',year))
        assert(re.match('[0-9]+',pmid))
        pub_sql = """INSERT INTO publications (PMID,title,first_author,last_author,journal,year)
                    VALUES (?,?,?,?,?,?)"""
        execute_sql_command(pub_sql,pub_info)
        start_idx = 2

    
    list_info = input_file[start_idx-1].strip().split('\t')
    list_name = list_info[0]
    gene_list = list(set([x.strip() for x in input_file[start_idx:]]))
    #convert any lowercase agi codes to uppercase
    gene_list = [string.upper(x) for x in gene_list]
        
    #check whether list has already been added
    cursor.execute("""SELECT count(*) FROM list_info WHERE list_name=? AND description=? AND PMID=?""",list_info)
    result_count = cursor.fetchall()[0][0]
    if result_count == 0:
        try:
            #insert list into list info
            cursor.execute("""INSERT INTO list_info (list_name,description,PMID) VALUES (?,?,?)""",list_info)
            for locus_id in gene_list:
                #only add if its a single locus id on its own
                if re.match(r'AT[0-9CM]G[0-9]{5}$',locus_id):
                    cursor.execute("""INSERT INTO gene_lists (locus_id,list_name) VALUES (?,?)""",[locus_id,list_name])
            db.commit()
            added_lists.append(list_name)
        except:
            failed_to_load_lists.append(list_name)
            db.rollback()
    else:
        already_present_lists.append(list_name)

print 'Already present:'
for x in already_present_lists:
    print x
print ''
print 'Added lists:'
for x in added_lists:
    print x
print ''
print 'Failed to load:'
for x in failed_to_load_lists:
    print x


db.close()