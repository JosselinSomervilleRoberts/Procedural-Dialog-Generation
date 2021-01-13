# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 00:20:08 2020

@author: josse
"""
#En bande organisée, personne peut nous canaliser
import random
from psclib.caracteristique import Caracteristique
from psclib.diversifieur import correct
from psclib.lien import CAUSE, CONSEQUENCE, SUITE


dictExp = {}

def ajouterPonctuation(s):
  return s[:1].upper() + s[1:] + "."



def buildQuestionsReponses():
    """
    Récupère depuis les fichiers .txt les questions réponses scriptées
    pour les demandes de cause, consequence et suite.
    """ 
    global dictExp
    dictExp = {}
    
    chemin_base = "psclib/fichiers_txt/questions_reponses/"
    liste1 = ["demander", "ne_pas_savoir"] # Les types de réponses scriptées
    liste2 = [[CAUSE, "cause"], [CONSEQUENCE, "consequence"], [SUITE, "suite"]] # Les différents liens
    
    for ext1 in liste1:
        chemin_intermediaire = chemin_base + ext1 + "_"
        dictExp[ext1] = {}
        for elt2 in liste2:
            index, ext2 = elt2[0], elt2[1]
            chemin = chemin_intermediaire + ext2 + ".txt"
            f = open(chemin, "r", encoding="ISO-8859-1")
            liste = f.readlines()
            f.close()
            
            dictExp[ext1][index] = []
            for ligne in liste:
                l1 = ligne.replace("\n","").split("=")[0]
                if len(l1) > 1:
                    dictExp[ext1][index].append(l1)
    
    print("Expressions chargées.")


def demanderLien(typeLien):
  global dictExp
  if len(dictExp.keys()) == 0:
      buildQuestionsReponses()
  return random.choice(dictExp["demander"][typeLien])

  return random.choice(dictExp[typeLien])


def nePasSavoirLien(typeLien):
  global dictExp
  if len(dictExp.keys()) == 0:
      buildQuestionsReponses()
  return random.choice(dictExp["ne_pas_savoir"][typeLien])




# Les histoires
class Histoire:

  def __init__(self, head = None, ton = None, titre = None,personnes = None, conteur = None ):
    self.head = head # Pointeur vers le 1er coeur (d'action) de l'histoire. Celui-ci pointe ensuite vers différents liens logiques ou autres coeurs.
    self.ton = ton # String, ton de l'histoire (triste, drôle, etc.)
    self.titre = titre # String, pour les comparaisons
    self.personnes = personnes # ___, personnages évoqués dans l'histoire (c'est là pour le moment, à voir si ça sera utile ou non)
    self.conteur = conteur # ___, Narrateur originel de l'histoire, pour différencier les histoires personnelles des histoires rapportées
    
    

  def getGraph(self, locuteur, interlocuteur, dot=None, index=1, coeurCurrent=None, indexParent=1):
    from graphviz import Digraph
      
    if dot is None:
      dot = Digraph(comment=self.titre)
      if coeurCurrent is None:
        coeurCurrent = self.head
      dot.node(str(index), coeurCurrent.toText(locuteur, interlocuteur))
      index += 1
      
    if len(coeurCurrent.liens) > 0:
      for lien in coeurCurrent.liens:
        dot.node(str(index), lien.coeur.toText(locuteur, interlocuteur))
        
        dot.edge(str(indexParent), str(index))
        index += 1
        dot = self.getGraph(locuteur, interlocuteur, dot=dot, index=index, coeurCurrent=lien.coeur, indexParent=index-1)
    
    return dot


  def toText(self, locuteur, interlocuteur, coeurCurrent=None, prefixe=""):
    """
    Génère le texte pour l'histoire.
    La façon dont s'enchaine l'histoire dépend des caractéristiques du locuteur et de l'interlocuteur
    - si le locuteur est "mystérieux", il aura peu tendance à ajouter les liens
    - si le locuteur est "bavard", lorsqu'il précise un lien, il aura tendance à en préciser beaucoup. Ceci est à différencer de "mystérieux".
    Par exemple si le coeur actuel à 3 liens : cause, conséquence et suite. S'il est mystérieux il aura peu tendance à préciser les liens. Si toutefois il
    décide de préciser un ou plusieurs le lies, le nombre de liens précisés dépendra de s'il est bavard ou non.
    - si l'interlocuteur a de la "curiosite", il aura tendance a poser des questions.
    
    A VERIFIER : j'ai l'impression qu'actuellement le locuteur ne peux enchainer les liens si l'interlocuteur ne lui pose pas de questions.
    EN COURS: ajout de la transmission d'infos

      Parameters
      ----------
      locuteur : Personnage
          C'est celui qui raconte l'histoire
      interlocuteur : Personnage
          C'est celui qui écoute l'histoire
      coeurCurrent : Coeur, optional
          Correspond au coeur actuel. Cela permet d'appeler récursivement la fonction toText notamment.
          Si n'est pas précisé, coeurCurrent vaut l'head de l'histoire. Ensuite si l'interlocuteur pose une question
          On peut rappeler toText mais en précisant que l'on ne démarre plus de head mais du coeur suivant.
      prefixe : str, optional
          Préfixe en début de phrase, par exemple "Parce que + ...."".

      Returns
      -------
      s : string
          Texte de la discussion

      """
    if coeurCurrent is None: coeurCurrent = self.head
    
    # Ajouter l'histoire
    indexHist = interlocuteur.indexHistoire(self.titre)
    if indexHist == -1:
        interlocuteur.histoires.append(Histoire(head=coeurCurrent, titre=self.titre))
        indexHist = interlocuteur.indexHistoire(self.titre)
        

    s = ""
    s1 = prefixe + coeurCurrent.toText(locuteur, interlocuteur)

    if not(coeurCurrent.liens is None) and len(coeurCurrent.liens) > 0: # Il existe un lien
      # Plus le perso est mystérieux, moins il a de chance de raconter les liens
      # Linéaire : mysterieux = 0 -> proba = 0.95, mysterieux=10 -> proba = 0.25
      probaRaconter = 0.95 - 0.07*locuteur.getCaracValue(Caracteristique(name="mysterieux"))
      #print("mysterieux", locuteur.prenom, locuteur.getCaracValue(Caracteristique(name="mysterieux")), "/ proba=", probaRaconter)

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
      #print("curiosite", interlocuteur.prenom, interlocuteur.getCaracValue(Caracteristique(name="curiosite")), "/ proba=", probaDemander)
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
