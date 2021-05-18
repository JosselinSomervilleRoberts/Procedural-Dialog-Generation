# -*- coding: utf-8 -*-
"""
Created on Wed Mar 31 14:57:28 2021

@author: schmi
"""

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import pickle

from psclib.objet import Personnage
from psclib.dialogue import dialogue
from psclib.caracteristique import CaracChiffree
from psclib.coeuraction import CoeurAction
from psclib.coeurdescriptif import CoeurDescriptif
from psclib.coeurdescriptifverbal import CoeurDescriptifVerbal
from psclib.action import Action
from psclib.objet import Objet
from psclib.lien import Lien
from psclib.histoire import CONSEQUENCE, OBJECTIF, SUITE, CAUSE, Histoire
from datetime import datetime

### CREATION DES PERSONNAGES ###

Alice = Personnage({"prenom":"Alice",
                           "nom":"Opéidémerveil",
                           "sexe":"f",
                           "ticsLangages": {"": 5, "euh": 0.5, "hum": 0.5},
                           "caracs": [CaracChiffree(name="bavard", value=3)]})

Bob = Personnage({"prenom":"Bob",
                         "nom":"Bricoleur",
                         "sexe":"m",
                         "caracs": [CaracChiffree(name="bavard", value=10),
                                    CaracChiffree(name="curiosite", value=5),
                                    CaracChiffree(name="memoire", value=5),
                                    CaracChiffree(name="compassion", value=5)]})

Charles = Personnage({"prenom":"Charles",
                     "nom":"Quin",
                     "sexe":"m",
                     "caracs": [CaracChiffree(name="curiosite", value=0),
                                CaracChiffree(name="memoire", value=2),
                                CaracChiffree(name="compassion", value=0)]})

Alice.ajouterRelations({"ami":[Bob, Charles]})
Bob.ajouterRelations({"ami":[Alice, Charles]})
Charles.ajouterRelations({"ami":[Alice, Bob]})

### CREATION D'HISTOIRES ###

# Alice promène son chien Bigni
Milou = Objet({"lib":"chien", "noms":["Milou"], "proprio":Alice})
Alice.animaux.append(Milou)

c1 = CoeurAction(sujet = Alice, action = Action(name="balader"), cod = Milou)
c1.ajouterMoment(date=datetime(2021,3,2), importance=200)
c1.ajouterLieu(name="dans la forêt", importance=10)

Voyageurs = Objet({"lib":"voyageur"})
c21 = CoeurAction(sujet = [Alice, Milou] , action=Action(name="rencontrer") , cod = Voyageurs)
c1.ajouterLien(Lien(coeur=c21, typeLien=SUITE, importance=20))

c22 = CoeurAction(sujet = Milou, action = Action(name="s'exercer"))
c1.ajouterLien(Lien(coeur=c22, typeLien=OBJECTIF, importance=10))

c31 = CoeurAction(sujet = [Alice, Voyageurs] , action=Action(name="parler"))
c31.ajouterManiere(name="ensemble", importance=30)
c21.ajouterLien(Lien(coeur=c31, typeLien=SUITE, importance=20))

c32 = CoeurDescriptifVerbal(sujet=Voyageurs, action=Action(name = "marcher"))
c32.ajouterLieu(name="dans la forêt", importance=10)
c21.ajouterLien(Lien(coeur=c32, typeLien = CAUSE, importance = 5))

Loup = Objet({"lib":"loup"})
c33 = CoeurAction(sujet = Loup, action = Action(name="battre"), cod = Milou, ton = "triste")
c33.ajouterMoment(date=datetime(2021,2,21), importance=200)
c22.ajouterLien(Lien(coeur=c33, typeLien = CAUSE, importance = 10))

Promenade = Objet({"lib":"promenade"})
c41 = CoeurAction(sujet = [Alice, Milou], action = Action(name="continuer"), cod = Promenade)
c31.ajouterLien(Lien(coeur=c41, typeLien=SUITE, importance=20))

c42 = CoeurDescriptif(sujet=Milou, carac=CaracChiffree(name="blesse", value=9), ton = "triste")
c33.ajouterLien(Lien(coeur=c42, typeLien=CONSEQUENCE, importance=20))

c51 = CoeurAction(sujet=[Alice, Milou], action=Action(name="monter"))
c51.ajouterLieu(name="sur la montagne")
c41.ajouterLien(Lien(coeur=c51, typeLien=SUITE, importance = 10))

c52 = CoeurAction(sujet=Alice, action=Action(name="pêcher"))
c52.ajouterLieu(name="à la rivière")
c41.ajouterLien(Lien(coeur=c52, typeLien=OBJECTIF, importance =20))

c6 = CoeurAction(sujet = [Alice, Milou], action = Action(name="dormir"))
c6.ajouterManiere(name="à la belle étoile")
c51.ajouterLien(Lien(coeur=c6, typeLien=SUITE, importance = 20))

h1 = Histoire(head=c1, titre="Alice promène son chien Milou")
Alice.creerHistoire(h1)
### MAIN ###

AJD = datetime(2021,3,22)
print("█ 1ère rencontre █\n")
print("█ Histoires connues par Bob : " + ', '.join(map(str,Bob.histoires)) + "\n")
print(dialogue(Alice, Bob, date=AJD, useTranslation=False, useCorrection=False))
print("\n█ Bob a apprit une histoire : " + ', '.join(map(str,Bob.histoires)))
print("\n█ 2ème rencontre █\n")
print(dialogue(Bob, Charles, date=AJD, useTranslation=False, useCorrection=False))

with open('transmission_histoires.pkl', 'wb') as output:
    histoire1 = Alice.histoires[0]
    pickle.dump(histoire1, output, pickle.HIGHEST_PROTOCOL)
    histoire2 = Bob.histoires[0]
    pickle.dump(histoire2, output, pickle.HIGHEST_PROTOCOL)
    histoire3 = Charles.histoires[0]
    pickle.dump(histoire3, output, pickle.HIGHEST_PROTOCOL)

del histoire1
del histoire2
del histoire3