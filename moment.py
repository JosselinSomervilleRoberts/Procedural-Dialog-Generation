# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 17:30:22 2021

@author: josse
"""


from psclib.complement import Complement
from datetime import timedelta


class Moment(Complement):
    
    def __init__(self, name=None, moment=None, rapport="", date=None):
        Complement.__init__(self, name=name)
        self.moment = moment # ceci est un coeur
        self.rapport = rapport
        self.date = date
        
    
    def getGraphText(self):
        if len(self.name) > 0: return self.name[0]
        
        if not(self.date is None):
            s= str(self.date) 
            return s
        
        rapport = self.rapport
        if rapport == "": rapport = "alors"
        s = "Par rapport à un coeur</td></tr>\n"
        s+= """<tr><td align="left"><I>Rapport:</I> """ + rapport + " que </td></tr>\n"
        s+= """<tr><td align="right"><font point-size='10'>""" + self.moment.getGraphText().replace("center", "left") + "</font>"
        return s
  
        
    def toText(self, locuteur=None, interlocuteur=None, date=None, useTranslation=True, useCorrection=True):
        # Si on a définit la date
        if not(self.date is None) and not(date is None):
            exp = None
            delta = self.date.date() - date.date()
            liste_vals = [[timedelta(days=365), "années"], [timedelta(days=30), "mois"], [timedelta(days=7), "semaines"], [timedelta(days=1), "jours"]]
            for couple in liste_vals:
                val, lib = couple[0], couple[1]
                if exp is None:
                    k = int(abs(delta) /val)
                    if k == 1: lib = lib[:-1] # On enlève le s
                    if k > 1:
                        exp = "il y a " + str(k) + " " + lib.replace("moi", "mois")
            if delta > timedelta() and not(exp is None):
                exp = exp.replace("il y a", "dans")
            if exp is None:
                exp = "aujourd'hui"
                
            if timedelta(days=1) <= delta < timedelta(days=2):
                exp = "demain"
            elif timedelta(days=-2) < delta <= timedelta(days=-1):
                exp = "hier"
                
            if self.date.hour != 0:
                exp += ", à " + str(self.date.hour) + "h"
                if self.date.minute != 0:
                    exp += str(self.date.minute)
            
            return exp
                        
        
        
        # Si il existe des dénomitations définies pour le Lieu, on les utilises
        exp = Complement.toText(self, locuteur=locuteur, interlocuteur=interlocuteur, useTranslation=useTranslation, useCorrection=useCorrection)
        if exp != "COMPLEMENT NON DEFINI": return exp
        
        # Sinon on crée une expression à partir de l'OBJET lieu et de son rapport (sur, à coté, ...)
        rapport = self.rapport
        if rapport == "": rapport = "alors"
        print("moment:", self.moment, " /self.date:", self.date, "date:", date)
        
        """
        if self.moment is None:
            return ""
        """
        
        return rapport + " que " + self.moment.toText(locuteur=locuteur, interlocuteur=interlocuteur, useTranslation=useTranslation, useCorrection=useCorrection)