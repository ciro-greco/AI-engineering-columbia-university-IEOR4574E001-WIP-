"""
Unit tests for the summarization chains.

These are fast, deterministic tests that check basic functionality.
Run with: python -m pytest src/evals/unit_tests.py -v
"""

from src.chains import summarize_v1
from src.evals.metrics import schema_ok, length_ok


def test_schema_ok():
    """
    Test that v1 outputs valid JSON with required fields.
    
    This is a basic sanity check - if this fails, something is very wrong
    with the prompt or model configuration.
    """
    # Generate a summary using v1
    out = summarize_v1("Battery lasts 2 hours. Screen is bright.")
    
    # Check that it's valid JSON with "summary" and "sentiment" fields
    assert schema_ok(out), f"Output is not valid JSON: {out}"


def test_summary_length():
    """
    Test that summaries respect the word limit.
    
    We ask for one sentence, which should be under 20 words for
    this simple input.
    """
    # Generate a summary
    out = summarize_v1("Battery lasts 2 hours. Screen is bright.")
    
    # Check it's not too long
    assert length_ok(out, max_words=20), f"Summary too long: {out}"