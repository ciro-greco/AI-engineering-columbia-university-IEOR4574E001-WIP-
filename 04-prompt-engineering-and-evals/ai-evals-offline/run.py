"""
Interactive script to test both summarization chains.

This is a simple way to see how v0 and v1 differ on any input text.
Run this to quickly test changes to the prompts.
"""

from src.chains import summarize_v0, summarize_v1

# Get input from the user
text = input("Enter text to summarize:\n> ").strip()

# Show v0 output (basic summarization)
print("\n--- Baseline (v0) ---")
print(summarize_v0(text))

# Show v1 output (JSON with sentiment)
print("\n--- Improved (v1) ---")
print(summarize_v1(text))