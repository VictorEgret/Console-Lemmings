# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 15:12:25 2021

@author: vegret
"""
class Lemming:
    # Classe représentant un lemming
    def __init__(self, x, y, direction, jeu):
        self.x = x
        self.y = y
        self.direction = direction
        self.jeu = jeu
        
    # Methode permettant de représenter le lemming  
    def __str__(self):
        if self.direction == -1:
            return '<'
        elif self.direction == 1:
            return '>'
        
    # Methode permettant au lemming de faire son prochain déplacement sur la carte    
    def action(self):
        bas = self.jeu.grotte[self.y+1][self.x]
        direction = self.jeu.grotte[self.y][self.x + self.direction]

        if bas.estLibre():
            self.jeu.grotte[self.y][self.x].depart()
            self.y += 1
            self.jeu.grotte[self.y][self.x].arrivee(self)
            return

        if direction.estLibre():
            self.jeu.grotte[self.y][self.x].depart()
            self.x += self.direction
            self.jeu.grotte[self.y][self.x].arrivee(self)
            return
            
        else:    
            self.direction = -self.direction
        return self.x, self.y
        
    # Methode qui retire le lemming de la partie
    def sort(self):
        self.jeu.lemmings.remove(self)
        
    # Methode qui change la direction du lemming    
    def changeDir(self):
        self.direction = -self.direction
        return self.direction
                
class Case:
    # Classe représentant une case de la carte
    def __init__(self, terrain, jeu, lemming=None):
        self.terrain = terrain
        self.jeu = jeu
        self.lemming = lemming
        
    # Methode permettant de représenter la case graphiquement    
    def __str__(self):
        if self.lemming == None:
            return self.terrain
        else:
            return self.lemming.__str__()
    
    # Methode qui permet de savoir si la case est libre
    def estLibre(self):
        return self.lemming == None and not self.terrain == '#'
    
    # Enleve le lemming de la case
    def depart(self):
        self.lemming = None
        
    # Met un lemming donné dans la case    
    def arrivee(self, lem):
        if self.terrain == '0':
            self.depart()
            lem.sort()
            self.jeu.finir()
        else:
            self.lemming = lem
        
class Jeu:
    # Classe permettant le chargement d'une carte et la gestion d'une partie
    def __init__(self, grotte, lemmings=[]):
        with open(grotte + ".txt") as f:
            terrain = []
            while 1:
                line = f.readline()
                if line == '':
                    break
                terrain.append([Case(char, self) for char in line if not char == "\n"])
        self.grotte = terrain
        self.lemmings = lemmings
        self.estFinie = False
        
        # Trouve la 1ere case vide en partant du haut
        self.firstCase = {"x": 0, "y": 0}
        for lvl in self.grotte:
            self.firstCase['x'] = 0
            for case in lvl:
                if case.__str__() == ' ':
                    return
                self.firstCase['x'] += 1
            self.firstCase['y'] += 1              
        
    # Affiche la carte    
    def afficher(self):
        for lvl in self.grotte:
            print(str([case.__str__() for case in lvl]).replace('[', '').replace(']', '').replace('\'', '').replace(',', ''))
        return self.grotte
    
    # Fait agir chaque lemming en jeu
    def tour(self):
        for lemming in self.lemmings:
            lemming.action()
        self.afficher()
        
    # Change la direction de chaque lemmings    
    def changeLemmingsDir(self):
        for lemming in self.lemmings:
            lemming.changeDir()
        self.afficher()
        
    # Met fin à la partie    
    def finir(self):
        self.estFinie = True
        print("Un lemming a atteint la sortie")
        
    # Démarre la partie    
    def demarre(self): 
        while not self.estFinie:
            cmd = input("Liste des commandes:\n- Q : Quitter\n- 1 : Ajouter un Lemming\n- T : Jouer un tour\n- A : Afficher la carte\n- D : Changer la direction des lemmings\n").upper()
            if cmd == 'Q':
                print("Partie terminée")
                break
            elif cmd == '1':
                if self.grotte[self.firstCase["y"]][self.firstCase["x"]].estLibre():
                    print("Un lemming a été ajouté")
                    newLemming = Lemming(self.firstCase["x"], self.firstCase["y"], 1, self)
                    self.lemmings.append(newLemming)
                    self.grotte[newLemming.y][newLemming.x].arrivee(newLemming)
                else:
                    print("Il y a un lemming sur la case de départ")
                self.afficher()
            elif cmd == 'T':
                self.tour()
            elif cmd == 'A':
                self.afficher()
            elif cmd == 'D':
                self.changeLemmingsDir()
            else:
                print("Mauvaise commande")

# On créé un jeu ayant pour carte le fichier "map" puis on le démarre
game = Jeu("map")
game.demarre()
