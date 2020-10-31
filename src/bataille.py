import Projet_stat_1 as ps
import boat
class Bataille() :

    def __init__(self) :
        self.grille = ps.genere_grille()
        self.initialGrille = self.grille.copy()
        self.rest = [(5, boat.specs[5][1]),(4, boat.specs[4][1]),(3, boat.specs[3][1]),(2, boat.specs[2][1]),(1, boat.specs[1][1])]

        cases = 0
        for i in range(1, 6) :
            cases = cases + boat.specs[i][1]
        self.restcases = cases

    def joue(self, position) :

        if not self.inside_grille(position) :
            #print("cases:",self.restcases)
            return -1
        x, y = position
        cible = self.grille[x][y]

        if cible == 0 :
            self.grille[x][y] = -1
        elif cible > -1 :
            for i in range(len(self.rest)):
                if self.rest[i][0] == self.grille[x][y]:
                    self.restcases = self.restcases  -  1
                    self.grille[x][y] = -2
                    #print("cases:",self.restcases)
                    return -2
            self.restcases = self.restcases  -  1
            self.grille[x][y] = -2
            self.rest.remove(i)
            #print("cases:",self.restcases)
            return -3
        #print("cases:",self.restcases)
        return cible

    def victoire(self) :
        return self.restcases == 0


    def inside_grille(self, position) :
        x, y = position
        return x < len(self.grille) and x >= 0 and y < len(self.grille[0]) and y >= 0

    def reset(self) :
        self.grille=self.initialGrille

    def get(self,position) :
        x,y = position
        return self.grille[x][y]
