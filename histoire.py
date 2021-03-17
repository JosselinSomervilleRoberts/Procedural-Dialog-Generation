# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 00:20:08 2020

@author: josse
"""
#En bande organisée, personne peut nous canaliser
import random
from math import log
from psclib.caracteristique import Caracteristique
from psclib.diversifieur import correct
from psclib.lien import COMPLEMENT, COMPLEMENT_LIEU, COMPLEMENT_TEMPS, COMPLEMENT_MANIERE, OBJECTIF, CAUSE, CONSEQUENCE, SUITE, Lien
from psclib.coeuraction import CoeurAction
from psclib.coeurdescriptif import CoeurDescriptif
from psclib.coeurdescriptifverbal import CoeurDescriptifVerbal
from psclib.coeur import CoeurComplement
from copy import copy, deepcopy

import re
from psclib.diversifieur import cong

STOP = -3
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
    liste1 = ["demander", "demander_avec_phrase", "ne_pas_savoir", "rappel", "mots_liaisons_continuer", "mots_liaisons_recommencer", "retour_arriere"] # Les types de réponses scriptées
    liste2 = [[COMPLEMENT_LIEU, "lieu"], [COMPLEMENT_TEMPS, "temps"], [COMPLEMENT_MANIERE, "maniere"], [OBJECTIF, "objectif"], [CAUSE, "cause"], [CONSEQUENCE, "consequence"], [SUITE, "suite"]] # Les différents liens
    
    for ext1 in liste1:
        chemin_intermediaire = chemin_base + "/" + ext1 + "/" + ext1 + "_"
        print(chemin_intermediaire)
        dictExp[ext1] = {}
        for elt2 in liste2:
            index, ext2 = elt2[0], elt2[1]
            chemin = chemin_intermediaire + ext2 + ".txt"
            f = open(chemin, "r", encoding="utf-8")
            liste = f.readlines()
            f.close()
            
            dictExp[ext1][index] = []
            for ligne in liste:
                l1 = ligne.replace("\n","").split("=")[0]
                if len(l1) > 1:
                    dictExp[ext1][index].append(l1)
    
    print("Expressions chargées.")
    
    
    
def getExpression(key, typeLien, dateCoeur=None, date=None, used=None):
    global dictExp
    if len(dictExp.keys()) == 0: buildQuestionsReponses()
    if used is None: used = []
    
    # Si il n'y a pas d'expressions (notamment pour les compléments)
    if len(dictExp[key][typeLien]) == 0: return "euh"
  
    # On enlève les expressions déja utilisées
    liste_exps = []
    for exp in dictExp[key][typeLien]:
        if not(exp in used):
            liste_exps.append(exp)

    exp = None
    if len(liste_exps) > 0: # Si il y a des expressions que l'on a pas encore utilisées
        choix = random.choice(liste_exps)
        used.append(choix)
        exp = choix
    else: # Si on a déja tout utilisé
        exp = random.choice(dictExp[key][typeLien])
    
    
    # On conjugue éventuellement les [...]
    c = re.search(r'\[[^0-9]*\]', exp)
    while not(c is None):
      v = c.group(0)[1:-1] # On trouve le verbe
      temps = None
      
      if dateCoeur is None or date is None:
          temps = "imparfait"
      else:
            if dateCoeur.date() == date.date():
                temps = "passé-composé"
            elif dateCoeur.date() < date.date():
                temps = "passé-composé"
            else:
                temps = "futur-simple"
            
      v_conj = cong(v, "indicatif", temps, 3).replace("je ","").replace("j\'","").replace("tu ","").replace("il ","").replace("nous ","").replace("vous ","").replace("ils ","").replace("qu\'", "").replace("que ", "")
      exp = exp.replace("[" + v + "]", v_conj)
      c = re.search(r'\[[^0-9]*\]', exp)
      
      
    # On conjugue éventuellement les {...}
    c = re.search(r'\{.*\}', exp)
    while not(c is None):
      v = c.group(0)[1:-1] # On trouve le verbe
      temps = None
      
      if dateCoeur is None or date is None:
          temps = "présent"
      else:
            if dateCoeur.date() == date.date():
                temps = "imparfait"
            elif dateCoeur.date() < date.date():
                temps = "imparfait"
            else:
                temps = "futur-simple"
            
      v_conj = cong(v, "indicatif", temps, 3).replace("je ","").replace("j\'","").replace("tu ","").replace("il ","").replace("nous ","").replace("vous ","").replace("ils ","").replace("qu\'", "").replace("que ", "")
      exp = exp.replace("{" + v + "}", v_conj)
      c = re.search(r'\{.*\}', exp)
      
      
    # On remplace les trucs du genre "ce est" par "c'est"
    c = re.search(r'[Cc]e [eé]', exp)
    while not(c is None):
        index = c.span()[0] + 1
        exp = exp[:index] + "'" + exp[index+2:]
        c = re.search(r'[Cc]e [eé]', exp)
    
    return exp


def demanderLien(typeLien, dateCoeur=None, date=None, used=None):
  return getExpression("demander", typeLien, dateCoeur, date, used)

def demanderAvecPhraseLien(typeLien, dateCoeur=None, date=None, used=None):
  return getExpression("demander_avec_phrase", typeLien, dateCoeur, date, used)

def nePasSavoirLien(typeLien, dateCoeur=None, date=None, used=None):
  return getExpression("ne_pas_savoir", typeLien, dateCoeur, date, used)

def rappel(typeLien, dateCoeur=None, date=None, used=None):
  return getExpression("rappel", typeLien, dateCoeur, date, used)

def motsLiasonsContinuer(typeLien, dateCoeur=None, date=None, used=None):
  return getExpression("mots_liaisons_continuer", typeLien, dateCoeur, date, used)

def motsLiasonsRecommencer(typeLien, dateCoeur=None, date=None, used=None):
  return getExpression("mots_liaisons_recommencer", typeLien, dateCoeur, date, used)

def retourArriere(typeLien, dateCoeur=None, date=None, used=None):
  return getExpression("retour_arriere", typeLien, dateCoeur, date, used)




# Les histoires
class Histoire:

  def __init__(self, head = None, ton = None, titre = None,personnes = None, conteur = None, dateDebut = None, importance = 0, relationPourRaconter = None):
    self.head = head # Pointeur vers le 1er coeur (d'action) de l'histoire. Celui-ci pointe ensuite vers différents liens logiques ou autres coeurs.
    self.ton = ton # String, ton de l'histoire (triste, drôle, etc.)
    self.titre = titre # String, pour les comparaisons
    self.personnes = personnes # ___, personnages évoqués dans l'histoire (c'est là pour le moment, à voir si ça sera utile ou non)
    self.conteur = conteur # ___, Narrateur originel de l'histoire, pour différencier les histoires personnelles des histoires rapportées
    self.dateDebut = dateDebut
    
    # Determine a qui on va dire l'histoire
    self.importance = importance
    self.relationPourRaconter = relationPourRaconter
    if relationPourRaconter is None:
        if self.importance < 1:
            self.relationPourRaconter = ["famille", "travail", "inconnu", "connaissance", "ami"]
        elif self.importance < 3:
            self.relationPourRaconter = ["famille", "travail", "connaissance", "ami"]
        elif self.importance < 10:
            self.relationPourRaconter = ["famille", "ami"]
        else:
            self.relationPourRaconter = ["famille"]
    
    # Pour les questions
    self.liensAExplorer = []
    self.liensADemander = []
    
    
    

  def getGraphDialog(self, locuteur, interlocuteur, dot=None, index=1, coeurCurrent=None, indexParent=1):
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


  def getGraph(self, dot=None, coeurCurrent=None, indexParent=1):
    from graphviz import Digraph
      
    if dot is None:
      dot = Digraph(comment=self.titre)
      if coeurCurrent is None:
        coeurCurrent = self.head
      if isinstance(coeurCurrent, CoeurAction):
        dot.attr('node', shape='box')
      if isinstance(coeurCurrent, CoeurDescriptif):
        dot.attr('node', shape='octagon')
      if isinstance(coeurCurrent, CoeurDescriptifVerbal):
        dot.attr('node', shape='polygon')
      if isinstance(coeurCurrent, CoeurComplement):
        dot.attr('node', shape='ellipse')
      dot.node(str(coeurCurrent.id), "<"+coeurCurrent.getGraphText()+">")
      indexParent = coeurCurrent.id
      
    if len(coeurCurrent.liens) > 0:
      for lien in coeurCurrent.liens:
        if isinstance(lien.coeur, CoeurAction):
            dot.attr('node', shape='box')
        if isinstance(lien.coeur, CoeurDescriptif):
            dot.attr('node', shape='octagon')
        if isinstance(lien.coeur, CoeurComplement):
            dot.attr('node', shape='ellipse')
        dot.node(str(lien.coeur.id), "<"+lien.coeur.getGraphText()+">")
        
        dot.edge(str(indexParent), str(lien.coeur.id), label="<"+lien.getGraphText()+">")
        dot = self.getGraph(dot=dot, coeurCurrent=lien.coeur, indexParent=lien.coeur.id)
    
    return dot



  def getCoeurs(self):
      """Renvoie tous les coeurs de l'histoire"""
      
      if self.head is None:
          return []
      
      aTraiter = [self.head]
      coeurs = []
      while len(aTraiter) > 0:
          # On enlève le coeur actuel
          coeur = aTraiter[0]
          coeurs.append(coeur)
          aTraiter = aTraiter[1:]
          
          # On ajoute les coeurs liés au coeur actuel
          aTraiter += [l.coeur for l in coeur.liens]
          
      return coeurs
          

  def getDifferences(self, hist2):
      diff = {}
      
      if not(self.titre == hist2.titre):
          raise NameError("Deux histoires n'ayant pas le même notre ne peuvent pas être comparées: " + str(self.titre) + " / " + str(hist2.titre))

      diff["conteur"] = self.conteur != hist2.conteur
      diff["ton"] = self.ton != hist2.ton
      
      coeurs1 = self.getCoeurs()
      coeurs2 = hist2.getCoeurs()
      
      # COmparaison des coeurs présents
      in1butNot2, in2butNot1, inBoth = [], [], []
      
      while len(coeurs1) > 0:
          coeur = coeurs1[0]
          coeurs1 = coeurs1[1:]
          if coeur.id in [c.id for c in coeurs2]:
              inBoth.append(coeur)
              indexIn2 = [c.id for c in coeurs2].index(coeur.id)
              coeurs2 = coeurs2[:indexIn2] + coeurs2[indexIn2 + 1:]
          else:
              in1butNot2.append(coeur)
              
      in2butNot1 = coeurs2.copy()
      
      diff["in1butNot2"] = in1butNot2
      diff["in2butNot1"] = in2butNot1
      """
      print("\n\nEN COMMUN")
      print(inBoth)
      print("\n\n")
      """
      return diff
          
          
      



  def toText(self, locuteur, interlocuteur, date=None, coeurActuel=None, histInterlocuteur=None, coeurInterlocuteur=None, 
             reponse=False, phrasesPrecedentes="", debutPhrase="", nbCoeursDansLaPhrase=0, expUsed=None, lastMentioned=None,
             liensAExplorer=None, liensADemander=None, 
             useTranslation=True, useCorrection=True): 
      
    global STOP
    
    # Pour avoir où placer le CCT
    indexCCT = len(debutPhrase)
    
    
    # Si il n'y a pas encore de DEMANDE ou D'EXPLORATION, alors les listes sont vides
    if liensAExplorer is None: liensAExplorer = []
    if liensADemander is None: liensADemander = []
    if expUsed is None: expUsed = []
    if lastMentioned is None: lastMentioned = [None, None]
    
    
    # On oublie potentiellement certaines questions
    liste_questions = [liensAExplorer, liensADemander]
    for questions in liste_questions:
        nbQuestions = len(questions)
        toBeRemoved = []
        
        for i in range(nbQuestions):
            probaOublier = 1 - ((nbQuestions - i)**0.5)*(interlocuteur.getCaracValue(Caracteristique(name="memoire")) / 10.) ** (0.33)
            if random.random() <= probaOublier:
                toBeRemoved.append(questions[i])
          
        if len(toBeRemoved):
            #print("ON OUBLIE UNE QUESTION !!!!!!")
            #print("len before:", len(questions))
            for elt in toBeRemoved:
                questions.remove(elt)
            #print("len after:", len(questions))
    
      
    # Si on commence à raconter l'histoire, on commence par le début
    # Il faut créer l'histoire dans la mémoire de l'interlocuteur
    if coeurActuel is None:
        coeurActuel = self.head
        indexHist = interlocuteur.ajouterHistoire(self.titre, head = self.head, ton = self.ton, personnes = self.personnes, conteur = locuteur)
        histInterlocuteur = interlocuteur.histoires[indexHist]
        coeurInterlocuteur = histInterlocuteur.head
        
        texteCoeur = coeurActuel.toText(locuteur, interlocuteur, date=date, premierCoeur=False, useTranslation=useTranslation, useCorrection=useCorrection)
        if texteCoeur[-1] == ",": texteCoeur = texteCoeur[:-1]
        phraseStart = "Je t'ai raconté que " + texteCoeur + " ?"
        phrasesPrecedentes = locuteur.imprimer(phraseStart, useTranslation=useTranslation, useCorrection=useCorrection)
        
        if indexHist == -1: #True
            phrasesPrecedentes += "\n" + interlocuteur.imprimer("Non, raconte !", diversify=False, useTranslation=useTranslation, useCorrection=useCorrection)
        else:
            conteur = interlocuteur.histoires[indexHist].conteur
            if conteur == locuteur:
                phrasesPrecedentes += "\n" + interlocuteur.imprimer("Oui tu m'en as déja parlé", diversify=False, useTranslation=useTranslation, useCorrection=useCorrection)
            else:
                phrasesPrecedentes += "\n" + interlocuteur.imprimer("Non mais " + conteur.toText(interlocuteur, locuteur, useTranslation, useCorrection) + " m'a déja raconté.", diversify=False, useTranslation=useTranslation, useCorrection=useCorrection)
            
            liensAExplorer += interlocuteur.histoires[indexHist].liensAExplorer
            liensADemander += interlocuteur.histoires[indexHist].liensADemander
            if len(liensAExplorer) > 0 or len(liensADemander) > 0:
                phrasesPrecedentes += "\n" + interlocuteur.imprimer("Mais je ne sais pas encore tout de cette histoire, notamment, ", diversify=False, useTranslation=useTranslation, useCorrection=useCorrection)
            
            return self.toText(locuteur, interlocuteur, date=date, coeurActuel=STOP, histInterlocuteur=histInterlocuteur, coeurInterlocuteur=coeurInterlocuteur,
                               reponse=False, phrasesPrecedentes=phrasesPrecedentes, debutPhrase="", nbCoeursDansLaPhrase=0, expUsed=None,
                               liensAExplorer=liensAExplorer, liensADemander=liensADemander,
                               useTranslation=useTranslation, useCorrection=useCorrection)
        
        return self.toText(locuteur, interlocuteur, date=date, coeurActuel=self.head, histInterlocuteur=histInterlocuteur,  coeurInterlocuteur=coeurInterlocuteur,
                           reponse=False, phrasesPrecedentes=phrasesPrecedentes, debutPhrase=locuteur.getTic(interlocuteur, False) + "alors, ", nbCoeursDansLaPhrase=0, expUsed=None,
                           liensAExplorer=None, liensADemander=None,
                           useTranslation=useTranslation, useCorrection=useCorrection)
            
            
    
    
    """
    # Mots pour continuer une phrase
    mots_liaisons_continuer = {COMPLEMENT_LIEU: [""], CAUSE: ["parce que", "car"], CONSEQUENCE: ["donc", "du coup"], SUITE: ["puis", "et puis", "et ensuite"]}
    # Mots pour recommencer une phrase
    mots_liaisons_recommencer = {COMPLEMENT_LIEU: [""], CAUSE: ["C\'est parce que"], CONSEQUENCE: ["Et donc", "Et du coup", "Du coup"], SUITE: ["Ensuite,", "Alors,"]}
    """
    
    liens = []
    # On transforme le coeur actuel en texte
    if not(coeurActuel == STOP):
        debutPhrase += locuteur.getTic(interlocuteur)
        debutPhrase += coeurActuel.toText(locuteur, interlocuteur, lastMentioned=lastMentioned, date=date, premierCoeur=(nbCoeursDansLaPhrase==0) and not(reponse), useTranslation=useTranslation, useCorrection=useCorrection)
        nbCoeursDansLaPhrase += 1
    
        # On trie les liens par importance
        liens = sorted(coeurActuel.liens, key=lambda x: x.importance)
    
    if len(liens) > 0:
      # On ajoute un lien bidon qui correspond au fait de ne pas continuer
      lienFin = Lien(coeur=None, typeLien=SUITE, importance=1)
      liens.append(lienFin)
      
      # On choisit au hasard un lien basé sur son importance (on privilégie fortement les liens qui ont eux-mêmes des liens autres que des compléments)
      weights = []
      for lien in liens:
          w = lien.importance
          if not(lien.coeur is None): w += 1000*(sum([not(l.typeLien in [COMPLEMENT, COMPLEMENT_LIEU, COMPLEMENT_TEMPS, COMPLEMENT_MANIERE]) for l in lien.coeur.liens]) > 0) # Si le lien a lui même des liens qui ne sont pas des compléments, on le favorive grandement
          if lien.typeLien in [COMPLEMENT, COMPLEMENT_LIEU, COMPLEMENT_TEMPS, COMPLEMENT_MANIERE]: w = 0 # Si c'est un complément, on ne le choisit pas
          weights.append(w)
          
      lienChoisi = random.choices(liens, weights=weights, k=1)[0]
      liens.remove(lienChoisi) # On le retire de la liste des liens
      if lienFin in liens: liens.remove(lienFin) # On retire le lien bidon qui correspond à la fin
      
      
      # On ajoute des précisions (éventuellement)
      sommeImportance = max(1,min(10,sum([lien.importance for lien in liens])))
      nbPrecisions = 0
      liensAPreciser = []
      
      random.shuffle(liens) # On mélange les liens car l'ordre importe (Plus on a fait de précisions, moins on a de chance d'en rajoute,
      # donc les premiers liens sont favorisés)
      for l in liens:
          # Plus on est bavard, plus on a de chance de préciser les liens
          # Plus le lien est important plus on a de chance de le préciser
          # Plus on a fait de précisions, moins on a de chance d'en rajouter
          probaPreciser = (0.25 + 0.07*locuteur.getCaracValue(Caracteristique(name="bavard"))) * l.importance / (sommeImportance*(1+nbPrecisions))
          if random.random() <= probaPreciser and l.importance > 0: # Si on précise le lien
              nbPrecisions += 1
              liensAPreciser.append(l)
      
    
      # Sinon on ajoute le lien
      # Il faut choisir si le lien sera ajouté comme suite à la phrase ou comme une question
      # D'abord, on ajoute les précisions.
      # Pour que la phrase est du sens, il faut ordonner les précisions dans l'ordre OBJECTIF, CAUSE, CONSEQUENCE, SUITE
      # Par exemple, Marcel promène son chien car il avait envie donc ils vont au parc et ils s'amusent (CAUSE, CONSEQUENCE, SUITE)
      # Mais: Marcel promène son chien et ils s'amusent car il avait envie donc ils vont au parc (SUITE, CAUSE, CONSEQUENCE) -> pas le même sens
      liensAPreciser = sorted(liensAPreciser, key=lambda x: 1000*x.typeLien + x.importance) # On trie par type de lien puis par importance
      

      # Pour l'instant, on va commencer avec quelque chose de simple pour choisir si on continue ou recommence une phrase
      # - on recommence toujours une phrase pour le lienChoisi sauf si la phrase précédente ne contient pas de précisions.
      # - pour les précisions, on recommence une phrase quand elle devient trop longue (dépend du nombre de caractères et du nombre de précisions)
      # on fera juste en sorte d'éviter de recommencer une phrase pour la dernière précision pour éviter des phrases avec un seul coeur.
      liensDansLaPhrase = 0
      lastLien = None
      phraseRecommencee = False
      for i in range(len(liensAPreciser)):
          lien = liensAPreciser[i]
          vaEtreExplore = False
          
          if lien.typeLien in [COMPLEMENT, COMPLEMENT_LIEU, COMPLEMENT_TEMPS, COMPLEMENT_MANIERE]: # C'est un complément
              ajout = locuteur.getTic(interlocuteur) + lien.coeur.toText(locuteur, interlocuteur, lastMentioned=lastMentioned, date=date, premierCoeur=nbCoeursDansLaPhrase==0, autoriserRadoter=False, useTranslation=useTranslation, useCorrection=useCorrection)
              if lien.typeLien == COMPLEMENT_TEMPS:
                  # On veut ajouter le CCT au début de la phrase,
                  # Il faut donc retrouver le début de la phrase d'abord
                  debutPhrase = debutPhrase[:indexCCT] + ajout + ", " + debutPhrase[indexCCT:]
              else:
                  debutPhrase += " " + ajout                    
          
          else: # Ce n'est pas un complément              
              liensDansLaPhrase += 1
              lastLien = lien
              probaRecommencer = (nbCoeursDansLaPhrase>1)*(0.2 + 0.002*len(debutPhrase.split(".")[-1]) + 0.1*nbCoeursDansLaPhrase) # 20% + 0.2% par caractère + 10% par liens déja dans la phrase
              
              if i == len(liensAPreciser) - 1: # Si c'est le dernier lien, proba de re commencer - 50%
                  probaRecommencer -= 0.5
                  
              
              if random.random() <= probaRecommencer: # On recommence une phrase
                  debutPhrase += ". " + motsLiasonsRecommencer(lien.typeLien, dateCoeur=lien.coeur.date, date=date, used=expUsed) + " " + lien.coeur.toText(locuteur, interlocuteur, lastMentioned=lastMentioned, date=date, premierCoeur=nbCoeursDansLaPhrase==0, useTranslation=useTranslation, useCorrection=useCorrection)
                  nbCoeursDansLaPhrase = 1
                  phraseRecommencee = True
              else: # On continue dans la même phrase
                  debutPhrase += " " + motsLiasonsContinuer(lien.typeLien, dateCoeur=lien.coeur.date, date=date, used=expUsed) + " " + lien.coeur.toText(locuteur, interlocuteur, lastMentioned=lastMentioned, date=date, premierCoeur=nbCoeursDansLaPhrase==0, useTranslation=useTranslation, useCorrection=useCorrection)
                  nbCoeursDansLaPhrase += 1
                  
              # Pour chaque précision, si la précision se poursuivait, on ne la suivra pas car on va suivre lienChoisi
              # Mais l'interlocuteur peut avoir envie de poser une question sur la suite de cette précision.
              # On appelle ça : EXPLORER un lien.
              if len(lien.coeur.liens) > 0:
                  # Son envie d'explorer va dépendre de :
                  # - l'importance du lien
                  # - la curiosité de l'interlocuteur
                  # - le nombre de précisions qu'il souhaite déja explorer
                  probaExplorer = 0.05 + 0.15*log(lien.importance) + 0.55*(interlocuteur.getCaracValue(Caracteristique(name="curiosite")) - 2*len(liensAExplorer))
                  if random.random() <= probaExplorer: # Si on explore le lien
                      vaEtreExplore = True
                 
                      
          # On l'ajoute à la mémoire de l'interlocuteur
          if True:
              probaRetenir = (interlocuteur.getCaracValue(Caracteristique(name="memoire")) / 10.) ** (0.33)
              
              coeurPrecisionCopy = None
              if vaEtreExplore or random.random() <= probaRetenir:
                  coeurPrecisionCopy = deepcopy(lien.coeur)
                  coeurPrecisionCopy.liens = []
                  if lien.typeLien != COMPLEMENT_TEMPS:
                      coeurPrecisionCopy.date = None
                  lienCopy = Lien(coeur=coeurPrecisionCopy, typeLien=lien.typeLien, importance=lien.importance)
                  coeurInterlocuteur.ajouterLien(lienCopy)
                  
              if vaEtreExplore:
                  liensAExplorer.append([coeurActuel, lien, coeurPrecisionCopy])
              #elif lien.typeLien == COMPLEMENT_TEMPS:
                      
            
             
                      
                  
      # Pour chaque lien non précisé, l'interlocuteur peut DEMANDER la précision
      # Il peut aussi demander des précisions dont le locuteur n'a pas la réponse (a ajouter)
      for l in liens:
          if not(l in liensAPreciser): # Si le lien n'a pas été précisé
              # Son envie dde demander va dépendre de :
              # - l'importance du lien
              # - la curiosité de l'interlocuteur
              # - le nombre de précisions qu'il souhaite déja demander
              probaDemander = 0.05 + 0.15*log(l.importance) + 0.55*(interlocuteur.getCaracValue(Caracteristique(name="curiosite")) - 2*len(liensADemander))
              if random.random() <= probaDemander and l.importance > 0: # Si on demande le lien
                  liensADemander.append([coeurActuel, l, coeurInterlocuteur])
              
      
        
      # Si on arrete l'histoire (i.e. on a choisi lienFin)
      if lienChoisi.coeur is None: # C'est le lien de fin
        return self.toText(locuteur, interlocuteur, date=date, coeurActuel=STOP, histInterlocuteur=histInterlocuteur, coeurInterlocuteur=coeurInterlocuteur,
                           phrasesPrecedentes=phrasesPrecedentes, debutPhrase=debutPhrase, nbCoeursDansLaPhrase=nbCoeursDansLaPhrase, expUsed=expUsed, lastMentioned=lastMentioned,
                           liensAExplorer=liensAExplorer, liensADemander=liensADemander,
                           useTranslation=useTranslation, useCorrection=useCorrection)
        #return phrasesPrecedentes + "\n" + locuteur.imprimer(ajouterPonctuation(debutPhrase), useTranslation=useTranslation, useCorrection=useCorrection)
    
    
    
    
      # =============== Enfin, on ajoute le lienChoisi ===================================== #
      
      # On l'ajoute à la mémoire de l'interlocuteur
      coeurPrincipalCopy = deepcopy(lienChoisi.coeur)
      coeurPrincipalCopy.liens = []
      lienChoisiCopy = Lien(coeur=coeurPrincipalCopy, typeLien=lienChoisi.typeLien, importance=lienChoisi.importance)
      coeurInterlocuteur.ajouterLien(lienChoisiCopy)
      
      # On change de coeurActuel pour l'interlocuteur
      coeurInterlocuteur = coeurPrincipalCopy
      
        
      # On ajoute sont texte
      # (On recommence une phrase pour ça)
      if phraseRecommencee or liensDansLaPhrase >= 1: # On a recommencé ou on a pas recommencé de phrase mais il y a eu des précisions
 
          # Si on a dit un truc plus prioritaire, il faut repréciser le coeur. (RETOUR ARRIERE)
          # Comme la définition des liens est faite par ordre de priorité, on peut simplement faire une comparaison sur le type
          if lastLien.typeLien >= lienChoisi.typeLien:
              debutPhrase += ". "
              retour = retourArriere(lienChoisi.typeLien, dateCoeur=lienChoisi.coeur.date, date=date, used=expUsed)
              phrase1 = coeurActuel.toText(locuteur, interlocuteur, lastMentioned=lastMentioned, date=date, premierCoeur=nbCoeursDansLaPhrase==0, useTranslation=useTranslation, useCorrection=useCorrection)
              retour = retour.replace("[1]", phrase1)
              debutPhrase += retour + " "
          else:
              debutPhrase += ". " + motsLiasonsRecommencer(lienChoisi.typeLien, dateCoeur=lienChoisi.coeur.date, date=date, used=expUsed) + " "
          nbCoeursDansLaPhrase = 1
      else: # On a pas recommencé de phrase et il n'y a eu aucune précision.
          probaRecommencer = (nbCoeursDansLaPhrase>1)*(0.2 + 0.002*len(debutPhrase.split(".")[-1]) + 0.1*nbCoeursDansLaPhrase) # 20% + 0.2% par caractère + 10% par liens déja dans la phrase
          if random.random() <= probaRecommencer:
              debutPhrase += ". " + motsLiasonsRecommencer(lienChoisi.typeLien, dateCoeur=lienChoisi.coeur.date, date=date, used=expUsed) + " "
              nbCoeursDansLaPhrase = 1
          else:
              debutPhrase += " " + motsLiasonsContinuer(lienChoisi.typeLien, dateCoeur=lienChoisi.coeur.date, date=date, used=expUsed) + " "
              nbCoeursDansLaPhrase += 1
              
      return self.toText(locuteur, interlocuteur, date=date, coeurActuel=lienChoisi.coeur, histInterlocuteur=histInterlocuteur, coeurInterlocuteur=coeurInterlocuteur,
                         phrasesPrecedentes=phrasesPrecedentes, debutPhrase=debutPhrase, nbCoeursDansLaPhrase=nbCoeursDansLaPhrase, expUsed=expUsed, lastMentioned=lastMentioned,
                         liensAExplorer=liensAExplorer, liensADemander=liensADemander,
                         useTranslation=useTranslation, useCorrection=useCorrection)
  
      # ==================================================================================== #
      
    else: # IL N'Y A PAS DE LIEN
    
        # Le locuteur peut décider de partir
        probaPartir = 1 - (0.4 + 0.05*locuteur.getCaracValue(Caracteristique(name="bavard")))
        if random.random() <= probaPartir:
            # On ajoute au texte
            if len(debutPhrase) > 0:
                phrasesPrecedentes += "\n" + locuteur.imprimer(ajouterPonctuation(debutPhrase), useTranslation=useTranslation, useCorrection=useCorrection)
                
            # On enregistre les demandes de l'interlocuteur
            histInterlocuteur.liensAExplorer += liensAExplorer
            histInterlocuteur.liensADemander += liensADemander
            
            phrasesPrecedentes += "\n" + locuteur.imprimer("Bon, sur ce, je dois filer moi !", useTranslation=useTranslation, useCorrection=useCorrection)
            return phrasesPrecedentes
    
    
    
        # L'interlocuteur peut maintenant poser ses questions (DEMANDE puis EXPLORATION)
        
        if len(liensADemander) > 0:
            d = random.choice(liensADemander)
            coeurCurrent, lien, coeurInterloc = d[0], d[1], d[2]
            
            # On retourne au bon endroit de l'histoire
            coeurInterlocuteur = coeurInterloc
            
            # On l'ajoute à la mémoire de l'interlocuteur
            coeurReponseCopy = deepcopy(lien.coeur)
            coeurReponseCopy.liens = []
            lienDemandeCopy = Lien(coeur=coeurReponseCopy, typeLien=lien.typeLien, importance=lien.importance)
            coeurInterlocuteur.ajouterLien(lienDemandeCopy)
              
            # On change de coeurActuel pour l'interlocuteur
            coeurInterlocuteur = coeurReponseCopy
            
            liensADemander.remove(d)
            demande = interlocuteur.getTic(interlocuteur) + demanderAvecPhraseLien(lien.typeLien, dateCoeur=lien.coeur.date, date=date, used=expUsed)
            if "[1]" in demande:
                phrase = coeurCurrent.toText(interlocuteur, locuteur, lastMentioned=lastMentioned, date=date, premierCoeur=False, useTranslation=useTranslation, useCorrection=useCorrection)
                demande = demande.replace("[1]", phrase)
                
            # On ajoute au texte
            if len(debutPhrase) > 0:
                phrasesPrecedentes += "\n" + locuteur.imprimer(ajouterPonctuation(debutPhrase), useTranslation=useTranslation, useCorrection=useCorrection)
            phrasesPrecedentes += "\n" + interlocuteur.imprimer(demande, useTranslation=useTranslation, useCorrection=useCorrection)
            debutPhrase = motsLiasonsRecommencer(lien.typeLien, dateCoeur=lien.coeur.date, date=date, used=expUsed) + " "
            return self.toText(locuteur, interlocuteur, date=date, coeurActuel=lien.coeur, histInterlocuteur=histInterlocuteur, coeurInterlocuteur=coeurInterlocuteur,
                               reponse=True, phrasesPrecedentes=phrasesPrecedentes, debutPhrase=debutPhrase, nbCoeursDansLaPhrase=0, expUsed=expUsed, lastMentioned=lastMentioned,
                               liensAExplorer=liensAExplorer, liensADemander=liensADemander,
                               useTranslation=useTranslation, useCorrection=useCorrection)
            
        elif len(liensAExplorer) > 0:
            d = random.choice(liensAExplorer)
            coeurCurrent, lien, coeurInterloc = d[0], d[1], d[2]
            
            # On choisit le lien le plus important pour la suite de l'exploration
            lienExploration = sorted(lien.coeur.liens, key=lambda x: x.importance) [-1]
            
            # On retourne au bon endroit de l'histoire
            coeurInterlocuteur = coeurInterloc
            
            # On l'ajoute à la mémoire de l'interlocuteur
            coeurReponseCopy = deepcopy(lienExploration.coeur)
            coeurReponseCopy.liens = []
            lienExplorationCopy = Lien(coeur=coeurReponseCopy, typeLien=lienExploration.typeLien, importance=lienExploration.importance)
            coeurInterlocuteur.ajouterLien(lienExplorationCopy)
              
            # On change de coeurActuel pour l'interlocuteur
            coeurInterlocuteur = coeurReponseCopy
            
            
            liensAExplorer.remove(d)
            
            
            # Pour rappel, voici à quoi ressemble l'architecture : 
            # coeurCurrent (déja raconté)   -----lien----->   lien.coeur (déja raconté)   -----lienExploration----->   lienExploration.coeur (PAS ENCORE RACONTE)
            rappelExplo = rappel(lien.typeLien, dateCoeur=lien.coeur.date, date=date, used=expUsed)
            phrase1 = coeurCurrent.toText(interlocuteur, locuteur, lastMentioned=lastMentioned, date=date, premierCoeur=False, useTranslation=useTranslation, useCorrection=useCorrection)
            phrase2 = lien.coeur.toText(interlocuteur, locuteur, lastMentioned=lastMentioned, date=date, premierCoeur=False, useTranslation=useTranslation, useCorrection=useCorrection)
            rappelExplo = rappelExplo.replace("[1]", phrase1).replace("[2]", phrase2)
            demande = interlocuteur.getTic(interlocuteur) +  rappelExplo + " " +  interlocuteur.getTic(interlocuteur) +  demanderLien(lienExploration.typeLien, dateCoeur=lienExploration.coeur.date, date=date, used=expUsed)
            
            # On ajoute au texte
            if len(debutPhrase) > 0:
                phrasesPrecedentes += "\n" + locuteur.imprimer(ajouterPonctuation(debutPhrase), useTranslation=useTranslation, useCorrection=useCorrection)
            phrasesPrecedentes += "\n" + interlocuteur.imprimer(demande, useTranslation=useTranslation, useCorrection=useCorrection)
            debutPhrase = motsLiasonsRecommencer(lienExploration.typeLien, dateCoeur=lien.coeur.date, date=date, used=expUsed) + " "
            
            return self.toText(locuteur, interlocuteur, date=date, coeurActuel=lienExploration.coeur, histInterlocuteur=histInterlocuteur, coeurInterlocuteur=coeurInterlocuteur,
                               reponse=True, phrasesPrecedentes=phrasesPrecedentes, debutPhrase=debutPhrase, nbCoeursDansLaPhrase=0, expUsed=expUsed, lastMentioned=lastMentioned,
                               liensAExplorer=liensAExplorer, liensADemander=liensADemander,
                               useTranslation=useTranslation, useCorrection=useCorrection)
            
        else: # Il n'y a pas de liens a demander ni explorer
            if len(debutPhrase) > 0:
                phrasesPrecedentes += "\n" + locuteur.imprimer(ajouterPonctuation(debutPhrase), useTranslation=useTranslation, useCorrection=useCorrection)
            return phrasesPrecedentes
     
      
      
      
        
