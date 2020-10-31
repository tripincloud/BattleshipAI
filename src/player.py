from random import *
import Projet_stat_1 as ps
import boat
import time
import string
import bataille as bt
import numpy as np

def partie(joueur) :
        game = bt.Bataille()
        compteur = 0
        while (not game.victoire()) :
            compteur = compteur + 1
            print(compteur)
            joueur.joue_coup(game)

        return compteur

class randomPlayer() :

    def __init__(self) :
        self.name = "Random AI"

    def joue_coup(self, bataille) :

        x, y = randint(0, 9), randint(0, 9)

        casecible = bataille.joue((x, y))

        while (casecible <= -1) :

            x, y = randint(0, 9), randint(0, 9)
            casecible = bataille.joue((x, y))

        return casecible



class heuristicPlayer() :

    def __init__(self) :
        self.name = "Heuristic AI"
        self.next_attack = []
        self.successful_attack = []

    def joue_coup(self, bataille) :

        casecible = -1

        while casecible <= -1 :
            if len(self.next_attack) == 0 :
                x, y = randint(0, 9), randint(0, 9)
            else :
                x, y = self.next_attack.pop()

            casecible = bataille.joue((x, y))

        if casecible != 0 :

            self.successful_attack.append((x, y))
            compteur = 0
            for i, j in [(1, 0), (0, 1), (-1, 0), (0, -1)] :
                if (x + i, y + j) in self.successful_attack :
                    compteur = compteur + 1
                    self.next_attack.append((x + i * -1, y + j * -1))

            if compteur == 0 :
                self.next_attack.append((x, y + 1))
                self.next_attack.append((x + 1, y))
                self.next_attack.append((x - 1, y))
                self.next_attack.append((x, y - 1 ))
        return casecible

class simpleProbabilisticPlayer() :

    def __init__(self) :
        self.name = "Simplified probabilistic AI"
        self.rest = [(5, boat.specs[5][1]),(4, boat.specs[4][1]),(3, boat.specs[3][1]),(2, boat.specs[2][1]),(1, boat.specs[1][1])]
        self.probas = np.zeros((10,10),dtype=int)

    def joue_coup(self, bataille) :
        self.probas = np.zeros((10,10),dtype=int)

        decalage = 0
        boostproba  = 0
        peut_poser = False
        casecible = -1
        while (casecible <= -1) :

            for bateau in self.rest :
                if bateau[1] == 0 :
                    continue
                for i in range(10) :
                    for j in range(10) :
                        if bataille.get((i,j)) == -1 :
                            self.probas[i][j] = 0
                        else :
                            decalage = 0
                            boostproba = 0
                            if bataille.get((i,j)) == -2 :
                                boostproba = 1
                                self.probas[i][j] = 0
                                decalage = 1

                            peut_poser = True

                            for v in range(1, boat.specs[bateau[0]][1]) :
                                if not bataille.inside_grille((i+v,j)) or bataille.get((i+v, j)) == -1 :
                                    peut_poser = False
                                    break

                                if bataille.get((i+v, j)) == -2 :
                                        boostproba  = boostproba + 1

                            if peut_poser :
                                for v in range(decalage, boat.specs[bateau[0]][1]) :
                                    if bataille.get((i+v, j)) != -2 :
                                        self.probas[i+v][j] = self.probas[i+v][j] + 1 + boostproba * 2

                            peut_poser = True
                            for h in range(1, boat.specs[bateau[0]][1]) :
                                if not bataille.inside_grille((i,j+h)) or bataille.get((i, j+h)) == -1 :
                                    peut_poser = False
                                    break

                                if bataille.get((i, j+h)) == -2 :
                                    boostproba  = boostproba  + 1

                            if peut_poser :
                                for v in range(decalage, boat.specs[bateau[0]][1]) :
                                    if bataille.get((i, j+v)) != -2 :
                                        self.probas[i][j+v] += 1 + boostproba  * 2



            liste_probas = [
                    probabilite for sous_liste in self.probas
                            for probabilite in sous_liste
                                                    ]
            maxProba = max(liste_probas)
            x = liste_probas.index(maxProba)//10
            y = (liste_probas.index(maxProba)+10)%10
            casecible = bataille.joue((x, y))
        
        if casecible != 0 :
            for i in range(len(self.rest)) :
                if self.rest[i][0] == casecible :
                    self.rest[i] = (self.rest[i][0], self.rest[i][1] - 1)

        return casecible

class monteCarlo() :
        def __init__(self) :
                self.name = "Monte-Carlo AI"
                self.bateaux = [1,2,3,4,5]
                self.probas = np.zeros((10,10),dtype=int)

        def grilleProbaUpdater(self,grille,bateaux):
                grilleproba = np.zeros((10,10),dtype=float)
                for i in range(len(bateaux)):
                        for x in range(10):
                            for y in range(10):
                                if(ps.peut_placer(grille,bateaux[i],(x,y),1)):
                                    for t in range (boat.specs[bateaux[i]][1]):
                                        grilleproba[x][y+t] = grilleproba[x][y+t]+ 1
                                if(ps.peut_placer(grille,bateaux[i],(x,y),2)):
                                    for t in range (boat.specs[bateaux[i]][1]):
                                        grilleproba[x+t][y] = grilleproba[x+t][y]+ 1
        
                return grilleproba

        def maxGrille(self,grille):
                maximum = 0
                xMax =0
                yMax =0
                for x in range(10):
                    for y in range(10):
                        if(grille[x][y]>=maximum):
                            maximum = grille[x][y]
                            xMax =x
                            yMax =y
                return (xMax,yMax)   

        
        def heuristicSearch(self,x,y,grille,bataille):
                parcours_tab =[(0,1),(0,-1),(1,0),(-1,0)]
                cptTest=0
                tailleBateau=0
                trouve=False
                for i in range(4):
                    if not (trouve):
                        (xTest,yTest)=(x+parcours_tab[i][0],y+parcours_tab[i][1])
                        if((xTest<=9 and yTest<=9 and xTest>=0 and yTest>=0) and grille[xTest][yTest]==0):
                            res=bataille.joue((xTest,yTest))
                            grille[xTest][yTest]= -1
                            if(res == -3) :
                                trouve = True
                            if(res == -2 ):               
                                trouve = True
                                (xInit,yInit)=(x,y)
                                (x,y)=(xTest,yTest)
                        
                                while(res != -3):
                                    if(res == -1):
                                        (x,y)=(xInit,yInit)
                                        if(i%2==0):
                                            i+=1
                                        else:
                                            i-=1
                                    if(res == -2 ):
                                        tailleBateau = tailleBateau + 1
                                    x=x+parcours_tab[i][0]
                                    y=y+parcours_tab[i][1]
                                    if(x<=9 and y<=9 and x>=0 and y>=0):
                                        grille[x][y]=-1
                                        res = bataille.joue((x,y))                         
                                    else:
                                        res = -1                                                      
                                break
        
                tailleBateau+=1
                for i in range (1,6):
                    if tailleBateau == boat.specs[i][1]:
                        bateau=i
                        return (grille,bateau)
                return (grille,-1)

                
        def joue_coup(self, bataille) :
            self.probas = self.grilleProbaUpdater(bataille.grille,self.bateaux)          
            casecible = -1   
            cpt = 0 
            while (casecible <= -1 and casecible != -3):
                cpt=cpt+1
                #print("compteur: ",cpt)
                xM,yM = self.maxGrille(self.probas)
                if(bataille.grille[xM][yM] == 0):
                    casecible = bataille.joue((xM,yM))    
                    if(casecible == -1):
                        self.probas[xM][yM] = -1
                        bataille.grille[xM][yM] = -1
                    else:
                        self.probas[xM][yM] = 0
                        bataille.grille[xM][yM] = -1

                        (bataille.grille,bateau)=self.heuristicSearch(xM,yM,bataille.grille,bataille)
                        if(bateau > 0):
                            if(bateau not in self.bateaux):
                                bateau=4
                            casecible = boat.specs[bateau][1]
                            self.bateaux.remove(bateau)
                            bateau = 0                       
                    self.probas = self.grilleProbaUpdater(bataille.grille,self.bateaux)
    
            return casecible

player = randomPlayer()
player1 = heuristicPlayer()
player2 = simpleProbabilisticPlayer()
player3 = monteCarlo()
partie(player)







        
                
        
