# -*- coding: utf-8 -*-
"""
Created on Wed Dec 16 18:59:03 2020

@author: josse
"""

#import pip
import subprocess

def install(package):
	subprocess.check_call(["python", '-m', 'pip', 'install', package])
    #pip.main(['install', package])

def installRequirements():
    install('verbecc')
    install('google_trans_new')
    install('language_tool_python')
    
def importAll():
    """
    from psclib.diversifieur import correct, cong, diversifier, get_syn
    from psclib.action import Action
    from psclib.objet import Objet, Personnage
    from psclib.caracteristique import Caracteristique, Type, CaracChiffree
    from psclib.histoire import Histoire, ajouterPonctuation, demanderLien, nePasSavoirLien
    from psclib.coeuraction import CoeurAction
    from psclib.coeurdescriptif import CoeurDescriptif
    from psclib.lien import Lien
    """
    pass