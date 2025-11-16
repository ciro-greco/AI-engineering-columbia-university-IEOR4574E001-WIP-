# Homework 1: Language Modeling and Supervised Fine-Tuning

This homework extends what you learned in Weeks 1 and 2 about how language models represent, generate, and adapt language.

You will explore decoding behavior in a pretrained language model and fine-tune an instruction-following model on a small supervised dataset.

## Submission format

For grading consistency, follow these exact rules:

1. Submit two Python scripts with your UNI in as part of the naming convention:
    
    ```
    <your_UNI>_question_1.py
    <your_UNI>_question_2.py
    ```
    
2. Include a `requirements.txt` file with the dependencies you used.
3. Each script must run from the command line exactly like:
    
    ```bash
    python cg3631_question_1.py
    ```
    
    Your grader will execute from the same directory where this document is located.
    
4. Submit well-commented, readable code.
- Your scripts must include clear, concise comments that explain what each major block does and why.
- Comments should clarify reasoning, assumptions, or equations, **not restate code line-by-line**. Remove only irrelevant clutter such as unused code or commented-out experiments.
- You genera rule should be aim for code that another engineer or a product manager can understand quickly without your presence.

### Recommended `requirements.txt`

```
numpy==1.26.4
pandas==2.2.2
torch==2.4.1
transformers==4.44.2
tqdm==4.66.5
accelerate==0.34.2
sentencepiece==0.2.0
```

### Working with Hugging Face Models

The open-source **Hugging Face Transformers** library lets you download and use pretrained models with a few lines of code.

All models used in this homework (`distilgpt2` and `google/flan-t5-small`) are publicly available and do **not** require an account or API key.

1. **Install the library**
    
    ```bash
    pip install transformers torch
    ```
    
2. **Load a model and tokenizer**
    
    The *tokenizer* converts text to model tokens, and the *model* generates or scores text.
    
    ```python
    from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM
    
    # Causal model for generation (Problem 2)
    tok_gpt2 = AutoTokenizer.from_pretrained("distilgpt2")
    model_gpt2 = AutoModelForCausalLM.from_pretrained("distilgpt2")
    
    # Seq2Seq model for fine-tuning (Problem 3)
    tok_t5 = AutoTokenizer.from_pretrained("google/flan-t5-small")
    model_t5 = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")
    
    ```
    
3. **Automatic download and caching**
    - The first time these commands run, the library downloads the weights (≈300 MB each) to
        
        `~/.cache/huggingface/transformers/`.
        
    - Future runs load the model from that local cache; no repeated downloads.
    - If you work on shared machines, each user gets their own cache.
4. **Offline use**
    
    After the first download, models can be used offline. If your environment blocks internet access, a TA can pre-download them and copy the cache folder to your machine.
    

## Problem 1. Decoding Controls and Structured Output (40%)

### Goal

Demonstrate how decoding parameters (temperature, top-k, top-p) affect diversity, repetition, and structure. Then improve reliability with a schema-constrained prompt.

### Model

`distilgpt2` from Hugging Face.

### Instructions

1. Load model and tokenizer.
2. Use the fixed base prompt:
    
    ```
    You are given a purchase request. Extract a JSON object with fields item and quantity.
    Text: "Order three boxes of blue markers for the design team."
    JSON:
    
    ```
    
3. Generate **10 samples** for each decoding setup:
    - Greedy: temperature=0.1
    - Temperature: {0.7, 1.0}
    - Top-k: {40, 200} with temperature=0.7
    - Top-p: {0.8, 0.95} with temperature=0.7
4. For each configuration, compute:
    - `distinct-1` and `distinct-2` (unique unigrams/bigrams)
    - Mean output length
    - Repetition rate (fraction of adjacent identical tokens)
    - JSON validity rate (fraction that parses correctly and has both `item` and `quantity` fields)
5. Repeat the same generation loop with an explicit schema prompt:
    
    ```
    Output must be valid JSON exactly: {"item": "<string>", "quantity": <integer>}. No commentary.
    
    ```
    
6. Compare validity before and after the schema prompt.
7. Print a concise table summarizing all metrics.
8. Add a short comment block (6–10 lines) explaining:
    - Which decoding controls increased diversity or drift.
    - How the schema prompt affected validity.
    - One improvement you would test next (e.g. constrained decoding or post-validation).

### Runtime notes

- Use `max_new_tokens=60`.
- Use a fixed random seed for reproducibility.

### Grading

| Component | Points |
| --- | --- |
| Correct decoding parameter sweeps | 15 |
| Diversity and repetition metrics | 10 |
| JSON validity and schema comparison | 10 |
| Interpretation and commentary | 5 |

---

## Problem 2. Supervised Fine-Tuning (Instruction Tuning) (60%)

### Goal

Fine-tune an instruction model (`google/flan-t5-small`) on a small synthetic dataset and compare zero-shot vs fine-tuned performance.

### Model rationale

`flan-t5-small` (≈80M parameters) is CPU-friendly, pre-instruction-tuned, and works in a text-to-text format, ideal for supervised fine-tuning demonstrations.

### Instructions

1. **Create two simple tasks in code:**
    - **Task A – Sentiment classification:** map product reviews to `positive` or `negative`.
    - **Task B – Information extraction:** given an order sentence, output JSON with `item` and `quantity`.
        
        Generate ~200 training and 60 evaluation examples (split across both tasks).
        
2. **Format each record** as:
    
    ```
    Input: "Classify sentiment as positive or negative. Review: 'battery died in two days.' Label:"
    Target: "negative"
    
    ```
    
    or
    
    ```
    Input: "Extract JSON with fields item (string) and quantity (integer). Text: 'Order three blue markers for design.' JSON:"
    Target: {"item": "blue markers", "quantity": 3}
    
    ```
    
3. **Baseline evaluation (before fine-tuning):**
    - Load `flan-t5-small`.
    - Generate predictions on the eval set.
    - Score:
        - Task A: exact match on labels.
        - Task B: JSON validity and field-level accuracy.
4. **Fine-tuning configuration:**
    - Tokenize with `max_length=128` for inputs, `max_length=48` for targets.
    - Use the Hugging Face `Trainer` API.
    - Suggested hyperparameters:
        
        ```
        learning_rate=5e-4
        num_train_epochs=1
        per_device_train_batch_size=4
        gradient_accumulation_steps=4
        weight_decay=0.0
        logging_steps=50
        save_total_limit=1
        max_steps=300  # optional cap
        
        ```
        
    - Train on CPU only.
5. **Evaluate after training:**
    - Reload the best checkpoint.
    - Repeat the same evaluation.
    - Print a small table:
        
        
        | Task | Metric | Before SFT | After SFT |
        | --- | --- | --- | --- |
        | A | Accuracy |  |  |
        | B | JSON validity |  |  |
        | B | Field match |  |  |
6. **Save artifacts:**
    - Save the fine-tuned model in `./sft_model/`.
    - Print total training time and parameter count.
7. **Comment block at the end (8–10 lines):**
    - Describe where SFT improved or failed.
    - Explain why instruction tuning helps with task formatting and schema alignment.
    - Ground your explanation in the *pretraining → SFT → preference optimization* phases discussed in lecture.
