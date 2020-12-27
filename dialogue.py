# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 00:52:22 2020

@author: josse
"""


import random
from psclib.diversifieur import diversifier



#--------------------------------------- Ensemble de fonctions secondaires pour le dialogue -------------------------------------

#----------- Fonction pour tester si p1 connaît p2 (non réflexif)
def connait(p1,p2): #p1 et p2 sont des objets Personnage
  for p in p1.contacts:
    if p.id == p2.id :
      return True
  return False

#----------- L'introduction du dialogue
def intro(p1,p2) : #p1 et p2 sont des objets Personnage
  etat = int(connait(p1,p2)) + 2*int(connait(p2,p1)) #etat est un entier
  if etat==0 : #les deux personnages ne se connaissent pas
    p2.contacts.append(p1.copyStrip()) #On ajoute un nouveau personnage, qui est une version "light" de p1 (plus tard, ce nouveau personnage n'aura que les caractéristiques connues par p2)
    p1.contacts.append(p2.copyStrip())
  if etat==1 : #p1 connait p2 mais pas l'inverse
    p2.contacts.append(p1.copyStrip())
  if etat==2 : #p2 connait p1 mais pas l'inverse
    p1.contacts.append(p2.copyStrip())

  if etat==0 :
    return accroche0(p1,p2)
  if etat==1 :
    return accroche1(p1,p2)
  if etat==2 : 
    return accroche1(p2,p1)
  if etat==3 :
    return accroche2(p1,p2)

  print("GROS PROBLEME DANS INTRO")
  return ""

#------------- Fonction annexe
def switcheroo(a,b) : #Echange aléatoirement a et b (peu importe ce que sont a et b)
    if random.randint(0,1) :
      return a, b
    else :
      return b, a

#------------- Fonction annexe
def intersection(histsA, histsB) : #On part de deux listes d'objets Histoire A et B, et on construit l'intersection, le reste de A et le reste B
  resteA, resteB, intersection = [], [], []
  for a in histsA : #construction de l'intersection et du reste de histsA
    isInB = False
    for b in histsB :
      if a.titre==b.titre :
        intersection.append(a)
        isInB = True
    if not (isInB) :
      resteA.append(a)
  for b in histsB : #construction du reste de histsB
    isInI = False
    for i in intersection :
      if i.titre==b.titre :
        isInI = True
    if not (isInI) :
      resteB.append(b)
  return resteA, resteB, intersection

#------------- Les accroches, pour introduire le dialogue
def accroche0(p1, p2) : #Les deux personnages ne se connaissent pas
  p, osef = switcheroo(p1,p2) #On ne s'intéresse qu'au premier objet renvoyé
  s = p.imprimer("Bonjour étranger, je ne vous ai jamais vu ici...")
  s += "\n" + osef.imprimer("Bonjour, moi non plus. Je m'appelle " + osef.prenom + " " + osef.nom + ". Et vous?")
  s += "\n" + p.imprimer("Moi je m'appelle " + p.prenom + " " + p.nom + ". Enchanté, " + osef.prenom + " " + osef.nom +". ")
  s += "\n" + osef.imprimer("Enchanté, " + p.prenom + " " + p.nom +". ")
  return s

def accroche1(p1, p2) : #p1 connaît p2 mais pas l'inverse
  s = p1.imprimer(diversifier("Bonjour ! Vous êtes "+p2.prenom+" "+p2.nom+", c'est ça ?"))
  s += "\n" + p2.imprimer(diversifier("Euh, oui. Je ne vous connais pas, vous êtes... ?"))
  s += "\n" + p1.imprimer(p1.prenom+" "+p1.nom+", enchanté. J'ai entendu parler de vous, c'est pour ça haha.")
  s += "\n" + p2.imprimer("Haha en effet.")
  return s

def accroche2(p1, p2) : #Les deux personnages se connaissent
  s = p1.imprimer("Salut mon pote !")
  s += "\n" + p2.imprimer("Salut à toi également l'ami !")
  return s

#------------- Les personnages ne racontent pas forcément leurs histoires jusqu'au bout
def testContinuer(p1,p2) : #On détermine si la conversation continue (=True) ou se termine (=False) selon les affinités des personnages (et une part d'aléatoire)
  return bool(random.getrandbits(1)) ############ FONCTION TEMPORAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIREEEEEEEEEEEEEEEEEEE

#------------- La fin du dialogue
def fin(p1,p2) : #Fonction temporaire (à redéfinir pour prendre en compte les affinités entre les personnages)
  s = p1.imprimer("Bon, c'était sympa de discuter.")
  s += "\n" + p2.imprimer("Oui totalement !")
  s += "\n" + p1.imprimer("Allez, à la prochaine fois !")
  s += "\n" + p2.imprimer("Salut !")
  return s

#------------- Les transitions (pas entamé pour le moment)
def transition() :
  return "---"

#------------- Détermination du locuteur et de l'interlocuteur / du cas où les personnages n'ont rien à raconter (pas d'histoire / histoires connues par les deux)
def quiparle(p1,p2) :
  hists1, hists2, intersect = intersection(p1.histoires, p2.histoires)
  if len(hists1)==0 :
    if len(hists2)==0 : #Les deux personnages n'ont rien à dire
      return None, None #Cas particulier
    else : #p1 n'a rien à dire, mais p2 si -> p2 est le locuteur (1ère position)
      return p2, p1
  else :
    if len(hists2)==0 : #p2 n'a rien à dire, mais p1 si -> p1 est le locuteur (1ère position)
      return p1, p2
    else : #Les deux ont quelque chose à raconter
      return switcheroo(p1,p2) #On choisit au hasard


#------------- #Fonction d'affichage de l'histoire ----------------------------- A DEVELOPPER PLUS TARD, pour prendre en compte le fait que l'histoire ne soit pas forcément racontée en entier
def raconter(loc, interloc) :
  histoire = pickStory(loc, interloc)
  s = histoire.toText(loc, interloc)
  return s, histoire #On retourne l'histoire racontée, pour l'ajouter plus tard dans la liste d'histoires connues par l'interlocuteur

#------------- #Fonction de sélection de l'histoire à raconter, qui n'est pas dans la liste des histoires connues par l'interlocuteur
def pickStory(loc, interloc) :
  resteLoc, resteInterloc, intersect = intersection(loc.histoires, interloc.histoires) #On prend les histoires que l'interlocuteur ne connaît pas
  return resteLoc[random.randrange(len(resteLoc))] #On en prend une au hasard





#-------------------------------------------------- La fonction (principale) du dialogue ----------------------------------------------
def dialogue(p1,p2) :
  s = intro(p1,p2) #L'intro
  continuer = True
  premierCycle = True #Indicateur
  while continuer :
    loc, interloc = quiparle(p1,p2) #On décide qui parle
    if loc!=None : #Cas normal : un personnage a une histoire à raconter
      s += "\n" + transition() #à définir
      s1, histoire = raconter(loc, interloc) #On choisit et raconte une histoire
      s += "\n" + s1
      interloc.histoires.append(histoire) #L'interlocuteur connaît maintenant l'histoire qu'on lui a raconté (à modifier, car en réalité il ne connait pas forcément TOUTE l'histoire)
      continuer = testContinuer(loc,interloc) #On teste si les personnages continuent de dialoguer
    else : #Les deux personnages n'ont pas d'histoire à se raconter
      continuer = False
      if premierCycle : #Cas où les personnages n'ont rien échangé avant que le dialogue se termine
        s += "\n" + "~~ Les deux personnages n'ont rien à se dire... Une gêne sensible s'installe... ~~"
    premierCycle = False
  s += "\n" + fin(p1,p2)
  return s