# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 14:02:42 2021

@author: josse
"""

class Relation:
    
    def __init__(self, perso = None, relationBase = "inconnu", relationDetaillee=""):
        self.perso = perso
        self.nbRencontres = 0
        self.nbDiscussions = 0
        self.relationBase = relationBase
        self.relationDetaillee = relationDetaillee
        
        if relationBase == "connaissance":
            self.relationBase = "inconnu"
            self.nbDiscussions = 1
        elif relationBase == "ami":
            self.relationBase = "inconnu"
            self.nbDiscussions = 3
            
        if relationDetaillee in ["parent", "enfant", "adelphe"]:
            self.relationBase = "famille"
            
        
    def getRelation(self):
        if self.relationBase != "inconnu":
            return self.relationBase + "/" + self.relationDetaillee
        else:
            if self.nbDiscussions < 1:
                return "inconnu"
            elif self.nbDiscussions < 3:
                return "connaissance"
            else:
                return "ami"