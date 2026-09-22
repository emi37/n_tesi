from crewai.tools import BaseTool
from pathlib import Path


class FileReaderTool(BaseTool):
    name: str = "file_reader"
    description: str = (
        "Legge il contenuto del file esempio.txt presente nella cartella data. "
        "Non richiede parametri."
    )

    def _run(self, query: str = "") -> str:
        percorso = Path(__file__).parent.parent / "data" / "programma.java"

        with open(percorso, "r", encoding="utf-8") as file:
            return file.read()