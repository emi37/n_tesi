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

# crea una tabella persone con attibuti: 
cursore_db.execute('''
    CREATE TABLE IF NOT EXISTS persone (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        eta INTEGER NOT NULL,
        professione TEXT
    )
''')

# pulisco la tabella e inserisco dei dati a caso nella tabella 
cursore_db.execute("DELETE FROM persone")
utenti = [
    ("Alice Montauti", 24, "Designer"),
    ("Luciani Emidio", 24, "Informatico"),
    ("Davide Berardinelli", 28, "Dottore"),
    ("Marco Berardinelli", 22, "Meccanico"),
    ("Giuseppe Sturba", 30, "Poliziotto"),
    ("Filippo Rastelli", 26, "Informatico")
]
cursore_db.executemany("INSERT INTO persone (nome, eta, professione) VALUES (?, ?, ?)", utenti)
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

schema_righe = ["struttura del db per l' agente: \n"] # è una list
# (non posso usare add perchè non è un metodo della classe list)

# faccio 2 for, uno che scorre le tabelle del db e uno annidato che scorre gli attributi di ogni tabella  
for tab in tabelle_nel_db:
    nome_tabella = tab[0]
    schema_righe.append(f"Tabella principale: {nome_tabella}")
    schema_righe.append("Colonne della tabella: ")
    
    cursore_db.execute(f"PRAGMA table_info({nome_tabella});") #è il metodo standard diciamo per leggere le colonne 
    colonne = cursore_db.fetchall() 
    
    for col in colonne: # scorro tutte le colonne/attributi dalla tabella in cui mi trovo(tab)
        schema_righe.append(f"- attributo: '{col[1]}' (tipo: {col[2]})")
        # risultato stampato: -->  
        # - attributo: 'eta' (tipo: INTEGER)
    schema_righe.append("") # questo serve a dividere visivamnte le tabelle nel file di testo, cosi da capire quando finisce una tabella e ne inizia un'altra.

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