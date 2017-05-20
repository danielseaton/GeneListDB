import sqlite3

##### USER INPUT STARTS
#Specify the database file to be initialised
database_file_path = 'GeneListDB.db'
##### USER INPUT ENDS

db = sqlite3.connect(database_file_path)
cursor = db.cursor()

setup_pub_schema = """CREATE TABLE publications (
                    PMID  VARCHAR(8) NOT NULL PRIMARY KEY,
                    title   VARCHAR(200),
                    first_author  VARCHAR(20),
                    last_author  VARCHAR(20),
                    journal   VARCHAR(60),
                    year   CHAR(4) )"""

setup_list_info_schema = """CREATE TABLE list_info (
                    list_name  VARCHAR(60) NOT NULL PRIMARY KEY,
                    description  VARCHAR(1000),
                    PMID  VARCHAR(8))"""

setup_list_schema = """CREATE TABLE gene_lists (
                     locus_id CHAR(9) NOT NULL,
                     list_name VARCHAR(60) NOT NULL)"""

index_by_list_name = """CREATE INDEX index_by_list_name ON gene_lists (list_name)"""
index_by_locus_id = """CREATE INDEX index_by_locus_id ON gene_lists (locus_id)"""

for sql in [setup_pub_schema,
            setup_list_info_schema,
            setup_list_schema,
            index_by_list_name,
            index_by_locus_id]:
    try:
        #execute the sql command
        cursor.execute(sql)
        #commit changes
        db.commit()
    except:
        print 'Failed to run query: '+sql
        # rollback if there's a problem
        db.rollback()

db.close()