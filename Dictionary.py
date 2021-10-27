#!/usr/bin/env python3

facts = { 'jeff': 'Is afraid of clowns.', 'David': 'Plays the piano.', 'Jason': 'Can fly an airplane.' }

def fact_fun(facts):
    for fact in facts:
       print("{}: {}".format(fact, facts[fact]))
    print()

fact_fun(facts)

facts['jeff'] = 'Is afraid of heights.'
facts['jill'] = 'Can hula dance.'

fact_fun(facts)
