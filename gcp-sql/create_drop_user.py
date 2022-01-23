#!/usr/bin/env python3

import os
import sys
import mysql.connector
from mysql.connector.constants import ClientFlag

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/home/kiran/devops/Terraform/Gcp/credentials.json"

config = {
    'user': 'root',
    'password': 'DB_PASS',
    'host': 'DB_PUBLICIP',
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': 'ssl/server-ca.pem',
    'ssl_cert': 'ssl/client-cert.pem',
    'ssl_key': 'ssl/client-key.pem'
}

def create_user():
  users = sys.argv[1:]
  
  print("Adding List of users to DB: \n",users)
  cnxn = mysql.connector.connect(**config)

  cursor = cnxn.cursor()

  for user in users:
    cursor.execute('select exists(select user from mysql.user where user="{}")'.format(user))
    out = cursor.fetchall()

    result=os.popen("echo '{}' | sed -e 's/\[(//g' -e 's/\,)]//g'".format(out)).read().strip()

    if int(result) == 1:
      print("\n{} User Already Exists in DB!!".format(user))
    else:
      cursor.execute('CREATE USER {}'.format(user)) 
      print("\nAdding User {} to DB!!".format(user))
      print("{} user newly added user to DB!".format(user))

  cnxn.close()

create_user()

def drop_user():
   users = sys.argv[1:] 
   
   cnxn = mysql.connector.connect(**config)
  
   cursor = cnxn.cursor()
  
   for user in users: 
     cursor.execute('DROP user {}'.format(user))
     print("\nDropping User {} from DB!! Cross Check in DB!!!".format(user))
     print("Done!")

   cnxn.close()

drop_user()
