#!/bin/python

#Written by Li Juan Chan in 22th July 2019 for the Summer of HPC 2019 program.
#This code copies the value of the time output of each simulation and store it in a dedicated file.



import sys

#Read the value from time.out file which contains the time output of the latest simulation
with open('time.out','r') as p:
    a = p.read()

#Open the dedicated file and append the value in the required format.
with open('time_compile.txt','a+') as q:
    # q.write('The time require to run rhoPimple in %s cores is %s seconds.\n'%(sys.argv[1],a[:-1]))
    # q.write('The time require to run rhoPimple and produce 19 images in %s cores is %s seconds.\n'%(sys.argv[1],a[:-1]))
    q.write('The time require to run rhoPimple with %s catalyst in %s cores is %s seconds.\n'%(sys.argv[2],sys.argv[1],a[:-1]))
