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