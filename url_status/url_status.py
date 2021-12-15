#!/usr/bin/env python3

import os
import sys
import socket
import urllib.request

host=socket.gethostname()
port=sys.argv[1]
url=("http://" +host+ ":" +port+"/index.html")

print(url)

def check_url_status(url):
      try:
        status = urllib.request.urlopen(url).getcode()

        if not 'status' in '200':
          print("Nginx is Up and Running on host: {} with port: {}".format(host,port))
      except:
        print("Nginx on host: {} with port: {} is not running. Please correct the port or container is down.".format(host,port))

check_url_status(url)
