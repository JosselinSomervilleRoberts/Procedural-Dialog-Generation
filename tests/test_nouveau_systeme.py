# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 17:36:40 2021

@author: josse
"""

from psclib.objet import Personnage
from psclib.endroit import Endroit
from psclib.evenement import Evenement
from datetime import datetime
from psclib.dialogue import dialogue


# Persos
marcel = Personnage(name="marcel")
jackie = Personnage(name="jackie")
kevin = Personnage(name="kevin")

# Endroits
boulangerie = Endroit(libelle = "boulangerie")
supermarche = Endroit(libelle = "supermarché")
place = Endroit(libelle = "place du village")
maison_marcel = Endroit(libelle = "maison de Marcel")
maison_jackie = Endroit(libelle = "maison de Jackie")
maison_kevin = Endroit(libelle = "maison de Kevin")



boulangerie.action_possibles = [Evenement("faire a manger", ["des croissants", "des pains aux chocolat", "des baguettes"]),
                          Evenement("choisir", "à manger"),
                          Evenement("acheter", ["des croissants", "des pains aux chocolat", "des baguettes"]),
                          Evenement("payer", "la commande"),
                          Evenement("decider", "de rien acheter")]

maison_marcel.action_possibles = [Evenement("dormir")]

supermarche.action_possibles = [Evenement("acheter", ["du Nutella", "des pattes", "du riz"]),
                          Evenement("decider", "de rien acheter")]



marcel.evenements[boulangerie] = [[0.2,0.8,0,0,0,0],
                                  [0.3,0.7,0,0,0,0],
                                  [0,0,0,0,0,0],
                                  [0,0,0,0,0,0],
                                  [0,0,0,0,0,0],
                                  [0,0,0,0,0,0]]

marcel.evenements[maison_marcel] = [[0,1],
                                    [0.2,0.8]]

marcel.evenements[supermarche] = [[0,0.7, 0.3],
                                  [0.5, 0.5, 0],
                                  [1, 0, 0]]


marcel.listeLieux = [boulangerie, maison_marcel, supermarche]
marcel.endroits = [[0.5, 0.32, 0.13, 0.05],
                   [0.2, 0.7, 0.1, 0],
                   [0, 0.5, 0.4, 0.1],
                   [0.6, 0, 0.2, 0.2]]

marcel.commencer_journee(datetime(2019,3,3))
for heure in range(8,22):
    marcel.update(heure)
marcel.finir_journee()

#print(marcel.histoires[0].toText(marcel, jackie, date=datetime(2019,3,3), useTranslation=False, useCorrection=False))
print(dialogue(marcel, jackie, date=datetime(2019,3,3), useTranslation=False, useCorrection=False))