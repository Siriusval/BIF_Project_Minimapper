class DMLinearMem():
    '''
    stores a matrix 2x|T| (2 lines and |T|+1columns), sequences S and T and the score system (match, mismatch, gap)
    defines some semi-global alignment functions, with linear memory complexity 
    '''

    def __init__(self, S, T, match, mismatch, gap):
        ''' defines and stores initial values'''
        
        self.S=S
        self.T=T
        self.gap=gap
        self.match=match
        self.mismatch=mismatch
        
        #only 2 lines
        self.matrix = [0 for i in range(2)]
        
        #Init lines with 0
        for i in range(2):
            self.matrix[i] = [0 for j in range(len(T)+1)]
    
    def printLine(self,count):
        '''
        Print one line of the matrix
        if first line, print also T
        else print only second line after
        '''
        width = 4
        
        #Print headers
        if(count== 0):

            vide = " "
            line = f"{vide:>{2*width}}"
        
            for j in range(0,len(self.T)):
                line += f"{self.T[j]:>{width}}"
            print(line)

            line = f"{vide:>{width}}"
            
            #print first line (no letter)
            for j in range(0,len(self.T)+1):
                line += f"{self.matrix[0][j]:>{width}}"
            print(line)
            
        
        #print only second line
        line = f"{self.S[count]:>{width}}"
        for j in range(0,len(self.T)+1):
            line += f"{self.matrix[1][j]:>{width}}"
        print(line)
           
            
    def score(self, a : str, b : str) -> int :
        '''
        Compare two char
        Return match score if equals
        else return mismatch score 
        '''
        if(a == b):
            return self.match
        return self.mismatch
    
    def getBestScore(self,shouldPrint: bool = False):     
        '''
        Fill the matrix but only keep 2 lines in memory
        '''
        #While last char of S not reached
        count = 0
        while(count < len(self.S)):
            #Calc second line
            for j in range(1,len(self.T)+1):
                #calc best value
                delete = self.matrix[0][j] + self.gap
                insert = self.matrix[1][j-1] + self.gap
                match = self.matrix[0][j-1] + self.score(self.S[count],self.T[j-1])
                
                self.matrix[1][j] = max(delete,insert,match)
            
            #
            if (shouldPrint):
                self.printLine(count)
            
            #Copy second line to first
            self.matrix[0] = self.matrix[1]
                        
            #Reset second line
            self.matrix[1] = [0 for i in range(len(self.T)+1)]
            
            #Increment number of line done / letters of S
            count +=1
            
        return max(self.matrix[0])
                
            