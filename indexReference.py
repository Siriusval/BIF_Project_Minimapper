# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 09:40:01 2020

@author: Valou
"""
class IndexReference:
    
    def __init__(self, text):
        self.text = text
        self.sa = self.getSA()
        self.bwt = self.bwt_from_sa()
         
         
    """
    getSuffixes
    return all suffixes of a string, in a list
    """
    def getSuffixes(self):
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
    
    def getSortedSuffixes(self,suffixes, reverse = False):
        return sorted(suffixes.items(), key=lambda x : x[1], reverse=reverse)
   
    """
    getSuffixesTable
    return only the indexes of the previously sorted suffix dict
    """
    def getSuffixesTable(self,sortedSuffixes):
        table = []
        for elem in sortedSuffixes:
            table.append(elem[0])
        return table
    
    """
    Full fonction
    Get all suffixes -> Sort them -> return SuffixArray
    """
    def getSA(self, rev = False):
        suffixes = self.getSuffixes()
        sortedSuffixes = self.getSortedSuffixes(suffixes,rev)
        suffixTable = self.getSuffixesTable(sortedSuffixes)
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
    def bwt_from_sa(self):
        sLength = len(self.sa)
        BWT = sLength*[0];
    
        for i in range (sLength):
            if self.sa[i] == 0:
                BWT[i] = '$'
            else :
                BWT[i] = self.text[self.sa[i]-1]
        return BWT