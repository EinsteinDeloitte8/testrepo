import sys
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.core import Document
from src.services.vectorial_db.chunking_base import ChunkingBase
from llama_index.core import SimpleDirectoryReader



class TokenChunking:
    """A simple class to split text into chunks."""
    
    def get_chunks_from_text(self, text: str, chunk_size: int = 512) -> list[str]:
        """Splits the text into chunks of the specified size based on word count.

        Args:
            text (str): The text to split into chunks.
            chunk_size (int): The desired size of each chunk (default is 512 words).

        Returns:
            list: A list of text chunks.
        """
        # Split the text into words
        words = text.split()
        
        # Prepare chunks by slicing the list of words
        chunks = []
        for i in range(0, len(words), chunk_size):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
        
        return chunks

def text_to_chunks(text: str, chunk_size: int = 512) -> list[str]:
    """Splits text into chunks of a specified size.

    Args:
        text (str): The text to split into chunks.
        chunk_size (int): The desired size of each chunk (default is 512 words).

    Returns:
        list: A list of text chunks.
    """
    chunker = TokenChunking()  # Initialize TokenChunking
    chunks = chunker.get_chunks_from_text(text, chunk_size)
    return chunks


text = """This is a very long text that we want to split into chunks. It can contain multiple paragraphs or just a huge paragraph. 
We will use the text_to_chunks function to split this into smaller chunks for easier processing."""

chunks = text_to_chunks(text, chunk_size=10)
for idx, chunk in enumerate(chunks):
    print(f"Chunk {idx + 1}: {chunk}\n")
