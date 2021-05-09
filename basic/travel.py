#!/usr/bin/env python3

distance = input("How far would you like to travel in miles? ")

distance = int(distance)

if distance < 3:
   travel = "walking"
elif distance < 300:
   travel = "driving"
else:
   travel = "flying"

print ("I suggest {} to your destination.".format(travel))
