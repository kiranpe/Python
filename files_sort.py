#!/usr/bin/env python3

unsorted_file = 'animals.txt'
sorted_file = 'animals-sorted.txt'

animals = []

def sort_fun():
 try:
  with open(unsorted_file) as unsorted:
   for line in unsorted:
     animals.append(line)
   animals.sort()

  with open(sorted_file, 'w') as sorted:
   for animal in animals:
    sorted.write(animal)

  with open('animals-sorted.txt') as file:
   print(file.read())

 except:
  print("Could not fine {} file".format(unsorted_file))

sort_fun()
