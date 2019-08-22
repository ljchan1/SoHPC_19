#!/bin/python

#Written by Li Juan Chan in 15th August 2019 for the Summer of HPC 2019 program.
#This code sorts the time compilation file based on the type of catalyst pipeline and number of cores.

catalyst = ['no', 'oneslice', 'threeslices', 'clip', 'region', 'glyph_3D', 'glyph_front', 'glyph_top', 'streamline_front', 'streamline_top']
for pipeline in catalyst:
    target = []   #target is the targetted line for each pipeline
    with open('time_compile.txt','r') as file:
        for line in file:
            if line.split()[7] == pipeline:   #to find the lines that have the keyword of pipeline
                target.append(line)     #store those lines in target list
    ncores = list(int(target[x].split()[10]) for x in range(len(target)))   #extract the number of cores from each line from target list
    idx = [ncores.index(x) for x in sorted(ncores)]     #get the indices that can use to sort the lines according to the number of cores
    sortline = [target[y] for y in idx]        #sort the lines using the indices
    q = "".join(sortline)         #remove those lines from  the list and join them together
    with open('time_final.txt','a+') as f:       #write the sorted lines into file
        f.write('Pipeline: %s\n'%(pipeline))
        f.write(q)
        f.write('\n')
