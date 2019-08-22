#!/bin/python

#Written by Li Juan Chan in 22th July 2019 for the Summer of HPC 2019 program.
#This code changes the number of processor cores in decomposeParDict file.

import sys

with open('decomposeParDict','r') as file:
    f = file.readlines()
    first = f[:17]   #get the top part
    last = f[18:]    #get the bottom part
    a = f[17][:20]
    b = ';\n'
    mid = a + sys.argv[1] + b    #join the middle part with the argument
    middle=[mid]     #turn middle part into a list to join all the parts
    total = first + middle + last
    j = "".join(total)   #turn it into a string to be written in a file
with open('decomposeParDict','w') as file:
    file.write(j)    #write into decomposeParDict file
