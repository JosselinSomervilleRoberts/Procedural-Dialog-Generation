# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 13:52:15 2021

@author: josse
"""


# CE FICHIER DOIT ETRE SITUE EN DEHORS DU DOSSIER PSCLIB






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





# ======================== Pour créer une caractéristique ======================== #
# On peut récupérer une caracteristique existante :
mysterieux = Caracteristique(name="mysterieux")

# En créer une nouvelle avec l'échelle de base (pas du tout, pas tres, un peu, tres, beaucoup, ...)
beaute = Caracteristique(lib="beau")
preoccupe = Caracteristique(lib="préoccupé")

# En créer une nouvelle avec une échelle personnalisée 
taille = Caracteristique(lib="taille", keepLib=False, intervals=[[0, "minuscule"], [1, "très petit"], [2, "petit"], [4, "pas très grand"], [5, "de taille normale"], [6, "grand"], [7, "très grand"], [8, "gigantesque"], [9, "colossal"]])
# Correspondance pour la taille :
# - de 0 à 1 : minuscule
# - de 1 à 2 : très petit
# - de 2 à 4 : petit
# - de 4 à 5 : pas très grand
# - de 5 à 6 : de taille normale
# - de 6 à 7 : grand
# - de 7 à 8 : très grand
# - de 8 à 9 : gigantesque
# - de 9 à 10 : colossal
# ================================================================================ #






# ======================== Pour créer un personnage ======================== #
# On peut récupérer un personnage existant :
marcel   =     Personnage(name="marcel")
jackie   =     Personnage(name="jackie")

# En créer un nouveau (à part nom, prenom aucun champ n'est obligatoire)
sammy    =     Personnage({"prenom": "Sammy",
                           "nom":"",
                           "sexe":"m",          # Sert pour les accords
                           "age":20,            # Non utilisé
                           "ticsLangages": {"": 5, "euh": 0.5, "hum": 0.5},         # Tics de langages avec leur proba (la somme doit être égale à 1)
                           "caracs": [CaracChiffree(name="bavard", value=8),        # Contrôle si un personnage parle beaucoup ou pas
                                      CaracChiffree(name="curiosite", value=10),    # Contrôle si un personnage pose beaucoup de questions
                                      CaracChiffree(name="hésitation", value=2),    # Contrôle le nombre de "euh..."
                                      CaracChiffree(name="memoire", value=8),       # Contrôle la capacité de retenir une histoire et les questions au fur et à mesure du dialogue
                                      CaracChiffree(name="compassion", value=6),    # Contrôle les réactions (émotions)
                                      CaracChiffree(carac=beaute, value = 2),       # Caractéristique uniquement descriptive
                                      CaracChiffree(carac=taille, value = 8)]})     # Caractéristique uniquement descriptive

# Il faut bien penser à ajouter les relations (dans les deux sens)
marcel.ajouterRelations({"ami":jackie})
jackie.ajouterRelations({"ami":marcel})
# ========================================================================== #






# ======================== Pour créer un objet ======================== #
# Il n'y a pas d'objets enregistrées, il faut les créer à chaque fois : (seul un lib ou un noms suffisent) :
boulangerie = Objet(dico={"lib": "boulangerie"})
boulangerie.isLieu = True

couteau = Objet(dico={"lib": "couteau"})

chien = Objet(dico={"lib": "chien",
                    "noms": ["Scooby-Doo", "Scooooby-Doo-bydooo"],
                    "caracs": [CaracChiffree(carac=beaute, value = 10),       
                               CaracChiffree(carac=taille, value = 5)]})

# On peut ensuite ajouter l'objet comme possession à quelqu'un
chien = sammy.ajouterPossession(chien)

# Ou on peut créer l'objet au moment où on l'ajoute comme possession
van = sammy.ajouterPossession(dico={"lib": "van"})

indices = Objet(dico={"lib": "indice", "quantite": 2})
# ===================================================================== #






# ======================== Pour créer une action ======================== #
# On peut récupérer une action existante :
rouler = Action(name="rouler")

# En créer une nouvelle : (il fuat donner la LISTE des expresssions)
# - la somme des probas des expressions doit être égale à 1
# Voici la structure :
# (xxx) :  xxx doit être conjugué
# [yyy] : yyy peut être remplacé par un synonyme
# C'est possible de faire ([zzz]) : pour conjuguer et utiliser les synonymes
enqueter = Action(lib="enquêter",
                  expressions = [[0.6, "[(enquêter)]"], [0.2, "[(investiguer)]"], [0.2, "[(mener)] l'enquête"]])
chercher = Action(lib="chercher",
                  expressions = [[1, "[(chercher)]"]]) # Attention aux doubles crochets
trouver = Action(lib="trouver",
                  expressions = [[0.8, "[(trouver)]"], [0.2, "[(découvrir)]"]])
monter = Action(lib="monter",
                  expressions = [[1, "[(monter)] dans"]]) # Attention aux doubles crochets

# On peut ajouter des adverbes :
rouler.adverbes = ["très vite"]
# ===================================================================== #





# ======================== Pour créer un coeur ======================== #
# Il y a 3 type de coeur :
# - CoeurAction : sujet, action, (cod) -> représente réellement une action, un truc qui se passe
# - CoeurDescriptif : sujet, caractéristique -> qualifie un objet
# - CoeurDescriptifVerbal : même chose que CoeurAction mais est traité comme une description (pour la concordance des temps notamment)

c1 = CoeurDescriptifVerbal(sujet=[sammy, chien], action=enqueter, ton="neutre")
c2 = CoeurDescriptifVerbal(sujet=sammy, action=chercher, cod=indices, ton="neutre")
c3 = CoeurDescriptif(sujet=sammy, carac=CaracChiffree(carac=preoccupe, value=8), ton="triste")
c4 = CoeurAction(sujet=[sammy, chien],  action=monter, cod=van, ton="neutre")
c5 = CoeurAction(sujet=van,  action=rouler)

c_moment = CoeurAction(sujet=chien, action=trouver, cod=couteau)
# ===================================================================== #





# ======================== Pour ajouter un lien ======================== #
# La suite ne montre pas un très bon exemple
# Si possible, il faut essayer de mettre les liens dans l'ordre
# C'est à dire, tous els liens de c1, puis tous ceux de c2, etc...


# Il y a 7 types de liens :
# - COMPLEMENT
# - COMPLEMENT_LIEU
# - COMPLEMENT_TEMPS
# - COMPLEMENT_MANIERE
# - OBJECTIF
# - CAUSE
# - CONSEQUENCE
# - SUITE

# Les compléments s'ajoutent de cette façon :
# COMPLEMENT :
# - un string
c1.ajouterComplement(name="sur un meurtre",     importance=20)

# LIEU :
# - un string
# OU
# - un objet avec un rapport (par défaut le rapport est "à")
c1.ajouterLieu(name="chez le boulanger",            importance=5)
c2.ajouterLieu(lieu=boulangerie, rapport="dans",    importance=10)

# MOMENT :
# - un string
# OU
# - une date
# OU
# - un rapport à un coeur
# ATTENTION : pour la ocncordance des temps, c'est bien de définir au moins UNE date au DEBUT de l'histoire.
# On est pas obligé de préciser la date pour chaque coeur, elle se propage automatiquement
# Par contre "hier" ou "demain" ne sont pas reconnus, il faut se servir des dates à la place
# Si on ne veut pas que la date n'apparaisse pas, on peut tout simplement regler l'importance à 0
c2.ajouterMoment(name="juste après",                   importance=5)
c1.ajouterMoment(date=datetime(2021,4,29),             importance=2)
c3.ajouterMoment(moment=c_moment, rapport="après",     importance=20)

# MANIERE :
# - un string
# C'est important de le différencier de COMPLEMENT
# Les questions ne seront pas posées de la même façon      
c1.ajouterManiere(name="avec tristesse",        importance=2)

# Les autres liens :
c1.ajouterLien(Lien(coeur=c2, typeLien=SUITE, importance=10))
c2.ajouterLien(Lien(coeur=c3, typeLien=SUITE, importance=10))
c3.ajouterLien(Lien(coeur=c4, typeLien=CONSEQUENCE, importance=5))
c4.ajouterLien(Lien(coeur=c5, typeLien=SUITE, importance=10))
# ====================================================================== #





# ======================== Pour créer une histoire ======================== #
hist = Histoire(head=c1, titre="L'enquête du meurtre du boulanger")
marcel.creerHistoire(hist)
# ========================================================================= #






# ======================== Pour raconter l'histoire ======================== #
ajd = datetime(2021,5,1)
script = dialogue(marcel, jackie, date=ajd, useTranslation=False, useCorrection=False)
print(script)
# ========================================================================= #