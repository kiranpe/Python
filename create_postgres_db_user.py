#!/usr/bin/env python3

import os
import sys
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_table = your-db-table-to-add-user
table_name = your-table-name
db_user = your-user
db_pass = your-pass-word
db_name = your-dbname

url=(f'postgresql+psycopg2://{db_user}:{db_pass}@cloud-sql-proxy:5432/{db_name}')

engine = create_engine(url)
Session = sessionmaker(engine)

with Session() as conn:
 data = []
 with open("/app/users.txt", 'r') as file:
    for line in file:
        data.append(line.replace("\n","").split(','))

    for idx in range(len(data)):
        lst = data[idx]

        name = lst[0]
        email = lst[1].strip()
        role = lst[2].strip()

        #create db user
        db_command = (f"INSERT {db_table}('{name}','{email}','{role}');")
        print(db_command)

        conn.execute(db_command)
        conn.commit()

result = conn.execute(f"SELECT * FROM {table_name};")

for row in result.fetchall():
  print(row)

conn.close()
