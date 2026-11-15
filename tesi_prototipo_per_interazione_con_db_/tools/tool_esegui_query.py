""" Cosa fa:
    riceve la query creata dal primo agente e controllata dal secondo
    blocca ancora una volta per sicurezza qualsiasi query che non sia una SELECT
    si connette al file del db, esegue la query e restituisce i risultati
"""

from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from pathlib import Path
import sqlite3

# percorso completo del db, come per lo schema in tool_leggi_schema
perc_db = Path(__file__).resolve().parent.parent / "db" / "database_tesi.db" 
# viene così            C:\Users\emidi\...\db\database_tesi.db
  
    # classe formata da un solo field/campo, cioè la query
class SchemaInputQuery(BaseModel): # classe 1
        query: str = Field(description = "La query sql generata e controllata da eseguire sul database SQLite.")

class ToolEseguiQuery(BaseTool): #  classe 2
    # name, description, args_schema sono etichette fisse della classe BaseTool di crewai,che rende la classe ToolEseguiQuery visibile all'LLM, richiamabile, permette di ricevere chiamate e restituire risposte

# in pratica la classe ToolEseguiQuery diventa visibile all'LLM perché eredita la classe BaseTool
    name: str = "tool_esegui_query"
    description: str = "Esegue la query sql sul database. Accetta SOLO query di lettura(che iniziano con SELECT o WITH)."
    args_schema: Type[BaseModel] = SchemaInputQuery # serve a collegare il tool alla prima classe 

    def _run(self, query: str) -> str: # funzione che prende in input la stringa della query e restituisce i risultati trovati nel db       
        #l'agente 2 passa la query dentro un blocco ```sql ... ``` tolgo i segni del blocco, cosi ho la query pulita da passare all'agente 3
          # l'agente 3 inoltre acetta solo query che iniziano solo per SELECT o WITH 
        query = query.replace("```sql", "").replace("```", "").strip()

        query_pulita = query.upper()
        #strip toglie spazi vuoti a inizio e alla fine
        #upper invece mette in maiuscolo la query

        if not query_pulita.startswith(("SELECT", "WITH")): #se la query non inizia con SELECT, allora torniamo errore
            return "Errore, puoi eseguire SOLO comandi di tipo SELECT per il momento."

        # faccio il try per la connessione al db ed eseguo la query
        try:
              # per usare mode=ro ,sqlite vuole il percorso scritto come indirizzo (file:///C:/...), quindi as_uri() e uri=True
            con = sqlite3.connect(perc_db.as_uri() + "?mode=ro", uri=True) # è la connessione a DB, uri true e mode=ro permettono di aprire il db in sola lettura
            cur = con.cursor()                                              # quindi è una sicurezza in più per NON eseguire query di DML/DDL se gli agenti dovessero farle passare per errore

            cur.execute(query) # il cursore prende la query dell'agente e la esegue nel DB
            risultati = cur.fetchall() # fetchall è il metodo che prende tutti i risultati della query eseguita dal cursore, e li mette nella variabile risultati
            con.close() # chiudo la connessione al db

            if not risultati: #se la lista dei risultati è vuota, allora semplicemente non ci sono risultati per quella query
                return "La query è corretta, ma non ci sono risultati nel db."

            return str(risultati) # else(implicito) trasformo la lista risultati in testo e lo do all'agente

        except Exception as e: # se l'agente sbaglia qualcosa salvo l'errore in e
            return f"Errore sql:  {str(e)}"