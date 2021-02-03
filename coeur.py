# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 00:23:22 2020

@author: josse
"""


from psclib.objet import Personnage
from psclib.diversifieur import correct
from psclib.lien import COMPLEMENT, COMPLEMENT_LIEU, COMPLEMENT_TEMPS, COMPLEMENT_MANIERE, OBJECTIF, CAUSE, CONSEQUENCE, SUITE, Lien
from psclib.complement import Complement
from psclib.lieu import Lieu
from psclib.moment import Moment
from psclib.maniere import Maniere
import random

idCounter = 1


# Classe abstraite qui définit la structure des coeurs et la manière dont ils s'enchaînent
class Coeur:
  
  def __init__(self, liens=None, infos=None, ton=None, id=None, parent=None, importance=None):
    global idCounter
    
    if id is None:
        self.id = idCounter
        idCounter+= 1
    else:
        self.id = id
        
    self.importance = importance
    self.parent = parent
    
    self.mode = "indicatif"
    self.temps = "présent"
    self.date = None
    
    self.ton = None
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


  def __eq__(self, other):
      if other is None: return False
      if not(isinstance(other, Coeur)): return False
      return self.id == other.id


  def ajouterComplement(self, complement=None, name="", importance=1):
      if complement is None: complement = Complement(name=name)
      coeur = CoeurComplement(complement, self, typeComplement=COMPLEMENT)
      self.liens.append(Lien(coeur, COMPLEMENT, importance=importance))
      
  def ajouterLieu(self, complement=None, name="", lieu=None, rapport="", importance=1):
      if complement is None: complement = Lieu(name=name, lieu=lieu, rapport=rapport)
      coeur = CoeurComplement(complement, self, typeComplement=COMPLEMENT_LIEU)
      lien = Lien(coeur, COMPLEMENT_LIEU, importance=importance)
      if not(self.date is None) and lien.coeur.date is None: lien.coeur.date = self.date
      self.liens.append(lien)
      
  def ajouterMoment(self, complement=None, name="", moment=None, rapport="", date=None, importance=1):
      if complement is None: complement = Moment(name=name, moment=moment, rapport=rapport, date=date)
      if not(date is None): self.date = date # On ajoute le temps
      coeur = CoeurComplement(complement, self, typeComplement=COMPLEMENT_TEMPS)
      if not(date is None): coeur.date = date
      self.liens.append(Lien(coeur, COMPLEMENT_TEMPS, importance=importance))
      
  def ajouterManiere(self, complement=None, name="", importance=1):
      if complement is None: complement = Maniere(name=name)
      coeur = CoeurComplement(complement, self, typeComplement=COMPLEMENT_MANIERE)
      lien = Lien(coeur, COMPLEMENT_MANIERE, importance=importance)
      if not(self.date is None) and lien.coeur.date is None: lien.coeur.date = self.date
      self.liens.append(lien)
      
  
  def ajouterLien(self, lien):
      # On ajoute le lien
      self.liens.append(lien)
      if lien.coeur.parent is None: lien.coeur.parent = self
      if lien.coeur.importance is None: lien.coeur.importance = lien.importance
      
      # Pour la concordance des temps
      if lien.typeLien == OBJECTIF:
          lien.coeur.mode = "subjonctif"
      elif lien.typeLien == COMPLEMENT_TEMPS:
          if not(lien.coeur.date is None):
              self.date = lien.coeur.date # On ajoute le temps
          else:
              print("PROBLEME DATE")
      #if lien.typeLien == SUITE or lien.typeLien == CONSEQUENCE or lien.typeLien == CAUSE:
      else:
          if not(self.date is None) and lien.coeur.date is None: lien.coeur.date = self.date
          
         
      
      #print(self.id, "(", self.date, ")", "----" + str(lien.typeLien) + "---->", lien.coeur.id, "(", self.date, ")")





class CoeurComplement(Coeur) :
  
    def __init__(self, complement = None, parent = None, typeComplement=COMPLEMENT, importance=None):
        Coeur.__init__(self, liens=None, infos=None, ton=None, id=None, parent=parent, importance=importance)
        self.complement = complement
        self.typeComplement = typeComplement
        
        
    def getGraphText(self):
        s = """<table border="0" cellborder="0" cellspacing="0">\n"""
        s+= """  <tr><td align="center"><b>COMPLEMENT (""" + str(self.id) + """)</b></td></tr>\n"""
        dict_comp = {COMPLEMENT: "Complément: ", COMPLEMENT_LIEU: "Lieu: ", COMPLEMENT_TEMPS: "Moment: ", COMPLEMENT_MANIERE: "Manière: "}
        s+= """  <tr><td align="left"><I>""" + dict_comp[self.typeComplement] + "</I>"
        s+= self.complement.getGraphText() + """</td></tr>\n"""
        s+="""</table>"""
        return s
    

    def toText(self, locuteur=None, interlocuteur=None, date=None, premierCoeur=True, lastMentioned=None, autoriserRadoter=True, useTranslation=True, useCorrection=True):
        phrase = self.complement.toText(locuteur=locuteur, interlocuteur=interlocuteur, date=date, useTranslation=useTranslation, useCorrection=useCorrection)
        
        probaRadoter = 0.5*autoriserRadoter
        if random.random() <= probaRadoter:
            return self.parent.toText(locuteur=locuteur, interlocuteur=interlocuteur, lastMentioned=lastMentioned, date=date, premierCoeur=True, useTranslation=useTranslation, useCorrection=useCorrection) + " " + phrase
            
        return phrase