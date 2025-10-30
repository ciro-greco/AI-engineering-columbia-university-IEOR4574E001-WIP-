"""
Chain implementations for different summarization approaches.

This module contains two versions of summarization:
- v0: Simple, basic summarization
- v1: Structured JSON output with sentiment analysis
"""

from pydantic import BaseModel
from time import time
from src.llm_local import chat
from src.tracer import trace


# Pydantic model for type validation (not used yet, but shows expected structure)
class SumOut(BaseModel):
    """Expected output structure for summarization."""
    summary: str


# This tells the LLM exactly what JSON format we want back
SCHEMA = """Return ONLY JSON: {"summary": string, "sentiment": string}"""
# Alternative for plain text: """Return ONLY plain text, not JSON."""


def summarize_v0(text: str) -> str:
    """
    Version 0: Basic summarization with minimal instructions.
    
    Args:
        text: The input text to summarize
        
    Returns:
        A plain text summary (format may vary)
    """
    # Record when we started (for measuring how long the LLM takes)
    t0 = time()
    
    # Create a simple prompt asking for a one-sentence summary
    prompt = f"Summarize the following text in one clear, single sentence:\n{text}"
    
    # Send the prompt to the LLM and get the response
    out = chat(prompt)
    
    # Save this interaction to runs.jsonl for later analysis
    # We track: function name, inputs, outputs, and how long it took
    trace("summarize_v0", {"text": text}, out, t0=t0)
    
    return out


def summarize_v1(text: str) -> str:
    """
    Version 1: Structured summarization with JSON output.
    
    This version returns both a summary and sentiment analysis in JSON format,
    making it easier to use the output in other parts of the system.
    
    Args:
        text: The input text to summarize
        
    Returns:
        A JSON string with "summary" and "sentiment" fields
    """
    # Record start time for latency measurement
    t0 = time()
    
    # Build a detailed prompt with:
    # - Role: Tell the model it's a "precise assistant"
    # - Rules: Clear instructions on what to do
    # - Format: Exact JSON structure expected
    # - Input: The text to process (clearly marked)
    prompt = f"""
You are a precise assistant that writes concise summaries.

Rules:
1. Summarize the input text in ONE factual sentence.
2. Do not add opinions or explanations.
3. Gauge the sentiment as one of: positive, negative, neutral.
4. Output must be exactly this JSON — no extra text:
{SCHEMA}

Input text:
{text}
"""
    
    # Send to LLM and get response
    out = chat(prompt)
    
    # Save this interaction for analysis
    trace("summarize_v1", {"text": text}, out, t0=t0)
    
    return out