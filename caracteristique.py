# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 23:53:41 2020

@author: josse
"""

from psclib.diversifieur import correct, get_syn


class Type:

  def __init__(self,type):
    self.type = type

  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return self.type == other.type
    return False


class Caracteristique:

  def getAvailable():
    return ["beaute", "couleur", "taille", "tailleH", "metier", "ageH", "mysterieux", "bavard", "curiosite", "colere"]

  def getAlike(s):
    """ Renvoie toutes les caractéristiques qui contiennent s dans leur nom"""
    liste = []
    for carac in Caracteristique.getAvailable():
      if s in carac:
        liste.append(carac)
    return liste

  def __init__(self, lib=None, types=None, intervals=None, keepLib=True, name=None):
    if not(name is None):
      if not(name in Caracteristique.getAvailable()) : raise NameError('Il n\'y a pas de Caracetiristique nommée ' + name)
      if name == "beaute": Caracteristique.__init__(self, "beau", [liste_types["physique"]]),
      if name == "couleur": Caracteristique.__init__(self, "couleur", [liste_types["physique"]], [[0,"rouge"], [2,"bleue"]], False),
      if name == "taille" : Caracteristique.__init__(self, "taille",[liste_types["physique"]], [[0,"minuscule"],[2,"petit"],[4,"moyen"],[6,"grand"],[8,"très grand"],[10,"gigantesque"]],False),
      if name == "tailleH" : Caracteristique.__init__(self, "grand",[liste_types["physique"]]),
      if name == "metier" : Caracteristique.__init__(self, "métier",[liste_types["physique"]], [[0,"boulanger"],[1,"patissier"],[2,"cordonnier"],[3,"barman"],[3,"marchand"],[4,"garde"],[5,"fonctionnaire"]] ) ,                                   
      if name == "ageH" : Caracteristique.__init__(self, "age",[liste_types["physique"]],[[0, "nourrisson"],[2,"petit"],[4,"enfant"],[6,"adolescent"],[8, "jeune adulte"],[10,"adulte"],[12, "mur"],[14,"vieux"],[16,"très vieux"],[18,"croûlant"]]),
      if name == "mysterieux" : Caracteristique.__init__(self, "mystérieux",[liste_types["caractere"]])
      if name == "bavard" : Caracteristique.__init__(self, "bavard",[liste_types["caractere"]])
      if name == "curiosite" : Caracteristique.__init__(self, "curieux",[liste_types["caractere"]])
      if name == "colere" : Caracteristique.__init__(self, "en colère",[liste_types["caractere"]])
    else:
      self.lib = lib # adjectif de la caracterisitque (par exemple beau) : str
      self.keepLib = keepLib # Est ce qu'on affiche le libellé apres le facteur d echelle : bool
      self.types = types # liste de types (par exemple physique, intelect) : liste de Type
      if types is None:
        self.types = []
      self.intervals = intervals
      if intervals is None:
        self.intervals = [[0, "vraiment pas"], [1, "pas"], [3, "pas très"], [5, ""], [7, "plutot"], [9, "très"], [10, "super"]]

  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return self.lib == other.lib
    return False


  def getGraphText(self):
      return self.lib
  

  def toText(self, value, useTranslation=True, useCorrection=True):
    prep = ""
    i = len(self.intervals) - 1
    continuer = True

    while continuer and i >= 0:
      if value >= self.intervals[i][0]:
        prep = self.intervals[i][1]
        continuer = False
      i -= 1

    return correct(prep + " " + get_syn(self.lib)*self.keepLib, useCorrection=useCorrection)


class CaracChiffree:

  def __init__(self, carac=None, value=None, name=None):
    if not(name is None):
      if name in Caracteristique.getAvailable():
        self = CaracChiffree.__init__(self, carac=Caracteristique(name=name), value=value)
      else:
        raise NameError('Il n\'y a pas de Caracteristique nommée ' + name)
    else:
      self.carac = carac
      self.value = value


  def isSame(self, other):
    """ Renvoie si \"other\" est égal à self.carac (pas de comparaison de valeur)"""
    if isinstance(other, CaracChiffree) : return self.carac == other.carac
    if isinstance(other, Caracteristique) : return self.carac == other
    raise RuntimeError("Impossible de comparer une CaracChiffrée avec ", type(other))
    
    
  def getGraphText(self):
      s = self.carac.getGraphText()
      if not(self.value is None):
          s += "<br/><I>Valeur:</I> " + str(self.value)
      return s

  def toText(self, useTranslation=True, useCorrection=True):
    return self.carac.toText(self.value, useTranslation=useTranslation, useCorrection=useCorrection)

  def __eq__(self, other):
    if isinstance(other, self.__class__):
      return ((self.carac == other.carac) and (self.value == other.value))
    return False
  
  def __gt__(self, other):
    if isinstance(other, self.__class__):
      return ((self.carac == other.carac) and (self.value > other.value))
    return False


liste_types = {"physique": Type("physique"),
               "psychologique": Type("psychologique"),
               "caractere": Type("caractere")}