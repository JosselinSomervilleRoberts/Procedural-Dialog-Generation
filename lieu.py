# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 16:12:44 2021

@author: josse
"""

from psclib.complement import Complement


class Lieu(Complement):
    
    def __init__(self, name=None, lieu=None, rapport=""):
        Complement.__init__(self, name=name)
        self.lieu = lieu
        self.rapport = rapport
        
        
    def getGraphText(self):
        if len(self.name) > 0: return self.name[0]
        rapport = self.rapport
        if rapport == "": rapport = "à"
        s = "Par rapport à un objet\n"
        s+= "   Objet: " + self.moment.getGraphText().replace("\n", "\n   ")
        s+= "\nRapport: " + rapport
        return s
        
        
    def toText(self, locuteur=None, interlocuteur=None, useTranslation=True, useCorrection=True):
        # Si il existe des dénomitations définies pour le Lieu, on les utilises
        exp = Complement.toText(self, locuteur=locuteur, interlocuteur=interlocuteur, useTranslation=useTranslation, useCorrection=useCorrection)
        if exp != "COMPLEMENT NON DEFINI": return exp
        
        # Sinon on crée une expression à partir de l'OBJET lieu et de son rapport (sur, à coté, ...)
        rapport = self.rapport
        if rapport == "": rapport = "à"
        return rapport + " " + self.lieu.toText(locuteur=locuteur, interlocuteur=interlocuteur, types=[[0.6, "physique"]], mentionProprio=True, useTranslation=useTranslation, useCorrection=useCorrection)