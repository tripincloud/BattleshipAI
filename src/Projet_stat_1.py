import numpy as np
from random import *
import matplotlib.pyplot as matpp
import time
import boat

                #Partie 1

def peut_placer(grille, bateau, position, direction) :
    x,y = position
    h = 0
    v = 0
    if grille[x][y] != 0 :
        return False
    for i in range(boat.specs[bateau][1]) :
        if direction == 1 :
            h = i
        else :
            v = i
        if x+v >= (len(grille)) or y+h >= (len(grille[0])) or grille[x+v][y+h] != 0 :
            return False
    return True

def place(grille, bateau, position, direction) :
    x,y = position
    h = 0
    v = 0
    if peut_placer(grille,bateau,position,direction) :
        for i in range(boat.specs[bateau][1]) :
            if direction == 1 :
                h = i
            elif direction == 2 :
                v = i
            grille[x+v][y+h] = bateau
    return grille

def place_alea(grille, bateau) :
    x = randint(0,9)
    y = randint(0,9)
    d = randint(1,2)
    while not(peut_placer(grille,bateau,(x,y),d)) :
        x = randint(0,9)
        y = randint(0,9)
        d = randint(1,2)
    place(grille, bateau, (x,y), d)

def affiche(grille) :
    matpp.grid(True)
    matpp.imshow(grille)
    matpp.show()

def eq(grilleA, grilleB) :
    for x in range (len(grilleA)) :
        for y in range (len(grilleB)) :
            if grilleA[x][y] != grilleB[x][y] :
                return False
    return True

def genere_grille() :
    grille = [[0 for y in range(10)] for x in range(10) ]
    for i in range(1,6) :
        place_alea(grille,i)
    return grille

                #Partie 2

def grille_vide() :
    return [[0 for y in range(10)] for x in range(10)]

def copyGrille(grille) :

    new_Grille = grille_vide()
    for i in range(len(grille)) :
        for j in range(len(grille[0])) :
            new_Grille[i][j] = grille[i][j]
    return new_Grille

def pos_config_bateau(grille, bateau) :
    ways = 0
    for i in range(10):
        for j in range(10):
            if (peut_placer(grille, bateau, (i,j), 1)):
                ways=ways+1
            if (peut_placer(grille, bateau, (i,j), 2)):
                ways=ways+1
    return ways

#print (pos_config_bateau(grille_vide(),4))

def pos_config_des_bateaux(grille, bateaux) :

    ways = 0
    if len(bateaux) == 0 :
        return 1
    else :
        for i in range(10):
            for j in range(10):

                if (peut_placer(grille, bateaux[0], (i,j), 1)):

                    ways = ways + pos_config_des_bateaux(place(copyGrille(grille), bateaux[0], (i,j), 1), bateaux[1:])

                if (peut_placer(grille, bateaux[0], (i,j), 2)):

                    ways = ways + pos_config_des_bateaux(place(copyGrille(grille), bateaux[0], (i,j), 2), bateaux[1:])

        return ways

#listeboat=[4]
#print (pos_config_des_bateaux(grille_vide(),listeboat))

def GenerateGrilleBateaux(bateaux):

    grille = np.zeros((10,10),dtype=int)

    for i in bateaux:
        place_alea(grille, i)
    return grille

def RandomEqualGrille(grille, bateaux):

    Generated_Grille = GenerateGrilleBateaux(bateaux)

    compteur= 1

    while not eq(grille, Generated_Grille) :
        Generated_Grille = GenerateGrilleBateaux(bateaux)
        compteur = compteur + 1

    return compteur

listeboat2=[3,5,2,4,1]
#print (RandomEqualGrille(GenerateGrilleBateaux(listeboat2),listeboat2))

def approximationAlgorithm(bateaux) :

    nombre_grilles = 1
    grille = np.zeros((10,10),dtype=int)
    for i in bateaux :
        nombre_grilles = nombre_grilles * pos_config_bateau(grille, i)
    return nombre_grilles

print (approximationAlgorithm(listeboat2))

def approximationAlgorithmV2(bateaux) : #Bonus

    nombre_grilles = 1
    grille = np.zeros((10,10),dtype=int)
    for i in bateaux :
        nombre_grilles = nombre_grilles * pos_config_bateau(grille, i)
        place_alea(grille,i)
    return nombre_grilles
