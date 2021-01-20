# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 16:12:07 2021

@author: josse
"""

import random


class Complement():
    
    def __init__(self, name=None):
        self.name = name
        if self.name is None or name == "": self.name = []
        if type(self.name) == str: self.name = [self.name]
        
    def toText(self, locuteur=None, interlocuteur=None, useTranslation=True, useCorrection=True):
        if len(self.name) > 0:
            return random.choice(self.name)
        else:
            return "COMPLEMENT NON DEFINI"