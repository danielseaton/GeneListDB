import pandas as pd
import re
import sqlite3

#list_name = 'legonaoli2009_toc1_down'
#list_name = 'legonaoli2009_toc1_up'

db = sqlite3.connect('GeneListDB.db')
cursor = db.cursor()

cursor.execute("DELETE FROM gene_lists WHERE list_name=?", (list_name,))