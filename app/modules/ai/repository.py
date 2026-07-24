import chromadb
from typing import List, Dict, Any


class AIRagRepository:
    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.chroma_client.get_or_create_collection(
            name="platforma_knowledge_base"
        )

    def adauga_document(self, doc_id: str, text: str, metadate: Dict[str, Any]) -> None:
        self.collection.add(documents=[text], metadatas=[metadate], ids=[doc_id])

    def cauta_documente_similare(
        self, interogare: str, numar_rezultate: int = 3
    ) -> List[Dict[str, Any]]:
        rezultate = self.collection.query(
            query_texts=[interogare], n_results=numar_rezultate
        )

        documente_potrivite = []
        if rezultate and rezultate.get("documents") and len(rezultate["documents"]) > 0:
            docs = rezultate["documents"][0]
            ids = rezultate["ids"][0]
            metas = (
                rezultate["metadatas"][0]
                if rezultate.get("metadatas")
                else [{} for _ in docs]
            )

            for i in range(len(docs)):
                documente_potrivite.append(
                    {"id": ids[i], "text": docs[i], "metadate": metas[i]}
                )
        return documente_potrivite

