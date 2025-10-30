"""
Dataset evaluation script for batch testing model performance.

Runs a chosen chain (v0 or v1) on all examples in a dataset and
calculates both rule-based and LLM judge metrics.
"""

import json
import pathlib
import statistics
from src.chains import summarize_v0, summarize_v1
from src.evals.metrics import schema_ok, length_ok, contains_ref_terms
from src.evals.llm_judge import llm_judge_quality, extract_llm_score

def run(chain_name, path, use_llm_judge=True):
    """
    Evaluate a chain on all examples in a dataset.
    
    Args:
        chain_name: Which chain to test ("v0" or "v1")
        path: Path to JSONL file with test examples
        use_llm_judge: Whether to include LLM judge evaluation (slower but more insightful)
    """
    # Select the right function based on chain name
    fn = {"v0": summarize_v0, "v1": summarize_v1}[chain_name]
    
    # Load all test examples from JSONL file (one JSON per line)
    rows = [json.loads(l) for l in pathlib.Path(path).read_text().splitlines()]
    
    # Will store results for each example
    results = []
    
    # Tell user what we're doing
    print(f"Evaluating {len(rows)} examples with {chain_name}...")
    if use_llm_judge:
        print("Using LLM judge for quality assessment (this will be slower)...")
    
    # Process each example in the dataset
    for i, r in enumerate(rows, 1):
        print(f"Processing example {i}/{len(rows)}...")
        
        # Generate summary using the selected chain
        # r["input"] is the text to summarize
        y = fn(r["input"])
        
        # Calculate rule-based metrics (fast, deterministic)
        result = {
          "schema": int(schema_ok(y)),  # 1 if valid JSON, 0 if not
          "short": int(length_ok(y)),    # 1 if under word limit, 0 if not
          "faith": contains_ref_terms(y, r["reference"]),  # 0.0 to 1.0 overlap
        }
        
        # Get LLM judge evaluation if requested
        # This makes another LLM call to evaluate the quality
        if use_llm_judge:
            # Ask LLM to score the output
            llm_scores = llm_judge_quality(r["input"], y, r["reference"])
            
            # Add LLM scores to our result
            result.update({
                "llm_overall": extract_llm_score(llm_scores),  # Combined score
                "llm_accuracy": llm_scores.get("accuracy", 3),  # 1-5 score
                "llm_clarity": llm_scores.get("clarity", 3),
                "llm_completeness": llm_scores.get("completeness", 3),
                "llm_conciseness": llm_scores.get("conciseness", 3),
                "llm_reasoning": llm_scores.get("reasoning", ""),  # Why these scores
            })
        
        results.append(result)
    
    # Calculate summary statistics across all examples
    agg = {
      "n": len(results),  # Total number of examples
      "schema_rate": sum(x["schema"] for x in results)/len(results),  # % valid JSON
      "short_rate": sum(x["short"] for x in results)/len(results),    # % under limit
      "faith_mean": statistics.mean(x["faith"] for x in results),     # Avg overlap
    }
    
    # Add LLM judge averages if we used it
    if use_llm_judge:
        agg.update({
            "llm_overall_mean": statistics.mean(x["llm_overall"] for x in results),
            "llm_accuracy_mean": statistics.mean(x["llm_accuracy"] for x in results),
            "llm_clarity_mean": statistics.mean(x["llm_clarity"] for x in results),
            "llm_completeness_mean": statistics.mean(x["llm_completeness"] for x in results),
            "llm_conciseness_mean": statistics.mean(x["llm_conciseness"] for x in results),
        })
    
    # Save detailed results to file for later analysis
    pathlib.Path("results.jsonl").write_text("\n".join(json.dumps(x) for x in results))
    
    # Print summary to console
    print(f"\n{chain_name} Results:")
    for key, value in agg.items():
        if isinstance(value, float):
            print(f"  {key}: {value:.3f}")  # Format floats to 3 decimal places
        else:
            print(f"  {key}: {value}")

if __name__ == "__main__":
    # Set up command-line argument parsing
    import argparse
    ap = argparse.ArgumentParser()
    
    # Which chain to evaluate
    ap.add_argument("--chain", choices=["v0","v1"], required=True)
    
    # Which dataset to use
    ap.add_argument("--dataset", default="data/examples.jsonl")
    
    # Option to skip LLM judge for faster testing
    ap.add_argument("--no-llm-judge", action="store_true", 
                    help="Skip LLM judge evaluation (faster, less insightful)")
    
    # Parse arguments and run evaluation
    args = ap.parse_args()
    run(args.chain, args.dataset, use_llm_judge=not args.no_llm_judge)
