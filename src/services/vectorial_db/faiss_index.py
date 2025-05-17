from faiss import IndexFlatL2, write_index, read_index
import numpy as np
import os
import sys 

from src.services.vectorial_db.token_chunking import TokenChunking
from src.services.models.embeddings import Embeddings  # Assuming Embeddings class is in a file named embeddings.py
from src.services.models.llm import LLM  # Assuming LLM class is in a file named llm.py


class FAISSIndex:
    """
    Manages a FAISS index for storing and retrieving text chunks based on their embeddings.

    Attributes:
        dimension (int): The dimension of the embeddings.
        embeddings (function): The function used to generate embeddings for text.
        index (faiss.IndexFlatL2): The FAISS index object.
        chunks_list (list): A list of text chunks stored in the index.

    Methods:
        _create_faiss_index(): Initializes a new FAISS index.
        ingest_text(): Adds text chunks to the index.
        retrieve_chunks(): Retrieves relevant chunks for a given query.
        save_index(): Saves the index and chunk list to disk.
        load_index(): Loads the index and chunk list from disk.
    """
    def __init__(self, dimension: int = 1536, embeddings=None):
        """Initialize the FAISSIndex with dimensions and embedding function."""
        if not embeddings:
            raise ValueError("No embeddings provided.")
        self.embeddings = Embeddings
        self.dimension = dimension
        self.index: IndexFlatL2 | None = None
        self._create_faiss_index()
        self.chunks_list: list = []
        print(f"FAISSIndex initialized with dimension: {self.dimension}")

    def _create_faiss_index(self):
        """Create a new FAISS index."""
        self.index = IndexFlatL2(self.dimension)
        print("FAISS index created.")

    def ingest_text(self, text: str | None = None, text_chunks: list | None = None) -> bool:
        """Ingests text to the FAISS index."""
        if not (text_chunks or text):
            raise ValueError("Either text or text_chunks must be provided.")
        
        if not text_chunks:
            print("No text chunks provided. Chunking the text...")
            text_chunks = TokenChunking.text_to_chunks(text)
            print(f"Text has been chunked into {len(text_chunks)} chunks.")
        
        for chunk in text_chunks:
            embedding = self.embeddings.get_embeddings(chunk)
            print(f"Embedding for chunk '{chunk[:30]}...' generated.")
            self.index.add(np.array([embedding]).astype('float32'))
            self.chunks_list.append(chunk)
            print(f"Chunk '{chunk[:30]}...' added to the index.")
        
        return True

    def retrieve_chunks(self, query: str, num_chunks: int = 5) -> list:
        """Retrieve chunks from the FAISS index based on a query."""
        print(f"Retrieving chunks for query: '{query[:30]}...'")
        
        query_embedding = self.embeddings.get_embeddings(text = query)
        query_vector = np.array([query_embedding]).astype('float32')
        
        print(f"Query embedding generated: {query_embedding[:5]}...")  # Print a part of the embedding for brevity
        
        _, I = self.index.search(query_vector, num_chunks)
        
        print(f"Top {num_chunks} matching indices: {I[0]}")
        
        retrieved_chunks = [self.chunks_list[i] for i in I[0]]
        print(f"Retrieved chunks: {retrieved_chunks[:5]}")  # Print the first few retrieved chunks
        return retrieved_chunks

    def save_index(self, path=r"./faiss_index"):
        """Save the index and chunk list to disk."""
        print(f"Saving index to '{path}' folder...")
        index_path = os.path.join(path, "index.faiss")
        chunks_path = os.path.join(path, "chunks.npy")
        if not os.path.exists(path):
            os.makedirs(path)
        write_index(self.index, index_path)
        np.save(chunks_path, self.chunks_list)
        print(f"Index and chunks saved to {path}.")

    def load_index(self, path: str = r"./faiss_index"):
        """Load the index and chunk list from disk."""
        print(f"Loading index from '{path}' folder...")
        index_path = os.path.join(path, "index.faiss")
        chunks_path = os.path.join(path, "chunks.npy")
        if not os.path.exists(path):
            raise FileNotFoundError("Index not found.")
        
        self.index = read_index(index_path)
        self.chunks_list = np.load(chunks_path, allow_pickle=True).tolist()
        
        print(f"Index loaded with {len(self.chunks_list)} chunks.")
