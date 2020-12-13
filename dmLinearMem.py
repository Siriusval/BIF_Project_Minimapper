# In[0]:
# Optimized matrix (2 lines)     
'''
Class for DMLinearMem
stores a matrix |S|x2 (|S|+1 lines and 2), sequences S and T and the score system (match, mismatch, gap)
defines some semi-global alignment functions
'''
class DMLinearMem:

    def __init__(self, S, T, match, mismatch, gap):
        ''' defines and stores initial values'''
        
        self.S=S
        self.T=T
        self.gap=gap
        self.match=match
        self.mismatch=mismatch
        
        self.matrix = [MatrixValue(0,0) for i in range(len(S)+1)]
        for i in range(len(S)+1):
            self.matrix[i] = [MatrixValue(0,j) for j in range(2)]

    def score(self,cara1,cara2):
        '''return the score of a match if cara1 = cara2 and the score of a mismatch if they are differents'''
        if(cara1 == cara2):
            return self.match
        else :
            return self.mismatch
    
    def initSemiGlobal(self):
        '''do the initialisation for the semi-global alignement'''
        for i in range(1,len(self.S)+1):
            self.matrix[i][0].value = i*self.gap
            self.matrix[i][0].start = 0
        for j in range(2):
            self.matrix[0][j].value = 0
            self.matrix[0][j].start = j
    
    def getBestScore(self):
        '''fill the matrix'''
        #We use this variable to store the maximum, otherwise it would be erased // initialize at only gap
        minimumScore = len(self.S)*self.gap
        #We fill the matrix column by column instead of line by line like previously because otherwise the result would be erased
        for j in range(1,len(self.T)+1):
            for i in range(1,len(self.S)+1):
                #for the initialisation of the positions
                if(i==1):
                    self.matrix[0][(j+1)%2].start = j-1
                    self.matrix[0][(j)%2].start = j-2
                #We only have two space aviable so we use modulo for reach the values 
                #Score for diagonal
                scoreDiag = self.matrix[i-1][(j+1)%2].value + self.score(self.T[j-1],self.S[i-1])
                #Score for left
                scoreLeft = self.matrix[i][(j+1)%2].value + self.gap
                #Score for up
                scoreUp = self.matrix[i-1][j%2].value + self.gap
                self.matrix[i][j%2].value = min(scoreDiag,scoreLeft,scoreUp)
                
                #Update the starting position
                if scoreDiag == min(scoreDiag,scoreLeft,scoreUp):
                    self.matrix[i][j%2].start = self.matrix[i-1][(j+1)%2].start
                elif scoreLeft == min(scoreDiag,scoreLeft,scoreUp):
                    self.matrix[i][j%2].start = self.matrix[i][(j+1)%2].start
                else :
                    self.matrix[i][j%2].start = self.matrix[i-1][j%2].start
                    
                #We change the value of maximum only if we are in the last line
                if(i == len(self.S) and self.matrix[i][j%2].value < minimumScore):
                    minimumScore = self.matrix[i][j%2].value
                    pos = self.matrix[i][j%2].start
                    
        return minimumScore,pos

# In[1]:
# HELPER CLASS
'''
represents the value in the matrix
it store the current value of alignement and the index where the word starts
'''
class MatrixValue:
    
    def __init__(self, value, start):
        ''' defines and stores initial values'''
        self.value = value
        self.start = start
