#!/usr/bin/env python3

with open('/etc/hosts') as hosts:
   print("File Closed? {} ".format(hosts.closed))
   print(hosts.read())

print("File Closed? {} ".format(hosts.closed))
