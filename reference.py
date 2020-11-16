# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 09:40:01 2020

@author: Valou
"""
import pickle
import gzip

class Reference:
    
    def __init__(self):
        self.text = None
        self.sa = None
        self.bwt = None

    """
    createIndex
    index a string and create SA and BWT 
    """         
    def createIndex(self, text):
        self.text = text
        self.sa = self.__getSA()
        self.bwt = self.__bwt_from_sa()

    """
    save
    Save the current Reference Object into a zip
    """
    def save(self,filename):
        #pickle.dump(index, open("myobjectIndex.dumped","wb"))
        pickle.dump(self, gzip.open(f'{filename}.dumped.gz', "wb"))

    """
    load
    Load a zip into a Reference Object
    """
    def load(self,filename):
        #Charger
        #index = pickle.load(open("myobjectIndex.dumped","rb"))
        ref = pickle.load(gzip.open(f'{filename}.dumped.gz', "rb"))
        self.text = ref.text
        self.sa = ref.sa
        self.bwt = ref.bwt
    
    """
    getSuffixes
    return all suffixes of a string, in a list
    """
    def __getSuffixes(self):
        suffixes = {}
        size = len(self.text)
        for i in range(size):
            suffixes[i] = self.text[i:]
        return suffixes
    
    """
    getSortedSuffixes
    return the list of suffixes ordered alphabetically ($<A<C<G<T)
    suffixes -> list of the suffixes to order
    """
    
    def __getSortedSuffixes(self,suffixes, reverse = False):
        return sorted(suffixes.items(), key=lambda x : x[1], reverse=reverse)

    """
    getSuffixesTable
    return only the indexes of the previously sorted suffix dict
    """
    def __getSuffixesTable(self,sortedSuffixes):
        table = []
        for elem in sortedSuffixes:
            table.append(elem[0])
        return table
    
    """
    Full fonction
    Get all suffixes -> Sort them -> return SuffixArray
    """
    def __getSA(self, rev = False):
        suffixes = self.__getSuffixes()
        sortedSuffixes = self.__getSortedSuffixes(suffixes,rev)
        suffixTable = self.__getSuffixesTable(sortedSuffixes)
        return suffixTable
    
    """
    Get BWT from SA
    BWT[i]     =    S[SA[i] -1] if SA[i] > 0
                    $           if SA[i] = 0
    
    S -> Text to search
    SA -> Suffix Array
    
    return Burrows Wheeler Transform, 
                aka list of last column of char in ordered circular suffixes
    """
    def __bwt_from_sa(self):
        sLength = len(self.sa)
        BWT = sLength*[0];
    
        for i in range (sLength):
            if self.sa[i] == 0:
                BWT[i] = '$'
            else :
                BWT[i] = self.text[self.sa[i]-1]
        return BWT