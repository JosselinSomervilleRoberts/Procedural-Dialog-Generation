# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 17:42:08 2021

@author: josse
"""

from psclib.coeuraction import CoeurAction
from psclib.action import Action
from psclib.objet import Objet
import random

class Evenement:
    
    def __init__(self, action, liste_cods = None):
        self.action = action
        if type(self.action) == str: self.action = Action(name=self.action)
        self.liste_cods = liste_cods
        if type(self.liste_cods) == str: self.liste_cods = [self.liste_cods]
        
        
    def getCoeur(self, perso):
        if self.liste_cods is None or len(self.liste_cods) == 0:
            return CoeurAction(sujet=perso, action=self.action)
        else:
            return CoeurAction(sujet=perso, action=self.action, cod=Objet(lib=random.choice(self.liste_cods)))