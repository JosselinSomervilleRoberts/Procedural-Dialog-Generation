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
  
  def __init__(self, sujet = None, action = None, cod = None, liens =  None, infos=None, parent=None, importance=None):
    Coeur.__init__(self, liens=liens, infos=infos, parent=parent, importance=importance)
    self.sujet = sujet
    self.action = action
    self.cod = cod
      

  def getGraphText(self):
      s = """<table border="0" cellborder="0" cellspacing="0">\n"""
      s+= """  <tr><td align="center"><b>COEUR ACTION</b></td></tr>\n"""
      if type(self.sujet) == list:
          s+= """  <tr><td align="left"><I>Sujet:</I> """ + """ et """.join([s.getGraphText() for s in self.sujet]) + """</td></tr>\n"""
      else:
          s+= """  <tr><td align="left"><I>Sujet:</I> """ + self.sujet.getGraphText() + """</td></tr>\n"""
      s+= """  <tr><td align="left"><I>Action:</I> """ + self.action.getGraphText() + """</td></tr>\n"""
      if not(self.cod is None): s+= """  <tr><td align="left"><I>Complément:</I> """ + self.cod.getGraphText() + """</td></tr>\n"""
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
                if premierCoeur:
                    self.temps = "imparfait"
                else:
                    self.temps = "passé-composé"
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
    
    s = s[:-1]
    self.transmissionInfos(locuteur, interlocuteur)
    exp = correct(s, useCorrection=useCorrection)
    return exp[0].lower() + exp[1:]