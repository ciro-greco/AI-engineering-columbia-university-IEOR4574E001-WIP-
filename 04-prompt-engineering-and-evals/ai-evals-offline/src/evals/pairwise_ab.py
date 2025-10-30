"""
A/B testing script for comparing two model versions head-to-head.

Runs both chains on the same inputs and compares their outputs using
both rule-based metrics and LLM judge evaluation.
"""

import json
import random
import pathlib
from src.chains import summarize_v0, summarize_v1
from src.evals.metrics import contains_ref_terms
from src.evals.llm_judge import llm_judge_pairwise


def ab(path, use_llm_judge=True):
    """
    Run A/B test comparing v0 and v1 on a dataset.
    
    Args:
        path: Path to JSONL file with test examples
        use_llm_judge: Whether to use LLM for quality comparison
    
    Returns:
        Dictionary with win counts and agreement statistics
    """
    # Load test examples
    rows = [json.loads(l) for l in pathlib.Path(path).read_text().splitlines()]
    
    print(f"Running A/B test on {len(rows)} examples...")
    if use_llm_judge:
        print("Using LLM judge for pairwise comparison (this will be slower)...")
    else:
        print("Using rule-based faithfulness comparison...")
    
    # Track wins for each method
    v1_wins_llm = 0   # How many times LLM judge prefers v1
    v1_wins_rule = 0  # How many times rule-based prefers v1
    detailed_results = []  # Store all comparisons for analysis
    
    for i, r in enumerate(rows, 1):
        print(f"Processing comparison {i}/{len(rows)}...")
        
        # Generate outputs from both versions on the same input
        output_v0 = summarize_v0(r["input"])  # Plain text summary
        output_v1 = summarize_v1(r["input"])  # JSON with sentiment
        
        # Rule-based comparison: check word overlap with reference
        faith_v0 = contains_ref_terms(output_v0, r["reference"])  # 0.0 to 1.0
        faith_v1 = contains_ref_terms(output_v1, r["reference"])  # 0.0 to 1.0
        
        # Determine winner based on faithfulness score
        rule_winner = "v1" if faith_v1 > faith_v0 else "v0"
        v1_wins_rule += int(faith_v1 > faith_v0)
        
        # Store comparison details (truncate long text for readability)
        result = {
            "input": r["input"][:100] + "..." if len(r["input"]) > 100 else r["input"],
            "v0_output": output_v0[:100] + "..." if len(output_v0) > 100 else output_v0,
            "v1_output": output_v1[:100] + "..." if len(output_v1) > 100 else output_v1,
            "rule_winner": rule_winner,
            "faith_v0": faith_v0,
            "faith_v1": faith_v1,
        }
        
        # LLM judge comparison (if requested)
        if use_llm_judge:
            # Randomly swap order to avoid position bias
            # (LLMs sometimes prefer the first or second option systematically)
            if random.random() < 0.5:
                # v0 is A, v1 is B
                judgment = llm_judge_pairwise(r["input"], output_v0, output_v1)
                llm_winner = "v0" if judgment["winner"] == "A" else "v1"
            else:
                # v1 is A, v0 is B (swapped)
                judgment = llm_judge_pairwise(r["input"], output_v1, output_v0)
                llm_winner = "v1" if judgment["winner"] == "A" else "v0"
            
            v1_wins_llm += int(llm_winner == "v1")
            result.update({
                "llm_winner": llm_winner,
                "llm_confidence": judgment.get("confidence", 1),
                "llm_reasoning": judgment.get("reasoning", ""),
            })
        
        detailed_results.append(result)
    
    # Summary results
    results = {
        "total_pairs": len(rows),
        "rule_based": {
            "v1_wins": v1_wins_rule,
            "v0_wins": len(rows) - v1_wins_rule,
            "v1_win_rate": v1_wins_rule / len(rows)
        }
    }
    
    if use_llm_judge:
        results["llm_judge"] = {
            "v1_wins": v1_wins_llm,
            "v0_wins": len(rows) - v1_wins_llm,
            "v1_win_rate": v1_wins_llm / len(rows)
        }
        
        # Agreement between methods
        agreement = sum(1 for r in detailed_results 
                       if r["rule_winner"] == r["llm_winner"])
        results["agreement_rate"] = agreement / len(rows)
    
    # Save detailed results
    pathlib.Path("ab_results.jsonl").write_text(
        "\n".join(json.dumps(r) for r in detailed_results)
    )
    
    print(f"\nA/B Testing Results:")
    print(f"Rule-based (faithfulness): v1 wins {results['rule_based']['v1_wins']}/{len(rows)} ({results['rule_based']['v1_win_rate']:.1%})")
    
    if use_llm_judge:
        print(f"LLM judge: v1 wins {results['llm_judge']['v1_wins']}/{len(rows)} ({results['llm_judge']['v1_win_rate']:.1%})")
        print(f"Agreement between methods: {results['agreement_rate']:.1%}")
    
    return results


if __name__ == "__main__":
    # Set up command-line arguments
    import argparse
    ap = argparse.ArgumentParser()
    
    # Dataset to test on
    ap.add_argument("--dataset", default="data/examples.jsonl")
    
    # Option to skip LLM judge
    ap.add_argument("--no-llm-judge", action="store_true", 
                    help="Skip LLM judge evaluation (faster, less insightful)")
    
    # Parse and run
    args = ap.parse_args()
    ab(args.dataset, use_llm_judge=not args.no_llm_judge)
