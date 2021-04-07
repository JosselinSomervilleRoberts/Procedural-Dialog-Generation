# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 14:02:42 2021

@author: josse
"""

class Relation:
    
    def __init__(self, perso = None, relation = "neutre"):
        # Relations neutres : "inconnu" (0) , "connaissance" (1,2) , "ami" (3 et +)
        # Relations spéciales : Base + Détail (ex: famille + parent)
        self.perso = perso
        self.nbRencontres = 0
        self.nbDiscussions = 0
        self.relationBase = relation
        self.relationDetaillee = ""
        
        if relation == "connaissance":
            self.relationBase = "neutre"
            self.nbDiscussions = 1
        elif relation == "ami":
            self.relationBase = "neutre"
            self.nbDiscussions = 3
            
        if relation in ["parent", "enfant", "adelphe"]:
            self.relationBase = "famille"
            self.relationDetaillee = relation
        
        if relation in ["patron","collègue","employé"]:
            self.relationBase = "travail"
            self.relationDetaillee = relation
            
        
    def getRelation(self):
        if self.relationBase != "neutre":
            return self.relationBase + "/" + self.relationDetaillee
        else:
            if self.nbDiscussions < 1:
                return "inconnu"
            elif self.nbDiscussions < 3:
                return "connaissance"
            else:
                return "ami"