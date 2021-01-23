# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 20:46:50 2021

@author: josse
"""

from psclib.complement import Complement


class Maniere(Complement):
    
    def __init__(self, name=None, moment=None, rapport=""):
        Complement.__init__(self, name=name)
        
        
    def getGraphText(self):
        return self.name[0]
    
    
    def toText(self, locuteur=None, interlocuteur=None, date=None, useTranslation=True, useCorrection=True):
        # Si il existe des dénomitations définies pour le Lieu, on les utilises
        exp = Complement.toText(self, locuteur=locuteur, interlocuteur=interlocuteur, useTranslation=useTranslation, useCorrection=useCorrection)
        return exp