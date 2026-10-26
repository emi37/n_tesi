"""
Cosa fa il tool:
    1 - riceve la query SQL creata dal primo agente;
    2 - blocca per sicurezza qualsiasi query che non sia una SELECT  (come ad es. DROP, UPDATE, DELETE);
    3 - si connette al file SQLite in locale ed esegue la query restituendo i risultati.
"""

from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import sqlite3
    # qui definisco il modulo che chinque voglia usare questo tool deve riempire.
    # il modulo è formato da un solo field/campo, chiamato "query"
class SchemaInputQuery(BaseModel): # Modulo A
        query: str = Field(description="La query sql generata da eseguire sul database SQLite in locale.")

class ToolEseguiQuery(BaseTool): # Modulo B   # modulo con 3 field per 
    # name, query, description ecc. sono etichette
    name: str = "tool_esegui_query"
    description: str = "Esegue la query sql sul database locale. Accetta SOLO query che iniziano con SELECT."
    args_schema: Type[BaseModel] = SchemaInputQuery # serve a collegare il tool al modulo A

    def _run(self, query: str) -> str: # funzione che prende in input la stringa della query e restituisce i risultati trovati nel db
    #1 - controllo sul tipo di comando, accetta solo select per evitare di dare troppi permessi
       
        query_pulita = query.strip().upper() 
        #strip toglie spazi vuoti a inizio o alla fine
        #upper invece mette in maiuscolo la query
        
        if not query_pulita.startswith("SELECT"): #se la query non inizia con SELECT, allora torniamo errore
            return "Errore, puoi eseguire SOLO comandi di tipo SELECT per il momento."

        # 2 - connessione al db e esecuzione della query
        try:
            #connessione al db, sqlite3 è la libreria che apre database_tesi.db e prende i dati da li
            con = sqlite3.connect("db/database_tesi.db") # è la connessione a DB
            cur = con.cursor()  
            
            cur.execute(query) # il cursore prende la query dell'agente e la esegue nel DB
            risultati = cur.fetchall() # fetchall è il metodo che prende tutti i risultati della query eseguita dal cursore, e li mette nella variabile risultati
            con.close() # chiudo la connessione al db
            
            if not risultati: #se la lista dei risultati è vuota, allora semplicemente non ci sono risultati per quella query
                return "La query è corretta, ma non ci sono risultati nel db."
                
            return str(risultati) # else(implicito) trasformo la lista risultati in testo e lo do all'agente 
            
        except Exception as e: # se l'agente sbaglia qualcosa, l'errore viene salvato in e
            # ritorno " e " all'agente, così che può correggere la query
            return f"Errore sql:  {str(e)}"