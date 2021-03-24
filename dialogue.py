# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 00:52:22 2020

@author: josse
"""


import random
from psclib.relation import Relation
from psclib.diversifieur import diversifier



#--------------------------------------- Ensemble de fonctions secondaires pour le dialogue -------------------------------------

#----------- Fonction pour tester si p1 connaît p2 (non réflexif)
def connait(p1,p2): #p1 et p2 sont des objets Personnage
  return p2.id in p1.contacts

#----------- L'introduction du dialogue
def intro(p1,p2, useTranslation=True, useCorrection=True) : #p1 et p2 sont des objets Personnage, p1 est le locuteur et p2 l'interlocuteur
  etat = int(connait(p1,p2)) + 2*int(connait(p2,p1)) #etat est un entier
  
  if not connait(p1,p2) :
      p1.contacts[p2.id] = Relation(p2.copyStrip())
  if not connait(p2,p1) :
      p2.contacts[p1.id] = Relation(p1.copyStrip())
  
  if p2.id in p1.contacts and p1.contacts[p2.id].getRelation().split("/")[0] == "famille":
      return accrocheFamille(p1,p2, useTranslation=useTranslation, useCorrection=useCorrection)
  
  if etat==0 : #les deux personnages ne se connaissent pas
    p1.contacts[p2.id].nbDiscussions += 1
    p2.contacts[p1.id].nbDiscussions += 1
    return accroche0(p1,p2)
  if etat==1 : #p1 connait p2 mais pas l'inverse
    return accroche1(p1,p2)
  if etat==2 : #p2 connait p1 mais pas l'inverse
    return accroche1(p2,p1)
  if etat==3 : #Les deux personnages se connaissent
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
  resteA, resteB, intersection, intersectionDif = [], [], [], []
  for a in histsA : #construction de l'intersection et du reste de histsA
    isInB = False
    for b in histsB :
      if a.titre==b.titre :
        #print(a.conteur, b.conteur)
        if a.conteur == b.conteur:
            intersection.append(a)
        else:
            intersectionDif.append((a,b))
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

#------------- Fonction annexe pour lire les parties scriptées depuis un fichier
def lireDepuisTxt(path, p1, p2) :
    f = open("psclib/fichiers_txt/"+path,"r", encoding="utf-8")
    listeStr = []
    ligne = f.readline()
    while ligne :
        listeStr.append(ligne)
        ligne = f.readline()
    f.close()
    if not listeStr : #Si erreur (fichier texte vide)
        s = "Erreur : fichier texte vide"
    else :
        s = random.choice(listeStr)
        s = token(p1, p2, s)
    return s

#------------- Fonction annexe de remplacage des tokens
def token(p1, p2, s) : #Remplace les tokens dans les parties scriptées
    s = s.replace("$n","\n")
    s = s.replace("$p1prenom", p1.prenom)
    s = s.replace("$p1nom", p1.nom)
    s = s.replace("$p2prenom", p2.prenom)
    s = s.replace("$p2nom", p2.nom)
    if p1.sexe == "f" :
        s = s.replace("$p1genre", "e")
        s = s.replace("$p1mrmme", "Mme")
    else :
        s = s.replace("$p1genre", "")
        s = s.replace("$p1mrmme", "Mr")
    if p2.sexe == "f" :
        s = s.replace("$p2genre", "e")
        s = s.replace("$p2mrmme", "Mme")
    else :
        s = s.replace("$p2genre", "")
        s = s.replace("$p2mrmme", "Mr")
    return s

#------------- Les accroches, pour introduire le dialogue -------------- IL FAUT FAIRE L'ETAPE DE PRESENTATION ELEMENTAIRE
def accroche0(p1, p2) : #Les deux personnages ne se connaissent pas -> Chacun se crée une représentation de l'autre
    p, q = switcheroo(p1,p2) #Cas particulier : on ne se soucie pas de qui est qui
    return lireDepuisTxt("intros/accroche2Inconnus.txt", p, q)

def accroche1(p1, p2) : #p1 connaît p2 mais pas l'inverse -> p2 se crée une représentation de p1
  return lireDepuisTxt("intros/accroche1Inconnu.txt", p1, p2)

def accroche2(p1, p2) : #Les deux personnages se connaissent
  return lireDepuisTxt("intros/accroche2Connus.txt", p1, p2)

def accrocheFamille(p1, p2,useTranslation=True, useCorrection=True):
    lien = p1.contacts[p2.id].getRelation().split("/")[1]
    print(lien)
    salutations = ["Coucou", "Salut"]
    appelation = ""
    if lien == "parent":
        appelation = ("papa" if p2.sexe == "m" else "maman")
    if lien == "adelphe":
        appelation = p2.prenom
    if lien == "enfant":
        if p2.sexe == "m":
            appelation = "mon fils"
        elif p2.sexe == "f":
            appelation = "ma fille"
        else:
            appelation = p2.prenom
            
    sal = random.choice(salutations)
    s = p1.imprimer(sal + " " + appelation + " !",  useTranslation=useTranslation, useCorrection=useCorrection) + "\n"
    s += p2.imprimer(sal + " !", useTranslation=useTranslation, useCorrection=useCorrection)  
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



def histoireQuiPeuventEtresRacontees(hists1, p1, p2):
    """Renvoie seulement les histoires dans hists1 que p1 peut raconter a p2"""
    lien = "inconnu"
    if p2.id in p1.contacts:
        lien = p1.contacts[p2.id].getRelation().split("/")[0]
    
    hists1_a_raconter = []
    for h in hists1:
        if lien in h.relationPourRaconter:
            hists1_a_raconter.append(h)
            
    return hists1_a_raconter



#------------- Détermination du locuteur et de l'interlocuteur / du cas où les personnages n'ont rien à raconter (pas d'histoire / histoires connues par les deux)
def quiparle(p1,p2) :
  hists1, hists2, intersect, intersectionDif = intersection(p1.histoires, p2.histoires)
  hists1_trie = sorted(histoireQuiPeuventEtresRacontees(hists1, p1, p2), key=lambda h: h.importance)[::-1]
  hists2_trie = sorted(histoireQuiPeuventEtresRacontees(hists2, p2, p1), key=lambda h: h.importance)[::-1]
  intersectionDif_trie_p1 = sorted(intersectionDif, key=lambda h: h[0].importance)[::-1]
  intersectionDif_trie_p2 = sorted(intersectionDif, key=lambda h: h[1].importance)[::-1]
  
  choix = []
  weights = []
  if len(hists1_trie) > 0:
      choix.append((p1, p2, hists1_trie[0]))
      weights.append(hists1_trie[0].importance)
  if len(hists2_trie) > 0:
      choix.append((p2, p1, hists2_trie[0]))
      weights.append(hists2_trie[0].importance)
  if len(intersectionDif_trie_p1) > 0:
      choix.append((p1, p2, intersectionDif_trie_p1[0]))
      weights.append(intersectionDif_trie_p1[0].importance)
  if len(intersectionDif_trie_p2) > 0:
      choix.append((p2, p1, intersectionDif_trie_p2[0]))
      weights.append(intersectionDif_trie_p2[0].importance)
      
  if len(choix) == 0:
      return None
  else:
      ch = random.choices(choix, weights=weights, k=1)[0]
      return ch


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
  result = quiparle(p1,p2)
  if result is None:
      return intro(p1, p2, useTranslation=useTranslation, useCorrection=useCorrection) + "~~ Les deux personnages n'ont rien à se dire... Une gêne sensible s'installe... ~~"
  (loc, interloc, hist) = result
  
  s = intro(loc, interloc, useTranslation=useTranslation, useCorrection=useCorrection) #L'intro
  continuer = True
  
  while continuer :
    p1.contacts[p2.id].nbDiscussions += 1
    p2.contacts[p1.id].nbDiscussions += 1
    s1 = hist.toText(loc, interloc, date=date, useTranslation=useTranslation, useCorrection=useCorrection)
    s += "\n" + s1
    #s += "\n" + reaction(hist,interloc)
    
    continuer = False
    # Pour enchainer
    result = quiparle(p1,p2)
    if result is None:
      s += "\n" + "~~ Les deux personnages n'ont rien à se dire... Une gêne sensible s'installe... ~~"
      continuer = False
    else:
      (loc, interloc, hist) = result
      s += "\n" + transition(useTranslation=useTranslation, useCorrection=useCorrection) #à définir
      
  s += "\n" + fin(p1,p2, useTranslation=useTranslation, useCorrection=useCorrection)
  return s