import chromadb
from chromadb.config import Settings
from typing import List
import os

class VectorStore:
    def __init__(self):
        self.client = chromadb.Client(Settings(
            persist_directory="./data/vector_store",
            anonymized_telemetry=False
        ))
        self.collection = self.client.get_or_create_collection(
            name="tax_documents",
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_document(self, text: str, metadata: dict = None):
        """Add a document to the vector store."""
        if metadata is None:
            metadata = {}
        
        # Generate a unique ID for the document
        doc_id = f"doc_{len(self.collection.get()['ids'])}"
        
        self.collection.add(
            documents=[text],
            metadatas=[metadata],
            ids=[doc_id]
        )
    
    def search(self, query: str, n_results: int = 3) -> List[str]:
        """Search for relevant documents."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results['documents'][0]
    
    def delete_document(self, doc_id: str):
        """Delete a document from the vector store."""
        self.collection.delete(ids=[doc_id])
    
    def clear(self):
        """Clear all documents from the vector store."""
        self.collection.delete(where={}) 