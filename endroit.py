# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 16:23:19 2021

@author: josse
"""

from psclib.lieu import Lieu
from psclib.objet import Objet


class Endroit:
    
    def __init__(self, objet = ""):
        self.posx = 0
        self.posy = 0
        self.objet = objet
        if type(self.objet) == str: self.objet = Objet(lib=self.objet)
        self.objet.isLieu = True
        self.action_possibles = []
        
    def get_lieu_suivant(self, personnage, heure):
        pass
    
    def get_evenement(self, personnage, heure):
        pass
    
    def get_lieu(self):
        return Lieu(lieu=self.objet, rapport="à")
    
    def arriver(self, personnage):
        self.personnagesPresent.append(personnage)