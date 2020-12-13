#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' convert a multi-line fasta file to a 1 line fasta file (ie. each sequence is represented as a single line'''

import sys

fasta_file = sys.argv[1]

filin = open(fasta_file,"r")
sequence = ""
for line in filin:
    if line[0] ==">":
        if sequence != "":
            print(sequence)
        print(line.rstrip("\n"))
        sequence=""
    else:
        line = line.rstrip("\n")
        sequence += line
print(sequence)
filin.close()

