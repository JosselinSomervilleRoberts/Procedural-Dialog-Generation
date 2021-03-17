# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 16:23:19 2021

@author: josse
"""

from psclib.lieu import Lieu
from psclib.objet import Objet


class Endroit:
    
    def __init__(self, libelle = ""):
        self.posx = 0
        self.posy = 0
        self.libelle = libelle
        self.action_possibles = []
        
    def get_lieu_suivant(self, personnage, heure):
        pass
    
    def get_evenement(self, personnage, heure):
        pass
    
    def get_lieu(self):
        return Lieu(lieu=Objet(lib=self.libelle), rapport="à la")
    
    def arriver(self, personnage):
        self.personnagesPresent.append(personnage)