#!/usr/bin/python3

def one():
  return 'To run all three terraform commands'

def two():
  return 'To run terraform init command'

def run_command(i):
  switcher = {
    1: one,
    2: two,
    3: lambda: 'three'
  }

  func = switcher.get(i, lambda: "Invalid Option")
  return func()
