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
def intro(p1,p2, useTranslation=True, useCorrection=True) : #p1 et p2 sont des objets Personnage
  etat = int(connait(p1,p2)) + 2*int(connait(p2,p1)) #etat est un entier

  if etat==0 : #les deux personnages ne se connaissent pas
    return accroche0(p1,p2, useTranslation=useTranslation, useCorrection=useCorrection)
  if etat==1 : #p1 connait p2 mais pas l'inverse
    return accroche1(p1,p2, useTranslation=useTranslation, useCorrection=useCorrection)
  if etat==2 : #p2 connait p1 mais pas l'inverse
    return accroche1(p2,p1, useTranslation=useTranslation, useCorrection=useCorrection)
  if etat==3 : #Les deux personnages se connaissent
    return accroche2(p1,p2, useTranslation=useTranslation, useCorrection=useCorrection)

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
  resteA, resteB, intersection, intersectionDif = [], [], [], []
  for a in histsA : #construction de l'intersection et du reste de histsA
    isInB = False
    for b in histsB :
      if a.titre==b.titre :
        #print(a.conteur, b.conteur)
        if a.conteur == b.conteur:
            intersection.append(a)
        else:
            intersectionDif.append(a)
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
      
  return resteA, resteB, intersection, intersectionDif

#------------- Les accroches, pour introduire le dialogue -------------- IL FAUT FAIRE L'ETAPE DE PRESENTATION ELEMENTAIRE
def accroche0(p1, p2, useTranslation=True, useCorrection=True) : #Les deux personnages ne se connaissent pas -> Chacun se crée une représentation de l'autre
  p, q = switcheroo(p1,p2) #On ne s'intéresse qu'au premier objet renvoyé
  s = p.imprimer("Bonjour étranger, je ne vous ai jamais vu ici...", useTranslation=useTranslation, useCorrection=useCorrection)
  s += "\n" + q.imprimer("Bonjour, moi non plus. Je m'appelle " + q.prenom + " " + q.nom + ". Et vous?", useTranslation=useTranslation, useCorrection=useCorrection)
  s += "\n" + p.imprimer("Moi je m'appelle " + p.prenom + " " + p.nom + ". Enchanté, " + q.prenom + " " + q.nom +". ", diversify=False, useTranslation=useTranslation, useCorrection=useCorrection)
  s += "\n" + q.imprimer("Enchanté, " + p.prenom + " " + p.nom +". ", diversify=False, useTranslation=useTranslation, useCorrection=useCorrection)
  p1.contacts.append(p2.copyStrip())
  p2.contacts.append(p1.copyStrip())
  return s

def accroche1(p1, p2, useTranslation=True, useCorrection=True) : #p1 connaît p2 mais pas l'inverse -> p2 se crée une représentation de p1
  s = p1.imprimer("Bonjour ! Vous êtes "+p2.prenom+" "+p2.nom+", c'est ça ?", useTranslation=useTranslation, useCorrection=useCorrection)
  s += "\n" + p2.imprimer("Euh, oui. Je ne vous connais pas, vous êtes... ?", useTranslation=useTranslation, useCorrection=useCorrection)
  s += "\n" + p1.imprimer(p1.prenom+" "+p1.nom+", enchanté. J'ai entendu parler de vous, c'est pour ça haha.", useTranslation=useTranslation, useCorrection=useCorrection)
  s += "\n" + p2.imprimer("Haha en effet.", diversify=False, useTranslation=useTranslation, useCorrection=useCorrection)
  p2.contacts.append(p1.copyStrip())
  return s

def accroche2(p1, p2, useTranslation=True, useCorrection=True) : #Les deux personnages se connaissent
  s = p1.imprimer("Salut mon pote !", useTranslation=useTranslation, useCorrection=useCorrection)
  s += "\n" + p2.imprimer("Salut à toi également l'ami !", useTranslation=useTranslation, useCorrection=useCorrection)
  return s

#------------- Les personnages ne racontent pas forcément leurs histoires jusqu'au bout
def testContinuer(p1,p2) : #On détermine si la conversation continue (=True) ou se termine (=False) selon les affinités des personnages (et une part d'aléatoire)
  return False #bool(random.getrandbits(1)) ############ FONCTION TEMPORAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIREEEEEEEEEEEEEEEEEEE

#------------- La fin du dialogue
def fin(p1,p2, useTranslation=True, useCorrection=True) : #Fonction temporaire (à redéfinir pour prendre en compte les affinités entre les personnages)
  s = p1.imprimer("Bon, c'était sympa de discuter.", useTranslation=useTranslation, useCorrection=useCorrection)
  s += "\n" + p2.imprimer("Oui totalement !", diversify=False, useTranslation=useTranslation, useCorrection=useCorrection)
  s += "\n" + p1.imprimer("Allez, à la prochaine fois !", useTranslation=useTranslation, useCorrection=useCorrection)
  s += "\n" + p2.imprimer("Salut !", diversify=False, useTranslation=useTranslation, useCorrection=useCorrection)
  return s

#------------- Les transitions (pas entamé pour le moment)
def transition(useTranslation=True, useCorrection=True) :
  return "---"

#------------- Détermination du locuteur et de l'interlocuteur / du cas où les personnages n'ont rien à raconter (pas d'histoire / histoires connues par les deux)
def quiparle(p1,p2) :
  hists1, hists2, intersect, intersectionDif = intersection(p1.histoires, p2.histoires)
  if len(hists1)==0 :
    if len(hists2)==0 : #Les deux personnages n'ont rien à dire
      if len(intersectionDif) > 0:
          return p1, p2
      else:
          return None, None #Cas particulier
    else : #p1 n'a rien à dire, mais p2 si -> p2 est le locuteur (1ère position)
      return p2, p1
  else :
    if len(hists2)==0 : #p2 n'a rien à dire, mais p1 si -> p1 est le locuteur (1ère position)
      return p1, p2
    else : #Les deux ont quelque chose à raconter
      return switcheroo(p1,p2) #On choisit au hasard


#------------- #Fonction d'affichage de l'histoire ----------------------------- A DEVELOPPER PLUS TARD, pour prendre en compte le fait que l'histoire ne soit pas forcément racontée en entier
def raconter(loc, interloc, date=None, useTranslation=True, useCorrection=True) :
  histoire = pickStory(loc, interloc)
  s = histoire.toText(loc, interloc, date=date, useTranslation=useTranslation, useCorrection=useCorrection)
  return s, histoire #On retourne l'histoire racontée, pour l'ajouter plus tard dans la liste d'histoires connues par l'interlocuteur

#------------- #Fonction de sélection de l'histoire à raconter, qui n'est pas dans la liste des histoires connues par l'interlocuteur
def pickStory(loc, interloc) :
  resteLoc, resteInterloc, intersect, intersectionDif = intersection(loc.histoires, interloc.histoires) #On prend les histoires que l'interlocuteur ne connaît pas
  if len(resteLoc) > 0:
      return resteLoc[random.randrange(len(resteLoc))] #On en prend une au hasard
  else:
      if len(intersectionDif) > 0: return intersectionDif[random.randrange(len(intersectionDif))]
      return None

#------------- #Fonction de réaction à la fin d'une histoire
def reaction(histoire,interloc) :
    if histoire.ton == "triste" :
        return reactiontriste(interloc)  # reaction d'une histoire triste
    if histoire.ton == "neutre" :
        return reactionneutre(interloc)  # reaction d'une histoire neutre
    if histoire.ton == "joyeuse" :
        return reactionjoyeuse(interloc)  # reaction d'une histoire joyeuse
    
    return "Je m'en fiche."            # pas de reaction


#------------- #Les réactions d'une histoire---------------------------------
def reactiontriste(interloc):    # reaction d'une histoire triste
    a = random.randint(1,2)
    if a == 1 :
        s = interloc.imprimer("Ah c'est dommage!", diversify=False)
    if a == 2 :   
        s = interloc.imprimer("Oh la la c'est vraiment triste!", diversify=False)
    #if a == 3 :
    return s

def reactionneutre(interloc):  # reaction d'une histoire neutre
    a = random.randint(1,2)
    if a == 1 :
        s = interloc.imprimer("Ah bon.", diversify=False)
    if a == 2 :   
        s = interloc.imprimer("Oh.", diversify=False)
    #if a == 3 :
    return s

def reactionjoyeuse(interloc):  # reaction d'une histoire joyeuse
    a = random.randint(1,2)
    if a == 1 :
        s = interloc.imprimer("Ah c'est bien!", diversify=False)
    if a == 2 :   
        s = interloc.imprimer("Wow c'est cool!", diversify=False)
    #if a == 3 :
    return s
#-------------------------------------------------- La fonction (principale) du dialogue ----------------------------------------------
def dialogue(p1,p2, date=None, useTranslation=True, useCorrection=True) :
  s = intro(p1,p2, useTranslation=useTranslation, useCorrection=useCorrection) #L'intro
  continuer = True
  premierCycle = True #Indicateur
  while continuer :
    loc, interloc = quiparle(p1,p2) #On décide qui parle
    if loc!=None : #Cas normal : un personnage a une histoire à raconter
      s += "\n" + transition(useTranslation=useTranslation, useCorrection=useCorrection) #à définir
      s1, histoire = raconter(loc, interloc, date=date, useTranslation=useTranslation, useCorrection=useCorrection) #On choisit et raconte une histoire
      s += "\n" + s1
      s += "\n" + reaction(histoire,interloc)
      #interloc.histoires.append(histoire) #L'interlocuteur connaît maintenant l'histoire qu'on lui a raconté (à modifier, car en réalité il ne connait pas forcément TOUTE l'histoire)
      continuer = testContinuer(loc,interloc) #On teste si les personnages continuent de dialoguer
    else : #Les deux personnages n'ont pas d'histoire à se raconter
      continuer = False
      if premierCycle : #Cas où les personnages n'ont rien échangé avant que le dialogue se termine
        s += "\n" + "~~ Les deux personnages n'ont rien à se dire... Une gêne sensible s'installe... ~~"
    premierCycle = False
  s += "\n" + fin(p1,p2, useTranslation=useTranslation, useCorrection=useCorrection)
  return s