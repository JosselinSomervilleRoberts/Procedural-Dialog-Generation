# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 23:50:39 2020

@author: josse
"""

from psclib.diversifieur import correct, diversifier, get_syn
from psclib.caracteristique import CaracChiffree, Caracteristique
from psclib.diversifieur import get_genre
from psclib.relation import Relation
import random

idCounter = 1



class Objet(object):

  def __init__(self, dico=None, lib=None, addDeterminant=True):
    global idCounter
    self.id = idCounter
    idCounter+= 1
    
    self.genre = None
    self.lib = lib
    self.proprio = None
    self.caracs = []
    self.noms = None
    self.quantite = 1
    self.isLieu = False
    self.addDeterminant = addDeterminant

    if not(dico is None):
      if "lib" in dico:
        self.lib = dico["lib"]
      if "proprio" in dico:
        self.proprio = dico["proprio"]
      if "caracs" in dico:
        self.caracs = dico["caracs"]
      if "noms" in dico:
        self.noms = dico["noms"]
    
    if not(self.lib is None): 
        self.genre = get_genre(self.lib)
        
        
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
  

  def toText(self, types=None, locuteur=None, interlocuteur=None, sujet=None, mentionProprio=True, useTranslation=True, useCorrection=True):
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
    if self.genre == 2:
        listePossessifs = ["ma", "ta", "sa", "mes", "tes", "leurs"]
    usePossessif = False
    if personne != 3 and personne != 6:
      usePossessif = True
    elif not(sujet is None) and len(sujet) == 1 and not(self.proprio is None) and self.proprio == sujet[0]:
      usePossessif = True

    if not(self.noms is None) and len(self.noms) > 0 and random.random() and self in interlocuteur.objets and random.random() >= 1/(1+len(self.noms)):
      return random.choice(self.noms)


    # Nom de l'objet
    determinant = "le"
    if self.genre == 2: determinant = "la"
    if not(self.addDeterminant):
        exp = self.lib
    else:
        exp = determinant + " " + get_syn(self.lib)
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
    if not(self.isLieu) and self.addDeterminant:
        if self.proprio is None: # On considère que c'est indéfini
          determinant = "un"
          if self.genre == 2: determinant = "une"
          exp = determinant + " " + exp[3:]
        elif usePossessif:
          exp = listePossessifs[personne-1] + " " +exp[3:]
        elif mentionProprio:
          exp += " de " + self.proprio.prenom + " " + self.proprio.nom
    elif self.isLieu:
        exp = "à " + exp
    
    exp = correct(exp, useCorrection=useCorrection)
    
    if not(self in interlocuteur.objets):
        interlocuteur.objets.append(self)
        if not(self.noms is None) and len(self.noms) > 0 and random.random():
            exp += ", " + random.choice(self.noms) + ","
    return exp[0].lower() + exp[1:]



class Personnage(Objet):

  def getAvailable():
    return ["inconnu", "lancelot", "mickey", "joe", "marcel", "jackie", "kevin","kerma","torva","fisker","agni","chieto","arold","clara","cassius","traula","alaric","alice","charles","rosamund"]

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
      if name == "marcel": self = Personnage.__init__(self, dico={"nom":"", "sexe": "m", "prenom":"Marcel", "caracs": [CaracChiffree(name="bavard", value=10)]})
      if name == "jackie": self = Personnage.__init__(self, dico={"nom":"", "sexe": "m", "prenom":"Jackie", "caracs": [CaracChiffree(name="curiosite", value=10)]})
      if name == "kevin": self = Personnage.__init__(self, dico={"nom":"", "sexe": "m", "prenom":"Kev", "ticsLangages": {"": 1, "genre": 1, "wesh,": 8, "en fait": 1, "du coup": 1},
                                                                 "caracs": [CaracChiffree(name="curiosite", value=10), CaracChiffree(name="politesse", value=2), 
                                                                            CaracChiffree(name="hésitation", value=10), CaracChiffree(name="memoire", value=2)]})
      if name == "kerma": self = Personnage.__init__(self, dico={"nom":"Boulanger", "sexe": "f", "prenom":"Kerma", "ticsLangages": {"": 5, "bon": 1, "alors,": 1},
                                                                 "caracs": [CaracChiffree(name="curiosite", value=10), CaracChiffree(name="politesse", value=5), 
                                                                            CaracChiffree(name="hésitation", value=2), CaracChiffree(name="memoire", value=7),
                                                                            CaracChiffree(name="bavard", value=8), CaracChiffree(name="compassion", value=7)]})
      if name == "fisker": self = Personnage.__init__(self, dico={"nom":"Forgeron", "sexe": "m", "prenom":"Fisker", "ticsLangages": {"": 5, "beh": 1, "boudiou,": 1, "par ma barbe":0.5 },
                                                                 "caracs": [CaracChiffree(name="curiosite", value=2), CaracChiffree(name="politesse", value=3), 
                                                                            CaracChiffree(name="hésitation", value=2), CaracChiffree(name="memoire", value=3),
                                                                            CaracChiffree(name="bavard", value=1), CaracChiffree(name="compassion", value=2)]})
      if name == "torva": self = Personnage.__init__(self, dico={"nom":"Charpentier", "sexe": "f", "prenom":"Torva", "ticsLangages": {"": 5, "cheh": 1, "meh,": 1},
                                                                 "caracs": [CaracChiffree(name="curiosite", value=5), CaracChiffree(name="politesse", value=5), 
                                                                            CaracChiffree(name="hésitation", value=7), CaracChiffree(name="memoire", value=10),
                                                                            CaracChiffree(name="bavard", value=2), CaracChiffree(name="compassion", value=8)]})
      
      
      
      
      if name == "agni": self = Personnage.__init__(self, dico={"nom":"Marchand", "sexe": "m", "prenom":"Agni", "ticsLangages": {"": 5, "bon": 1, "alors,": 1},
                                                                 "caracs": [CaracChiffree(name="curiosite", value=10), CaracChiffree(name="politesse", value=5), 
                                                                            CaracChiffree(name="hésitation", value=2), CaracChiffree(name="memoire", value=7),
                                                                            CaracChiffree(name="bavard", value=8), CaracChiffree(name="compassion", value=7)]})
      if name == "chieto": self = Personnage.__init__(self, dico={"nom":"Chef", "sexe": "f", "prenom":"Chieto", "ticsLangages": {"": 5,"bon":1},
                                                                 "caracs": [CaracChiffree(name="curiosite", value=7), CaracChiffree(name="politesse", value=7), 
                                                                            CaracChiffree(name="hésitation", value=1), CaracChiffree(name="memoire", value=9),
                                                                            CaracChiffree(name="bavard", value=3), CaracChiffree(name="compassion", value=4)]})
      if name == "arold": self = Personnage.__init__(self, dico={"nom":"Paysan", "sexe": "m", "prenom":"Arold", "ticsLangages": {"": 5, "eh beh": 2, "bah diu": 2, "maizalors": 2, "ouhmi diou": 2},
                                                                 "caracs": [CaracChiffree(name="curiosite", value=10), CaracChiffree(name="politesse", value=2), 
                                                                            CaracChiffree(name="hésitation", value=1), CaracChiffree(name="memoire", value=3),
                                                                            CaracChiffree(name="bavard", value=10), CaracChiffree(name="compassion", value=8)]})
      if name == "clara": self = Personnage.__init__(self, dico={"nom":"Bucheron", "sexe": "f", "prenom":"Clara", "ticsLangages": {"": 5, "hum": 0.5, "meh": 0.5},
                                                                 "caracs": [CaracChiffree(name="curiosite", value=4), CaracChiffree(name="politesse", value=8), 
                                                                            CaracChiffree(name="hésitation", value=4), CaracChiffree(name="memoire", value=9),
                                                                            CaracChiffree(name="bavard", value=2), CaracChiffree(name="compassion", value=1)]})
      if name == "cassius": self = Personnage.__init__(self, dico={"nom":"Chasseur", "sexe": "m", "prenom":"Cassius", "ticsLangages": {"": 5, "ah la la": 1, "oh lo lo": 1, "damn": 1},
                                                                 "caracs": [CaracChiffree(name="curiosite", value=10), CaracChiffree(name="politesse", value=2), 
                                                                            CaracChiffree(name="hésitation", value=5), CaracChiffree(name="memoire", value=5),
                                                                            CaracChiffree(name="bavard", value=7), CaracChiffree(name="compassion", value=7)]})
      if name == "traula": self = Personnage.__init__(self, dico={"nom":"Alouro", "sexe": "f", "prenom":"Traula", "ticsLangages": {"": 1},
                                                                 "caracs": [CaracChiffree(name="curiosite", value=5), CaracChiffree(name="politesse", value=10), 
                                                                            CaracChiffree(name="hésitation", value=0), CaracChiffree(name="memoire", value=10),
                                                                            CaracChiffree(name="bavard", value=3), CaracChiffree(name="compassion", value=7)]})
      if name == "alaric": self = Personnage.__init__(self, dico={"nom":"Tanneur", "sexe": "m", "prenom":"Alaric", "ticsLangages": {"": 5, "grmf": 2, "eh": 2, "hm": 2},
                                                                 "caracs": [CaracChiffree(name="curiosite", value=7), CaracChiffree(name="politesse", value=3), 
                                                                            CaracChiffree(name="hésitation", value=5), CaracChiffree(name="memoire", value=9),
                                                                            CaracChiffree(name="bavard", value=1), CaracChiffree(name="compassion", value=8)]})
      if name == "alice": self = Personnage.__init__(self, dico={"nom":"Paysan", "sexe": "f", "prenom":"Alice", "ticsLangages": {"": 5,"crénom":1,"ah":1},
                                                                 "caracs": [CaracChiffree(name="curiosite", value=7), CaracChiffree(name="politesse", value=8), 
                                                                            CaracChiffree(name="hésitation", value=2), CaracChiffree(name="memoire", value=7),
                                                                            CaracChiffree(name="bavard", value=7), CaracChiffree(name="compassion", value=9)]})
                                                                                          
      if name == "charles": self = Personnage.__init__(self, dico={"nom":"Paysan", "sexe": "m", "prenom":"Charles", "ticsLangages": {"": 5, "euuuuuh":1,"attends":1},
                                                                 "caracs": [CaracChiffree(name="curiosite", value=10), CaracChiffree(name="politesse", value=1), 
                                                                            CaracChiffree(name="hésitation", value=2), CaracChiffree(name="memoire", value=4),
                                                                            CaracChiffree(name="bavard", value=8), CaracChiffree(name="compassion", value=3)]})
      if name == "rosamund": self = Personnage.__init__(self, dico={"nom":"Paysan", "sexe": "f", "prenom":"Rosamund", "ticsLangages": {"": 5, "hum": 2},
                                                                 "caracs": [CaracChiffree(name="curiosite", value=2), CaracChiffree(name="politesse", value=7), 
                                                                            CaracChiffree(name="hésitation", value=3), CaracChiffree(name="memoire", value=3),
                                                                            CaracChiffree(name="bavard", value=3), CaracChiffree(name="compassion", value=3)]})
                                                                                          
                                                                                          
     
    else:
      Objet.__init__(self, dico=dico) # A RAJOUTER dico EN ARGUMENT
      
      # Caracteristiques
      self.setCarac(CaracChiffree(name="bavard", value=5), overWrite=False)
      self.setCarac(CaracChiffree(name="curiosite", value=5), overWrite=False)
      self.setCarac(CaracChiffree(name="politesse", value=5), overWrite=False)
      self.setCarac(CaracChiffree(name="compassion", value=5), overWrite=False)
      self.setCarac(CaracChiffree(name="hésitation", value=5), overWrite=False)
      self.setCarac(CaracChiffree(name="memoire", value=5), overWrite=False)
      
      # Tics de langages
      self.ticsLangages = {"": 1, "genre": 0, "wesh,": 0, "en fait": 0, "du coup": 0}
      
      # Identité et liens aux autres
      self.nom = None
      self.prenom = None
      self.id = None
      self.sexe = None
      self.age = None
      self.objets = []
      self.animaux = []
      self.contacts = {} #Liste d'objets Personnage, représente les gens connus par le personnage (ainsi que, plus tard, les informations connues par le personnage sur ses contacts)
      
      # Génération d'histoires
      self.evenements = {}
      self.endroits = []
      self.histJournaliere = None
      self.coeurJournalier = None
      self.current_evenement = 0
      self.current_endroit = 0
      self.vientDarriverJournalier = True
      self.listeLieux = []
      

      if not(dico is None):
        if "ticsLangages" in dico:
          self.ticsLangages = dico["ticsLangages"] 
        if "nom" in dico:
          self.nom = dico["nom"] #Nom est un string
        if "prenom" in dico:
          self.prenom = dico["prenom"] #Prenom est un string
        if "age" in dico:
          self.age = dico["age"] #Age est un int
        if "sexe" in dico:
          self.sexe = dico["sexe"] #Sexe est -non défini- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!         
        if "animaux" in dico:
            self.animaux = dico["animaux"] #Animaux est une liste d'objets (désignant des animaux de compagnie)
        self.ajouterRelations(dico)
   
      if not (self.prenom is None) and not (self.nom is None):
        self.id = self.prenom+self.nom #Id est un string (plus simple pour comparer des personnages)

      self.histoires = [] #Liste d'objets Histoire, représente les histoires connues par le personnage, peu importe qu'il soit le narrateur ou non


  def ajouterRelations(self, dico):
      for nom in ["parent", "enfant", "adelphe", "neutre", "inconnu", "connaissance", "ami", "patron", "collègue", "employé"]:
          if nom in dico:
              self.contacts[dico[nom].id] = Relation(dico[nom].copyStrip(), relation=nom)


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
          if "animaux" in dico: #Ajout
            for animal in dico["animaux"]:
              if animal not in self.animaux:
                  self.animaux.append(animal)
                
                
  def getGraphText(self):
      return self.toText()


  def toText(self, locuteur=None, interlocuteur=None, sujet=None, useTranslation=True, useCorrection=True):
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
  
    
  def ajouterHistoire(self, titre, head = None, ton = None, personnes = None, conteur = None, importance = 1):
      """Ajoute l'histoire au personnage s'il ne la connait pas déja et renvoie -1 dans ce cas
      S'il la connait déja ne l'ajoute pas et renvoie sont index"""
      from psclib.histoire import Histoire
      from copy import copy
      
      index = self.indexHistoire(titre)
      
      if index == -1:
          headCopied = copy(head)
          headCopied.liens = []
          headCopied.date = None
          h = Histoire(head = headCopied, ton = ton, titre = titre, personnes = personnes, conteur = conteur, importance=importance)
          self.histoires.append(h)
          return -1
      return index
  
    
  def creerHistoire(self, hist):
      if not(hist is None) and self.indexHistoire(hist.titre) == -1:
          hist.conteur = self
          self.histoires.append(hist)
          
  def update(self, heure):
      from psclib.lien import Lien, SUITE
      from psclib.coeuraction import CoeurAction
      from psclib.action import Action
      
      # Si on a pas commencé l'histoire
      if self.coeurJournalier is None:
          # On choisit un endroit aleatoirement
          self.current_endroit = random.choices([k for k in range(len(self.endroits[0]))], weights=self.endroits[0], k=1)[0]
          # Si on va quelque part
          if self.current_endroit != 0:
              self.coeurJournalier = CoeurAction(sujet=self, action=Action(name="aller"), cod=self.listeLieux[self.current_endroit-1].objet)
              #self.coeurJournalier.ajouterLieu(complement=self.listeLieux[self.current_endroit-1].get_lieu(), importance = 1000)
              self.coeurJournalier.ajouterMoment(date=self.histJournaliere.dateDebut.replace(hour=heure), importance=2)
              self.histJournaliere.head = self.coeurJournalier
              self.current_evenement = 0
              self.vientDarriverJournalier = True
      
      # Si on fait rien, on change de lieu et qu'on ne viens pas d'arriver
      if (self.current_evenement == 0) and not(self.vientDarriverJournalier):
         prev_endroit = self.current_endroit
         l = self.endroits[self.current_endroit]
         self.current_endroit = random.choices([k for k in range(len(l))], weights=l, k=1)[0]
              
         # Si on bouge quelque part
         if prev_endroit != self.current_endroit and self.current_endroit != 0:
            coeur = CoeurAction(sujet=self, action=Action(name="aller"), cod=self.listeLieux[self.current_endroit-1].objet)
            #coeur.ajouterLieu(complement=self.listeLieux[self.current_endroit-1].get_lieu(), importance = 1000)
            coeur.ajouterMoment(date=self.histJournaliere.dateDebut.replace(hour=heure), importance=2)
            self.coeurJournalier.ajouterLien(Lien(coeur = coeur, typeLien = SUITE, importance = 0.5 + 0.2*self.getCaracValue(Caracteristique(name="bavard"))))
            self.coeurJournalier = coeur
            self.current_evenement = 0
            self.vientDarriverJournalier = True
              
      # Si on est quelquepart
      if self.current_endroit != 0:
         # on cherche une activité
         prev_evenement = self.current_evenement
         l = self.evenements[self.listeLieux[self.current_endroit-1]][self.current_evenement]
         self.current_evenement = random.choices([k for k in range(len(l))], weights=l, k=1)[0]
              
         # Si il y a un évenement nouveau
         if self.current_evenement != 0 and prev_evenement != self.current_evenement:
            coeur = self.listeLieux[self.current_endroit-1].action_possibles[self.current_evenement-1].getCoeur(self) # On génère le coeur
            coeur.ajouterMoment(date=self.histJournaliere.dateDebut.replace(hour=heure), importance=2)
            self.coeurJournalier.ajouterLien(Lien(coeur = coeur, typeLien = SUITE, importance = 0.5 + 0.2*self.getCaracValue(Caracteristique(name="bavard"))))
            self.coeurJournalier = coeur
            self.vientDarriverJournalier = False
                  
                  
  def commencer_journee(self, date):
      from psclib.histoire import Histoire
      if self.histJournaliere is None:
          self.histJournaliere = Histoire(titre="Hstoire de " + self.toText() + " le " + str(date), conteur=self, personnes=[self], dateDebut=date)
          self.coeurJournalier = None
          self.current_evenement = 0
          self.current_endroit = 0
          self.vientDarriverJournalier = True
      else:
          raise Exception("L histoire journaliere de " + self.toText() + " n est pas finie, impossible d en créer une nouvelle")
      
  def finir_journee(self):
      if not(self.histJournaliere is None):
          self.histoires.append(self.histJournaliere)
          self.histJournaliere = None
          self.coeurJournalier = None