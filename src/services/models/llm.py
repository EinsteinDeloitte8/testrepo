from openai import AzureOpenAI
import os

class LLM:
    """Handles interactions with the Azure OpenAI LLM (Large Language Model).

    Attributes:
        client (AzureOpenAI): The Azure OpenAI client instance.
        model_name (str): The name of the Azure OpenAI LLM model to use.

    Methods:
        get_response(history, context, user_input): Generates a response from the LLM based on the conversation history, context, and user input.
    """
    '''
    def __init__(self):
        """Initializes the LLM class with Azure OpenAI client and model information."""
        # AzureOpenAI client setup
        azure_endpoint = os.getenv("AZURE_LLM_ENDPOINT")
        azure_deployment = os.getenv("AZURE_LLM_DEPLOYMENT_NAME")
        api_key = os.getenv("AZURE_LLM_API_KEY")
        api_version = os.getenv("AZURE_LLM_API_VERSION")

        self.client = AzureOpenAI(
            azure_endpoint=azure_endpoint,
            azure_deployment=azure_deployment,
            api_version=api_version,
            api_key=api_key
        )
        self.model_name = os.getenv("AZURE_LLM_MODEL_NAME")
'''
    def get_response(history, context, user_input):
        """Generates a response from the LLM.

        Args:
            history (list): A list of previous messages in the conversation history.
            context (str): Relevant information from the knowledge base to provide context to the LLM.
            user_input (str): The user's current input.

        Returns:
            str: The LLM's generated response.
        """
        azure_endpoint = os.getenv("AZURE_LLM_ENDPOINT")
        azure_deployment = os.getenv("AZURE_LLM_DEPLOYMENT_NAME")
        api_key = os.getenv("AZURE_LLM_API_KEY")
        api_version = os.getenv("AZURE_LLM_API_VERSION")

        client = AzureOpenAI(
            azure_endpoint=azure_endpoint,
            azure_deployment=azure_deployment,
            api_version=api_version,
            api_key=api_key
        )
        model_name = os.getenv("AZURE_LLM_MODEL_NAME")


        prompt = f"Context: {context}\nHistory: {history}\nUser: {user_input}\nAI:"

        # Generating the response using the LLM model
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "system", "content": "You are an assistant."},
                      {"role": "user", "content": prompt}]
        )
        
        
        return response.choices[0].message.content

