"""
LLM-as-Judge evaluation functions.

Uses another LLM call to evaluate the quality of model outputs.
This provides more nuanced assessment than simple rule-based metrics.
"""

import json
from time import time
from src.llm_local import chat
from src.tracer import trace


def llm_judge_quality(input_text: str, output: str, reference: str = None) -> dict:
    """
    Use an LLM to evaluate output quality on multiple dimensions.
    
    Args:
        input_text: The original text that was summarized
        output: The summary to evaluate
        reference: Optional reference summary for comparison
        
    Returns:
        Dictionary with scores for each dimension (1-5) and reasoning
        
    Notes:
        - Each dimension is scored 1 (Poor) to 5 (Excellent)
        - Includes qualitative reasoning to explain the scores
        - Falls back to default scores if LLM response can't be parsed
    """
    # Record start time for latency tracking
    t0 = time()
    
    # Build a prompt that asks the LLM to act as an evaluator
    # We want scores on 4 dimensions plus an overall score
    prompt = f"""You are an expert evaluator of text summaries. Rate this summary on a scale of 1-5 for each dimension.

Input text: {input_text}

Summary to evaluate: {output}

{f"Reference summary: {reference}" if reference else ""}

Rate on these dimensions (1=Poor, 2=Below Average, 3=Average, 4=Good, 5=Excellent):

- **Accuracy**: How well does it capture the key information from the input?
- **Clarity**: Is it well-written, clear, and easy to understand?
- **Completeness**: Does it cover the important points without missing key details?
- **Conciseness**: Is it appropriately brief without being too short or too long?

Return ONLY this JSON format:
{{"accuracy": int, "clarity": int, "completeness": int, "conciseness": int, "overall": int, "reasoning": "brief explanation"}}"""

    # Get the LLM's evaluation
    result = chat(prompt)
    
    # Log this judge call for analysis
    trace("llm_judge_quality", 
          {"input": input_text, "output": output, "reference": reference}, 
          result, t0=t0)
    
    try:
        # Try to parse the JSON response
        scores = json.loads(result.strip())
        return scores
    except json.JSONDecodeError:
        # If the LLM didn't return proper JSON, provide fallback scores
        # This ensures the evaluation pipeline doesn't break
        return {
            "accuracy": 3,      # Default to "average" scores
            "clarity": 3, 
            "completeness": 3, 
            "conciseness": 3, 
            "overall": 3, 
            "reasoning": "Failed to parse LLM response", 
            "raw_response": result  # Keep the original for debugging
        }


def llm_judge_pairwise(input_text: str, output_a: str, output_b: str) -> dict:
    """
    Compare two outputs and decide which is better.
    
    Args:
        input_text: The original text that was summarized
        output_a: First summary (labeled "A")
        output_b: Second summary (labeled "B")
        
    Returns:
        Dictionary with winner ("A" or "B"), confidence (1-5), and reasoning
        
    Notes:
        - Used for A/B testing between different model versions
        - Confidence indicates how sure the judge is (1=unsure, 5=very sure)
        - Provides reasoning to explain the decision
    """
    # Record start time
    t0 = time()
    
    # Build a prompt for pairwise comparison
    # The LLM needs to pick which summary is better overall
    prompt = f"""You are an expert evaluator comparing two summaries of the same text. Determine which summary is better overall.

Input text: {input_text}

Summary A: {output_a}

Summary B: {output_b}

Consider:
- Accuracy: Which better captures key information?
- Clarity: Which is clearer and better written?
- Completeness: Which covers important points better?
- Conciseness: Which is more appropriately brief?

Return ONLY this JSON format:
{{"winner": "A" or "B", "confidence": int (1-5), "reasoning": "brief explanation of why this summary is better"}}"""

    # Get the LLM's judgment
    result = chat(prompt)
    
    # Log this comparison
    trace("llm_judge_pairwise", 
          {"input": input_text, "output_a": output_a, "output_b": output_b}, 
          result, t0=t0)
    
    try:
        # Parse the JSON response
        judgment = json.loads(result.strip())
        return judgment
    except json.JSONDecodeError:
        # Fallback if parsing fails - default to A with low confidence
        return {
            "winner": "A", 
            "confidence": 1,  # Very low confidence
            "reasoning": "Failed to parse LLM response", 
            "raw_response": result
        }


def extract_llm_score(llm_result: dict) -> float:
    """
    Extract a single numeric score from the LLM judge result.
    
    Args:
        llm_result: Dictionary returned by llm_judge_quality
        
    Returns:
        A float score (typically 1.0 to 5.0)
        
    Notes:
        - Prefers the "overall" score if available
        - Otherwise averages the individual dimension scores
        - Returns 3.0 as default if no scores found
    """
    # First try to use the overall score
    if "overall" in llm_result and isinstance(llm_result["overall"], (int, float)):
        return float(llm_result["overall"])
    
    # If no overall score, calculate average of individual dimensions
    score_keys = ["accuracy", "clarity", "completeness", "conciseness"]
    scores = []
    
    for key in score_keys:
        if key in llm_result and isinstance(llm_result[key], (int, float)):
            scores.append(float(llm_result[key]))
    
    # Return average if we have scores, otherwise default to 3.0
    if scores:
        return sum(scores) / len(scores)
    else:
        return 3.0  # Default to "average" score