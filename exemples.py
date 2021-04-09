# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 13:45:52 2021

@author: josse
"""

from psclib.diversifieur import correct, cong, diversifier, get_syn, buildSynonyms
from psclib.action import Action
from psclib.objet import Objet, Personnage
from psclib.caracteristique import Caracteristique, Type, CaracChiffree
from psclib.histoire import Histoire, ajouterPonctuation, demanderLien, nePasSavoirLien, SUITE, CAUSE, CONSEQUENCE, OBJECTIF
from psclib.coeuraction import CoeurAction
from psclib.coeurdescriptif import CoeurDescriptif
from psclib.coeurdescriptifverbal import CoeurDescriptifVerbal
from psclib.lien import Lien
from psclib.dialogue import dialogue, pickStory, raconter, quiparle, transition, fin, testContinuer, intersection, switcheroo, intro, connait
from psclib.complement import Complement
buildSynonyms()

from datetime import datetime




def getExemplesDispo():
    return ["conjugaison", "transmisson info"]


def exemple(name, graph=False):
    
    
    if name=="qinpei":
        if True:
            monak = Personnage(name="lancelot")
            anne = Personnage(name="jackie")
            monak.ajouterRelations({"ami":anne})
            anne.ajouterRelations({"ami":monak})
            chien = monak.ajouterPossession({"lib": "chien", "noms": ["Bigni"]})
            voyageur = Objet({"lib": "voyageur"})
            loup = Objet({"lib": "loup"})
            
            balader = Action(name="balader")
            balader.adverbes = ["tranquillement"]
            
            c1 = CoeurAction(sujet=monak, action=balader, cod=chien, ton = "joyeux")  
            c1.ajouterLieu(name="dans la forêt", importance=10)                        
            #c1.ajouterManiere(name="avec joie", importance=20)
            c2 = CoeurAction(sujet=monak, action=Action(name="exercer"), cod=chien, ton = "joyeux")
            c3 = CoeurAction(sujet=[monak,chien], action=Action(name="rencontrer"),cod = voyageur,ton = "neutre")
            c4 = CoeurAction(sujet=loup, action=Action(name="battre"),cod=chien,ton ="triste")
            c5 = CoeurDescriptifVerbal(sujet=voyageur, action=Action(name = "marcher"), ton = "neutre")
            c5.ajouterLieu(name="dans la forêt", importance=10)
            c6 = CoeurAction(sujet=[monak,chien], action=Action(name="continuer"),ton="neutre")
            c7 = CoeurAction(sujet=monak,action=Action(name="pêcher"),ton="neutre")
            c7.ajouterLieu(name="à la rivière")
            c8 = CoeurAction(sujet=[monak,chien], action=Action(name="monter"),ton="neutre")
            c8.ajouterLieu(name="sur la montagne")
            c9 = CoeurAction(sujet=[monak,chien],action=Action(name="dormir"),ton="joyeux")
            c9.ajouterLieu(name="à la belle étoile")
            c10 = CoeurDescriptif(sujet=chien, carac=CaracChiffree(name="blesse", value=8), ton = "triste")
            
            
            
            c1.ajouterLien(Lien(coeur=c2, typeLien=OBJECTIF, importance=10))
            c1.ajouterLien(Lien(coeur=c3, typeLien=SUITE, importance=20))
            c2.ajouterLien(Lien(coeur=c4, typeLien=CAUSE,importance=1 ))
            c3.ajouterLien(Lien(coeur=c5, typeLien=CAUSE,importance=1 ))
            c4.ajouterLien(Lien(coeur=c10, typeLien=CONSEQUENCE,importance=3 ))
            c3.ajouterLien(Lien(coeur=c6, typeLien=SUITE,importance=3 ))
            c6.ajouterLien(Lien(coeur=c7, typeLien=OBJECTIF,importance=3 ))
            c6.ajouterLien(Lien(coeur=c8, typeLien=SUITE,importance=3 ))
            c8.ajouterLien(Lien(coeur=c9, typeLien=SUITE,importance=3 ))
            
            hist = Histoire(head=c1, titre="Monak marche avec son chien")
            hist.ton = "joyeux"
            monak.creerHistoire(hist)
            
            ajd = datetime(2021,1,22)
            print(dialogue(monak, anne, date=ajd, useTranslation=False, useCorrection=False))
            
    
    
    if name == "conjugaison":
        
        for i in range(3):
            
            marcel = Personnage(name="marcel")
            jackie = Personnage(name="jackie")
            marcel.ajouterRelations({"enfant":jackie})
            jackie.ajouterRelations({"parent":marcel})
            chien = marcel.ajouterPossession({"lib": "chien", "noms": ["Bubule"]})
            voiture = Objet({"lib": "voiture"})
            veterinaire = Objet({"lib": "veterinaire"})
            
            rouler = Action(name="rouler")
            rouler.adverbes = ["trop vite"]
            
            c1 = CoeurAction(sujet=marcel, action=Action(name="balader"), cod=chien, ton = "joyeux")                    
            c1.ajouterLieu(name="au parc", importance=5)                        
            c1.ajouterManiere(name="avec joie", importance=20)                                          
            c2 = CoeurAction(sujet=voiture, action=Action(name="ecraser"), cod=chien, ton = "triste")
            c3 = CoeurDescriptifVerbal(sujet=voiture, action=rouler, ton = "neutre")
            c4 = CoeurDescriptif(sujet=marcel, carac=CaracChiffree(name="colere", value=8), ton = "triste")
            c5 = CoeurAction(sujet=[marcel,chien], action=Action(name="aller voir"), cod=veterinaire, ton = "triste")
            c6 = CoeurAction(sujet=veterinaire, action=Action(name="soigner"), cod=chien, ton = "joyeux")   
            c7 = CoeurAction(sujet=marcel, action=Action(name="casser"), cod=voiture, ton = "triste") 
            c8 = CoeurAction(sujet=chien, action=Action(name="se défouler"), ton = "neutre")
            
            #c2.ajouterMoment(moment=c1, importance=50)
            c1.ajouterLien(Lien(coeur=c2, typeLien=SUITE, importance=5))
            c1.ajouterLien(Lien(coeur=c8, typeLien=OBJECTIF, importance=20))
            c2.ajouterLien(Lien(coeur=c3, typeLien=CAUSE, importance=1))
            c2.ajouterLien(Lien(coeur=c4, typeLien=CONSEQUENCE, importance=1))
            c2.ajouterLien(Lien(coeur=c5, typeLien=CONSEQUENCE, importance=3))
            c5.ajouterLien(Lien(coeur=c6, typeLien=SUITE, importance=1.5))
            c4.ajouterLien(Lien(coeur=c7, typeLien=CONSEQUENCE, importance=1.5))
            
            
            hist = Histoire(head=c1, titre="Marcel promene son chien")
            hist.ton = "triste"
            marcel.creerHistoire(hist)
            
            
            nom = ""
            if i==0:
                print("\n\n\n========= SI ON NE PRECISE PAS LES MOMENTS ==========")
                nom = "histoire_sans_moment"
            elif i==1:
                print("\n\n\n========= SI ON PRECISE EXPLICITEMENT LES MOMENTS ==========")
                c1.ajouterMoment(date=datetime(2021,1,20,20, 10, 53), importance=200)
                c6.ajouterMoment(date=datetime(2021,1,21), importance=200)
                c7.ajouterMoment(date=datetime(2021,1,23), importance=200)
                nom = "histoire_moments_explicites"
            elif i==2:
                print("\n\n\n========= SI ON PRECISE IMPLICITEMENT LES MOMENTS ==========")
                c1.ajouterMoment(date=datetime(2021,1,20,20, 10, 53), importance=0)
                c6.ajouterMoment(date=datetime(2021,1,21), importance=0)
                c7.ajouterMoment(date=datetime(2021,1,23), importance=0)
                nom = "histoire_moments_implicites"
                
            if graph:
                dot = hist.getGraph()
                dot.render(nom, view=True, format="png")
    
            ajd = datetime(2021,1,22)
            print(dialogue(jackie, marcel, date=ajd, useTranslation=False, useCorrection=False))
            
          
            
            
            
    if name=="transmisson info":
        marcel = Personnage(name="marcel")
        jackie = Personnage(name="jackie")
        kevin = Personnage(name="kevin")
        
        chien = marcel.ajouterPossession({"lib": "chien", "noms": ["Bubule"]})
        voiture = Objet({"lib": "voiture"})
        veterinaire = Objet({"lib": "veterinaire"})
        
        rouler = Action(name="rouler")
        rouler.adverbes = ["trop vite"]
        
        
        c1 = CoeurAction(sujet=marcel, action=Action(name="balader"), cod=chien)                    
        c1.ajouterLieu(name="au parc", importance=5)
        c1.ajouterMoment(date=datetime(2021,1,20,20, 10, 53), importance=200)                       
        c1.ajouterManiere(name="avec joie", importance=20)                                          
        c2 = CoeurAction(sujet=voiture, action=Action(name="ecraser"), cod=chien)
        c3 = CoeurDescriptifVerbal(sujet=voiture, action=rouler)
        c4 = CoeurDescriptif(sujet=marcel, carac=CaracChiffree(name="colere", value=8))
        c5 = CoeurAction(sujet=[marcel,chien], action=Action(name="aller voir"), cod=veterinaire)
        c6 = CoeurAction(sujet=veterinaire, action=Action(name="soigner"), cod=chien)
        c6.ajouterMoment(date=datetime(2021,1,21), importance=200)
        c7 = CoeurAction(sujet=marcel, action=Action(name="casser"), cod=voiture)
        c7.ajouterMoment(date=datetime(2021,1,23), importance=200)
        c8 = CoeurAction(sujet=chien, action=Action(name="se défouler"))
        
        #c2.ajouterMoment(moment=c1, importance=50)
        c1.ajouterLien(Lien(coeur=c2, typeLien=SUITE, importance=5))
        c1.ajouterLien(Lien(coeur=c8, typeLien=OBJECTIF, importance=20))
        c2.ajouterLien(Lien(coeur=c3, typeLien=CAUSE, importance=1))
        c2.ajouterLien(Lien(coeur=c4, typeLien=CONSEQUENCE, importance=1))
        c2.ajouterLien(Lien(coeur=c5, typeLien=CONSEQUENCE, importance=3))
        c5.ajouterLien(Lien(coeur=c6, typeLien=SUITE, importance=1.5))
        c4.ajouterLien(Lien(coeur=c7, typeLien=CONSEQUENCE, importance=1.5))
    
        
        hist = Histoire(head=c1, titre="Marcel promene son chien")
        hist.ton = "triste"
        marcel.creerHistoire(hist)
        
    
        ajd = datetime(2021,1,22)
        
        print("\n\n\n")
        print(dialogue(jackie, marcel, date=ajd, useTranslation=False, useCorrection=False))
        
        if graph:
            persos = [marcel, jackie]
            for p in persos:
                dot = p.histoires[0].getGraph()
                dot.render("histoire_1_" + p.toText(), view=True, format="png")
                
        print("\n\n\n")
        print(dialogue(jackie, kevin, date=ajd, useTranslation=False, useCorrection=False))
        
        if graph:
            persos = [marcel, jackie, kevin]
            for p in persos:
                dot = p.histoires[0].getGraph()
                dot.render("histoire_2_" + p.toText(), view=True, format="png")
                
        print("\n\n\n")
        print(dialogue(kevin, marcel, date=ajd, useTranslation=False, useCorrection=False))
        
        if graph:
            persos = [marcel, jackie, kevin]
            for p in persos:
                dot = p.histoires[0].getGraph()
                dot.render("histoire_3_" + p.toText(), view=True, format="png")
        
        
        
