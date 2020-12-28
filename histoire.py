# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 00:20:08 2020

@author: josse
"""

import random
from psclib.caracteristique import Caracteristique
from psclib.diversifieur import correct
from psclib.lien import CAUSE, CONSEQUENCE, SUITE



def ajouterPonctuation(s):
  return s[:1].upper() + s[1:] + "."


def demanderLien(typeLien):
  dictExp = {}
  dictExp[CAUSE] = ["Mais Pourquoi ?"]
  dictExp[CONSEQUENCE] = ["Et donc ?"]
  dictExp[SUITE] = ["Et ensuite ?"]

  return random.choice(dictExp[typeLien])


def nePasSavoirLien(typeLien):
  dictExp = {}
  dictExp[CAUSE] = ["Je ne sais pas pourquoi..."]
  dictExp[CONSEQUENCE] = ["J\'en sais rien"]
  dictExp[SUITE] = ["Bah rien."]

  return random.choice(dictExp[typeLien])




# Les histoires
class Histoire:

  def __init__(self, head = None, ton = None, titre = None,personnes = None, conteur = None ):
    self.head = head # Pointeur vers le 1er coeur (d'action) de l'histoire. Celui-ci pointe ensuite vers différents liens logiques ou autres coeurs.
    self.ton = ton # String, ton de l'histoire (triste, drôle, etc.)
    self.titre = titre # String, pour les comparaisons
    self.personnes = personnes # ___, personnages évoqués dans l'histoire (c'est là pour le moment, à voir si ça sera utile ou non)
    self.conteur = conteur # ___, Narrateur originel de l'histoire, pour différencier les histoires personnelles des histoires rapportées


  def toText(self, locuteur, interlocuteur, coeurCurrent=None, prefixe=""):
    if coeurCurrent is None: coeurCurrent = self.head

    s = ""
    s1 = prefixe + coeurCurrent.toText(locuteur, interlocuteur)

    if not(coeurCurrent.liens is None) and len(coeurCurrent.liens) > 0: # Il existe un lien
      # Plus le perso est mystérieux, moins il a de chance de raconter les liens
      # Linéaire : mysterieux = 0 -> proba = 0.95, mysterieux=10 -> proba = 0.25
      probaRaconter = 0.95 - 0.07*locuteur.getCaracValue(Caracteristique(name="mysterieux"))

      liensRacontes = []
      liensOmis = []

      for lien in random.sample(coeurCurrent.liens, len(coeurCurrent.liens)):
        # Plus le perso est bavard plus il aura tendance à enchainer les liens
        # coeff Linéaire : bavard = 0 -> coeffDimin = 20, bavard=10 -> coeffDimin = 1.1
        coeff = 20 - 1.89*locuteur.getCaracValue(Caracteristique(name="bavard"))
        # exposant allant de 0 a 1 par rapport à la proportion d'hisoires racontées
        exposant = 2.*((1.+(len(liensRacontes)/float(len(coeurCurrent.liens)))) / (1.+len(liensOmis)/float(len(coeurCurrent.liens))) - 0.5)/3.
        proba = probaRaconter / float(coeff**exposant)

        if random.random() <= proba: # On raconte le lien
          liensRacontes.append(lien)
        else:
          liensOmis.append(lien)

      addLiens = True
      for l in liensRacontes :
        if l.typeLien == CAUSE and addLiens:
          s1 += " parce que " + l.coeur.toText(locuteur, interlocuteur)
        if l.typeLien == CONSEQUENCE and addLiens:
          s1 += " donc "+ l.coeur.toText(locuteur, interlocuteur)
        if l.typeLien == SUITE and addLiens:
          s1 += " puis "+ l.coeur.toText(locuteur, interlocuteur)
          addLiens = False
          coeurCurrent = l.coeur
          liensOmis = coeurCurrent.liens
          liensRacontes = []

      s += locuteur.imprimer(ajouterPonctuation(s1))

      # L'interlocuteur pose des questions
      # Plus le perso est curieux, plus il a de chance de demander les liens
      # Linéaire : curieux = 0 -> proba = 0.25, curieux=10 -> proba = 0.95
      probaDemander = 0.25 + 0.07*interlocuteur.getCaracValue(Caracteristique(name="curiosite"))
      probaDemanderInfoExistante = 0.75 # Proba de demander une info dans liensOmis

      if random.random() <= probaDemander:
        if len(liensOmis) > 0 and random.random() <= probaDemanderInfoExistante: # On demande une info existante
          l = random.choice(liensOmis)
          s += "\n" + interlocuteur.imprimer(demanderLien(l.typeLien))
          
          dictPrefixe = {}
          dictPrefixe[CAUSE] = ["Parce que "]
          dictPrefixe[CONSEQUENCE] = ["Donc "]
          dictPrefixe[SUITE] = ["Ensuite, "]
          s += "\n" + self.toText(locuteur, interlocuteur, coeurCurrent=l.coeur, prefixe=random.choice(dictPrefixe[l.typeLien]))
        else:
          liensPossibles = [CAUSE, CONSEQUENCE, SUITE]
          # Il ne faut pas demander un lien qui a déjà été précisé
          for l in liensRacontes:
            liensPossibles.remove(l.typeLien)
          # Si on a déja mentionné tous les liens, liensPossibles est vide
          # Dans ce cas on demande la suite
          if len(liensPossibles) == 0:
            liensPossibles = [SUITE]

          typeLien = random.choice(liensPossibles)
          s += "\n" + interlocuteur.imprimer(demanderLien(typeLien), diversify=False)
          s += "\n" + locuteur.imprimer(nePasSavoirLien(typeLien), diversify=False)
    else:
      s += locuteur.imprimer(ajouterPonctuation(s1))

    return s