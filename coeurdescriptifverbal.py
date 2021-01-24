# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 17:54:30 2021

@author: josse
"""

from psclib.coeuraction import CoeurAction


class CoeurDescriptifVerbal(CoeurAction):
    
    def __init__(self, sujet = None, action = None, cod = None, liens =  None, infos=None, parent=None, importance=None):
        CoeurAction.__init__(self, sujet = sujet, action = action, cod = cod, liens =  liens, infos = infos, parent=parent, importance=importance)
        
        
    def toText(self, locuteur=None, interlocuteur=None, date=None, premierCoeur=True, sujetMentionedBefore=False, useTranslation=True, useCorrection=True):
        # Change uniquement premierCoeur à Vrai pour la concordance des temps
        return CoeurAction.toText(self, locuteur=locuteur, interlocuteur=interlocuteur, date=date, premierCoeur=True, sujetMentionedBefore=sujetMentionedBefore, useTranslation=useTranslation, useCorrection=useCorrection)