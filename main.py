from dotenv import load_dotenv
load_dotenv(override=True)


from src.services.models.embeddings import Embeddings
from src.services.vectorial_db.faiss_index import FAISSIndex
from src.ingestion.ingest_files import ingest_files_data_folder
from src.services.models.llm import LLM
import os
from dotenv import load_dotenv
import time

def rag_chatbot(llm, input_text: str, history: list, index, top_k: int = 5):
    """Retrieves relevant information from the FAISS index, generates a response using the LLM, and manages the conversation history.

    Args:
        llm (LLM): An instance of the LLM class for generating responses.
        input_text (str): The user's input text.
        history (list): A list of previous messages in the conversation history.
        index (FAISSIndex): An instance of the FAISSIndex class for retrieving relevant information.
        top_k (int): Number of top documents to retrieve from the index.

    Returns:
        tuple: A tuple containing the AI's response and the updated conversation history.
    """

    # Step 1: Retrieve context from the FAISS index

    retrieved_contexts = index.retrieve_chunks(input_text,num_chunks=top_k)
    context_text = "\n".join(retrieved_contexts)

    # Step 2: Construct the prompt for the LLM
    history_text = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in history])
    prompt = (
        f"Context:\n{context_text}\n\n"
        f"Conversation history:\n{history_text}\n"
        f"User: {input_text}\n"
        f"Assistant:"
    )

    # Step 3: Generate a response using the LLM
    llm = LLM
    response = llm.get_response(" ", context_text,input_text)

    # Step 4: Update conversation history
    history.append({"role": "user", "content": input_text})
    history.append({"role": "assistant", "content": response})

    return response, history



def main():
    """Main function to run the chatbot."""

    embeddings = Embeddings()
    index = FAISSIndex(embeddings=embeddings.get_embeddings)

    try:
        index.load_index()
    except FileNotFoundError:
        raise ValueError("Index not found. You must ingest documents first.")

    llm = LLM()
    history = []
    print("\n# INTIALIZED CHATBOT #")
    while True:
        user_input = str(input("You:  "))
        if user_input.lower() == "exit":
            break
        response, history = rag_chatbot(llm, user_input, history, index)
        
        print("AI: ", response)


if __name__ == "__main__":
    main()