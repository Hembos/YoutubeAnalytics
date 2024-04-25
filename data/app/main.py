import psycopg2 as pg


conn = pg.connect(
   database="postgres", user='postgres', password='postgres', host='127.0.0.1', port= '5432'
)

conn.autocommit = True

cursor = conn.cursor()

sql = ''' CREATE database youtube '''
 
# executing above query
cursor.execute(sql)

conn.close()