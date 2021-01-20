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
    
    
    
def getExpression(key, typeLien, used=None):
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

    if len(liste_exps) > 0: # Si il y a des expressions que l'on a pas encore utilisées
        choix = random.choice(liste_exps)
        used.append(choix)
        return choix
    else: # Si on a déja tout utilisé
        return random.choice(dictExp[key][typeLien])


def demanderLien(typeLien, used=None):
  return getExpression("demander", typeLien, used)

def demanderAvecPhraseLien(typeLien, used=None):
  return getExpression("demander_avec_phrase", typeLien, used)

def nePasSavoirLien(typeLien, used=None):
  return getExpression("ne_pas_savoir", typeLien, used)

def rappel(typeLien, used=None):
  return getExpression("rappel", typeLien, used)

def motsLiasonsContinuer(typeLien, used=None):
  return getExpression("mots_liaisons_continuer", typeLien, used)

def motsLiasonsRecommencer(typeLien, used=None):
  return getExpression("mots_liaisons_recommencer", typeLien, used)

def retourArriere(typeLien, used=None):
  return getExpression("retour_arriere", typeLien, used)




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


  def toTextOld(self, locuteur, interlocuteur, coeurCurrent=None, prefixe="", s0=""):
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
      
      # On ordonne les liens dans l'ordre CAUSE, CONSEQUENCE, SUITE
      importanceTotale = 0
      liste_liens = []
      indexDebutConsequence = 0
      for lien in random.sample(coeurCurrent.liens, len(coeurCurrent.liens)):
          importanceTotale += lien.importance
          if lien.typeLien == CAUSE:
              liste_liens = [lien] + liste_liens
              indexDebutConsequence += 1
          elif lien.typeLien == SUITE:
              liste_liens += [lien]
          else:
              liste_liens = liste_liens[:indexDebutConsequence] + [lien] + liste_liens[indexDebutConsequence+1:]
      

      lienPrincipal = None
      importanceLienPrincipal = 0
      for lien in liste_liens:
        # Plus le perso est bavard plus il aura tendance à enchainer les liens
        # coeff Linéaire : bavard = 0 -> coeffDimin = 20, bavard=10 -> coeffDimin = 1.1
        coeff = 20 - 1.89*locuteur.getCaracValue(Caracteristique(name="bavard"))
        # exposant allant de 0 a 1 par rapport à la proportion d'hisoires racontées
        exposant = 2.*((1.+(len(liensRacontes)/float(len(coeurCurrent.liens)))) / (1.+len(liensOmis)/float(len(coeurCurrent.liens))) - 0.5)/3.
        proba = probaRaconter / float(coeff**exposant)

        if lien.importance==3 or importanceTotale*random.random() <= (lien.importance**2)*proba: # On raconte le lien
          liensRacontes.append(lien)
          if lien.importance > importanceLienPrincipal:
              lienPrincipal = lien
        else:
          liensOmis.append(lien)




      # - Si il y a plusieurs liens: on ajoute dans la même phrase tous les liens sauf le lienPrincipal,
      # puis on met un point et on recommence une phrase avec le lien principal.
      # - Si il n'y a qu'un seul lien, il y a une chance sur 2 de recommencer une phrase.
      # Le lien principal doit être à la fin
      liens_continuer = {CAUSE: " parce que ", CONSEQUENCE: " donc ", SUITE: " puis "}
      liens_recommencer = {CAUSE: "C\'est parce que ", CONSEQUENCE: "Et donc ", SUITE: "Ensuite, "}
      
      if len(liensRacontes) == 1:
        if random.random() <= 0.5:
          s1 += ". " + liens_recommencer[liensRacontes[0].typeLien]
        else:
          s1 += liens_continuer[liensRacontes[0].typeLien]
        return self.toText(locuteur, interlocuteur, coeurCurrent=liensRacontes[0].coeur, prefixe=s1, s0=s0)
      
      elif len(liensRacontes) > 1:    
        for l in liensRacontes :
          if not(l == lienPrincipal):
            s1 += liens_continuer[liensRacontes[0].typeLien] + l.coeur.toText(locuteur, interlocuteur)
        s1 += ". " + liens_recommencer[lienPrincipal.typeLien]
        return self.toText(locuteur, interlocuteur, coeurCurrent=lienPrincipal.coeur, prefixe=s1, s0=s0)

      s0 += "\n" + locuteur.imprimer(ajouterPonctuation(s1))



      # L'interlocuteur pose des questions
      # Plus le perso est curieux, plus il a de chance de demander les liens
      # Linéaire : curieux = 0 -> proba = 0.25, curieux=10 -> proba = 0.95
      probaDemander = 0.25 + 0.07*interlocuteur.getCaracValue(Caracteristique(name="curiosite"))
      #print("curiosite", interlocuteur.prenom, interlocuteur.getCaracValue(Caracteristique(name="curiosite")), "/ proba=", probaDemander)
      probaDemanderInfoExistante = 0.75 # Proba de demander une info dans liensOmis

      if random.random() <= probaDemander:
        if len(liensOmis) > 0 and random.random() <= probaDemanderInfoExistante: # On demande une info existante
          l = random.choice(liensOmis)
          demande = demanderLien(l.typeLien)
          if "[]" in demande:
              phrase = coeurCurrent.toText(interlocuteur, locuteur)
              demande = demande.replace("[]", phrase)
                
          s0 += "\n" + interlocuteur.imprimer(demande)
          
          dictPrefixe = {}
          dictPrefixe[CAUSE] = ["Parce que "]
          dictPrefixe[CONSEQUENCE] = ["Donc "]
          dictPrefixe[SUITE] = ["Ensuite, "]
          return self.toText(locuteur, interlocuteur, coeurCurrent=l.coeur, prefixe=random.choice(dictPrefixe[l.typeLien]), s0=s0)
          #s0 += "\n" + self.toText(locuteur, interlocuteur, coeurCurrent=l.coeur, prefixe=random.choice(dictPrefixe[l.typeLien]))
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
          demande = demanderLien(typeLien)
          if "[]" in demande:
              phrase = coeurCurrent.toText(interlocuteur, locuteur)
              demande = demande.replace("[]", phrase)
                
          s0 += "\n" + interlocuteur.imprimer(demande)
          #s0 += "\n" + interlocuteur.imprimer(demanderLien(typeLien), diversify=False)
          s0 += "\n" + locuteur.imprimer(nePasSavoirLien(typeLien), diversify=False)
    else:
      s0 += "\n" + locuteur.imprimer(ajouterPonctuation(s1))
      
    return s0 



  def toText(self, locuteur, interlocuteur, coeurActuel=None, phrasesPrecedentes="", debutPhrase="", nbCoeursDansLaPhrase=0, liensAExplorer=None, liensADemander=None, expUsed=None, useTranslation=True, useCorrection=True): 
    # Si on commence à raconter l'histoire, on commence par le début
    if coeurActuel is None: coeurActuel = self.head
    
    # Si il n'y a pas encore de DEMANDE ou D'EXPLORATION, alors les listes sont vides
    if liensAExplorer is None: liensAExplorer = []
    if liensADemander is None: liensADemander = []
    if expUsed is None: expUsed = []
    
    """
    # Mots pour continuer une phrase
    mots_liaisons_continuer = {COMPLEMENT_LIEU: [""], CAUSE: ["parce que", "car"], CONSEQUENCE: ["donc", "du coup"], SUITE: ["puis", "et puis", "et ensuite"]}
    # Mots pour recommencer une phrase
    mots_liaisons_recommencer = {COMPLEMENT_LIEU: [""], CAUSE: ["C\'est parce que"], CONSEQUENCE: ["Et donc", "Et du coup", "Du coup"], SUITE: ["Ensuite,", "Alors,"]}
    """
    
    # On transforme le coeur actuel en texte
    debutPhrase += coeurActuel.toText(locuteur, interlocuteur, useTranslation=useTranslation, useCorrection=useCorrection)
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
      
      # Si on arrete l'histoire (i.e. on a choisi lienFin)
      if lienChoisi.coeur is None: # C'est le lien de fin
        return phrasesPrecedentes + "\n" + locuteur.imprimer(ajouterPonctuation(debutPhrase), useTranslation=useTranslation, useCorrection=useCorrection)
      
      # On ajoute des précisions (éventuellement)
      sommeImportance = min(10,sum([lien.importance for lien in liens]))
      nbPrecisions = 0
      liensAPreciser = []
      
      random.shuffle(liens) # On mélange les liens car l'ordre importe (Plus on a fait de précisions, moins on a de chance d'en rajoute,
      # donc les premiers liens sont favorisés)
      for l in liens:
          # Plus on est bavard, plus on a de chance de préciser les liens
          # Plus le lien est important plus on a de chance de le préciser
          # Plus on a fait de précisions, moins on a de chance d'en rajouter
          probaPreciser = (0.25 + 0.07*locuteur.getCaracValue(Caracteristique(name="bavard"))) * l.importance / (sommeImportance*(1+nbPrecisions))
          if random.random() <= probaPreciser: # Si on précise le lien
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
          
          if lien.typeLien in [COMPLEMENT, COMPLEMENT_LIEU, COMPLEMENT_TEMPS, COMPLEMENT_MANIERE]: # C'est un complément
              ajout = lien.coeur.toText(locuteur, interlocuteur, autoriserRadoter=False, useTranslation=useTranslation, useCorrection=useCorrection)
              if lien.typeLien == COMPLEMENT_TEMPS:
                  # On veut ajouter le CCT au début de la phrase,
                  # Il faut donc retrouver le début de la phrase d'abord
                  liste_phrases = debutPhrase.split(". ")
                  liste_phrases[-1] = ajout + ", " + liste_phrases[-1]
                  debutPhrase = ". ".join(liste_phrases) # On réassemble
              else:
                  debutPhrase += " " + ajout
          
          else: # Ce n'est pas un complément
              liensDansLaPhrase += 1
              lastLien = lien
              probaRecommencer = (nbCoeursDansLaPhrase>1)*(0.2 + 0.002*len(debutPhrase.split(".")[-1]) + 0.1*nbCoeursDansLaPhrase) # 20% + 0.2% par caractère + 10% par liens déja dans la phrase
              
              if i == len(liensAPreciser) - 1: # Si c'est le dernier lien, proba de re commencer - 50%
                  probaRecommencer -= 0.5
                  
              
              if random.random() <= probaRecommencer: # On recommence une phrase
                  debutPhrase += ". " + motsLiasonsRecommencer(lien.typeLien, expUsed) + " " + lien.coeur.toText(locuteur, interlocuteur, useTranslation=useTranslation, useCorrection=useCorrection)
                  nbCoeursDansLaPhrase = 1
                  phraseRecommencee = True
              else: # On continue dans la même phrase
                  debutPhrase += " " + motsLiasonsContinuer(lien.typeLien, expUsed) + " " + lien.coeur.toText(locuteur, interlocuteur, useTranslation=useTranslation, useCorrection=useCorrection)
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
                      liensAExplorer.append([coeurActuel, lien])
                      
                  
      # Pour chaque lien non précisé, l'interlocuteur peut DEMANDER la précision
      # Il peut aussi demander des précisions dont le locuteur n'a pas la réponse (a ajouter)
      for l in liens:
          if not(l in liensAPreciser): # Si le lien n'a pas été précisé
              # Son envie dde demander va dépendre de :
              # - l'importance du lien
              # - la curiosité de l'interlocuteur
              # - le nombre de précisions qu'il souhaite déja demander
              probaDemander = 0.05 + 0.15*log(l.importance) + 0.55*(interlocuteur.getCaracValue(Caracteristique(name="curiosite")) - 2*len(liensADemander))
              if random.random() <= probaDemander: # Si on demande le lien
                  liensADemander.append([coeurActuel, l])
              
      
      # Enfin, on ajoute le lienChoisi
      # (On recommence une phrase pour ça)
      if phraseRecommencee or liensDansLaPhrase >= 1: # On a recommencé ou on a pas recommencé de phrase mais il y a eu des précisions
          
          # Si on a dit un truc plus prioritaire, il faut repréciser le coeur. (RETOUR ARRIERE)
          # Comme la définition des liens est faite par ordre de priorité, on peut simplement faire une comparaison sur le type
          if lastLien.typeLien >= lienChoisi.typeLien:
              debutPhrase += ". "
              retour = retourArriere(lienChoisi.typeLien, expUsed)
              phrase1 = coeurActuel.toText(locuteur, interlocuteur, useTranslation=useTranslation, useCorrection=useCorrection)
              retour = retour.replace("[]", phrase1)
              debutPhrase += retour + " "
          else:
              debutPhrase += ". " + motsLiasonsRecommencer(lienChoisi.typeLien, expUsed) + " "
          nbCoeursDansLaPhrase = 1
      else: # On a pas recommencé de phrase et il n'y a eu aucune précision.
          probaRecommencer = (nbCoeursDansLaPhrase>1)*(0.2 + 0.002*len(debutPhrase.split(".")[-1]) + 0.1*nbCoeursDansLaPhrase) # 20% + 0.2% par caractère + 10% par liens déja dans la phrase
          if random.random() <= probaRecommencer:
              debutPhrase += ". " + motsLiasonsRecommencer(lienChoisi.typeLien, expUsed) + " "
              nbCoeursDansLaPhrase = 1
          else:
              debutPhrase += " " + motsLiasonsContinuer(lienChoisi.typeLien, expUsed) + " "
              nbCoeursDansLaPhrase += 1
              
      return self.toText(locuteur, interlocuteur, coeurActuel=lienChoisi.coeur, phrasesPrecedentes=phrasesPrecedentes, debutPhrase=debutPhrase, nbCoeursDansLaPhrase=nbCoeursDansLaPhrase, liensAExplorer=liensAExplorer, liensADemander=liensADemander, expUsed=expUsed, useTranslation=useTranslation, useCorrection=useCorrection)
      
    else: # IL N'Y A PAS DE LIEN
        # L'interlocuteur peut maintenant poser ses questions (DEMANDE puis EXPLORATION)
        
        if len(liensADemander) > 0:
            d = random.choice(liensADemander)
            coeurCurrent, lien = d[0], d[1]
            liensADemander.remove(d)
            demande = demanderAvecPhraseLien(lien.typeLien, expUsed)
            if "[]" in demande:
                phrase = coeurCurrent.toText(interlocuteur, locuteur, useTranslation=useTranslation, useCorrection=useCorrection)
                demande = demande.replace("[]", phrase)
                
            # On ajoute au texte
            phrasesPrecedentes += "\n" + locuteur.imprimer(ajouterPonctuation(debutPhrase), useTranslation=useTranslation, useCorrection=useCorrection)
            phrasesPrecedentes += "\n" + interlocuteur.imprimer(demande, useTranslation=useTranslation, useCorrection=useCorrection)
            debutPhrase = motsLiasonsRecommencer(lien.typeLien, expUsed) + " "
            return self.toText(locuteur, interlocuteur, coeurActuel=lien.coeur, phrasesPrecedentes=phrasesPrecedentes, debutPhrase=debutPhrase, nbCoeursDansLaPhrase=0, liensAExplorer=liensAExplorer, liensADemander=liensADemander, expUsed=expUsed, useTranslation=useTranslation, useCorrection=useCorrection)
            
        elif len(liensAExplorer) > 0:
            d = random.choice(liensAExplorer)
            coeurCurrent, lien = d[0], d[1]
            liensAExplorer.remove(d)
            
            # On choisit le lien le plus important pour la suite de l'exploration
            lienExploration = sorted(lien.coeur.liens, key=lambda x: x.importance) [-1]
            # Pour rappel, voici à quoi ressemble l'architecture : 
            # coeurCurrent (déja raconté)   -----lien----->   lien.coeur (déja raconté)   -----lienExploration----->   lienExploration.coeur (PAS ENCORE RACONTE)
            rappelExplo = rappel(lien.typeLien, expUsed)
            phrase1 = coeurCurrent.toText(interlocuteur, locuteur, useTranslation=useTranslation, useCorrection=useCorrection)
            phrase2 = lien.coeur.toText(interlocuteur, locuteur, useTranslation=useTranslation, useCorrection=useCorrection)
            rappelExplo = rappelExplo.replace("[]", phrase1).replace("()", phrase2)
            demande = rappelExplo + " " + demanderLien(lienExploration.typeLien)
            
            # On ajoute au texte
            phrasesPrecedentes += "\n" + locuteur.imprimer(ajouterPonctuation(debutPhrase), useTranslation=useTranslation, useCorrection=useCorrection)
            phrasesPrecedentes += "\n" + interlocuteur.imprimer(demande, useTranslation=useTranslation, useCorrection=useCorrection)
            debutPhrase = motsLiasonsRecommencer(lienExploration.typeLien, expUsed) + " "
            return self.toText(locuteur, interlocuteur, coeurActuel=lienExploration.coeur, phrasesPrecedentes=phrasesPrecedentes, debutPhrase=debutPhrase, nbCoeursDansLaPhrase=0, liensAExplorer=liensAExplorer, liensADemander=liensADemander, expUsed=expUsed, useTranslation=useTranslation, useCorrection=useCorrection)
            
        else: # Il n'y a pas de liens a demander ni explorer
            return phrasesPrecedentes + "\n" + locuteur.imprimer(ajouterPonctuation(debutPhrase), useTranslation=useTranslation, useCorrection=useCorrection)
     
      
      
      
        
