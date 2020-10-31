import random
import numpy as np


class Senseur():
    def __init__(self, n, p,repartition):
        self.matrice_proba = np.empty((n,p), dtype=float)
        self.c = (n+p)*50
        self.generate_random(n,p)
        if(repartition == 1):
            self.generate_centred(n,p)
        elif(repartition == 2):
            self.generate_borders(n,p)
        elif(repartition == 3):
            self.generate_left_flanc(n,p)

        self.place_senseur(n,p)
        print(self.pos)


    def div_n_show(self,n,p,mat):
        d = np.sum(mat,dtype=float)
        for i in range (n):
            for j in range (p):
                mat[i][j]= mat[i][j]/d
                
        print(mat)
        print(np.sum(mat,dtype=float))


    def generate_random(self,n,p):
        for i in range(n):
            for j in range(p):
                self.matrice_proba[i][j]=float(random.randint(0,self.c))
                
        self.div_n_show(n,p,self.matrice_proba)
                

    def generate_centred(self,n,p):
        for i in range(int(n/2),int(n/2+1)):
            for j in range(int(p/2),int(p/2+1)):
                self.matrice_proba[i][j]=float(random.randint(4*self.c,6*self.c))

        self.div_n_show(n,p,self.matrice_proba)

    def generate_borders(self,n,p):
        for i in [0,n-1]:
            for j in range(p):
                self.matrice_proba[i][j]=float(random.randint(3*self.c,4*self.c))
        for j in [0,n-1]:
            for i in range(n):
                self.matrice_proba[i][j]=float(random.randint(3*self.c,4*self.c))

        self.div_n_show(n,p,self.matrice_proba)

    def generate_left_flanc(self,n,p):
        for i in range(n):
            for j in range(2):
                if (j<p):
                    self.matrice_proba[i][j]=0

        self.div_n_show(n,p,self.matrice_proba)

    def place_senseur(self,n,p):
        s=0
        k = random.random()
        for i in range(n):
            for j in range(p):
                if (k < s + self.matrice_proba[i][j]):
                    self.pos=(i,j)
                    return None
                s = s + self.matrice_proba[i][j]
        print("Erreur place_senseur")
        return (-1,-1)


    def cherche(self,ps):
        compteur = 0
        while(True):
            compteur = compteur + 1
            (i,j) = np.unravel_index(np.argmax(self.matrice_proba),  self.matrice_proba.shape)
            if (i,j) == self.pos:
                k = random.random()
                if (k < ps):
                    print("Senseur trouvé en pos "+ str(self.pos))
                    return compteur
            self.matrice_proba = self.matrice_proba / (1 - self.matrice_proba[i][j]*ps)
            self.matrice_proba[i][j] = self.matrice_proba[i][j] * (1-ps)

s = Senseur(5,5,0)
print(s.cherche(0.1))
