#!/usr/bin/env python3
#How to Run
#

import os
import sys
import json
import mysql.connector
from mysql.connector.constants import ClientFlag

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/kiran/devops/Terraform/Gcp/credentials.json"

with open("db_details.json") as file:
  data = json.load(file)
  db_user = (data['host_details'][0]['DB_USER'])
  db_pass = (data['host_details'][0]['DB_PASS'])
  db_host = (data['host_details'][0]['DB_HOST'])
  ssl_ca_cert = (data['host_details'][0]['SSL_CA'])
  ssl_client_cert = (data['host_details'][0]['SSL_CRT'])
  ssl_client_key = (data['host_details'][0]['SSL_KEY'])

config = {
    'user': db_user,
    'password': db_pass,
    'host': db_host,
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': ssl_ca_cert,
    'ssl_cert': ssl_client_cert,
    'ssl_key': ssl_client_key
}

def create_user():
  db = sys.argv[1]
  name = sys.argv[2]
  user_email = sys.argv[3]
  market_code = sys.argv[4]
  
  db_table = sys.argv[5]
  
  print("Adding User {} to {} DB!!\n".format(name,db))
  cnxn = mysql.connector.connect(**config)

  cursor = cnxn.cursor(buffered=True)
  cursor.execute('use {}'.format(db))
  #cursor.execute('create table {} (user VARCHAR(50), email VARCHAR(50), marketValue VARCHAR(50))'.format(db_table))
  
  cursor.execute('insert into {} (user,email,marketValue) values("{}","{}","{}")'.format(db_table,name,user_email,market_code))

  cnxn.commit()
  
  cursor.execute('select * from {}'.format(db_table))

  out = cursor.fetchall()
  
  for row in out: 
    print(row)

  cnxn.close()

create_user()
