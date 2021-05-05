# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 10:30:39 2021

@author: olivi
"""
from tkinter import * 
import random
from psclib.diversifieur import correct, cong, diversifier, get_syn, buildSynonyms
from psclib.action import Action
from psclib.objet import Objet, Personnage
from psclib.caracteristique import Caracteristique, Type, CaracChiffree
from psclib.histoire import Histoire, ajouterPonctuation, demanderLien, nePasSavoirLien, SUITE, CAUSE, CONSEQUENCE
from psclib.coeuraction import CoeurAction
from psclib.coeurdescriptif import CoeurDescriptif
from psclib.lien import Lien
from psclib.dialogue import dialogue, pickStory, raconter, quiparle, transition, fin, testContinuer, intersection, switcheroo, intro, connait
import numpy as np
from datetime import datetime
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



"""Ce fichier est un afficheur de dialogues pour deux personnages. Le dialogue en entrée est défini par la chaine de caractères ci-dessous"""











a = True




def affichageGraphique(L = "Kerma Boulanger : Salut mon reuf !\nFisker Forgeron : Bonsoir Palézo !!!!!\nKerma Boulanger : Cuz everytime we touch, I get this feeling, & Everytime we kiss, I swear I could fly, Can't you feel my heart beat fast, I want this to last, Need you by my side.\nFisker Forgeron : A plus dans le bus"):
    global a
    
    L_P = ["kerma","fisker"] #Nom de personnages prédéfinis 


    
    UNIFORME = 0
    GAUCHE,DROITE,NEXT = 0,1,2
    def toAction(lib):
        return Action(lib=lib,expressions=[[1,lib]])
    
    
    
    class PersoG :
        def __init__(self,x,y,img,imgf,canvas,cote_bulle=DROITE,preset=None):
            self.x = x
            self.y = y
            self.ox = x
            self.oy = y
            self.marche = False
            self.canvas = canvas
            self.cote_bulle = cote_bulle
            self.dialogue = []
            if preset is None :
                self.perso = Personnage({"prenom":random.choice(["Alice","Léon","Pierre","Carole","Michel","Gonzague","Aline","Joachim","Olivier","Josselin","Tanguy","Paul","Arnaud"]),"nom":random.choice(["Dupont","Dubois","Dupuis","Von Zimmeln","Labaye","Tourenq","Einstein","Holmes","Proust","Tolstoi"]),"caracs": [CaracChiffree(name="bavard", value=7)] })
            else :
                self.perso = Personnage(name=preset)
            #canvas.create_image(200, 460, image=PhotoImage(file='arbre.png'))
            self.img = canvas.create_image(x, y, image=img)
            self.imgf = canvas.create_image(x, y, image=imgf)
            canvas.itemconfigure(self.imgf,state=HIDDEN)
            if cote_bulle == DROITE :
                self.bulle = canvas.create_rectangle(x, y-200, x+200,y-50 , fill='white')
                self.texte = canvas.create_text ( x+5 , y-195, text = "",width=195,anchor=NW )
            else :
                self.bulle = canvas.create_rectangle(x-200, y-200, x,y-50 , fill='white')
                self.texte = canvas.create_text ( x-195 , y-195, text = "",width=199,anchor=NW )
            
        def nouvel_objectif(self,x,y):
            self.ox = x
            self.oy = y
            self.marche = True
            canvas.itemconfigure(self.bulle,state=HIDDEN)
            canvas.itemconfigure(self.texte,state=HIDDEN)
        def avancer(self):
            if (not self.marche):
                return False
            dx = max( min(self.ox-self.x,2) , -2)
            if dx>0:
                canvas.itemconfigure(self.img,state=NORMAL)
                canvas.itemconfigure(self.imgf,state=HIDDEN)
            elif dx<0:
                canvas.itemconfigure(self.img,state=HIDDEN)
                canvas.itemconfigure(self.imgf,state=NORMAL)
            dy = max( min(self.oy-self.y,2) , -2)
            self.x += dx
            self.y += dy
            canvas.move(self.img,dx,dy)
            canvas.move(self.imgf,dx,dy)
            canvas.move(self.bulle,dx,dy)
            canvas.move(self.texte,dx,dy)
            self.marche = not (self.x == self.ox and self.y == self.oy)
            return self.marche
        def parler(self,texte=NEXT):
            if texte == NEXT :
                if len(self.dialogue)>0 :
                    self.parler(self.dialogue.pop(0))
                    return True
                else :
                    self.parler("")
                    return False
            canvas.itemconfigure(self.bulle,state=NORMAL if texte!="" else HIDDEN)
    
            canvas.itemconfigure(self.texte,state=NORMAL if texte!="" else HIDDEN)
            canvas.itemconfig(self.texte, text=texte)
            if self.cote_bulle == GAUCHE:
                canvas.itemconfigure(self.img,state=NORMAL)
                canvas.itemconfigure(self.imgf,state=HIDDEN)
            if self.cote_bulle == DROITE:
                canvas.itemconfigure(self.img,state=HIDDEN)
                canvas.itemconfigure(self.imgf,state=NORMAL)
            return True
        def setCoteBulle(self,cote):
            if cote == self.cote_bulle:
                return
            dx = 200 if cote == DROITE else -200
            canvas.move(self.bulle,dx,0)
            canvas.move(self.texte,dx,0)
            self.cote_bulle = cote
        def dialoguer(self,perso2,L=None):
            L = dialogue(self.perso, perso2.perso,date=datetime(2021,2,10), useTranslation=False, useCorrection=False) if L is None else L
            print(L)
            print("\n")
            L=L.split("\n")
            L = [elt.split(" : ") for elt in L]
            L = [elt for elt in L if len(elt)==2]
            
            for i in range(len(L)):
                if len(L[i][1])>380 :
                    p,s = L[i][0],L[i][1]
                    L[i][1]= s[:370]+" ..."
                    L.insert(i+1,[p,"... "+s[370:]])
            self.dialogue = []
            perso2.dialogue =  []
            if len(L)==0:
                return
            nom_loc = L[0][0]
            for ligne in L :
                if ligne[0]==nom_loc:
                    self.dialogue.append(ligne[1])
                    perso2.dialogue.append("")
                else:
                    perso2.dialogue.append(ligne[1])
                    self.dialogue.append("")
    
    
    root = Tk()
    root.title("PSC - Génération procédurale de dialogues")
    canvas = Canvas(root, width=750, height=500)
    canvas.pack()
    
    
    #arbre = PhotoImage(file='arbre.png')
    img_fond = PhotoImage(file='cafe.png')
    canvas.create_image(750, 450, image=img_fond)
    img_table = PhotoImage(file='table.png')
    img_table2 = PhotoImage(file='table2.png')
    img_table3 = PhotoImage(file='table3.png')
    #canvas.create_image(650, 320, image=arbre)
    #canvas.create_image(50, 330, image=arbre)
    for x in [375,1125]:
        for y in [350,600,850]:
            canvas.create_image(x, y, image=random.choice([img_table,img_table2,img_table3]))
    
    #canvas.create_image(200, 460, image=arbre)
    #canvas.create_image(600, 500, image=arbre)
    images = [ [PhotoImage(file='p'+str(i+1)+'.png'),PhotoImage(file='p'+str(i+1)+'f.png')] for i in range(2)]
    persos = [PersoG(750,450,images[id][0],images[id][1],canvas,GAUCHE,preset=L_P[id]) for id in range(len(images))]
    '''
    img1 = PhotoImage(file='p1.png')
    perso1 = PersoG(40,400,img1,canvas,GAUCHE)
    img2 = PhotoImage(file='p2.png')
    
    perso2 = PersoG(260,400,img2,canvas,DROITE)
    perso1.parler("What the fuck did you just fucking say about me, you little bitch? I'll have you know I graduated top of my class in the Navy Seals, and I've been involved in numerous secret raids on Al-Quaeda, and I have over 300 confirmed kills.")
    perso2.parler("Souvent, pour s'amuser, les hommes d'équipage prennent des albatros, vastes oiseaux des mers, qui suivent, indolents compagnons de voyage, les navires glissants sur les gouffres amers.")
    '''
    
    #tables = [ [[x-75,y-10],[x+75,y-10]] for x in [375,1125] for y in [350,600,850] ]
    tables = [ [[300,340],[450,340]]]
    table = random.choice(tables)
    
    '''
    perso1.nouvel_objectif(table[0][0], table[0][1])
    perso2.nouvel_objectif(table[1][0], table[1][1])
    persos = [perso1,perso2]
    '''
    couples_formes =  [[0 for i in range(len(persos))] for j in range(len(persos))]
    def melange(persos,tables):
        #random.shuffle(persos)
        n = len(persos)
        npersos= []
        L = set(range(n))
        while len(L)>0:
            a = L.pop()
            npersos.append(a)
            c=True
            while c ==True :
                b = random.choice(list(L))
                print(b)
                if couples_formes[a][b]==0 or random.random()<0.1:
                    couples_formes[a][b] = 1
                    couples_formes[b][a] = 1
                    L.remove(b)
                    npersos.append(b)
                    c = False
        for i in range(n//2):
            persos[npersos[2*i]].nouvel_objectif(tables[i][0][0], tables[i][0][1])
            persos[npersos[2*i]].setCoteBulle(GAUCHE)
            persos[npersos[2*i+1]].nouvel_objectif(tables[i][1][0], tables[i][1][1])
            persos[npersos[2*i+1]].setCoteBulle(DROITE)
        return npersos
            
    config = []
    a= True
    def modification(entraindeparler=False):
        wait = 0
        marche = False
        for p in persos :
            marche = p.avancer() or marche
        if not marche :
            wait = 20000
            discute = False
            for p in persos :
                discute= p.parler() or discute
            if not discute :
                pass
                '''
                config = melange(persos,tables)
                for i in range(len(persos)//2):
                    persos[config[2*i]].dialoguer(persos[config[2*i+1]])
                    
                    '''
    
        if wait==0:
            canvas.after(10+wait,modification)
        global a
        if a and not marche:
            root.bind("<Key>", modification) 
            a = False
    config = melange(persos,tables)
    
    for i in range(len(persos)):
        for j in range(len(persos)):
            if i<j :
                persos[i].perso.ajouterRelations({"ami":persos[j].perso})
                persos[j].perso.ajouterRelations({"ami":persos[i].perso})
    
    
    
    
    
    for i in range(len(persos)//2):
        persos[config[2*i]].dialoguer(persos[config[2*i+1]],L)
    canvas.after(10,modification)
    root.mainloop()
