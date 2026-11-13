""" Cosa fa:
    1 - entrambi gli agenti chiamano il tool passandogli la richiesta dell'utente (Groq non accetta tool senza nessun parametro);
    2 - trova il file db/schema.txt partendo dalla posizione di questo file (così funziona da qualsiasi cartella venga lanciato il crew);
    3 - legge il file e restituisce all'agente il testo dello schema, che l'agente usa per scrivere (agente 1) o controllare (agente 2) la query.
"""

from crewai.tools import BaseTool
from pathlib import Path # è una libreria di python per gestire i percorsi dei file

# __file__ è il percorso di questo file                                 --> .../tools/tool_leggi_schema.py
# .resolve() lo "risolve"/lo rende completo                             --> C:\Users\emidi\n_tesi\tesi_prototipo_per_interazione_con_db_\tools\tool_leggi_schema.py 
# .parent è la cartella che contiene tool_leggi_schema(è tipo il cd..)  --> .../tools
# .parent.parent è la cartella del progetto                             --> .../tesi_prototipo_per_interazione_con_db_
# infine con / aggiungo le sottocartelle che mi servono                 --> .../db/schema.txt
perc_schema = Path(__file__).resolve().parent.parent / "db" / "schema.txt"

class ToolLeggiSchema(BaseTool):
#(name e description sono le etichette che l'agente 1 legge per capire quando usare il tool)
    name: str = "tool_leggi_schema" 
    description: str=(
        "Legge lo schema del database SQLite locale(tabelle, colonne e tutto il resto) e lo restituisce come testo. "
        "Usalo PRIMA di scrivere o controllare una query, per sapere quali tabelle e colonne esistono davvero. "
        "Come argomento passa la richiesta dell'utente."
    )
        # niente modulo A (args_schema): CrewAI lo crea da solo leggendo i parametri di _run, qui c'è solo "richiesta"
   # NB: il parametro serve perché Groq rifiuta i tool senza parametri (errore "'required' present but 'properties' is missing")

    def _run(self, richiesta: str) -> str: # riceve la richiesta dell'utente e restituisce il testo dello schema
        # metto la richiesta in testa, così l'agente ha davanti sia la domanda che lo schema; utf-8 serve per le lettere accentate
        return f"Schema del database per la richiesta '{richiesta}':\n" + perc_schema.read_text(encoding="utf-8")
