import faiss
import numpy as np
from typing import List, Dict
import os
import json
import hashlib

class VectorStore:
    def __init__(self):
        self.dimension = 100  # Simple embedding dimension
        self.index = faiss.IndexFlatL2(self.dimension)
        self.documents = []
        self.metadata_list = []
        
        # Create data directory if it doesn't exist
        os.makedirs("./data/vector_store", exist_ok=True)
        
        # Load existing data if available
        self.load_data()
    
    def add_document(self, text: str, metadata: dict = None):
        """Add a document to the vector store."""
        if metadata is None:
            metadata = {}
        
        # Create a simple embedding using hashing
        embedding = self._create_embedding(text)
        
        # Add to FAISS index
        self.index.add(np.array([embedding]).astype('float32'))
        
        # Store document and metadata
        self.documents.append(text)
        self.metadata_list.append(metadata)
        
        # Save data
        self.save_data()
    
    def search(self, query: str, n_results: int = 3) -> List[str]:
        """Search for relevant documents."""
        # Create query embedding
        query_embedding = self._create_embedding(query)
        
        # Search in FAISS
        D, I = self.index.search(np.array([query_embedding]).astype('float32'), k=min(n_results, len(self.documents)))
        
        # Return found documents
        return [self.documents[i] for i in I[0]]
    
    def _create_embedding(self, text: str) -> np.ndarray:
        """Create a simple embedding using hashing."""
        # Hash the text
        hash_obj = hashlib.sha256(text.encode())
        hash_bytes = hash_obj.digest()
        
        # Convert hash to numbers and normalize
        numbers = np.frombuffer(hash_bytes, dtype=np.uint8)
        embedding = numbers[:self.dimension].astype(np.float32)
        embedding = embedding / np.linalg.norm(embedding)
        
        return embedding
    
    def save_data(self):
        """Save the current state to disk."""
        data_dir = "./data/vector_store"
        
        # Save documents and metadata
        with open(os.path.join(data_dir, "documents.json"), "w", encoding="utf-8") as f:
            json.dump({
                "documents": self.documents,
                "metadata": self.metadata_list
            }, f, ensure_ascii=False, indent=2)
        
        # Save FAISS index
        faiss.write_index(self.index, os.path.join(data_dir, "index.faiss"))
    
    def load_data(self):
        """Load the state from disk if available."""
        data_dir = "./data/vector_store"
        doc_path = os.path.join(data_dir, "documents.json")
        index_path = os.path.join(data_dir, "index.faiss")
        
        if os.path.exists(doc_path) and os.path.exists(index_path):
            # Load documents and metadata
            with open(doc_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.documents = data["documents"]
                self.metadata_list = data["metadata"]
            
            # Load FAISS index
            self.index = faiss.read_index(index_path)
    
    def clear(self):
        """Clear all documents from the vector store."""
        self.index = faiss.IndexFlatL2(self.dimension)
        self.documents = []
        self.metadata_list = []
        self.save_data() 