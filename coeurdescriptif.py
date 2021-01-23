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
  
  def __init__(self, sujet = None , carac = None, liens=None, infos=None):
    Coeur.__init__(self,liens,infos)
    self.sujet = sujet
    self.carac = carac
    
    
  def getGraphText(self):
      s = """<table border="0" cellborder="0" cellspacing="0">\n"""
      s+= """  <tr><td align="center"><b>COEUR DESCRIPTIF</b></td></tr>\n"""
      if type(self.sujet) == list:
          s+= """  <tr><td align="left"><I>Sujet:</I> """ + """ et """.join([s.getGraphText() for s in self.sujet]) + """</td></tr>\n"""
      else:
          s+= """  <tr><td align="left"><I>Sujet:</I> """ + self.sujet.getGraphText() + """</td></tr>\n"""
      s+= """  <tr><td align="left"><I>Caractéristique:</I> """ + self.carac.getGraphText() + """</td></tr>\n"""
      s+="""</table>"""
      return s
  

  def toText(self, locuteur=None, interlocuteur=None, date=None, premierCoeur=True, sujetMentionedBefore=False, useTranslation=True, useCorrection=True):
    # On gère les temps
    if self.mode != "subjonctif":
        self.mode = "indicatif"
        if self.date is None or date is None:
            self.temps = "présent"
        else:
            if self.date.date() == date.date():
                self.temps = "présent"
            elif self.date.date() < date.date():
                self.temps = "imparfait"
            else:
                self.temps = "futur-simple"
                
      
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

    vb = cong("etre", self.mode, self.temps, personne)
    exp = ""
    if not(usePronom):
      for suj in self.sujet:
        exp += suj.toText(locuteur=locuteur, interlocuteur=interlocuteur, useTranslation=useTranslation, useCorrection=useCorrection) + " et "
      exp = exp[:-4]
      exp += " " + vb.replace("je ","").replace("j\'","").replace("tu ","").replace("il ","").replace("nous ","").replace("vous ","").replace("ils ","").replace("qu\'", "").replace("que ", "")
    else:
      exp = vb

    exp += " " + self.carac.toText(useTranslation=useTranslation, useCorrection=useCorrection)
    s = correct(exp, useCorrection=useCorrection)
    self.transmissionInfos(locuteur, interlocuteur)
    return s[0].lower() + s[1:]