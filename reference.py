from karkkainan import simple_kark_sort
import pickle
import gzip

class Reference:
    '''An object witch discribe the indexed sequence'''
    
    def __init__(self):
        self.text = None
        self.sa = None
        self.bwt = None
        self.N = None
        self.rank = None

    """
    createIndex
    index a string and create SA and BWT 
    """         
    def createIndex(self, text):
        self.text = text+"$"
        self.sa = self.__getSA()
        self.bwt = self.__bwt_from_sa()
        (N,rank) = self.get_N_and_rank(self.bwt)
        self.N = N
        self.rank = rank
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
        (N,rank) = self.get_N_and_rank(self.bwt)
        self.N = N
        self.rank = rank
    
    
    """
    Use the function of tp3 / karkkainan
    """
    def __getSA(self, rev = False):
        return simple_kark_sort(self.text)
    
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
    
    '''
    retourne N et rank qui correspondent respectivement au nombre d'occurences pour chaque lettre dans s et le rang de la lettre bwt[i]
    '''
    def get_N_and_rank(self,bwt) :
        rank = [0]*len(bwt)
        N = dict()
        for i in range(len(bwt)):
            caractere = bwt[i]
            #si caractere n'est pas dans le dictionnaire, le rajouter.
            if not(caractere in N):
                N[caractere] = 0
            #incrementation du nombre de caractere
            N[caractere] += 1
            #rank mis à jour commencant a 0
            rank[i] = N[caractere] - 1
        return N, rank
    
    '''
    retourne la liste des index des occurences de p dans s
    '''
    def P_in_S(self,P):
        m = len(P)
        # inf (resp sup) est la borne inferieure (resp superieure) dans F du caractere courant (dans P)
        inf = self.lf(P[m-1], 0)
        sup = inf + self.N[P[m-1]] - 1
        pos_p = m - 2
        while pos_p > -1:
            first = self.find_first(P[pos_p], inf)
            if first > sup :
                #dans ce cas on est sorti des limites inf et sup ce qui signifie que le mot recherche n'est pas dans s
                return []
            # pas besoin de verification ici : last sera au moins first
            last = self.find_last(P[pos_p], sup)
            inf = self.lf(P[pos_p], self.rank[first])
            sup =self.lf(P[pos_p], self.rank[last])
            pos_p -= 1
        result = []
        for i in range(inf, sup + 1):
            result.append(self.sa[i])
        return sorted(result)
    
    '''
    renvoie la position dans F du caractere c de rang r (dans bwt) On suppose que la lettre et le rang existe dans s
    '''
    def lf(self,c, r):
        #les suffixes etant tries par ordre croissant le premier caractere est toujours $
        if c == '$':
            return 0
        #la liste des lettres de l'alphabet triee par order lexicographique
        alpha = ['$','A','C','G','T']
        n = len(alpha)
        position = 0
        i = 0
        while alpha[i] < c and i < n:
            #la position, F etant triee par ordre lexicographique sera la somme de toutes les occurences des lettres precedantes plus son rang
            position += self.N[alpha[i]]
            i += 1
        return position + r
    
    '''
    trouve l'index du premier caractere c a partir de inf jusqu'au dernier de bwt
    '''
    def find_first(self,c, inf):
        while inf < len(self.bwt) and c != self.bwt[inf]:
            inf += 1
        return inf
    
    '''
    trouve l'index du dernier caractere c a partir de sup jusqu'a 0 dans bwt
    '''
    def find_last(self,c, sup):
        while sup > -1 and c != self.bwt[sup]:
            sup -= 1
        return sup