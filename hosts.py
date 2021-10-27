#!/usr/bin/env python3

hosts = open('/etc/hosts')

print(hosts.read())

print("current position is: {}".format(hosts.tell()))
print(hosts.read())

hosts.seek(0)
print("current position is: {}".format(hosts.tell()))
print(hosts.read())


print("File Closed? {} ".format(hosts.closed))

if not hosts.closed:
  hosts.close()

print("File Closed? {} ".format(hosts.closed))
