# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 23:50:39 2020

@author: josse
"""

from psclib.diversifieur import correct, diversifier, get_syn
from psclib.caracteristique import CaracChiffree
import random

class Objet:

  def __init__(self, dico=None):
    self.id = None
    self.lib = None
    self.proprio = None
    self.caracs = []
    self.noms = None
    self.quantite = 1

    if not(dico is None):
      if "lib" in dico:
        self.lib = dico["lib"]
      if "proprio" in dico:
        self.proprio = dico["proprio"]
      if "caracs" in dico:
        self.caracs = dico["caracs"]
      if "noms" in dico:
        self.noms = dico["noms"]
    
  def __str__(self):
    return str([self.id,self.proprio,self.caracs,self.noms])

  def ecrire(self):
    return self.toText()

  def setCarac(self, caracChif, overWrite=True):
    """Assigne \"caracChif\" (une instance de CaracChiffree) à l'objet. S'occupe notamment de
    gérer si la carac doit être ajoutée ou modifier car déja présente."""
    alreadyExists = False
    for c in self.caracs:
      if c.isSame(caracChif):
        alreadyExists = True
        if overWrite:
            c.value = caracChif.value
    if not(alreadyExists):
      self.caracs.append(caracChif)


  def getCaracValue(self, carac):
    """Retourne la valeur de \"carac\" (une instance de Caracteristique). Renvoie -1 si la carac n'est pas présente"""
    for c in self.caracs:
      if c.isSame(carac):
        return c.value
    return -1 # On ne renvoie pas None car None correspond au fait qu'on ne connaisse pas la valeur, ici ça veut dire qu'elle n'existe pas (c'est différent)


  def toText(self, types=None, locuteur=None, interlocuteur=None, mentionProprio=True):
    """
    Si la liste des \"noms\" est fournie, choisi au hasard pami ces noms
    Sinon crée un nom à partir du libellé, des caracs et du proprio
    - types : liste de couples [proba(float), type(str)]
    """

    if locuteur is None : locuteur = Personnage()
    if interlocuteur is None : interlocuteur = Personnage() 
    personne = 3
    if locuteur == self.proprio:
      personne = 1
    elif interlocuteur == self.proprio:
      personne = 2
    if self.quantite > 1:
      personne += 3

    listePossessifs = ["mon", "ton", "son", "mes", "tes", "leurs"]
    usePossessif = False
    if personne % 3 != 0:
      usePossessif = True

    if not(self.noms is None) and len(self.noms) > 0:
      return random.choice(self.noms)


    # Nom de l'objet
    exp = "lae " + get_syn(self.lib)
    #print("exp", exp)
   
    # On cherche les caracteristiques que l'on va preciser
    caracs_a_preciser = []
    if not(types is None):
      for t in types:
        for c in self.caracs:
          if t[1] in c.types:
            # On randomise
            if random.random() <= t[0]:
              caracs_a_preciser.append(c)

    # On ajoute les caracteristiques
    for c in caracs_a_preciser:
      exp += " " + c.toText() + " et"
    if len(caracs_a_preciser) > 0:
      exp = exp[:-3]



    # Add proprio explicite
    if self.proprio is None: # On considère que c'est indéfini
      exp = "un " + exp[4:]
    elif usePossessif:
      exp = listePossessifs[personne-1] + " " +exp[4:]
    elif mentionProprio:
      exp += " de " + self.proprio.prenom + " " + self.proprio.nom
    
    exp = correct(exp)
    return exp



class Personnage(Objet):

  def getAvailable():
    return ["inconnu", "lancelot", "mickey", "joe", "marcel", "jackie"]

  def getAlike(s):
    """ Renvoie tous les Personnage qui contiennent s dans leur nom"""
    liste = []
    for perso in Personnage.getAvailable():
      if s in perso:
        liste.append(perso)
    return liste
  
  def __init__(self, dico=None, name=None):

    if not(name is None):
      if not(name in Personnage.getAvailable()) : raise NameError('Il n\'y a pas de Personnage nommé ' + name)
      if name == "inconnu": self = Personnage.__init__(self, dico={"nom":"Inconnu", "prenom":"Soldat"})
      if name == "lancelot": self = Personnage.__init__(self, dico={"nom":"Du Lac", "prenom":"Lancelot"})
      if name == "mickey": self = Personnage.__init__(self, dico={"nom":"Mouse", "prenom":"Mickey"})
      if name == "joe": self = Personnage.__init__(self, dico={"nom":"Dalton", "prenom":"Joe"})
      if name == "marcel": self = Personnage.__init__(self, dico={"nom":"", "prenom":"Marcel", "caracs": [CaracChiffree(name="bavard", value=3)]})
      if name == "jackie": self = Personnage.__init__(self, dico={"nom":"", "prenom":"Jackie", "caracs": [CaracChiffree(name="curiosite", value=10)]})
    else:
      Objet.__init__(self, dico=dico) # A RAJOUTER dico EN ARGUMENT
      self.setCarac(CaracChiffree(name="mysterieux", value=5), overWrite=False)
      self.setCarac(CaracChiffree(name="bavard", value=5), overWrite=False)
      self.setCarac(CaracChiffree(name="curiosite", value=5), overWrite=False)
      self.nom = None
      self.prenom = None
      self.id = None
      self.sexe = None
      self.age = None
      self.humeur = None
      self.animaux = []

      if not(dico is None):
        #juste pour comparer facilement
        if "nom" in dico:
          self.nom = dico["nom"] #Nom est un string
        if "prenom" in dico:
          self.prenom = dico["prenom"] #Prenom est un string
        if "age" in dico:
          self.age = dico["age"] #Age est un int
        if "sexe" in dico:
          self.sexe = dico["sexe"] #Sexe est -non défini- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if "humeur" in dico:
            self.humeur = dico["humeur"] #Humeur est un string (remplacer par une caractéristique CaracChiffree ?)
        if "animaux" in dico:
            self.animaux = dico["animaux"] #Animaux est une liste d'objets (désignant des animaux de compagnie)
      #rajouter famille, métier, etc (pas que des valeurs fixes)
   
      if not (self.prenom is None) and not (self.nom is None):
        self.id = self.prenom+self.nom #Id est un string (plus simple pour comparer des personnages)

      self.contacts = [] #Liste d'objets Personnage, représente les gens connus par le personnage (ainsi que, plus tard, les informations connues par le personnage sur ses contacts)
      self.histoires = [] #Liste d'objets Histoire, représente les histoires connues par le personnage, peu importe qu'il soit le narrateur ou non

  
  def copyStrip(self): #Retourne les caractéristiques de base sous forme d'un dictionnaire
    return Personnage({"nom":self.nom, "prenom":self.prenom, "sexe":self.sexe})
  

  def imprimer(self, texte, diversify=True) : #Méthode pour faire parler le personnage (on ajoute juste qui parle avant le texte)
    if diversify: texte = diversifier(texte)
    return self.prenom + " " + self.nom + " : " + texte
    
  
  def getContact(self, id) : #Retourne la vision qu'a "self" du personnage "id" - A COMPLETER LORSQU'ON TRAITERA LES ECHANGES D'INFORMATIONS
    for p in self.contacts :
      if p.id == id :
        return p
    return None

  def miseAJour(self, dico=None): #Utilisé pour mettre à jour une représentation à partir d'un dictionnaire d'informations
      if dico:
          if "nom" in dico: #Ecrase
            self.nom = dico["nom"]
          if "prenom" in dico: #Ecrase
            self.prenom = dico["prenom"]
          if "age" in dico: #Ecrase
            self.age = dico["age"]
          if "humeur" in dico: #Ecrase
            self.humeur = dico["humeur"]
          if "animaux" in dico: #Ajout
            for animal in dico["animaux"]:
              if animal not in self.animaux:
                  self.animaux.append(animal)


  def toText(self, locuteur=None, interlocuteur=None):
    return self.prenom + " " + self.nom