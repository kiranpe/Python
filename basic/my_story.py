#!/usr/bin/env python3

def my_story():
    name = input("what is your name? ")
    gender = input("are you male/female? ")
    city = input("what city are you from? ")
    age  = input ("what is your age? ")
    job  = input("what is your current job? ")
  
    age  = int(age)

    the_story = create_story(name,city,age,job,gender)
    display_story(the_story)

def create_story(name,city,age,job,gender):
    if gender.lower() == 'male':
       his_or_her = 'His'
    elif gender.lower() == 'female':
       his_or_her = 'Her'
    else:
       his_or_her = '' 

    if gender.lower() == 'male':
       he_or_she = 'He'
    elif gender.lower() == 'female':
       he_or_she = 'She'
    else:
       he_or_she = ''

    if age >= 30:
       mess = "eligible for H1B Visa."
    else:
       mess = "not eligible for H1B."

    story = ("{0} is from {1}.\n"
             "{5} age is {2} and {6} is doing {3} job.\n"
             "and {6} is {4}".format(name,city,age,job,mess,his_or_her,he_or_she))

    return story
    
def display_story(story):
    print()
    print("Here is your story!!!")
    print()
    print(story)

my_story()
