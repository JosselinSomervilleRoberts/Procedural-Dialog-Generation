# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 15:41:05 2021

@author: lenovo
"""

import warnings
warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made")
warnings.filterwarnings("ignore", message="Trying to unpickle estimator")

from psclib.diversifieur import correct, cong, diversifier, get_syn, buildSynonyms
from psclib.action import Action
from psclib.objet import Objet, Personnage
from psclib.caracteristique import Caracteristique, Type, CaracChiffree
from psclib.histoire import Histoire, ajouterPonctuation, demanderLien, nePasSavoirLien, SUITE, CAUSE, CONSEQUENCE
from psclib.coeuraction import CoeurAction
from psclib.coeurdescriptif import CoeurDescriptif
from psclib.lien import Lien
from psclib.dialogue import dialogue, pickStory, raconter, quiparle, transition, fin, testContinuer, intersection, switcheroo, intro, connait


villageois = Personnage({"prenom":"Villageois","nom":"Bob","sexe":"m","age":29,"humeur":"effrayé"})
villageois.caracs[0].value = 4
villageois.caracs[1].value = 8
villageois.caracs[2].value = 6

dragon = Objet({"lib":"dragon","noms":["un dragon","un gigantesque dragon":"une créature draconique"]})

garde = Personnage({"prenom":"Garde","nom":"Steven","sexe":"m","age":43,"humeur":"alarmé"})
garde.caracs[0].value = 2
garde.caracs[1].value = 8
garde.caracs[2].value = 7

seigneur = Personnage({"prenom":"Seigneur","nom":"Godefroy","sexe":"m","age":56,"humeur":"préoccupé"})
seigneur.caracs[0].value = 7
seigneur.caracs[1].value = 4
seigneur.caracs[2].value = 9

lancelot = Personnage({"prenom":"Lancelot","nom":"du Lac","sexe":"m","age":34,"humeur":"fier"})
lancelot.caracs[0].value = 8
lancelot.caracs[1].value = 6
lancelot.caracs[2].value = 8


c1 = CoeurAction(sujet=villageois, action=Action(expressions=[[0.5,"[voir]"],[0.2,"[aperçevoir]"],[0.2,"[découvrir]"],[0.1,"[entrevoir]"]]), cod=dragon, lieu="derrière la montagne")
c2 = CoeurAction(sujet=villageois, action=Action(expressions=[[0.4,"[courir]"],[0.3,"se [précipiter]"],[0.3,"[accourir]"]]), lieu="ici")
c1.liens.append(Lien(coeur=c2,typeLien=CONSEQUENCE))

c3 = CoeurAction(sujet=seigneur, action=Action(expressions=[[1,"[envoyer]"]]), lieu="derrière la montagne")
c4 = CoeurAction(sujet=lancelot, action=Action(expressions=[[0.4,"[vaincre]"],[0.4,"[tuer]"],[0.2,"[terrasser]"]]), cod=dragon)
c3.liens.append(Lien(coeur=c4,typeLien=SUITE))
c5 = CoeurDescriptif(sujet=seigneur, carac=CaracChiffree(carac=Caracteristique(lib="soulagé"), value=5))
c4.liens.append(Lien(coeur=c5,typeLien=CONSEQUENCE))
c4b = CoeurAction(sujet=lancelot, action=Action(expressions=[[1,"[se faire tuer]"]]), cod=dragon)
c3.liens.append(Lien(coeur=c4b,typeLien=SUITE))
c5b = CoeurDescriptif(sujet=seigneur, carac=CaracChiffree(carac=Caracteristique(lib="soulagé"), value=0))
c4.liens.append(Lien(coeur=c5b,typeLien=CONSEQUENCE))

h1 = Histoire(head=c1,titre="Appariton du dragon")
villageois.histoires.append(h1)
h2 = Histoire(head=c3,titre="Dragon battu")

print(dialogue(garde,villageois)) #Le villageois alerte le garde de la présence d'un dragon
print("----------------------------")
print(dialogue(garde,seigneur)) #Le garde alerte le seigneur de la présence d'un dragon
print("----------------------------")
seigneur.histoires.append(h2) #Ajout d'une histoire : le seigneur a envoyé Lancelot tuer le dragon (il a soit réussi, soit échoué)
print(dialogue(seigneur,garde)) #Le seigneur informe son garde du sort du dragon et de Lancelot