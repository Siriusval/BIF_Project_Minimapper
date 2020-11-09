# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 10:43:40 2020

@author: Valou
"""

from indexReference import IndexReference

class ExactPatternIdentification:
    
    def __init__(self, index : IndexReference):
        self.BWT = index.bwt
        self.SA = index.sa
        self.N, self.rank = self.__get_rank() #N -> liste d'occurences

    
    """
    Get rank from BWT
    
    BWT -> Burrrows Wheeler Transform
    
    return N -> number of occurrences for each char
           rank -> rank of each char
    """
    def __get_rank(self):
        bwtLength = len(self.BWT)
        rank = bwtLength *[0]
        N = dict()
    
        for i in range(bwtLength):
            char = self.BWT[i] #get each char in order
            if char not in N: #if char not in map already
                N[char] = 0
            
            N[char] += 1 #add one occurrence
            rank[i] = N[char]-1 #rank of this specific char is sum(occ of this char) -1
        return N, rank

    """
    LF(c,r,N)
    Find the position of a char with a specific rank in the F column
    
    c -> char to find
    r -> rank of this char
    N -> number of occurrences
    
    return the position of the character in F
    """
    
    def __LF (self,c, r):
        if c == '$':
            return 0
        alpha = ['$', 'A', 'C', 'G', 'T']
        alphaSize = len(alpha)
        skipIndex = 0
    
        for i in range(alphaSize):
            currentLetter = alpha[i]
            if currentLetter < c : #if the letter is before the searched char
          
                # add the number of occurences of the previous letter, 
                #ex, if we want C, and theres 100 A before, s = 100
                skipIndex += self.N[currentLetter]
            else:
                return skipIndex + r
            
    """
    Find first occurrence of a char in L(BWT) column
    
    char -> char to look for
    i -> index where the window start
    BWT -> BWT
    
    return i, the new inferior bound
    """
    def __find_first(self,c,i):
        #tant que i ne dépasse pas la fin de BWT
        #si le caractere est different, reduit la borne inf
        while i < len(self.BWT) and self.BWT[i] != c:
            i = i+1
    
        return i 
    
    """
    Find last occurrence of a char in L(BWT) column
    
    char -> char to look for
    j -> index where the window end
    BWT -> BWT
    
    return j, the new superior bound
    """
    def __find_last(self,c,j):
        #tant que j est toujours dans BWT
        #si le caractere est different, reduit la borne sup
        while j > -1 and self.BWT[j] != c:
            j = j -1
        
        return j
    
        """
    search a pattern in text thanks to BWT
    
    P -> pattern 
    BWT -> Burrows Wheeler Transform
    N -> occurrences for each different char
    rank -> rank of all chars
    
    return (i,j), the starting and ending position of all suffixes with the pattern
    """
    
    def search(self,P):
      
        pLength = len(P)
        #i
        startingIndex = self.__LF(P[pLength-1],0) #find the index of the last char of the pattern in F
    
        #the ending index is now 
        #the index of the first suffix beginning with a char
        # + all the occurences of this same char
        #j
        endingIndex = startingIndex + self.N[P[pLength-1]] -1 
    
        #(i,j) -> window of possible matchs, can only be reduced
    
        pos_p = pLength - 2 #position du char precedent
        #match = list()
    
        while pos_p >= 0: #tant qu'il reste des caracteres precedents
            #get first occ of previous letter in  L
            first = self.__find_first(P[pos_p],startingIndex)
    
            if first > endingIndex : #si on dépasse la fenetre, le pattern n'est pas contenu dans s
                return (-1,-1)
    
            # trouver l'index de la lettre precedente du pattern dans L
            #borne inf
            startingIndex = self.__LF(P[pos_p], self.rank[first]) #A, 2, occurrences[]
    
            #get last occ of preivous letter in L
            last = self.__find_last(P[pos_p],endingIndex)
    
            # trouver l'index de la lettre precedente du pattern dans L 
            #borne sup
            endingIndex = self.__LF(P[pos_p], self.rank[last]) #A, 3, occurrences[]
    
            pos_p = pos_p - 1 #go to previous char in pattern
    
        #return (startingIndex, endingIndex)
        return self.__listPos(startingIndex, endingIndex)
    
    
    """
    return a list of the positions of the pattern P in a text using SA
    """
    def __listPos(self,startingIndex, endingIndex):
        result = []
        for i in range(startingIndex, endingIndex + 1):
            result.append(self.SA[i])
        return sorted(result)

