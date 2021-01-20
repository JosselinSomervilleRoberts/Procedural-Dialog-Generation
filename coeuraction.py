# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 00:24:55 2020

@author: josse
"""

from psclib.coeur import Coeur
from psclib.objet import Personnage
from psclib.diversifieur import correct


# Coeurs d'action, représente une action, une étape, dans la narration
class CoeurAction(Coeur) :
  
  def __init__(self, sujet = None, action = None, cod = None,lieu = None, moment = None, liens =  None, infos=None):
    Coeur.__init__(self, liens,infos)
    self.sujet = sujet
    self.action = action
    self.cod = cod
    self.lieu = lieu
    self.moment = moment # A DEFINIR
    
  def toText(self, locuteur=None, interlocuteur=None, sujetMentionedBefore=False, useTranslation=True, useCorrection=True):
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
    if sujetMentionedBefore or personne <= 2 or personne == 4 or personne == 5:
      usePronom = True
      
    s = ""
    if self.action is not None :
      vb = self.action.toText("indicatif","présent",personne)
      exp = ""
      if not(usePronom):
        for suj in self.sujet:
          exp += suj.toText(locuteur=locuteur, interlocuteur=interlocuteur, useTranslation=useTranslation, useCorrection=useCorrection) + " et "
        exp = exp[:-4]
        exp += " " + vb.replace("je ","").replace("j\'","").replace("tu ","").replace("il ","").replace("nous ","").replace("vous ","").replace("ils ","")
      else:
        exp = vb
      s += exp + " "

    if self.cod is not None :
      s+= self.cod.toText(locuteur=locuteur, interlocuteur=interlocuteur, useTranslation=useTranslation, useCorrection=useCorrection) + " "
    if self.lieu is not None :
      s+= self.lieu + " "

    if self.moment is not None :
      s+= self.moment.toText(useTranslation=useTranslation, useCorrection=useCorrection) + " "
    s = s[:-1]
    self.transmissionInfos(locuteur, interlocuteur)
    return correct(s, useCorrection=useCorrection)