#!/usr/bin/env python3

import os
import sys

data = []
with open("data.txt",'r') as file:
 for line in file:
  data.append(line.replace("\n", "").split(','))

 for idx in range(len(data)):
    one,two,three,four = data[idx]
  
    name = str(one).strip()
    email = str(two).strip() 
    marketvalue = str(three).strip()
    role = str(four).strip()
   
    idx += 1 
    print(name)
    print(email)
    print(marketvalue)
    print(role)
