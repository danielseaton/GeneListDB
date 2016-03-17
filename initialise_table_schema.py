import MySQLdb

db = MySQLdb.connect("localhost","root","zoomzoom","GeneListDB")
cursor = db.cursor()

setup_pub_schema = """CREATE TABLE publications (
                    PMID  VARCHAR(8) NOT NULL PRIMARY KEY,
                    title   VARCHAR(200),
                    first_author  VARCHAR(20),
                    last_author  VARCHAR(20),
                    journal   VARCHAR(60),
                    year   CHAR(4) )"""

setup_list_info_schema = """CREATE TABLE list_info (
                    list_id  MEDIUMINT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    list_name  VARCHAR(60) NOT NULL,
                    description  VARCHAR(1000),
                    PMID  VARCHAR(8))"""

setup_list_schema = """CREATE TABLE gene_lists (
                     locus_id CHAR(9) NOT NULL,
                     list_id MEDIUMINT NOT NULL)"""

#for table_name in ['publications','list_info','gene_lists']:
#    try:
#        #execute the sql command
#        cursor.execute('DROP TABLE %s' % (table_name))
#        #commit changes
#        db.commit()
#    except:
#        # rollback if there's a problem
#        print "Failed to drop "+table_name
#        db.rollback()

for sql in [setup_pub_schema,setup_list_info_schema,setup_list_schema]:
    try:
        #execute the sql command
        cursor.execute(sql)
        #commit changes
        db.commit()
    except:
        print 'Failed to run query: '+sql
        # rollback if there's a problem
        db.rollback()