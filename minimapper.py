# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 10:51:12 2020

@author: Valou
"""
# IMPORTS

import argparse #Manage arguments
from reference import Reference #Import class that can create bwt on a reference string
from dmLinearMem import DMLinearMem
from exactPatternIdentification import ExactPatternIdentification

# FUNCTIONS
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
 
def getSequence(filename="str"):
    input = open(filename,"r")
    input.readline() #skip first line
    sequence = input.readline()
    input.close()
    return sequence
    
def openReads(filename : str):
    stream = open(filename, "r")
    return stream

def getNextRead(stream):
    name = stream.readline()[1:].strip()
    if not name:
        return -1,-1
    content = stream.readline().strip()
    return name,content

def alignSemiGlobal(read,index,posSeedInRef,posSeedInRead,k,dmax):

    #getSubstring of ref for alignement
    startIndexReference = posSeedInRef - dmax - posSeedInRead #pos of anchor - dmax - number of char before the seed in the read
    startIndexReference = startIndexReference if startIndexReference > 0 else 0 
    
    endIndexReference = posSeedInRef + dmax + len(read) - posSeedInRead #pos of anchor + dmax + number of char after the seed in the read
    endIndexReference = endIndexReference if endIndexReference < len(index.text)-1 else len(index.text)-1 
    
    substringRef = index.text[startIndexReference:endIndexReference]
    dm = DMLinearMem(read,substringRef, 0, -1, -1)
    
    return dm.getBestScore()
    
def getBestSemiGlobalAlg(read : str,index : Reference,k : int,dmax : int, reverse : bool = False):
    
    if(reverse):
        read = reverseCompl(read)
        
    epi= ExactPatternIdentification(index)
    seeds = [read[i:i+k] for i in range(0, len(read)-k+1)]
    bestNbError = -1
    bestPos = -1
    for i in range(0,len(seeds)):
        seed = seeds[i]
        positions = epi.search(seed) #find positions of seed in Ref
        if(positions == -1): #seed not in reference, go to next seed
            continue
        
        for position in positions: #attention a ne pas retraiter une portion deja traitéé(liste tuple ?)
            nbError = alignSemiGlobal(read,index,position,i,k,dmax) # get nb error
            nbError = abs(nbError) #minus to pos
            
            #if first value
            if (bestNbError == -1):
                bestNbError = nbError
                bestPos = position 
            #else if less errors
            elif (nbError < bestNbError):
                bestNbError = nbError
                bestPos = position
    
    return bestNbError,bestPos

def appendResults(outputStream,readName:str,bestPos : int,isRevCompl:bool,bestScore:int):
    t = "\t"
    str =f'{readName}{t}{bestPos}{t}{"-" if isRevCompl else "+"}{t}{bestScore}{t}\n'
    outputStream.write(str)

def reverseCompl(sequence : str):
    buffer = ""
    compl = {
        "A": "T",
        "C": "G",
        "G": "C",
        "T": "A",
    }
    for i in range(len(sequence)-1,-1,-1):
       buffer += compl.get(sequence[i], "Err")
    
    return buffer
    
    
    
"""
Find the best alignments of all reads on a reference
output a text file with results
"""
def main():
    #Get arguments
    args = argParse()
    print("Args : ","\n",args,"\n")
    
    #create Index
    sequence = getSequence(args.ref)
    reference = Reference()
    reference.createIndex(sequence)
    print("Reference : ","\n",reference.text[:10],"...","\n")
    
    
    #open Reads
    readStream = openReads(args.reads)
    
    readName,readContent = getNextRead(readStream)
    print("First read :","\n",readName,readContent,"\n")
    print("RevCompl :","\n",reverseCompl(readContent),"\n")
    #outputStream
    outputStream = open(args.out, "w")


        
    while(readContent!= -1):
        print(readName,"(processing)")
        
        #Get best align for read
        bestNbError,bestPos = getBestSemiGlobalAlg(readContent,reference,args.k,args.dmax,False)#(score,pos)
        isRevCompl = False
        foundResult = bestNbError != -1
        
        #get best align for revComplement of read
        bestNbErrorRev,bestPosRev = getBestSemiGlobalAlg(readContent,reference,args.k,args.dmax,True)#(score,pos)
        foundResultRev = bestNbErrorRev != -1
        
        #if both found, return the one with less errors or closer to the left
        if(foundResult and foundResultRev):
            if((bestNbErrorRev < bestNbError) or (bestNbErrorRev == bestNbError and bestPosRev<bestPos)):
                bestNbError = bestNbErrorRev
                bestPos = bestPosRev
                isRevCompl = True
        #if only foundResultRev
        elif(foundResultRev):
            bestNbError = bestNbErrorRev
            bestPos = bestPosRev
            isRevCompl = True
        
        
        
        if((foundResult or foundResultRev) and bestNbError <= args.dmax):
            appendResults(outputStream,readName,bestPos,isRevCompl,bestNbError) #with tabs
        
        readName,readContent = getNextRead(readStream)

    outputStream.close()
    
    #print out file
    print()
    f = open(args.out,"r")
    print(f.read())
    f.close()


    
    
    

    
    
    
# MAIN CALL
main()