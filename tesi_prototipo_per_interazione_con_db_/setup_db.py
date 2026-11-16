# NOTA: cosa fa questo file? - crea la struttura del database(ovvero database_tesi.db) + crea il file schema.txt e lo aggiorna ogni qual volta che viene modificata la struttura del db
# schema.txt viene letto dall'agente 1 

# ho scaricato l'estensione di visual studio code, SQLite Viewer per poter leggere il file binario database_tesi.db

import sqlite3
import os
# l'idea è che si crea prima:
# la cartella, 
# poi il file,
# poi la griglia
# e infine si inseriscono le righe/record/i dati effettivi di ogni persona.
 
# Come nei db normali, il ragionamento è uguale

#  ----------------------  1)  ----------------------

# crea la cartella 'db' se non esiste già; all'interno mettiamo i file del db
os.makedirs("db", exist_ok=True)

# si connette e crea (automaticamente) il file del database sqLite
con_db= sqlite3.connect("db/database_tesi.db")
cursore_db = con_db.cursor()

cursore_db.execute("DROP TABLE IF EXISTS utenti")


# COLLATE NOCASE permette di non tener conto se una lettera è maiuscola o minuscola nei confronti 
cursore_db.execute('''
    CREATE TABLE utenti (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL COLLATE NOCASE,
        eta INTEGER NOT NULL,
        lavoro TEXT COLLATE NOCASE
    )
''')

utenti = [
    ("Emidio", 24, "Informatico"),
    ("Alice", 18, "Designer"),
    ("Alice R.", 29, "Ingegnere"),   
    ("Giuseppe", 61, "Poliziotto"),
    ("Andrea", 43, "Impiegato"),
    ("Carmine", 54, "Cameriere"),
    ("Dalila", 19, "Tuttofare"),
    ("Davide", 50, "Biotecnologo"),
    ("Filippo", 71, "Dottore"),
    ("Alessandro", 52, "Operaio") ,
    ("Francesca", 31, "Grafica"),  
    ("Marco", 40, "Meccanico"),      
    ("Sara", 18, "Nutrizionista"),
    ("Edoardo", 30, "R6 Pro player"),
    ("Dorian", 35, "Regista")
      
]
cursore_db.executemany("INSERT INTO utenti (nome, eta, lavoro) VALUES (?, ?, ?)", utenti)
cursore_db.execute("DROP TABLE IF EXISTS allarmi")
cursore_db.execute("DROP TABLE IF EXISTS accessi")
cursore_db.execute("DROP TABLE IF EXISTS dispositivi")

cursore_db.execute('''
    CREATE TABLE dispositivi (
        dispositivo_id INTEGER PRIMARY KEY AUTOINCREMENT,
        proprietario_id INTEGER NOT NULL REFERENCES utenti(id),
        tipo TEXT NOT NULL COLLATE NOCASE,
        aggiornato INTEGER NOT NULL
    )
''')

cursore_db.execute('''
    CREATE TABLE accessi (
        accesso_id INTEGER PRIMARY KEY AUTOINCREMENT,
        utente_id INTEGER NOT NULL REFERENCES utenti(id),
        dispositivo_id INTEGER NOT NULL REFERENCES dispositivi(dispositivo_id),
        data_ora TEXT NOT NULL,
        riuscito INTEGER NOT NULL,
        citta TEXT NOT NULL COLLATE NOCASE
    )
''')

cursore_db.execute('''
    CREATE TABLE allarmi (
        allarme_id INTEGER PRIMARY KEY AUTOINCREMENT,
        accesso_id INTEGER NOT NULL REFERENCES accessi(accesso_id),
        gravita TEXT NOT NULL COLLATE NOCASE,
        gestito_da INTEGER REFERENCES utenti(id)
    )
''')

dispositivi = [
    (1, "Laptop", 1),
    (1, "Smartphone", 1),
    (3, "Laptop", 1),
    (4, "PC fisso", 0),
    (5, "PC fisso", 0),
    (11, "Tablet", 1),
    (12, "Smartphone", 0),
    (14, "PC fisso", 1),
    (15, "Laptop", 0),
    (13, "Smartphone", 1)
]
cursore_db.executemany("INSERT INTO dispositivi (proprietario_id, tipo, aggiornato) VALUES (?, ?, ?)", dispositivi)

accessi = [
    (1, 1, "2026-11-10 09:00", 1, "Monticelli"),
    (1, 2, "2026-11-10 13:30", 1, "Monticelli"),
    (3, 3, "2026-11-10 08:45", 1, "Monticelli"),
    (4, 4, "2026-11-10 10:15", 1, "Teramo"),
    (12, 7, "2026-11-10 22:10", 0, "L'Aquila"),
    (12, 7, "2026-11-10 22:11", 0, "L'Aquila"),
    (12, 7, "2026-11-11 23:40", 0, "L'Aquila"),
    (12, 7, "2026-11-12 02:05", 0, "L'Aquila"),
    (12, 7, "2026-11-12 02:07", 1, "L'Aquila"),
    (14, 8, "2026-11-11 21:00", 1, "Val Vomano"),
    (14, 1, "2026-11-12 03:15", 1, "Teramo"),
    (15, 9, "2026-11-12 09:00", 1, "L'Aquila"),
    (15, 9, "2026-11-12 18:30", 1, "Francavilla"),
    (5, 5, "2026-11-13 08:30", 0, "San Nicolò"),
    (5, 5, "2026-11-13 08:32", 1, "San Nicolò"),
    (11, 6, "2026-11-13 11:00", 1, "Francavilla"),
    (13, 10, "2026-11-13 12:00", 1, "Teramo"),
    (2, 6, "2026-11-14 16:20", 0, "Monticelli"),
    (8, 4, "2026-11-14 01:30", 0, "L'Aquila"),
    (8, 4, "2026-11-14 01:31", 0, "L'Aquila"),
    (10, 2, "2026-11-14 20:00", 0, "San Nicolò"),
    (1, 1, "2026-11-15 09:10", 1, "Monticelli"),
    (14, 8, "2026-10-01 11:30", 1, "Val Vomano"),
    (13, 10, "2026-10-02 09:10", 1, "Teramo"),
    (15, 9, "2026-10-03 10:05", 1, "Francavilla"),
    (4, 4, "2026-10-03 13:15", 1, "Teramo"),
    (3, 3, "2026-10-03 20:15", 1, "Monticelli"),
    (1, 1, "2026-10-04 15:20", 1, "Monticelli"),
    (14, 8, "2026-10-04 20:45", 1, "Val Vomano"),
    (4, 4, "2026-10-05 09:05", 1, "Teramo"),
    (15, 9, "2026-10-05 09:45", 1, "Francavilla"),
    (5, 5, "2026-10-05 12:00", 1, "San Nicolò"),
    (14, 8, "2026-10-05 22:20", 1, "Val Vomano"),
    (11, 6, "2026-10-07 08:50", 1, "Francavilla"),
    (14, 8, "2026-10-07 11:50", 1, "Val Vomano"),
    (5, 5, "2026-10-07 23:15", 1, "San Nicolò"),
    (12, 7, "2026-10-08 07:00", 1, "L'Aquila"),
    (14, 8, "2026-10-10 15:10", 1, "Val Vomano"),
    (4, 4, "2026-10-10 22:50", 1, "Teramo"),
    (14, 8, "2026-10-11 07:40", 1, "Val Vomano"),
    (11, 6, "2026-10-11 08:00", 1, "Francavilla"),
    (12, 7, "2026-10-11 18:40", 1, "L'Aquila"),
    (5, 5, "2026-10-11 20:10", 1, "San Nicolò"),
    (15, 9, "2026-10-11 23:00", 1, "Francavilla"),
    (5, 5, "2026-10-12 07:30", 1, "San Nicolò"),
    (12, 7, "2026-10-12 09:10", 1, "L'Aquila"),
    (14, 8, "2026-10-12 11:00", 1, "Val Vomano"),
    (4, 4, "2026-10-12 19:15", 1, "Teramo"),
    (11, 6, "2026-10-12 19:45", 1, "Francavilla"),
    (11, 6, "2026-10-13 09:40", 1, "Francavilla"),
    (15, 9, "2026-10-13 21:45", 1, "Francavilla"),
    (12, 7, "2026-10-14 14:15", 1, "L'Aquila"),
    (15, 9, "2026-10-14 23:50", 1, "Francavilla"),
    (11, 6, "2026-10-15 12:15", 1, "Francavilla"),
    (14, 8, "2026-10-16 15:30", 1, "Val Vomano"),
    (4, 4, "2026-10-16 17:10", 1, "Teramo"),
    (5, 5, "2026-10-16 22:50", 1, "San Nicolò"),
    (12, 7, "2026-10-17 08:40", 1, "L'Aquila"),
    (14, 8, "2026-10-17 14:40", 1, "Val Vomano"),
    (13, 10, "2026-10-18 22:00", 1, "Teramo"),
    (15, 9, "2026-10-19 19:40", 1, "Francavilla"),
    (12, 7, "2026-10-19 20:45", 1, "L'Aquila"),
    (15, 9, "2026-10-20 09:15", 1, "Francavilla"),
    (11, 6, "2026-10-20 15:30", 1, "Francavilla"),
    (5, 5, "2026-10-20 19:15", 1, "San Nicolò"),
    (15, 9, "2026-10-21 07:00", 1, "Francavilla"),
    (11, 6, "2026-10-21 08:15", 1, "Francavilla"),
    (14, 8, "2026-10-21 15:40", 1, "Val Vomano"),
    (13, 10, "2026-10-21 22:05", 1, "Teramo"),
    (14, 8, "2026-10-22 11:10", 1, "Val Vomano"),
    (5, 5, "2026-10-22 14:10", 1, "San Nicolò"),
    (15, 9, "2026-10-22 20:00", 1, "Francavilla"),
    (5, 5, "2026-10-23 09:45", 1, "San Nicolò"),
    (15, 9, "2026-10-23 14:20", 1, "Francavilla"),
    (11, 6, "2026-10-23 19:10", 1, "Francavilla"),
    (14, 8, "2026-10-24 11:05", 1, "Val Vomano"),
    (13, 10, "2026-10-25 23:15", 1, "Teramo"),
    (12, 7, "2026-10-26 08:30", 1, "L'Aquila"),
    (11, 6, "2026-10-26 16:20", 1, "Francavilla"),
    (14, 8, "2026-10-26 19:05", 1, "Val Vomano"),
    (12, 7, "2026-10-27 22:05", 1, "L'Aquila"),
    (5, 5, "2026-10-28 20:45", 1, "San Nicolò"),
    (11, 6, "2026-10-28 23:50", 1, "Francavilla"),
    (14, 8, "2026-10-31 12:00", 1, "Val Vomano"),
    (12, 7, "2026-10-31 18:00", 1, "L'Aquila"),
    (4, 4, "2026-10-31 20:20", 1, "Teramo"),
    (13, 10, "2026-11-01 17:50", 1, "Teramo"),
    (4, 4, "2026-11-01 18:45", 1, "Teramo"),
    (14, 8, "2026-11-01 21:10", 1, "Val Vomano"),
    (11, 6, "2026-11-01 22:05", 1, "Francavilla"),
    (5, 5, "2026-11-02 08:20", 1, "San Nicolò"),
    (11, 6, "2026-11-02 08:50", 1, "Francavilla"),
    (13, 10, "2026-11-02 10:10", 1, "Teramo"),
    (12, 7, "2026-11-02 11:05", 1, "L'Aquila"),
    (12, 7, "2026-11-03 10:00", 1, "L'Aquila"),
    (15, 9, "2026-11-03 19:40", 1, "Francavilla"),
    (11, 6, "2026-11-04 17:50", 1, "Francavilla"),
    (14, 8, "2026-11-05 09:05", 1, "Val Vomano"),
    (12, 7, "2026-11-05 21:10", 1, "L'Aquila"),
    (15, 9, "2026-11-05 21:15", 1, "Francavilla"),
    (15, 9, "2026-11-06 19:40", 1, "Francavilla"),
    (14, 8, "2026-11-07 16:10", 1, "Val Vomano"),
    (13, 10, "2026-11-08 12:30", 1, "Teramo"),
    (12, 7, "2026-11-08 17:40", 1, "L'Aquila")
]
cursore_db.executemany("INSERT INTO accessi (utente_id, dispositivo_id, data_ora, riuscito, citta) VALUES (?, ?, ?, ?, ?)", accessi)

allarmi = [
    (8, "media", 1),
    (9, "alta", 1),
    (11, "alta", None),
    (13, "media", 3),
    (18, "bassa", None),
    (20, "alta", 3),
    (21, "media", None)
]
cursore_db.executemany("INSERT INTO allarmi (accesso_id, gravita, gestito_da) VALUES (?, ?, ?)", allarmi)
con_db.commit()
con_db.close() # chiude la connessione al db 


# crea un file di testo schema.txt che verrà preso dal primo agente
# questo perceh gli agenti non possono accedere a file binari, come database_tesi.db
# ma possono accedere solo a file di testo

# ogni volta che vado a modificare la struttura del db, il file schema.txt verrà aggiornato automaticamente 


# --------------------- fino a qui ho creato il db locale con tutte le informazioni per fare le prove, ora devo creare il file schema.txt
# che verrà letto dall'agente ------------------------------------------------



#  ----------------------  2)  ----------------------
# creo il file di testo schema.txt per l'agente(quando cambio la struttura del db, schema.txt si aggiorna in automatico)
# 
#  
# ristabilisco la connessione con il db e creo il cursore che andrà a scorrere la struttura 
con_db = sqlite3.connect("db/database_tesi.db")
cursore_db = con_db.cursor()

cursore_db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence';")
# la query sopra 
tabelle_nel_db = cursore_db.fetchall() # prende i nomi di tutte le tabelle che trova sul db e le mette nella list  tabelle_nel_db

schema_righe = ["struttura del db per l' agente: \n"]

# faccio 2 for, uno che scorre le tabelle del db e uno annidato che scorre gli attributi di ogni tabella  
for tab in tabelle_nel_db:
    nome_tabella = tab[0]
    schema_righe.append(f"Tabella principale: {nome_tabella}")
    schema_righe.append("Colonne della tabella: ")
    
    cursore_db.execute(f"PRAGMA table_info({nome_tabella});") #è il metodo standard diciamo per leggere le colonne 
    colonne = cursore_db.fetchall() 
    
    for col in colonne: # scorro tutte le colonne/attributi dalla tabella in cui mi trovo
        # per ogni colonna aggiungo una riga allo schema: col[1] è il nome della colonna, col[2] è il tipo
        schema_righe.append(f"- attributo: '{col[1]}' (tipo: {col[2]})")
        #per la colonna età nello schema sarebbe:   - attributo: 'eta' (tipo: INTEGER)

    cursore_db.execute(f"PRAGMA foreign_key_list({nome_tabella});")
    for fk in cursore_db.fetchall():
        schema_righe.append(f"- collegamento: '{fk[3]}' si collega a '{fk[4]}' della tabella {fk[2]}")
    schema_righe.append("") # questo serve a mettere degli apici "" , così da dividere le tabelle nel file txt e capire quando finisce una tabella e ne inizia un'altra.

con_db.close()

with open("db/schema.txt", "w", encoding="utf-8") as f: # f(file) è il nome accorciato di schema.txt
    f.write("\n".join(schema_righe))

print("creata la cartella 'db' con dentro 'database_tesi.db' e 'schema.txt'.")

# il for delle colonne/attributi è particolare perchè sqlite descrive di default le caratteristiche degli attributi come un insieme di "indici" 
# in questo modo: 

# l'attributo età(della tabella persone)viene descritto di default così:
# col[0]: numero di servizio (che non ci interessa)

# col[1]: il nome della colonna (età)

# col[2]: il tipo di dato (INTEGER)

# col[3]: altra informazione che non ci interessa

# col[4]: il valore di default(se esiste)

# col[5]: se è una chiave primaria o no
#----------------------------------------------------------------#

# le uniche informazioni che voglio far leggere agli agenti, e quindi mettere nel foglio schema.txt, sono 
# quelle di indice 1 e 2, cioè nome e tipo; per questo all'interno del ciclo scrivo {col[1]} e {col[2]} ; 


# ----------------------------------------------
# f è il format, cioè toglie le {} 