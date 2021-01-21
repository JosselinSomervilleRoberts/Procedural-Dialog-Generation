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
      

  def getGraphText(self):
      s = """<table border="1" cellborder="0" cellspacing="1">\n"""
      s+= """  <tr><td align="center"><b>COEUR ACTION</b></td></tr>\n"""
      if type(self.sujet) == list:
          s+= """  <tr><td align="left">Sujet:</I> """ + """ et """.join([s.getGraphText() for s in self.sujet]) + """</td></tr>\n"""
      else:
          s+= """  <tr><td align="left">Sujet:</I> """ + self.sujet.getGraphText() + """</td></tr>\n"""
      s+= """  <tr><td align="left">Action:</I> """ + self.action.getGraphText() + """</td></tr>\n"""
      if not(self.cod is None): s+= """  <tr><td align="left">Complément:</I> """ + self.cod.getGraphText() + """</td></tr>\n"""
      s+="""</table>"""
      return s

    
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
      vb = self.action.toText(self.mode, self.temps,personne)
      exp = ""
      if not(usePronom):
        for suj in self.sujet:
          exp += suj.toText(locuteur=locuteur, interlocuteur=interlocuteur, useTranslation=useTranslation, useCorrection=useCorrection) + " et "
        exp = exp[:-4]
        exp += " " + vb.replace("je ","").replace("j\'","").replace("tu ","").replace("il ","").replace("nous ","").replace("vous ","").replace("ils ","").replace("qu\'", "").replace("que ", "")
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
    exp = correct(s, useCorrection=useCorrection)
    return exp[0].lower() + exp[1:]