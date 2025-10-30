"""
Interface to the local Ollama LLM server.

This module handles communication with Ollama, which runs LLMs locally
on your machine. Ollama must be running separately (ollama serve).
"""

import ollama


def chat(prompt: str) -> str:
    """
    Send a prompt to the local Ollama server and get a response.
    
    Args:
        prompt: The text prompt to send to the model
        
    Returns:
        The model's text response
        
    Notes:
        - Uses the "llama3" model (must be downloaded with: ollama pull llama3)
        - Temperature is set to 0 for deterministic outputs (same input = same output)
        - The model runs locally, so no API keys or internet needed
    """
    # Call Ollama's chat API with:
    # - model: Which LLM to use (llama3 in our case)
    # - messages: A list with one message from the "user" role
    # - options: Model settings (temperature=0 means no randomness)
    res = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}],
        options={"temperature": 0}
    )
    
    # Extract just the text content from the response
    # The full response includes metadata we don't need right now
    return res["message"]["content"]