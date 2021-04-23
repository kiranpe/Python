#!/usr/bin/python3

name = input("What's your name: ")
age = int(input("Please enter your age {0}: ".format(name)))

if age > 18:
   print("{0} age is {1}\nYou can Vote!!".format(name,age)) 
elif age < 18:
   print("Your age is {0} years low..Please come back after {0} years to Vote!!".format(18-age))
else:
   print("At age 18, you can Vote!!") 
