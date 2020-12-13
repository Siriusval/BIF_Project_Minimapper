#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' sub-sample a read file + selects only certain reads + change headers in read[i]
    read selection :
        - skips the 50000 th first reads
        - no other letters than A,C,G,T
        - at least 100 nt of size
    outputs to stdout
'''

import sys

fasta_file = sys.argv[1]

NBreads = 10000
filin = open(fasta_file,"r")
counter = 0
i = 0
for line in filin:
    i += 1
    if i<2*50000:
        continue
    if line[0] !=">":
        line = line.rstrip("\n")
        if line.strip('ACGT') == '' and len(line)>=100:
            print(">read"+str(counter))
            print(line)
            counter += 1
            if counter>=NBreads:
                break
filin.close()

