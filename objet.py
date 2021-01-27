# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 23:50:39 2020

@author: josse
"""

from psclib.diversifieur import correct, diversifier, get_syn
from psclib.caracteristique import CaracChiffree, Caracteristique
import random

idCounter = 1



class Objet(object):

  def __init__(self, dico=None):
    global idCounter
    self.id = idCounter
    idCounter+= 1
    
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
        
        
  def __eq__(self, other):
      if other is None: return False
      if not(isinstance(other, Objet)): return False
      return self.id == other.id
    
    
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


  def getGraphText(self):
      if not(self.noms is None) and len(self.noms) > 0: return self.noms[0]
      return self.toText()
  

  def toText(self, types=None, locuteur=None, interlocuteur=None, mentionProprio=True, useTranslation=True, useCorrection=True):
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
    if personne != 3 and personne != 6:
      usePossessif = True

    if not(self.noms is None) and len(self.noms) > 0 and random.random() and self in interlocuteur.objets and random.random() >= 1/(1+len(self.noms)):
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
      exp += " " + c.toText(useTranslation=useTranslation, useCorrection=useCorrection) + " et"
    if len(caracs_a_preciser) > 0:
      exp = exp[:-3]



    # Add proprio explicite
    if self.proprio is None: # On considère que c'est indéfini
      exp = "un " + exp[4:]
    elif usePossessif:
      exp = listePossessifs[personne-1] + " " +exp[4:]
    elif mentionProprio:
      exp += " de " + self.proprio.prenom + " " + self.proprio.nom
    
    exp = correct(exp, useCorrection=useCorrection)
    
    if not(self in interlocuteur.objets):
        interlocuteur.objets.append(self)
        if not(self.noms is None) and len(self.noms) > 0 and random.random():
            exp += ", " + random.choice(self.noms) + ","
    return exp[0].lower() + exp[1:]



class Personnage(Objet):

  def getAvailable():
    return ["inconnu", "lancelot", "mickey", "joe", "marcel", "jackie", "kevin"]

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
      if name == "marcel": self = Personnage.__init__(self, dico={"nom":"", "prenom":"Marcel", "caracs": [CaracChiffree(name="bavard", value=10)]})
      if name == "jackie": self = Personnage.__init__(self, dico={"nom":"", "prenom":"Jackie", "caracs": [CaracChiffree(name="curiosite", value=10)]})
      if name == "kevin": self = Personnage.__init__(self, dico={"nom":"", "prenom":"Kev", "ticsLangages": {"": 1, "genre": 1, "wesh,": 8, "en fait": 1, "du coup": 1},
                                                                 "caracs": [CaracChiffree(name="curiosite", value=10), CaracChiffree(name="politesse", value=2), 
                                                                            CaracChiffree(name="hésitation", value=10), CaracChiffree(name="memoire", value=2)]})
    else:
      Objet.__init__(self, dico=dico) # A RAJOUTER dico EN ARGUMENT
      self.setCarac(CaracChiffree(name="bavard", value=5), overWrite=False)
      self.setCarac(CaracChiffree(name="curiosite", value=5), overWrite=False)
      self.setCarac(CaracChiffree(name="politesse", value=5), overWrite=False)
      self.setCarac(CaracChiffree(name="compassion", value=5), overWrite=False)
      self.setCarac(CaracChiffree(name="hésitation", value=5), overWrite=False)
      self.setCarac(CaracChiffree(name="memoire", value=5), overWrite=False)
      
      self.ticsLangages = {"": 1, "genre": 0, "wesh,": 0, "en fait": 0, "du coup": 0}
      if "ticsLangages" in dico:
          self.ticsLangages = dico["ticsLangages"] 
      
      self.nom = None
      self.prenom = None
      self.id = None
      self.sexe = None
      self.age = None
      
      self.objets = []
      
      self.humeur = None
      self.animaux = []
      self.pere = None
      self.mere = None
      self.enfants = []
      

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
        if "pere" in dico:
            self.pere = dico["pere"] #Père est un string ou objet ou personnage
        if "mere" in dico:
            self.mere = dico["mere"] #Mère est un string ou objet ou personnage
        if "pere" in dico:
            self.enfants = dico["enfants"] #Enfants est une liste de strings ou objets ou personnages
      #rajouter famille, métier, etc (pas que des valeurs fixes)
   
      if not (self.prenom is None) and not (self.nom is None):
        self.id = self.prenom+self.nom #Id est un string (plus simple pour comparer des personnages)

      self.contacts = [] #Liste d'objets Personnage, représente les gens connus par le personnage (ainsi que, plus tard, les informations connues par le personnage sur ses contacts)
      self.histoires = [] #Liste d'objets Histoire, représente les histoires connues par le personnage, peu importe qu'il soit le narrateur ou non



  def __eq__(self, other):
      if other is None: return False
      if not(isinstance(other, Personnage)): return False
      return self.prenom == other.prenom and self.nom == other.nom
  
    
  def getTic(self, interlocuteur=None, ajouterTic=True):
      s = ""
      
      if ajouterTic:
          tic = random.choices(list(self.ticsLangages.keys()), weights=list(self.ticsLangages.values()), k=1)[0]
          s += tic
          if tic != "":
              s += " "
              
      probaHesiter = 0.075*self.getCaracValue(Caracteristique(name="hésitation"))
      if random.random() <= probaHesiter:
          nbPoints = random.randint(3 , 3 + int(0.35*self.getCaracValue(Caracteristique(name="hésitation"))))
          s += "euh" + "."*nbPoints + " " 
      
      return s
  
  def copyStrip(self): #Retourne les caractéristiques de base sous forme d'un dictionnaire
    return Personnage({"nom":self.nom, "prenom":self.prenom, "sexe":self.sexe})
  

  def imprimer(self, texte, diversify=True, useTranslation=True, useCorrection=True) : #Méthode pour faire parler le personnage (on ajoute juste qui parle avant le texte)
    if diversify: texte = diversifier(texte, useTranslation=useTranslation)
    return self.prenom + " " + self.nom + " : " + texte
    
  
  def getContact(self, id) : #Retourne la vision qu'a "self" du personnage "id" - A COMPLETER LORSQU'ON TRAITERA LES ECHANGES D'INFORMATIONS
    for p in self.contacts :
      if p.id == id :
        return p
    return None


  def ajouterPossession(self, dico):
      dico["proprio"] = self
      objet = Objet(dico)
      self.objets.append(objet)
      return objet

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
          if "pere" in dico and not self.pere: #Seulement si pas encore d'info sur le père
            self.pere = dico["pere"]
          if "mere" in dico and not self.mere: #Seulement si pas encore d'info sur la mère
            self.mere = dico["mere"]
          if "enfants" in dico: #Ajout
            for enfant in dico["enfants"]:
              if enfant not in self.enfants:
                self.enfants.append(enfant)
                
                
  def getGraphText(self):
      return self.toText()


  def toText(self, locuteur=None, interlocuteur=None, useTranslation=True, useCorrection=True):
    return self.prenom + " " + self.nom


  def indexHistoire(self, titre):
      """
      Renvoie l'index de l'histoire ayant pour titre "titre"
      Si le personnage ne la connait pas, renvoie -1
      """
      for i in range(len(self.histoires)):
          h = self.histoires[i]
          if not(h is None) and not(h.titre is None) and h.titre == titre:
              return i
      return -1
  
    
  def ajouterHistoire(self, titre, head = None, ton = None, personnes = None, conteur = None):
      """Ajoute l'histoire au personnage s'il ne la connait pas déja et renvoie -1 dans ce cas
      S'il la connait déja ne l'ajoute pas et renvoie sont index"""
      from psclib.histoire import Histoire
      from copy import copy
      
      index = self.indexHistoire(titre)
      
      if index == -1:
          headCopied = copy(head)
          headCopied.liens = []
          headCopied.date = None
          h = Histoire(head = headCopied, ton = ton, titre = titre, personnes = personnes, conteur = conteur)
          self.histoires.append(h)
          return -1
      return index
  
    
  def creerHistoire(self, hist):
      if not(hist is None) and self.indexHistoire(hist.titre) == -1:
          hist.conteur = self
          self.histoires.append(hist)