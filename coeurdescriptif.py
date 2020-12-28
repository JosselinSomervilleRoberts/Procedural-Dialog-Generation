# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 00:26:33 2020

@author: josse
"""

from psclib.coeur import Coeur
from psclib.objet import Personnage
from psclib.diversifieur import correct, cong, diversifier


# Coeurs descriptifs, pour décrire quelque chose, pause dans le déroulé de l'histoire, verbe d'état
class CoeurDescriptif(Coeur):
  
  def __init__(self, sujet = None , carac = None, liens=None):
    Coeur.__init__(self,liens)
    self.sujet = sujet
    self.carac = carac

  def toText(self, locuteur=None, interlocuteur=None, sujetMentionedBefore=False):
    if not(type(self.sujet) == list):
      self.sujet = [self.sujet]
    if locuteur is None : locuteur = Personnage()
    if interlocuteur is None : interlocuteur = Personnage() 
    personne = 3
    if locuteur in self.sujet:
      personne = 1
    elif interlocuteur in self.sujet:
      personne = 2
    if len(self.sujet) > 1 or self.sujet[0].quantite > 1:
      personne += 3

    usePronom = False
    if sujetMentionedBefore or personne <= 2:
      usePronom = True

    vb = cong("etre", "indicatif", "présent", personne)
    exp = ""
    if not(usePronom):
      for suj in self.sujet:
        exp += suj.toText(locuteur=locuteur, interlocuteur=interlocuteur) + " et "
      exp = exp[:-4]
      exp += " " + vb.replace("je ","").replace("j\'","").replace("tu ","").replace("il ","").replace("nous ","").replace("vous ","").replace("ils ","")
    else:
      exp = vb

    exp += " " + self.carac.toText()
    s = correct(exp)
    return s