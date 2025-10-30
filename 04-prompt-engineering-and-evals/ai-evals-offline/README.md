# AI Application Evaluation Framework

This project demonstrates three core evaluation concepts for AI applications: **LLM Unit Tests**, **Model-Based Evaluation**, and **A/B Testing**. Students will learn how to systematically evaluate and compare different versions of AI summarization models.

## Main points
1. How to write unit tests for LLM applications
2. How to design automated evaluation metrics
3. How to run A/B tests comparing model versions
4. How to structure an evaluation pipeline for AI systems

## Setup Instructions

### Step 1: Environment Setup

Create and activate a virtual environment:

```bash
# Create virtual environment
python -m venv ai-evals-env

# Activate it (macOS/Linux)
source ai-evals-env/bin/activate

# Or on Windows
# ai-evals-env\Scripts\activate
```

### Step 2: Install Dependencies

```bash
# Navigate to project root 
cd /path/to/AI-engineering-IEOR4574E001

# Install all dependencies including evaluation framework
pip install -r requirements.txt

# Install the evaluation framework in development mode
# Note: This uses setup.py to make src.chains, src.evals etc. importable as modules
pip install -e 04-prompt-engineering-and-evals/ai-evals-offline/
```

### Step 3: Set Up Local LLM Server (Ollama)

This project uses Ollama to run models locally for evaluation.

> **⚠️ Production Note**: In real-world applications, you'd typically containerize model servers using Docker to ensure consistent environments and avoid system-level dependencies. We're installing Ollama as a system daemon here for simplicity, but this isn't considered a best practice for production deployments.

#### Install Ollama:
- **macOS**: `brew install ollama` or download from [ollama.ai](https://ollama.ai)
- **Linux**: `curl -fsSL https://ollama.ai/install.sh | sh`
- **Windows**: Download from [ollama.ai](https://ollama.ai)

#### Download and start the model:
```bash
# Download Llama3 model (this may take several minutes)
ollama pull llama3

# Start Ollama server (keep this running in a separate terminal)
ollama serve
```

#### Verify setup:
```bash
# Test that the model works
ollama run llama3 "Hello, how are you?"
```

### Step 4: Verify Installation

Test that all imports work correctly:
```bash
python -c "from src.chains import summarize_v0, summarize_v1; print('Setup complete')"
```

---

## Understanding AI Evaluation

### **The Problem: How do you know if v1 is better than v0?**

We have two summarization approaches:
- **v0**: Basic single-sentence summarization
- **v1**: Structured JSON output with summary + sentiment

Let's learn how to evaluate them systematically!

---

## Understanding the System Architecture

### Data Flow
```
Input Text → Chain (v0/v1) → Ollama LLM → Automatic Tracing → Metrics → Results
```

### Key Components
- **`src/chains.py`**: Business logic for v0/v1 summarization
- **`src/tracer.py`**: Automatic logging of every model call
- **`src/llm_local.py`**: Ollama integration with temperature=0
- **Output Files**: `runs.jsonl` (traces), `results.jsonl` (evaluations)

---

## Part 1: LLM Unit Tests

**Concept**: Fast, deterministic tests that validate specific behaviors of your AI system.

### What are LLM Unit Tests?
- Quick sanity checks for your AI models
- Test specific, measurable behaviors
- Catch regressions when you change prompts or models
- Similar to traditional unit tests but for AI outputs

### Run the Unit Tests:

```bash
# Run unit tests to verify basic functionality
python -m pytest src/evals/unit_tests.py -v
```

### Examine the Tests:

Look at `src/evals/unit_tests.py`:
```python
def test_schema_ok():
    out = summarize_v1("Battery lasts 2 hours. Screen is bright.")
    assert schema_ok(out)  # Validates JSON format

def test_summary_length():
    out = summarize_v1("Battery lasts 2 hours. Screen is bright.")
    assert length_ok(out, max_words=20)  # Checks word count
```

### Key Learning:
- Unit tests are **fast** and **reliable**
- They test **specific behaviors** (format, length)
- They **don't measure quality** - just basic compliance

---

## Part 2: LLM-as-Judge Evaluation

**Concept**: Use another LLM to evaluate the quality of model outputs, providing more nuanced assessment than rule-based metrics.

### What is LLM-as-Judge Evaluation?
- Uses an LLM to assess output quality on multiple dimensions
- Provides scores for accuracy, clarity, completeness, and conciseness
- More closely correlates with human judgment than simple rules
- Includes qualitative reasoning for each assessment
- Combines both rule-based metrics and LLM judge scores

### Examine the Dataset:

Look at `data/examples.jsonl` to understand the evaluation format:
```json
{"input": "The new smartphone has excellent battery life...", "reference": "Phone has good battery but poor screen quality."}
```

### Run Dataset Evaluation:

```bash
# Evaluate v0 (baseline) with LLM judge (slower but more insightful)
python src/evals/dataset_eval.py --chain v0 --dataset data/examples.jsonl

# Evaluate v1 (improved) with LLM judge
python src/evals/dataset_eval.py --chain v1 --dataset data/examples.jsonl

# For faster testing, skip LLM judge (rule-based metrics only)
python src/evals/dataset_eval.py --chain v1 --dataset data/examples.jsonl --no-llm-judge
```

### Understanding the Metrics:

The evaluation now provides both **rule-based** and **LLM judge** metrics:

**Rule-Based Metrics (Fast)**:
1. **Schema Rate**: % of outputs that follow correct JSON format
2. **Short Rate**: % of outputs that meet length requirements  
3. **Faith Mean**: Average word overlap score with reference text

**LLM Judge Metrics (Slower, More Insightful)**:
1. **Accuracy**: How well does it capture key information? (1-5)
2. **Clarity**: Is it well-written and clear? (1-5)
3. **Completeness**: Does it cover important points? (1-5)
4. **Conciseness**: Is it appropriately brief? (1-5)
5. **Overall**: Combined quality score (1-5)
6. **Reasoning**: Qualitative explanation of the scores

### Examine the Code:

- **Rule-based metrics**: `src/evals/metrics.py` - fast, deterministic functions
- **LLM judge**: `src/evals/llm_judge.py` - nuanced quality assessment using LLM

### Key Learning:
- **Rule-based metrics**: Fast, consistent, but limited in scope
- **LLM judge**: Slower, more nuanced, correlates better with human judgment
- **Combined approach**: Use both for comprehensive evaluation
- **Cost vs. insight trade-off**: LLM judging requires more model calls

---

## Part 3: A/B Testing (Pairwise Comparison)

**Concept**: Direct head-to-head comparison between model versions.

### What is A/B Testing?
- Compare two versions on the same inputs
- Mimics real-world deployment decisions
- More realistic than isolated evaluation
- Helps determine which version to deploy

### Run A/B Testing:

```bash
# Run pairwise comparison with LLM judge (recommended)
python src/evals/pairwise_ab.py

# For faster testing, use only rule-based comparison
python src/evals/pairwise_ab.py --no-llm-judge
```

This will:
1. Run both v0 and v1 on each example
2. Compare outputs using **both** rule-based and LLM judge methods
3. Show agreement/disagreement between evaluation approaches
4. Save detailed results to `ab_results.jsonl`

### Understanding A/B Results:

The enhanced output shows:
- **Rule-based winner**: Based on faithfulness (word overlap) 
- **LLM judge winner**: Based on overall quality assessment
- **Agreement rate**: How often both methods agree
- **Confidence scores**: LLM's confidence in its judgments
- **Disagreement analysis**: Cases where methods disagree with reasoning

### Key Learning:
- **Multiple evaluation perspectives**: Rule-based vs. LLM judgment
- **Agreement analysis**: Validates evaluation consistency  
- **Qualitative insights**: LLM provides reasoning for decisions
- **Method comparison**: Shows when simple metrics vs. nuanced judgment differ

---

## Part 4: Interactive Testing & Trace Analysis

### Test Individual Functions:

```bash
# Interactive testing (recommended first step)
python run.py
# Enter text to see both v0 and v1 outputs side-by-side
```

### Understanding Automatic Tracing:

Every model call is automatically logged with:
- Unique ID, timestamp, latency
- Full input/output for debugging
- Cumulative performance metrics

```bash
# View recent traces (last 5 calls)
tail -5 runs.jsonl | python -m json.tool

# Count total logged calls
wc -l runs.jsonl

# Monitor calls in real-time
tail -f runs.jsonl
```

### Modify and Experiment:

Try modifying the prompts in `src/chains.py`:
1. Change the v1 prompt instructions
2. Run evaluations again
3. Compare the results

---

## Part 5: Building an Evaluation Pipeline

### Integration: Combining All Approaches

A complete evaluation workflow should include:

1. **Unit Tests**: Fast feedback during development
2. **Automated Metrics**: Scalable regression testing
3. **A/B Testing**: Final deployment decisions

### Recommended Workflow:

```bash
# 1. Run unit tests (fast feedback)
python -m pytest src/evals/unit_tests.py

# 2. Run automated evaluation with LLM judge (comprehensive)
python src/evals/dataset_eval.py --chain v1 --dataset data/examples.jsonl

# 3. Run A/B testing with LLM judge (deployment decision)
python src/evals/pairwise_ab.py

# 4. Analyze results with interactive dashboard
streamlit run src/dashboards/streamlit_app.py

# Alternative: CLI dashboard (now includes LLM judge metrics)
python src/dashboards/summarize_results.py

# 5. Examine raw traces (optional)
head runs.jsonl
```

---

## Part 6: Configuration & Customization

### Model Settings:
Edit `src/llm_local.py` to modify:
- **Model**: Change from "llama3" to other Ollama models
- **Temperature**: Currently 0 for deterministic outputs
- **Options**: Add max_tokens, top_p, etc.

### Custom Metrics:
Add new evaluation functions in `src/evals/metrics.py`:
```python
def your_metric(output: str, reference: str) -> float:
    # Your evaluation logic
    return score
```

---

## Part 7: Dashboard Analysis

**Concept**: Comprehensive analysis and visualization of evaluation results.

### What the Dashboard Actually Shows:

From a typical session, you'll see:
- **Expanded model calls** (more calls due to LLM judge evaluation)
- **Performance analysis**: Chain latency comparison including judge calls
- **Multi-dimensional quality**: LLM scores for accuracy, clarity, completeness, conciseness
- **Method comparison**: Rule-based vs LLM judge agreement rates
- **Qualitative insights**: Sample LLM reasoning for evaluation decisions
- **A/B test analysis**: Detailed disagreement cases and confidence scores

### What are Evaluation Dashboards?
- Visual and statistical analysis of model performance
- Historical tracking of metrics over time
- Operational insights for production decisions
- Debugging tools for understanding model behavior

### CLI Dashboard Analysis:

```bash
# Comprehensive analysis of all results
python src/dashboards/summarize_results.py

# Custom analysis with specific files
python src/dashboards/summarize_results.py --results results.jsonl --traces runs.jsonl

# Focus on results only (skip traces)
python src/dashboards/summarize_results.py --no-traces

# Show more example outputs
python src/dashboards/summarize_results.py --examples 5
```

### Dashboard Features:

The CLI dashboard provides:

1. **Evaluation Results Summary**:
   - Dataset size and completion rates
   - Schema compliance percentages
   - Length compliance rates
   - Faithfulness score distribution

2. **Trace Analysis**:
   - Total model calls and average latency
   - Per-chain performance comparison
   - Timeline analysis (duration and call rates)
   - Success rates and error detection

3. **Chain Comparison**:
   - Head-to-head performance metrics
   - Latency and reliability comparison
   - Usage patterns and recommendations

4. **Example Outputs**:
   - Sample inputs and outputs for debugging
   - Latency per call for performance analysis

### Interactive Web Dashboard:

For a modern, interactive web interface, use the Streamlit dashboard:

```bash
# Launch Streamlit dashboard
streamlit run src/dashboards/streamlit_app.py
```

This opens a web browser with an interactive dashboard featuring:

**5 Main Tabs:**
1. **Results Summary**: Key metrics, faithfulness distributions, compliance rates
2. **Performance Analysis**: Latency histograms, timeline charts, performance statistics  
3. **Chain Comparison**: Head-to-head comparisons, usage distribution, violin plots
4. **Output Examples**: Filterable sample inputs/outputs with metadata
5. **Insights & Recommendations**: Auto-generated insights and actionable next steps

**Interactive Features:**
- **Real-time updates** when new data is available
- **Interactive Plotly charts** with zoom, pan, hover details
- **Filterable content** by chain, time range, metrics
- **Export functionality** for sharing reports
- **Professional UI** perfect for stakeholder presentations

### Alternative: Jupyter Analysis:

For detailed data science analysis, use the Jupyter notebook:

```bash
# Install Jupyter if not already installed
pip install jupyter

# Launch Jupyter notebook
jupyter notebook src/dashboards/notebook.ipynb
```

### Key Dashboard Insights:

From typical analysis, you'll see:
- **Performance Winner**: Which chain is faster and more reliable
- **Trade-offs**: Speed vs. quality vs. structure compliance
- **Operational Metrics**: Real latency and throughput data
- **Quality Distribution**: How consistent model outputs are

### Example Dashboard Output:

```
EVALUATION RESULTS SUMMARY
==================================================
Dataset Size: 2 examples
Schema Compliance: 100.0% (2/2)
Length Compliance: 100.0% (2/2)
Faithfulness: 0.583 ± 0.118

CHAIN COMPARISON
==================================================
Chain           Calls    Avg Latency  Success Rate
--------------------------------------------------
summarize_v0    12       1052ms       100.0%      
summarize_v1    34       663ms        100.0%      
```


## Troubleshooting

### Common Issues:
**Ollama connection failed**:
```bash
# Verify Ollama is running
ollama list
# Restart if needed
ollama serve
```

**Trace files growing large**:
```bash
# Check trace file size
ls -lh runs.jsonl
# Archive old traces if needed
mv runs.jsonl runs_backup_$(date +%Y%m%d).jsonl
```

**Evaluation seems slow**:
- Each model call takes ~500-1000ms
- Consider reducing dataset size for testing
- Monitor with: `tail -f runs.jsonl`

---

## Key Takeaways

### Evaluation Hierarchy:
1. **Unit Tests**: Fast, specific, deterministic
2. **Automated Metrics**: Scalable, may miss nuance
3. **A/B Testing**: Realistic, requires volume
4. **Dashboard Analysis**: Comprehensive insights for decisions

### Interpreting Results:
- **Rule-based faithfulness 0.5-0.7**: Good word overlap with reference text
- **Schema 100%**: All outputs follow JSON format correctly  
- **LLM judge scores 3.0-4.0+**: Good to excellent quality (out of 5)
- **Agreement rate >70%**: Strong consistency between evaluation methods
- **Latency considerations**: LLM judge adds ~500-1000ms per evaluation
- **A/B Testing**: Need >10 examples for meaningful comparison

### Trade-offs:
- **Speed vs. Nuance**: Rule-based metrics are fast, LLM judge is slower but more insightful  
- **Cost vs. Quality**: LLM judge requires more model calls but better correlates with human judgment
- **Consistency vs. Flexibility**: Rule-based is deterministic, LLM judge can vary between runs
- **Scale vs. Depth**: Rule-based scales easily, LLM judge provides deeper analysis

### Best Practices:
- **Combine approaches**: Use rule-based for speed, LLM judge for insight
- **Start with LLM judge**: Better correlation with human judgment
- **Monitor agreement**: High disagreement suggests evaluation issues
- **Consider cost**: LLM judge doubles or triples evaluation time
- **Use reasoning**: LLM explanations help debug model issues
- **Validate judge quality**: Ensure LLM judge aligns with your quality standards

---

## Resources

- [Ollama Documentation](https://ollama.ai)
- [LLM Evaluation Best Practices](https://docs.anthropic.com/claude/docs/evals)
- [Statistical Significance in A/B Testing](https://en.wikipedia.org/wiki/A/B_testing)