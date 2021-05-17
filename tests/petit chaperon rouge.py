# -*- coding: utf-8 -*-
"""
Created on Wed May  5 15:07:46 2021

@author: lenovo
"""
###### CE FICHIER DOIT ETRE SITUE EN DEHORS DU DOSSIER PSCLIB

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from psclib.objet import Personnage
from psclib.dialogue import dialogue
from psclib.caracteristique import CaracChiffree, Caracteristique
from psclib.coeuraction import CoeurAction
from psclib.coeurdescriptif import CoeurDescriptif
from psclib.coeurdescriptifverbal import CoeurDescriptifVerbal
from psclib.action import Action
from psclib.objet import Objet
from psclib.lien import Lien
from psclib.histoire import CONSEQUENCE, OBJECTIF, SUITE, CAUSE, Histoire
from datetime import datetime


beaute = Caracteristique(lib="beau")
malade = Caracteristique(lib="malade", keepLib=False, intervals=[[0, "minuscule"], [1, "très petit"], [2, "un peu"], [4, "pas très grand"], [5, "de taille normale"], [6, "grand"], [7, "gravement"], [8, "gravement"], [9, "gravement"]])
taille = Caracteristique(lib="taille", keepLib=False, intervals=[[0, "minuscule"], [1, "très petit"], [2, "petit"], [4, "pas très grand"], [5, "de taille normale"], [6, "grand"], [7, "très grand"], [8, "gigantesque"], [9, "colossal"]])

marcel   =     Personnage({"prenom": "Marcel",
                           "nom":"",
                           "sexe":"m",          # Sert pour les accords
                           "age":20,            # Non utilisé
                           "ticsLangages": {"": 5, "euh": 0.5, "hum": 0.5},         # Tics de langages avec leur proba (la somme doit être égale à 1)
                           "caracs": [CaracChiffree(name="bavard", value=10),        # Contrôle si un personnage parle beaucoup ou pas
                                      CaracChiffree(name="curiosite", value=10),    # Contrôle si un personnage pose beaucoup de questions
                                      CaracChiffree(name="hésitation", value=2),    # Contrôle le nombre de "euh..."
                                      CaracChiffree(name="memoire", value=8),       # Contrôle la capacité de retenir une histoire et les questions au fur et à mesure du dialogue
                                      CaracChiffree(name="compassion", value=6)]})

sammy    =     Personnage({"prenom": "Sammy",
                           "nom":"",
                           "sexe":"m",          # Sert pour les accords
                           "age":20,            # Non utilisé
                           "ticsLangages": {"": 5, "euh": 0.5, "hum": 0.5},         # Tics de langages avec leur proba (la somme doit être égale à 1)
                           "caracs": [CaracChiffree(name="bavard", value=5),        # Contrôle si un personnage parle beaucoup ou pas
                                      CaracChiffree(name="curiosite", value=10),    # Contrôle si un personnage pose beaucoup de questions
                                      CaracChiffree(name="hésitation", value=8),    # Contrôle le nombre de "euh..."
                                      CaracChiffree(name="memoire", value=8),       # Contrôle la capacité de retenir une histoire et les questions au fur et à mesure du dialogue
                                      CaracChiffree(name="compassion", value=6)]}) 
pcr = Personnage({"prenom": "Le petit chaperon rouge",
                           "nom":"",
                           "sexe":"f",          
                           "age":8,          
                           "caracs": [CaracChiffree(name="bavard", value=8),        # Contrôle si un personnage parle beaucoup ou pas
                                      CaracChiffree(name="curiosite", value=10),    # Contrôle si un personnage pose beaucoup de questions
                                      CaracChiffree(name="hésitation", value=2),    # Contrôle le nombre de "euh..."
                                      CaracChiffree(name="memoire", value=8),       # Contrôle la capacité de retenir une histoire et les questions au fur et à mesure du dialogue
                                      CaracChiffree(name="compassion", value=6),    # Contrôle les réactions (émotions)
                                      CaracChiffree(carac=beaute, value = 10)]})
grandmere = Personnage({"prenom": "La grand-mère",
                           "nom":"",
                           "sexe":"f",          
                           "age":80,          
                           "caracs": [CaracChiffree(name="bavard", value=8),        # Contrôle si un personnage parle beaucoup ou pas
                                      CaracChiffree(name="curiosite", value=10),    # Contrôle si un personnage pose beaucoup de questions
                                      CaracChiffree(name="hésitation", value=2),    # Contrôle le nombre de "euh..."
                                      CaracChiffree(name="memoire", value=8),       # Contrôle la capacité de retenir une histoire et les questions au fur et à mesure du dialogue
                                      CaracChiffree(name="compassion", value=6),    # Contrôle les réactions (émotions)
                                      CaracChiffree(carac=malade, value = 8)]})

marcel.ajouterRelations({"ami":sammy})
sammy.ajouterRelations({"ami":marcel})



#foret = Objet(dico={"lib": "forêt"})
#foret.isLieu = True
chezgrandmere = Objet(dico={"lib": "chez la grand-mère"})
chezgrandmere.isLieu = True

#pcr =  Objet(dico={"lib": "le petit chaperon rouge"})
loup = Objet(dico={"lib": "loup"})
#grandmere = Objet(dico={"lib": "la grand-mère", "caracs": [CaracChiffree(carac=malade, value = 8),  CaracChiffree(carac=taille, value = 5)]})
#grandmere = pcr.ajouterPossession(grandmere)
papillon = Objet(dico={"lib": "papillon"})

sortir = Action(lib="sortir",
                  expressions = [[1, "[(sortir)]"]])
voir = Action(name="voir")
#allervoir = Action(lib="aller voir")
rencontrer = Action(name="rencontrer")
partir = Action(lib="partir",
                  expressions = [[1, "[(partir)]"]])
vouloirmanger = Action(lib="vouloir manger",
                  expressions = [[1, "[(vouloir)] manger"]])
arriver = Action(lib="arriver",
                  expressions = [[1, "[(arriver)]"]])
chasser = Action(name="chasser")
manger = Action(name="manger")

partir.adverbes = ["très vite"]
arriver.adverbes = ["tardivement"]

c1 = CoeurAction(sujet = pcr,action = sortir,ton = "neutre")
c1.ajouterManiere(name="avec des galettes", importance= 5)
c2 = CoeurAction(sujet = pcr,action = voir, cod = grandmere, ton = "neutre")
c3 = CoeurDescriptif(sujet=grandmere, carac=CaracChiffree(carac = malade, value=8), ton = "triste")
c4 = CoeurAction(sujet = pcr,action = rencontrer, cod = loup, ton = "neutre")
c4.ajouterLieu(name="dans la forêt",            importance=5)
c5 = CoeurAction(sujet = loup ,action = partir, ton = "neutre")
c6 = CoeurAction(sujet = loup ,action = vouloirmanger, cod = grandmere, ton = "triste")
c7 = CoeurAction(sujet = pcr ,action = arriver, ton = "triste")
c7.ajouterLieu(name="chez la grand-mère",            importance=5)
#c7.ajouterLieu(lieu=foret, rapport="",    importance=10)

c8 = CoeurAction(sujet = pcr ,action = chasser, cod = papillon, ton = "joyeux")
c9 = CoeurAction(sujet = loup ,action = manger, cod = pcr, ton = "triste")


c1.ajouterLien(Lien(coeur=c2, typeLien=OBJECTIF, importance=10))
c2.ajouterLien(Lien(coeur=c3, typeLien=CAUSE, importance=10))
c1.ajouterLien(Lien(coeur=c4, typeLien=SUITE, importance=10))
c4.ajouterLien(Lien(coeur=c5, typeLien=SUITE, importance=10))
c5.ajouterLien(Lien(coeur=c6, typeLien=CAUSE, importance=10))
c5.ajouterLien(Lien(coeur=c7, typeLien=SUITE, importance=10))
c7.ajouterLien(Lien(coeur=c8, typeLien=CAUSE, importance=10))
c7.ajouterLien(Lien(coeur=c9, typeLien=CONSEQUENCE, importance=10))

ajd = datetime(2021,1,22)

hist = Histoire(head=c1, titre="Le petit chaperon rouge")
sammy.creerHistoire(hist)

script = dialogue(marcel, sammy, date=ajd, useTranslation=False, useCorrection=False)
print(script)
