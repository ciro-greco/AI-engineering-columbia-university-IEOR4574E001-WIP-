#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI dashboard for summarizing evaluation results and trace analysis.
"""

import json
import pathlib
import statistics
from collections import Counter, defaultdict
from datetime import datetime
import argparse

def load_jsonl(path):
    """Load JSONL file into list of dictionaries."""
    try:
        return [json.loads(line) for line in pathlib.Path(path).read_text().splitlines() if line.strip()]
    except FileNotFoundError:
        print(f"ERROR: File not found: {path}")
        return []
    except json.JSONDecodeError as e:
        print(f"ERROR: JSON decode error in {path}: {e}")
        return []

def summarize_results(results_file="results.jsonl"):
    """Summarize evaluation results from dataset_eval.py output."""
    print("EVALUATION RESULTS SUMMARY")
    print("=" * 50)
    
    results = load_jsonl(results_file)
    if not results:
        print(f"No results found in {results_file}")
        return
    
    # Calculate metrics
    n = len(results)
    schema_rate = sum(r.get("schema", 0) for r in results) / n if n > 0 else 0
    short_rate = sum(r.get("short", 0) for r in results) / n if n > 0 else 0
    faith_scores = [r.get("faith", 0) for r in results if "faith" in r]
    faith_mean = statistics.mean(faith_scores) if faith_scores else 0
    faith_std = statistics.stdev(faith_scores) if len(faith_scores) > 1 else 0
    
    print(f"Dataset Size: {n} examples")
    print(f"Schema Compliance: {schema_rate:.1%} ({int(schema_rate * n)}/{n})")
    print(f"Length Compliance: {short_rate:.1%} ({int(short_rate * n)}/{n})")
    print(f"Faithfulness: {faith_mean:.3f} ± {faith_std:.3f}")
    
    # Check if LLM judge metrics are available
    has_llm_metrics = any("llm_overall" in r for r in results)
    
    if has_llm_metrics:
        print(f"\nLLM JUDGE METRICS")
        print("-" * 30)
        
        llm_overall = [r.get("llm_overall", 0) for r in results if "llm_overall" in r]
        llm_accuracy = [r.get("llm_accuracy", 0) for r in results if "llm_accuracy" in r]
        llm_clarity = [r.get("llm_clarity", 0) for r in results if "llm_clarity" in r]
        llm_completeness = [r.get("llm_completeness", 0) for r in results if "llm_completeness" in r]
        llm_conciseness = [r.get("llm_conciseness", 0) for r in results if "llm_conciseness" in r]
        
        if llm_overall:
            print(f"Overall Quality: {statistics.mean(llm_overall):.2f}/5 ± {statistics.stdev(llm_overall) if len(llm_overall) > 1 else 0:.2f}")
        if llm_accuracy:
            print(f"Accuracy: {statistics.mean(llm_accuracy):.2f}/5")
        if llm_clarity:
            print(f"Clarity: {statistics.mean(llm_clarity):.2f}/5")
        if llm_completeness:
            print(f"Completeness: {statistics.mean(llm_completeness):.2f}/5")
        if llm_conciseness:
            print(f"Conciseness: {statistics.mean(llm_conciseness):.2f}/5")
        
        # Show some reasoning examples
        reasonings = [r.get("llm_reasoning", "") for r in results if r.get("llm_reasoning")]
        if reasonings:
            print(f"\nSAMPLE LLM REASONING:")
            for i, reasoning in enumerate(reasonings[:3], 1):
                print(f"{i}. {reasoning}")
    
    # Distribution analysis
    if faith_scores:
        print(f"\nFAITHFULNESS DISTRIBUTION")
        print("-" * 30)
        print(f"Min:  {min(faith_scores):.3f}")
        if len(faith_scores) >= 4:
            q = statistics.quantiles(faith_scores, n=4)
            print(f"Q25:  {q[0]:.3f}")
            print(f"Med:  {statistics.median(faith_scores):.3f}")
            print(f"Q75:  {q[2]:.3f}")
        else:
            print(f"Med:  {statistics.median(faith_scores):.3f}")
        print(f"Max:  {max(faith_scores):.3f}")

def analyze_traces(traces_file="runs.jsonl"):
    """Analyze model execution traces."""
    print("\nTRACE ANALYSIS")
    print("=" * 50)
    
    traces = load_jsonl(traces_file)
    if not traces:
        print(f"No traces found in {traces_file}")
        return
    
    # Performance analysis
    latencies = [t.get("latency_ms", 0) for t in traces]
    chain_counts = Counter(t.get("name", "unknown") for t in traces)
    
    print(f"Total Calls: {len(traces)}")
    print(f"Average Latency: {statistics.mean(latencies):.0f}ms")
    print(f"Chain Usage:")
    for chain, count in chain_counts.most_common():
        avg_latency = statistics.mean([t["latency_ms"] for t in traces if t.get("name") == chain])
        print(f"   • {chain}: {count} calls, {avg_latency:.0f}ms avg")
    
    # Timeline analysis
    if traces:
        timestamps = [t.get("ts", 0) for t in traces if t.get("ts")]
        if timestamps:
            start_time = min(timestamps)
            end_time = max(timestamps)
            duration = end_time - start_time
            print(f"\nTIMELINE")
            print(f"   Duration: {duration:.1f}s")
            print(f"   Rate: {len(traces)/duration:.1f} calls/sec")

def compare_chains(traces_file="runs.jsonl"):
    """Compare performance between different chains."""
    print("\nCHAIN COMPARISON")
    print("=" * 50)
    
    traces = load_jsonl(traces_file)
    if not traces:
        return
    
    # Group by chain
    chains = defaultdict(list)
    for trace in traces:
        chain_name = trace.get("name", "unknown")
        chains[chain_name].append(trace)
    
    if len(chains) < 2:
        print("Need at least 2 different chains for comparison")
        return
    
    print("Chain Performance Comparison:")
    print(f"{'Chain':<15} {'Calls':<8} {'Avg Latency':<12} {'Success Rate':<12}")
    print("-" * 50)
    
    for chain, chain_traces in sorted(chains.items()):
        calls = len(chain_traces)
        latencies = [t.get("latency_ms", 0) for t in chain_traces]
        avg_latency = statistics.mean(latencies) if latencies else 0
        successes = sum(1 for t in chain_traces if t.get("output"))
        success_rate = successes / calls if calls > 0 else 0
        
        print(f"{chain:<15} {calls:<8} {avg_latency:<12.0f} {success_rate:<12.1%}")

def summarize_ab_results(ab_file="ab_results.jsonl"):
    """Summarize A/B testing results with LLM judge analysis."""
    print(f"\nA/B TESTING ANALYSIS")
    print("=" * 50)
    
    ab_results = load_jsonl(ab_file)
    if not ab_results:
        print(f"No A/B results found in {ab_file}")
        return
    
    n = len(ab_results)
    
    # Rule-based comparison
    rule_v1_wins = sum(1 for r in ab_results if r.get("rule_winner") == "v1")
    rule_v0_wins = n - rule_v1_wins
    print(f"Rule-based (faithfulness):")
    print(f"  v1 wins: {rule_v1_wins}/{n} ({rule_v1_wins/n:.1%})")
    print(f"  v0 wins: {rule_v0_wins}/{n} ({rule_v0_wins/n:.1%})")
    
    # LLM judge comparison
    has_llm = any("llm_winner" in r for r in ab_results)
    if has_llm:
        llm_v1_wins = sum(1 for r in ab_results if r.get("llm_winner") == "v1")
        llm_v0_wins = n - llm_v1_wins
        print(f"\nLLM judge:")
        print(f"  v1 wins: {llm_v1_wins}/{n} ({llm_v1_wins/n:.1%})")
        print(f"  v0 wins: {llm_v0_wins}/{n} ({llm_v0_wins/n:.1%})")
        
        # Agreement analysis
        agreements = sum(1 for r in ab_results if r.get("rule_winner") == r.get("llm_winner"))
        print(f"\nAgreement between methods: {agreements}/{n} ({agreements/n:.1%})")
        
        # Confidence analysis
        confidences = [r.get("llm_confidence", 0) for r in ab_results if "llm_confidence" in r]
        if confidences:
            print(f"Average LLM confidence: {statistics.mean(confidences):.1f}/5")
        
        # Show disagreement cases
        disagreements = [r for r in ab_results if r.get("rule_winner") != r.get("llm_winner")]
        if disagreements:
            print(f"\nDISAGREEMENT CASES ({len(disagreements)} examples):")
            for i, case in enumerate(disagreements[:3], 1):
                print(f"{i}. Rule: {case.get('rule_winner')}, LLM: {case.get('llm_winner')}")
                print(f"   Reasoning: {case.get('llm_reasoning', 'No reasoning')[:100]}...")

def show_examples(traces_file="runs.jsonl", limit=3):
    """Show example inputs and outputs."""
    print(f"\nEXAMPLE OUTPUTS (showing {limit})")
    print("=" * 50)
    
    traces = load_jsonl(traces_file)
    if not traces:
        return
    
    for i, trace in enumerate(traces[:limit], 1):
        name = trace.get("name", "unknown")
        input_text = trace.get("inputs", {}).get("text", "No input")
        output = trace.get("output", "No output")
        latency = trace.get("latency_ms", 0)
        
        print(f"\n{i}. {name} ({latency}ms)")
        print(f"Input:  {input_text[:100]}{'...' if len(input_text) > 100 else ''}")
        print(f"Output: {output[:200]}{'...' if len(output) > 200 else ''}")

def main():
    parser = argparse.ArgumentParser(description="Analyze evaluation results and traces")
    parser.add_argument("--results", default="results.jsonl", help="Results file from dataset_eval.py")
    parser.add_argument("--traces", default="runs.jsonl", help="Traces file from model runs")
    parser.add_argument("--ab-results", default="ab_results.jsonl", help="A/B test results file")
    parser.add_argument("--examples", type=int, default=3, help="Number of examples to show")
    parser.add_argument("--no-traces", action="store_true", help="Skip trace analysis")
    parser.add_argument("--no-examples", action="store_true", help="Skip example outputs")
    parser.add_argument("--no-ab", action="store_true", help="Skip A/B test analysis")
    
    args = parser.parse_args()
    
    # Results summary
    if pathlib.Path(args.results).exists():
        summarize_results(args.results)
    else:
        print(f"Results file {args.results} not found. Run dataset_eval.py first.")
    
    # A/B test analysis
    if not args.no_ab and pathlib.Path(args.ab_results).exists():
        summarize_ab_results(args.ab_results)
    elif not args.no_ab:
        print(f"\nA/B results file {args.ab_results} not found. Run pairwise_ab.py first.")
    
    # Trace analysis
    if not args.no_traces and pathlib.Path(args.traces).exists():
        analyze_traces(args.traces)
        compare_chains(args.traces)
        
        if not args.no_examples:
            show_examples(args.traces, args.examples)
    elif not args.no_traces:
        print(f"\nTrace file {args.traces} not found. Run some evaluations first.")

if __name__ == "__main__":
    main()