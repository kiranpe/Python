#!/usr/bin/env python3

with open('new_file.txt', 'w') as the_file:
   the_file.write("Hello Kiran!! How is it going??\n")
   the_file.write("Keep going.. become expert in pyhton as well!!")

with open('new_file.txt') as the_file:
   print(the_file.read())

