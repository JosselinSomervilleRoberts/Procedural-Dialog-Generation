# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 19:01:59 2020

@author: josse
"""


CORRECTION_VERBES = 100

import csv

import sqlite3
conn = sqlite3.connect('mots.db')

c = conn.cursor()

# Create table
c.execute('''CREATE TABLE liste_mots (
    id         INTEGER PRIMARY KEY ASC AUTOINCREMENT,
    lemme      TEXT,
    type       INT,
    genre      INT,
    nombre     INT,
    freq_livre REAL,
    freq_film  REAL
);''')

import io

# Ouvre la BDD de reference
tsv_file = io.open("Lexique383.tsv", mode="r", encoding="utf-8")
read_tsv = csv.reader(tsv_file, delimiter="\t")


dictio = {}

for row in read_tsv:
    lemme = row[2].lower()
    typ = row[3]
    nb_typ = -1
    if typ == "VER":
        nb_typ = 0
    elif typ == "AUX":
        nb_typ = 1
    elif typ == "NOM":
        nb_typ = 2
    elif typ == "ADJ":
        nb_typ = 3
    elif typ == "ADV":
        nb_typ = 4
    elif typ == "PRE":
        nb_typ = 5
    elif typ == "ONO":
        nb_typ = 6
        
    if nb_typ == -1:
        print("TYPE NON VALIDE : ", row)
        
    try:
        freq_l = float(row[7])
        freq_f = float(row[6])
        
        if nb_typ == 0:
            freq_l /= CORRECTION_VERBES
            freq_f /= CORRECTION_VERBES
        
        genre = 0
        if str(row[4]) == "m":
            genre = 1
        elif str(row[4]) == "m":
            genre = 2
            
        nombre = 0
        if str(row[4]) == "s":
            nombre = 1
        elif str(row[4]) == "p":
            nombre = 2
        
        if not(lemme in dictio):
            dictio[lemme] = [nb_typ, freq_l, freq_f, genre, nombre]
        else:
            if nb_typ == 0 and row[0].lower() == lemme:
                dictio[lemme] = [nb_typ, dictio[lemme][1] + freq_l, dictio[lemme][2] + freq_f, genre, nombre]
            elif nb_typ == 0:
                dictio[lemme] = [nb_typ, dictio[lemme][1] + freq_l, dictio[lemme][2] + freq_f, dictio[lemme][3], dictio[lemme][4]]

    except:
        print("NOT FLOAT : ", row)
        
 
query_insert = '''INSERT INTO liste_mots(lemme, type, freq_livre, freq_film, genre, nombre) VALUES(?,?,?,?,?,?);'''
for lemme in dictio:
    print(lemme)
    values = dictio[lemme]
    data_tuple = (lemme, values[0], values[1], values[2], values[3], values[4])
    c.execute(query_insert, data_tuple)
    conn.commit()
    
  