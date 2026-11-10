""" Cosa fa:
    1 - l'agente 1 lo chiama e basta;
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
        "Usalo PRIMA di scrivere o controllare una query, per sapere quali tabelle e colonne esistono davvero."
    )
        # non serve il modulo A (args_schema): _run non ha parametri, quindi CrewAI crea da solo un modulo vuoto

    def _run(self) -> str: # funzione che non prende niente in input e restituisce il testo dello schema
        return perc_schema.read_text(encoding="utf-8") # leggo tutto il file e lo restituisco all'agente; utf-8 serve per le lettere accentate
