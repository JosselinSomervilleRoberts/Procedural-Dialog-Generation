# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 00:24:13 2020

@author: josse
"""


CAUSE = 1
CONSEQUENCE = 2
SUITE = 3


#HEY c ets joss
# test 2
# Les liens entre les coeurs
class Lien :

  def __init__ (self, coeur = None, typeLien = None):
    self.coeur = coeur # Objet Coeur vers lequel le lien pointe : ??? -> lien -> coeur
    self.typeLien = typeLien # Entier identifiant le type de lien (CAUSE = 1, CONSEQUENCE = 2, SUITE = 3)