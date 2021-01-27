# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 17:54:30 2021

@author: josse
"""

from psclib.coeuraction import CoeurAction


class CoeurDescriptifVerbal(CoeurAction):
    
    def __init__(self, sujet = None, action = None, cod = None, liens =  None, infos=None, parent=None, importance=None):
        CoeurAction.__init__(self, sujet = sujet, action = action, cod = cod, liens =  liens, infos = infos, parent=parent, importance=importance)
        
        
    def getGraphText(self):
      s = """<table border="0" cellborder="0" cellspacing="0">\n"""
      s+= """  <tr><td align="center"><b>COEUR DESCRIPTIF (""" + str(self.id) + """)</b></td></tr>\n"""
      if type(self.sujet) == list:
          s+= """  <tr><td align="left"><I>Sujet:</I> """ + """ et """.join([s.getGraphText() for s in self.sujet]) + """</td></tr>\n"""
      else:
          s+= """  <tr><td align="left"><I>Sujet:</I> """ + self.sujet.getGraphText() + """</td></tr>\n"""
      s+= """  <tr><td align="left"><I>Action:</I> """ + self.action.getGraphText() + """</td></tr>\n"""
      if not(self.cod is None): s+= """  <tr><td align="left"><I>Complément:</I> """ + self.cod.getGraphText() + """</td></tr>\n"""
      s+="""</table>"""
      return s
        
        
    def toText(self, locuteur=None, interlocuteur=None, date=None, premierCoeur=True, sujetMentionedBefore=False, useTranslation=True, useCorrection=True):
        # Change uniquement premierCoeur à Vrai pour la concordance des temps
        return CoeurAction.toText(self, locuteur=locuteur, interlocuteur=interlocuteur, date=date, premierCoeur=True, sujetMentionedBefore=sujetMentionedBefore, useTranslation=useTranslation, useCorrection=useCorrection)