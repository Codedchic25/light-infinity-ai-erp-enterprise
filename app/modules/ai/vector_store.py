import os
import chromadb
from pypdf import PdfReader


class PDFVectorPipeline:
    def __init__(
        self,
        chroma_path: str = "./data/chromadb",
        collection_name: str = "retete_fabrica",
    ):
        os.makedirs(chroma_path, exist_ok=True)
        self.chroma_client = chromadb.PersistentClient(path=chroma_path)
        self.collection_name = collection_name

    def proceseaza_si_indexeaza_pdf(self, pdf_path: str) -> str:
        """Extrage textul dintr-un PDF tehnic si il insereaza securizat in baza vectoriala ChromaDB."""
        if not os.path.exists(pdf_path):
            return f"âŒ Fisierul PDF la calea {pdf_path} nu a fost gasit."

        try:
            reader = PdfReader(pdf_path)
            text_complet = ""
            for idx, pagina in enumerate(reader.pages):
                text_pagina = pagina.extract_text()
                if text_pagina:
                    text_complet += text_pagina + "\n"

            if not text_complet.strip():
                return "âš ï¸ PDF-ul a fost citit, dar nu contine text procesabil."

            # Segmentare grosiera pe paragrafe pentru granulare semantica
            paragrafe = [
                p.strip() for p in text_complet.split("\n\n") if len(p.strip()) > 20
            ]

            # Curatare sau obtinere colectie
            try:
                self.chroma_client.delete_collection(name=self.collection_name)
            except Exception:
                pass

            collection = self.chroma_client.create_collection(name=self.collection_name)

            ids = [f"pdf_chunk_{i}" for i in range(len(paragrafe))]
            metadate = [
                {"sursa": os.path.basename(pdf_path)} for _ in range(len(paragrafe))
            ]

            collection.add(documents=paragrafe, metadatas=metadate, ids=ids)
            return f"âœ… Succes! S-au indexat {len(paragrafe)} segmente text din {os.path.basename(pdf_path)} in RAG."
        except Exception as e:
            return f"âŒ Eroare la procesarea pipeline-ului RAG: {str(e)}"

