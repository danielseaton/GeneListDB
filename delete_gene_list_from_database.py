import pandas as pd
import re
import sqlite3

#list_name = 'legnaoli2009_toc1_down'
#list_name = 'legnaoli2009_toc1_up'
list_name = 'zhang2009_otsBox_down'
#list_name = 'zhang2009_otsBox_up'

db = sqlite3.connect('GeneListDB.db')
cursor = db.cursor()

cursor.execute("DELETE FROM gene_lists WHERE list_name=?", (list_name,))
cursor.execute("DELETE FROM list_info WHERE list_name=?", (list_name,))

db.close()