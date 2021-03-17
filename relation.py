# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 14:02:42 2021

@author: josse
"""

class Relation:
    
    def __init__(self, perso = None, relationBase = "inconnu", relationDetaille=""):
        self.perso = perso
        self.nbRencontres = 0
        self.nbDiscussions = 0
        self.relationBase = relationBase
        self.relationDetaille = relationDetaille
        
    def getRelation(self):
        if self.relationBase != "inconnu":
            return self.relationBase + "/" + self.relationDetaille
        else:
            if self.nbDiscussions <= 1:
                return "inconnu"
            elif self.nbDiscussions <= 3:
                return "connaissance"
            else:
                return "ami"