import csv
import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()

with open('ranked_output.csv','r') as fin:
    dr = csv.DictReader(fin)
    fields = dr.fieldnames
    c.execute('drop table if exists ranked_output')
    c.execute('create table ranked_output ({})'.format(','.join('"{}"'.format(field) for field in fields)))
    for row in dr:
        c.execute('insert into ranked_output values ({})'.format(','.join('?' for _ in fields)), tuple(row[field] for field in fields))

conn.commit()
conn.close()

