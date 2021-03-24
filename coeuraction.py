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
  
  def __init__(self, sujet = None, action = None, cod = None, ton = None,liens =  None, infos=None, parent=None, importance=None):
    Coeur.__init__(self, liens=liens, infos=infos, ton = ton, parent=parent, importance=importance)
    self.sujet = sujet
    self.action = action
    self.cod = cod
      

  def getGraphText(self):
      s = """<table border="0" cellborder="0" cellspacing="0">\n"""
      s+= """  <tr><td align="center"><b>COEUR ACTION (""" + str(self.id) + """)</b></td></tr>\n"""
      if type(self.sujet) == list:
          s+= """  <tr><td align="left"><I>Sujet:</I> """ + """ et """.join([s.getGraphText() for s in self.sujet]) + """</td></tr>\n"""
      else:
          s+= """  <tr><td align="left"><I>Sujet:</I> """ + self.sujet.getGraphText() + """</td></tr>\n"""
      s+= """  <tr><td align="left"><I>Action:</I> """ + self.action.getGraphText() + """</td></tr>\n"""
      if not(self.cod is None): s+= """  <tr><td align="left"><I>Complément:</I> """ + self.cod.getGraphText() + """</td></tr>\n"""
      s+="""</table>"""
      return s

  def reaction(self):
      return Coeur.reaction(self)
    
  def toText(self, locuteur=None, interlocuteur=None, date=None, premierCoeur=True, lastMentioned=None, useTranslation=True, useCorrection=True):
    if lastMentioned is None: lastMentioned = [None, None]
      
    # On gère les temps
    if self.mode != "subjonctif":
        self.mode = "indicatif"
        
        if self.date is None or date is None:
            self.temps = "présent"
        elif type(self.date) == str:
            pass
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
    
    genreSujet = None
    for s in self.sujet:
        if s.genre == 1:
            genreSujet = 1
        elif s.genre==2 and genreSujet is None:
            genreSujet = 2
      
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
    if personne%3 != 0:
      usePronom = True
    elif self.sujet in lastMentioned:
        usePronom = True
    else:
        if not(genreSujet is None):
            lastMentioned[genreSujet-1] = self.sujet
            
    
    personneCod = 3
    codUsePronom = False
    expCod = ""
    
    if not(self.cod is None):
        if locuteur in [self.cod]:
            personneCod = 1
        elif interlocuteur in [self.cod]:
            personneCod = 2
        if len([self.cod]) > 1 or [self.cod][0].quantite > 1:
            personneCod += 3
            
        
        if personneCod%3 != 0:
          codUsePronom = True
        elif not(self.cod.genre is None) and ([self.cod] in lastMentioned) and ((personne%3 != 0) or self.cod.genre != genreSujet):
                codUsePronom = True
        else:
            if not(self.cod.genre is None) and self.cod.genre != genreSujet:
                lastMentioned[self.cod.genre-1] = [self.cod]
                
        if not(self.cod is None) and codUsePronom:
            pronoms = [["me", "te", "le", "nous", "vous", "les"], ["me", "te", "la", "nous", "vous", "les"]]
            genre = self.cod.genre
            if genre is None: genre = 1
            expCod = " " + pronoms[genre-1][personneCod-1]
            if self.temps=="passé-composé":
                expCod = expCod.replace("le", "l\'").replace("la", "l\'")
    
            
            
      
    s = ""
    if self.action is not None :
      vb = self.action.toText(self.mode, self.temps,personne)
      exp = ""
      if not(usePronom):
        for i in range(len(self.sujet)):
          suj = self.sujet[i]
          sujPrev = []
          if i > 0:
              sujPrev = [self.sujet[i-1]]
          exp += suj.toText(locuteur=locuteur, interlocuteur=interlocuteur, sujet=sujPrev, useTranslation=useTranslation, useCorrection=useCorrection) + " et "
        exp = exp[:-4]
        
        exp += expCod
        exp += " " + vb.replace("je ","").replace("j\'","").replace("tu ","").replace("il ","").replace("nous ","").replace("vous ","").replace("ils ","").replace("qu\'", "").replace("que ", "")
      else:
        if genreSujet == 2: vb = vb.replace("il ", "elle ").replace("ils ", "elles ")
        if expCod != "" :
            vb = vb.replace("j\'", "je ")
            liste = vb.split(" ")
            liste = liste[:-1 - (self.temps=="passé-composé")] + [expCod.replace(" ", "")] + liste[-1 - (self.temps=="passé-composé"):]
            exp = " ".join(liste)
        else:
            exp = vb
            
            
      if not(self.cod is None) and self.cod.genre == 2 and self.temps=="passé-composé":
          exp += "e"
          
      exp = exp.replace("\' ", "\'")
      s += exp + " "

    if self.cod is not None and not(codUsePronom):
      s+= self.cod.toText(locuteur=locuteur, interlocuteur=interlocuteur, sujet=self.sujet,  useTranslation=useTranslation, useCorrection=useCorrection) + " "
    
    s = s[:-1]
    self.transmissionInfos(locuteur, interlocuteur)
    exp = correct(s, useCorrection=useCorrection)
    return exp[0].lower() + exp[1:]