# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 00:24:13 2020

@author: josse
"""

COMPLEMENT = 0
COMPLEMENT_LIEU = 1
COMPLEMENT_TEMPS = 2
COMPLEMENT_MANIERE = 3
CAUSE = 4
CONSEQUENCE = 5
SUITE = 6
AJOUT = 7
OBJECTIF = 8


class Lien :

  def __init__ (self, coeur = None, typeLien = None, importance = 1):
    self.coeur = coeur # Objet Coeur vers lequel le lien pointe : ??? -> lien -> coeur
    self.typeLien = typeLien # Entier identifiant le type de lien (CAUSE = 1, CONSEQUENCE = 2, SUITE = 3)
    self.importance = importance