import MySQLdb

db = MySQLdb.connect("localhost","root","zoomzoom","GeneListDB")
cursor = db.cursor()

setup_pub_schema = """CREATE TABLE publications (
                    PMID  VARCHAR(8),
                    title   VARCHAR(200),
                    first_author  VARCHAR(20),
                    last_author  VARCHAR(20),
                    year   YEAR(4) )"""

setup_list_info_schema = """CREATE TABLE list_info (
                    list_id  CHAR(8),
                    list_name  VARCHAR(60),
                    description  VARCHAR(1000),
                    PMID  VARCHAR(8))"""

setup_list_schema = """CREATE TABLE gene_lists (
                     locus_id CHAR(8),
                     list_id CHAR(8))"""

for sql in [setup_pub_schema,setup_list_info_schema,setup_list_schema]:
    try:
        #execute the sql command
        cursor.execute(sql)
        #commit changes
        db.commit()
    except:
        # rollback if there's a problem
        db.rollback()