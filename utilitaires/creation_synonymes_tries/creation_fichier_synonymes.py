# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 15:45:04 2020

@author: josse
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 20:14:40 2020

@author: josse
"""

import io
import sqlite3
import numpy as np
from math import ceil
conn = sqlite3.connect('mots.db')
c = conn.cursor()
query_select = '''SELECT freq_film FROM liste_mots WHERE lemme = ? AND type = ?;'''


NsynMax = 3
ThreshHoldSimilarity = 0.4
IndexMax = 20
ThresholdUsage = 30



# Ouvre la BDD de reference
file = io.open("synonymes.txt", mode="r", encoding="utf-8")
f = open("synonymes_tries.txt", "a")

liste = file.readlines()
dict_syn = {}
dict_syn[-1] = {}
dict_syn[0] = {}
dict_syn[2] = {}
dict_syn[3] = {}
dict_syn[4] = {}
dict_syn[5] = {}

for i in range(len(liste)-1):
    mot = liste[i].split("|")[0]
    l = liste[i+1].split("|")
    typ = l[0][1:-1]
    liste_syn = l[1:]
    
    nb_typ = -1
    if "Verbe" in typ:
        nb_typ = 0
    elif "Nom" in typ:
        nb_typ = 2
    elif "Adjectif" in typ:
        nb_typ = 3
    elif "Adverbe" in typ:
        nb_typ = 4
    elif "Preposition" in typ:
        nb_typ = 5
        
    
    liste_syn = [x.replace("\n","") for x in liste_syn]    
    dict_syn[nb_typ][mot.replace("\n","")] = liste_syn
    
    


def syn_is_in(typ, mot, syn, degre):
    global dict_syn
    if degre == 0:
        return int(mot == syn)
    else:
        if syn in dict_syn[typ]:
            l_syn = dict_syn[typ][syn]
            # S'il n'y a qu'un seul synonyme et que c'est le mot on renvoie 1 sinon 0
            if len(l_syn) == 1:
                if l_syn[0] == mot:
                    return 1
                else:
                    return 0
            if degre == 1:
                if mot in l_syn or mot==syn:
                    return 1
                else:
                    return 0
            else:
                r = 0
                total = len(l_syn)
                for s in l_syn:
                    if s == mot:
                        total -= 1
                    else:
                        r += syn_is_in(typ, mot, s, degre -1)
                return r / float(total) # Moyenne
        else:
            return 1 # avant c etait 0

def trier_syn(typ, s):
    global dict_syn
    l_syn = dict_syn[typ][s][:IndexMax]
    val_syn = []
    for i in range(len(l_syn)):
        syn = l_syn[i]
        
        # Si le synonyme est courant dans la langue française
        data_tuple = (syn, typ)
        c.execute(query_select, data_tuple)
        record = c.fetchone()
        if record != None:
            usage = record[0]
            
            if usage >= ThresholdUsage/2.0:   
                # Si le synonyme est proche du mot
                similarity = syn_is_in(typ, s, syn, 3)
                if similarity >= ThreshHoldSimilarity/2.0:
                    val_syn.append([syn,i,similarity,usage])
    
    
    v = []
    nbmin = 1             
    if len(val_syn) > nbmin:
        for x in val_syn:
            if x[2] >= ThreshHoldSimilarity:
                v.append(x)
        if len(v) < nbmin:
            v = sorted(val_syn, key=lambda syn: syn[2])[::-1][:nbmin]
    else:
        v = val_syn
          
    #print("fiini")
    v2 = []              
    if len(v) > nbmin:
        for x in v:
            if x[3] >= ThresholdUsage:
                v2.append(x)
        if len(v2) < nbmin:
            v2 = sorted(v, key=lambda syn: syn[3])[::-1][:nbmin]
    else:
        v2 = v
        
    val_syn = v2
    #print("fini2")
    
    # Tri des synonymes basé sur la fonction :
    # syn = [nom,i,similarity,usage]
    liste_syn_sorted = sorted(val_syn, key=lambda syn: 0.5/(1+syn[1])**0.5 + 1.4*syn[2] - 0.005*syn[3]**0.5)[::-1]
    
    # On crée les couples [synonyme, score]
    syn_f = [[syn[0], 0.5/(1+syn[1])**0.5 + 1.4*syn[2] - 0.005*syn[3]**0.5] for syn in liste_syn_sorted[:NsynMax]]
    
    # On normalise els scores pour les mettre en %
    score_total = np.sum(np.array([x[1] for x in syn_f]))
    syn_final = [[syn[0],round(100*syn[1]/score_total,1)] for syn in syn_f]
    return syn_final



def syn(typ, s, debug=True, write=False):
    lsyn = trier_syn(typ, s)
    print(s)
    if debug:
        print("Synonymes de", s, ":", lsyn)
        print(dict_syn[typ][s])
        print("")
        
    if write:
        sE = s + "="
        for elt in lsyn:
            registre = 1 # Correspond a courant
            sE += elt[0] + ":" + str(elt[1]) + ":" + str(registre) + "/"
        if len(lsyn) > 0:
            sE = sE[:-1]
        f.write(sE + "\n")
    


def buildNewFile():
    for typ in [0,2,3,4]:
        for s in dict_syn[typ].keys():
            syn(typ, s, write=True, debug=False)


"""
syn(2,"homme")
syn(2,"chaise")
syn(2,"canapé")
syn(2,"stylo")
syn(2,"crayon")
syn(2,"tarte")
syn(0, "être")
syn(2,"ordinateur")
syn(0, "frapper")
"""
buildNewFile()
f.close()
#syn(3,"pénible")
#syn(2, "chanson")