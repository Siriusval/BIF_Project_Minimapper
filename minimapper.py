#!/usr/bin/env python
# coding: utf-8
"""
Created on Mon Nov 16 10:51:12 2020

@author: Alban Gutierrez_Andre
@author: Valentin Hulot
"""
# In[0]:

# IMPORTS
from os import path # allow access to files
from reference import Reference # Manage operations on genome
from timer import Timer # Time execution of function
from argParser import argParse # Manage argument of program
from dmLinearMem import DMLinearMem # Manage matrix and semiGlobal alignment


# In[1]:
# OPEN GENOME

'''
Get the sequence from the reference file
filename -> the name of the reference file
return str, the string that represents the sequence
'''
def getSequence(filename:str):
    input = open(filename,"r")
    input.readline() #skip first line
    sequence = input.readline().strip()
    input.close()
    return sequence


# In[2]:
# OPEN READS

'''
Get the stream on the reads file
Allows us to get the next read when we need
filename -> name of the read file
return the stream on the reads file
'''
def openReads(filename : str):
    stream = open(filename, "r")
    return stream


'''
Get the next read in the reads file
stream -> the stream on the reads file
return (name,content) the name of the read and the string that represents it
'''
def getNextRead(stream):
    name = stream.readline()[1:].strip()
    if not name:
        return -1,-1
    content = stream.readline().strip()
    return name,content


# In[3]:
# ALIGN READ ON REF

'''
from a seed, return the index of the genome to align the read on
read -> the read to align
indexedReference -> the indexed reference
posSeedInRef -> index of the seed in the reference (when aligned)
posSeedInRead -> index of the seed in the read
dmax -> max number of error 
return (startIndex, endIndex), the portion of the reference to index on
'''
def getAlignIndex(read,indexedReference,posSeedInRef,posSeedInRead,dmax):
    #getSubstring of ref for alignement
    startIndexReference = posSeedInRef - dmax - posSeedInRead #pos of anchor - dmax - number of char before the seed in the read
    startIndexReference = startIndexReference if startIndexReference > 0 else 0 
    
    endIndexReference = posSeedInRef + dmax + len(read) - posSeedInRead #pos of anchor + dmax + number of char after the seed in the read
    endIndexReference = endIndexReference if endIndexReference < len(indexedReference.text) - 1 else len(indexedReference.text) - 1 
    
    return (startIndexReference,endIndexReference)

'''
align a read on the reference, based on the seed that was exactly aligned
read -> the read to align
indexedReference -> the indexed reference object
startIndexReference -> start of the sub-portion of the ref to use
endIndexReference -> end of the sub-portion of the ref to use
return (score,pos) the best score and the position of the semi global alignment
'''
def alignSemiGlobal(read,indexedReference,startIndexReference,endIndexReference):

    substringRef = indexedReference.text[startIndexReference:endIndexReference+1]
    dm = DMLinearMem(read,substringRef, 0, 1, 1)
    dm.initSemiGlobal()
    score,pos = dm.getBestScore()
    pos = pos + startIndexReference
    
    return score,pos

'''
do multiple alignment of read on reference
get the best semi global alignement
read -> the read to align
indexedReference -> the indexed reference object
k -> size of seed
dmax -> max number of error
return (bestScore, bestPos), the best alignment of read on ref
'''
def getBestSemiGlobalAlg(read,indexedReference,k,dmax):
    #epi= ExactPatternIdentification(index)
    seeds = [read[i:i+k] for i in range(0, len(read) - k + 1)]
    bestScore = len(read)
    bestPos = -1
    # A list of the previous positions  
    previousPositions = []
    #for all seed
    for i in range(0,len(seeds)):

        seed = seeds[i]
        positions = indexedReference.P_in_S(seed) #find positions of seed in Ref
        #for each positions of a seed
        for position in positions: #attention a ne pas retraiter une portion deja traitéé(liste tuple ?)

            # get start index
            (startIndex, endIndex) = getAlignIndex(read,indexedReference,position,i,dmax)
            #if read not !already aligned
            if(not (startIndex in previousPositions)):
                score,pos = alignSemiGlobal(read,indexedReference,startIndex,endIndex)
                previousPositions.append(startIndex)
            
            if score == 0 :
                return score,pos
            if (score < bestScore):
                bestScore = score
                bestPos = pos
    
    return bestScore,bestPos


# In[4]:
# RESULTS OUTPUT

'''
append a line with results on the output file
outputStream -> fileStream to write in
bestPos -> pos of best alignment
isRevCompl -> + if normal, - if reverse complement
bestScore -> score of best alignment
'''
def appendResults(outputStream,readName:str,bestPos : int,isRevCompl:bool,bestScore:int):
    t = "\t"
    str =f'{readName}{t}{bestPos}{t}{"-" if isRevCompl else "+"}{t}{bestScore}\n'
    outputStream.write(str)


# In[5]:
# REVERSE COMPLEMENT
'''
Return the reveres complement of a string
sequence -> sequence to reverse
return str, the reverse complement of the sequence
'''
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


# In[6]:
# MAIN

'''
Find the best alignments of all reads on a reference
output a text file with results
'''
def main():
    #Get arguments
    args = argParse()
    print("- ARGS :")
    print(args,"\n")
    
    
    #create indexedReference    
    print("- REFERENCE :")
    reference = Reference()
    #check if already indexed
    fileName = path.splitext(args.ref)[0]
    # retrieve from .gz
    if(path.exists(fileName+".dumped.gz")):
        reference.load(fileName)
        print("reference loaded from dumped.gz")
    #index sequence
    else:
        sequence = getSequence(args.ref)
        reference.createIndex(sequence) 
        reference.save(fileName)
        print("reference indexed and saved")

    print("DEBUG",reference.N)       
    print("Reference : ","\n",reference.text[:10],"...","\n")
    #open Reads
    print("- READS :")

    readStream = openReads(args.reads)
    readName,readContent = getNextRead(readStream)
    print("First read :",readName,readContent)
    print("RevCompl :",reverseCompl(readContent),"\n")
    #outputStream
    outputStream = open(args.out, "w")


    #Start the timer
    print("- FINDING ALIGNEMENT :")
    with Timer() as total_time:
        while(readContent!= -1):
            print(readName,"(processing)")
            isRevCompl = False
            bestScore,bestPos = getBestSemiGlobalAlg(readContent,reference,args.k,args.dmax)
            bestScoreRev,bestPosRev = getBestSemiGlobalAlg(reverseCompl(readContent),reference,args.k,args.dmax)


            #if the reverse search is better we take it
            if(bestScoreRev < bestScore):
                bestScore,bestPos = bestScoreRev,bestPosRev
                isRevCompl = True
    
            #Found a result
            if(bestScore != len(readContent)):
                if bestScore <= args.dmax:
                    appendResults(outputStream,readName,bestPos,isRevCompl,bestScore) #with tabs
            
            readName,readContent = getNextRead(readStream)
    
    total_time.print('\nIt tooks {} secondes.',5)
    print()

        

    outputStream.close()
    
    #print out file
    print("- RESULTS :")
    f = open(args.out,"r")
    print(f.read())
    f.close()
    print("exported in:",args.out)


# In[7]:
'''
MAIN
'''
main()




