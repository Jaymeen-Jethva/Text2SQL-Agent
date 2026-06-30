from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

from config import EMBEDDING_MODEL, DATABASE_DIR


class VectorStoreService:
    def __init__(self, index_name: str = "semantic_index"):
        self.index_name = index_name
        self.index_path = DATABASE_DIR / index_name
        
        self.embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        self.vector_store = None
        
    def save(self):
        if self.vector_store:
            self.vector_store.save_local(str(self.index_path))
            
    def load(self) -> bool:
        if self.index_path.exists():
            self.vector_store = FAISS.load_local(
                str(self.index_path), 
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            return True
        return False
        
    def update_incremental(self, documents: list[Document]):
        if self.vector_store is None:
            if not self.load():
                self.vector_store = FAISS.from_documents(documents, self.embeddings)
            else:
                self.vector_store.add_documents(documents)
        else:
            self.vector_store.add_documents(documents)
        self.save()
            
    def similarity_search(self, query: str, k: int = 5, filter_dict: dict = None) -> list[Document]:
        if self.vector_store is None:
            if not self.load():
                return []
            
        return self.vector_store.similarity_search(query, k=k, filter=filter_dict)
