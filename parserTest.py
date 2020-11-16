# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 10:05:03 2020

@author: Valou
"""
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '-ref',
    help="Reference sequence (ex : genome.fasta)",
    required=True,
    metavar="REFERENCE"
)
parser.add_argument(
    '-reads',
    help="Patterns to align (ex : reads.fasta)",
    required=True
)
parser.add_argument(
    '-k',
    help="Seed size (ex : 15)",
    required=True
)
parser.add_argument(
    '-dmax',
    help="Maximum number of differences (ex : 4)",
    required=True
)
parser.add_argument(
    '-out',
    help="Name of output file (ex : result-k15-dmax4.txt)",
    required=True
)

args = parser.parse_args()

print("ref :",args.ref)
print("reads :",args.reads)
print("k :",args.k)
print("dmax :",args.dmax)
print("out :",args.out)
