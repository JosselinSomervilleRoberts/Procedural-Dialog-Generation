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
  
  def __init__(self, liens=None, infos=None):
    global idCounter
    self.id = idCounter
    idCounter+= 1
    
    self.mode = "indicatif"
    self.temps = "présent"
    
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


  def ajouterComplement(self, complement=None, name="", importance=1):
      if complement is None: complement = Complement(name=name)
      coeur = CoeurComplement(complement, self, typeComplement=COMPLEMENT)
      self.liens.append(Lien(coeur, COMPLEMENT, importance=importance))
      
  def ajouterLieu(self, complement=None, name="", lieu=None, rapport="", importance=1):
      if complement is None: complement = Lieu(name=name, lieu=lieu, rapport=rapport)
      coeur = CoeurComplement(complement, self, typeComplement=COMPLEMENT_LIEU)
      self.liens.append(Lien(coeur, COMPLEMENT_LIEU, importance=importance))
      
  def ajouterMoment(self, complement=None, name="", moment=None, rapport="", importance=1):
      if complement is None: complement = Moment(name=name, moment=moment, rapport=rapport)
      coeur = CoeurComplement(complement, self, typeComplement=COMPLEMENT_TEMPS)
      self.liens.append(Lien(coeur, COMPLEMENT_TEMPS, importance=importance))
      
  def ajouterManiere(self, complement=None, name="", importance=1):
      if complement is None: complement = Maniere(name=name)
      coeur = CoeurComplement(complement, self, typeComplement=COMPLEMENT_MANIERE)
      self.liens.append(Lien(coeur, COMPLEMENT_MANIERE, importance=importance))
      
  
  def ajouterLien(self, lien):
      self.liens.append(lien)
      if lien.typeLien == OBJECTIF:
          lien.coeur.mode = "subjonctif"





class CoeurComplement(Coeur) :
  
    def __init__(self, complement = None, parent = None, typeComplement=COMPLEMENT):
        Coeur.__init__(self, None, None)
        self.complement = complement
        self.parent = parent
        self.typeComplement = typeComplement
        
        
    def getGraphText(self):
        s = "===== COEUR COMPLEMENT ====="
        dict_comp = {COMPLEMENT: "Complément: ", COMPLEMENT_LIEU: "Lieu: ", COMPLEMENT_TEMPS: "Moment: ", COMPLEMENT_MANIERE: "Manière: "}
        s+= "\n" + dict_comp[self.typeComplement]
        s+= self.complement.getGraphText()
        return s
    

    def toText(self, locuteur=None, interlocuteur=None, autoriserRadoter=True, useTranslation=True, useCorrection=True): 
        phrase = self.complement.toText(locuteur=locuteur, interlocuteur=interlocuteur, useTranslation=useTranslation, useCorrection=useCorrection)
        
        probaRadoter = 0.5*autoriserRadoter
        if random.random() <= probaRadoter:
            return self.parent.toText(locuteur=locuteur, interlocuteur=interlocuteur, useTranslation=useTranslation, useCorrection=useCorrection) + " " + phrase
            
        return phrase