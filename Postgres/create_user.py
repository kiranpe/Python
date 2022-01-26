#!/usr/bin/python3

import psycopg2
import sys

table_name = "users"

# declare connection instance
conn = psycopg2.connect(
    dbname = "testdb",
    user = "postgres",
    host = "172.X.X.1",
    port = XXXX,
    password = "xxxxxx"
)

name = sys.argv[1]
email = sys.argv[2]
marketvalue = sys.argv[3]
role = sys.argv[4]

# declare a cursor object from the connection
cursor = conn.cursor()

#create db user
cursor.execute(f"insert into {table_name}(name,email,marketvalue,role) values('{name}','{email}','{marketvalue}','{role}');")
conn.commit()

# execute an SQL statement using the psycopg2 cursor object
cursor.execute(f"SELECT * FROM {table_name};")
out=cursor.fetchall()

# enumerate() over the PostgreSQL records
for row in enumerate(out):
    print(row)

# close the cursor object to avoid memory leaks
cursor.close()

# close the connection as well
conn.close()
