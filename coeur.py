# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 00:23:22 2020

@author: josse
"""

"je ne suis plus raciste. youhou"
#J'étais recherché ouais j'étais même pas au courant
from psclib.objet import Personnage
from psclib.diversifieur import correct
from psclib.lien import CAUSE, CONSEQUENCE, SUITE


# Classe abstraite qui définit la structure des coeurs et la manière dont ils s'enchaînent
class Coeur:
  
  def __init__(self, liens=None, infos=None):
    self.id = None # Champ à définir
    self.liens = liens
    if self.liens is None:
      self.liens = []
    self.infos = infos #Infos est une liste contenant des listes à 2 éléments [personnage, informations(dictionnaire)]
    if self.infos is None:
      self.infos = []
      
  def transmissionInfos(self, loc=None, interloc=None):
      if self.infos and loc and interloc : #Si il y a des infos à transmettre et que loc et interloc sont définis...
          for k in self.infos:
              representation = interloc.getContact(k[0].id)
              if not representation: #Si l'interlocuteur ne connait pas le sujet des informations
                  interloc.contacts.append(k[0].copyStrip())
                  representation = interloc.contacts[-1]
              representation.miseAJour(k[1]) #Mise à jour avec les informations contenues dans le coeur
      

  # PLUS UTILISE (Mais je garde au cas ou)
  def suivrelesliens(liens,s,p1=None,p2=None):
    """ p1 = locuteur, p2 = interlocuteur"""
    if p1 is None : p1 = Personnage() 
    if p2 is None : p2 = Personnage() 

    # A CHANGER POUR INTERACTIVITE
    for l in liens :
      if l.typeLien == CAUSE :
        s+= " parce que "+l.coeur.toText(p1,p2,suivre=False,pct=False)
      if l.typeLien == CONSEQUENCE :
        s += " donc "+ l.coeur.toText(p1,p2,suivre=False,pct=False)
      if l.typeLien == SUITE :
        s += " puis "+ l.coeur.toText(p1,p2,suivre=False,pct=False)
    return correct(s)
