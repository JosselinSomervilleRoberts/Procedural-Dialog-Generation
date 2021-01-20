# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 17:30:22 2021

@author: josse
"""


from psclib.complement import Complement


class Moment(Complement):
    
    def __init__(self, name="", moment=None, rapport=""):
        Complement.__init__(self, name=name)
        self.moment = moment # ceci est un coeur
        self.rapport = rapport
        
        
    def toText(self, locuteur=None, interlocuteur=None, useTranslation=True, useCorrection=True):
        # Si il existe des dénomitations définies pour le Lieu, on les utilises
        exp = Complement.toText(self, locuteur=locuteur, interlocuteur=interlocuteur, useTranslation=useTranslation, useCorrection=useCorrection)
        if exp != "COMPLEMENT NON DEFINI": return exp
        
        # Sinon on crée une expression à partir de l'OBJET lieu et de son rapport (sur, à coté, ...)
        rapport = self.rapport
        if rapport == "": rapport = "à"
        return rapport + " que " + self.moment.toText(locuteur=locuteur, interlocuteur=interlocuteur, useTranslation=useTranslation, useCorrection=useCorrection)