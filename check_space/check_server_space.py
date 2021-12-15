#!/usr/bin/env python3

import os
import socket
import shutil

host = socket.gethostname()
volumes = ["/", "/home", "/dev"]

def disk_usage():
 for volume in volumes:
  total, used, free = shutil.disk_usage(volume)

  print("Total: %d GiB" % (total // (2**30)))
  print("Free: %d GiB" % (free // (2**30)))
  print("Used: %d GiB" % (used / (2**30)))

  Used = (used // (2**30))

  if(Used > 10):
    print("{} volume is getting full on host: {}.. Please clean it up!!".format(volume,host))
  else:
    print("{} volume is Fine on this host: {}".format(volume,host)) 

disk_usage()
