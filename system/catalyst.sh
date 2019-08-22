#!/bin/python

#Written by Li Juan Chan in 12th August 2019 for the Summer of HPC program 2019.
#This code changes the name of the pipeline file in the catalyst file.

import sys

with open('catalyst','r') as file:
    f = file.readlines()  # Read the file
    first = f[:8]   # Store the top part
    last = f[9:]   # Store the bottom part
    midfirst = f[8][:26]
    midlast = '.py"\n'
    mid = midfirst + sys.argv[1] + midlast    # Join the middle part
    middle = [mid]   # Change the middle part into a list
    total = first + middle + last  # Join all the parts together
    j = "".join(total)   # Change the list in to a string
with open('catalyst','w') as file:
    file.write(j)   # Write into catalyst file
