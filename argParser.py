import argparse 
#Manage arguments

'''
Parse the arguments of the function
ref : name of the reference file
reads : name of the reads file
k : seed size
dmax : max number of error for a read alignment
out : output file for result
'''
def argParse():
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
        required=True,
        type=int
    )
    parser.add_argument(
        '-dmax',
        help="Maximum number of differences (ex : 4)",
        required=True,
        type=int
    )
    parser.add_argument(
        '-out',
        help="Name of output file (ex : result-k15-dmax4.txt)",
        required=True
    )
    
    args = parser.parse_args()
    
    return args