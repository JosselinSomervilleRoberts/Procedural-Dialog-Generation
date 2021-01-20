# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 00:24:13 2020

@author: josse
"""

COMPLEMENT = 0
COMPLEMENT_LIEU = 1
COMPLEMENT_TEMPS = 2
COMPLEMENT_MANIERE = 3
OBJECTIF = 4
CAUSE = 5
CONSEQUENCE = 6
AJOUT = 7
SUITE = 8
LOINTAIN = 9


class Lien :

  def __init__ (self, coeur = None, typeLien = None, importance = 1):
    self.coeur = coeur # Objet Coeur vers lequel le lien pointe : ??? -> lien -> coeur
    self.typeLien = typeLien # Entier identifiant le type de lien (CAUSE = 1, CONSEQUENCE = 2, SUITE = 3)
    self.importance = importance