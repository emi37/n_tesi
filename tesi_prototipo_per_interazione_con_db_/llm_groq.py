""" Cosa fa:
    1 - crea il collegamento all'LLM (gpt-oss-120b su Groq) che usano gli agenti;
    2 - passa dal provider OpenAI "nativo" di CrewAI invece che da LiteLLM, perché con LiteLLM CrewAI manda a Groq
        un campo interno (cache_breakpoint) che Groq rifiuta, e il crew si blocca con BadRequestError;
    3 - gli agenti lo usano scrivendo nel loro file .jsonc:  "llm": {"python": "llm_groq.groq_llm"}
"""

import os # serve per leggere le variabili d'ambiente, cioè quelle del file .env
from crewai import LLM

  # Groq ha un indirizzo che "parla" come le API di OpenAI, quindi posso usare il provider openai di CrewAI puntandolo lì
groq_llm = LLM(
    model="openai/openai/gpt-oss-120b",        # il primo openai/ dice a CrewAI quale provider usare, il resto (openai/gpt-oss-120b) è il nome del modello su Groq
    base_url="https://api.groq.com/openai/v1", #  indirizzo di Groq compatibile con OpenAI
    api_key=os.environ["GROQ_API_KEY"],     # la chiave la prendo dal .env, così non finisce scritta nel codice (e quindi su github)
)
