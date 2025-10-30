"""
Tracing system for logging all model interactions.

This module automatically records every LLM call to a JSONL file,
creating a complete audit trail for debugging and analysis.
"""

import time
import uuid
import orjson  # Fast JSON library
import pathlib

# Where we save all the traces (one JSON object per line)
LOG = pathlib.Path("runs.jsonl")


def trace(name, inputs, output, meta=None, t0=None):
    """
    Log a single model interaction to the trace file.
    
    Args:
        name: Name of the function/chain that made this call (e.g., "summarize_v0")
        inputs: The inputs sent to the model (usually {"text": "..."})
        output: The model's response text
        meta: Optional metadata dictionary for extra info
        t0: Start time (from time.time()) to calculate latency
        
    Notes:
        - Each trace gets a unique ID for tracking
        - Latency is automatically calculated if t0 is provided
        - Appends to runs.jsonl (creates file if it doesn't exist)
        - Uses JSONL format (one JSON object per line) for easy streaming
    """
    # Build the trace record with all the information we want to track
    rec = {
        "id": str(uuid.uuid4()),  # Unique identifier for this specific call
        "name": name,              # Which function made this call
        "ts": time.time(),         # Timestamp when trace was recorded
        "latency_ms": int(1000 * (time.time() - (t0 or time.time()))),  # How long the LLM took
        "inputs": inputs,          # What we sent to the model
        "output": output,          # What the model returned
        "meta": meta or {}        # Any extra metadata
    }
    
    # Append this record to the log file as a new line
    # If the file exists, read it first and append, otherwise start fresh
    # orjson.dumps() converts Python dict to JSON bytes
    if LOG.exists():
        # Read existing content and append new record
        existing_content = LOG.read_bytes()
        LOG.write_bytes(existing_content + orjson.dumps(rec) + b"\n")
    else:
        # Create new file with first record
        LOG.write_bytes(orjson.dumps(rec) + b"\n")