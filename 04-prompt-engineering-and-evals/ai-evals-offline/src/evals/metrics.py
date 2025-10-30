"""
Rule-based evaluation metrics for model outputs.

These are fast, deterministic functions that check specific properties
of the model's output without needing another LLM call.
"""

import json
import re


def schema_ok(s: str) -> bool:
    """
    Check if the output is valid JSON with required fields.
    
    Args:
        s: The model output string to check
        
    Returns:
        True if output is valid JSON with "summary" and "sentiment" fields
        
    Notes:
        - Used to verify v1 outputs follow the expected format
        - Returns False for plain text or malformed JSON
    """
    # Remove any leading/trailing whitespace
    s = s.strip()
    
    try:
        # Try to parse as JSON
        obj = json.loads(s)
    except Exception:
        # If parsing fails, it's not valid JSON
        return False
    
    # Check it's a dictionary with required fields
    # Both "summary" and "sentiment" must be present
    return isinstance(obj, dict) and "summary" in obj and "sentiment" in obj


def length_ok(s: str, max_words=20) -> bool:
    """
    Check if the summary is within the word limit.
    
    Args:
        s: The model output (can be JSON or plain text)
        max_words: Maximum allowed words in the summary
        
    Returns:
        True if the summary has <= max_words
        
    Notes:
        - Extracts the summary from JSON if needed
        - Counts words using regex pattern \w+
    """
    try:
        # If it's JSON, extract just the summary field
        txt = json.loads(s).get("summary", "")
    except Exception:
        # If not JSON, use the whole string
        txt = s
    
    # Count words using regex (\w+ matches sequences of word characters)
    word_count = len(re.findall(r"\w+", txt))
    
    # Check if within limit
    return word_count <= max_words


def contains_ref_terms(output: str, reference: str) -> float:
    """
    Calculate how many reference words appear in the output (faithfulness).
    
    Args:
        output: The model's generated summary
        reference: The expected/reference summary
        
    Returns:
        Float between 0 and 1 (fraction of reference words found in output)
        
    Notes:
        - Higher score means output is more "faithful" to the reference
        - Case-insensitive comparison
        - Works with both JSON and plain text outputs
    """
    try:
        # If output is JSON, extract the summary field
        if isinstance(output, str) and output.strip().startswith('{'):
            output_obj = json.loads(output)
            output_text = output_obj.get("summary", output)
        else:
            output_text = output
    except:
        # If anything fails, just use the raw output
        output_text = output
    
    # Extract all words from both texts (lowercase for comparison)
    # \w+ matches word characters (letters, digits, underscore)
    output_words = set(re.findall(r'\w+', output_text.lower()))
    ref_words = set(re.findall(r'\w+', reference.lower()))
    
    # Handle empty reference (avoid division by zero)
    if not ref_words:
        return 0.0
    
    # Count how many reference words appear in the output
    overlap = len(output_words.intersection(ref_words))
    
    # Return as a fraction (0.0 to 1.0)
    return overlap / len(ref_words)