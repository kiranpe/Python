#!/usr/bin/env python3

import os
import sys

data = []
with open("data.txt",'r') as file:
 for line in file:
  data.append(line.replace("\n", "").split(','))

 for idx in range(len(data)):
    lst = data[idx]
  
    name = lst[0].strip()
    email = lst[1].strip() 
    marketvalue = lst[2].strip()
    role = lst[3].strip()
   
    idx += 1 
    print(name)
    print(email)
    print(marketvalue)
    print(role)
