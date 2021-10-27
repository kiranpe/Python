#!/usr/bin/env python3

def file_fun():
  with open('file.txt') as the_file:
    line_number = 1
    for line in the_file:
      print("{} : {}".format(line_number, line.rstrip()))
      line_number += 1

file_fun()
      
