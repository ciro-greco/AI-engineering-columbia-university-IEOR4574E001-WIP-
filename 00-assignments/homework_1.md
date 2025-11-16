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
- As a general rule, you should aim for code that another engineer or a product manager can understand quickly without your presence.

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
    
    # Causal model for generation (Problem 1)
    tok_gpt2 = AutoTokenizer.from_pretrained("distilgpt2")
    model_gpt2 = AutoModelForCausalLM.from_pretrained("distilgpt2")
    
    # Seq2Seq model for fine-tuning (Problem 2)
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

Demonstrate how decoding parameters (temperature, top-k, top-p) affect diversity, repetition, and structure. Then, improve reliability with a schema-constrained prompt.

### Model

`distilgpt2` from Hugging Face.

### Instructions

1. Load model and tokenizer.
2. Use the this as a base prompt:
    
    ```
    You are given a purchase request. Extract a JSON object with fields item and quantity.
    Text: "Order three boxes of blue markers for the design team."
    JSON:
    
    ```
    
3. Generate **10 samples** for each decoding setup:
    - Greedy: temperature=0
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


## Problem 2. Supervised Fine-Tuning (Instruction Tuning) (60%)

### Goal

Fine-tune an instruction model (`google/flan-t5-small`) on a small synthetic dataset and compare zero-shot vs fine-tuned performance.

### Model rationale

`flan-t5-small` (≈80M parameters) is CPU-friendly, pre-instruction-tuned, and works in a text-to-text format, ideal for supervised fine-tuning demonstrations.

### Instructions

1. **Create two simple tasks in code:**
    - **Task A – Sentiment classification:** map product reviews to `very_negative`, `negative`, `neutral`, `positive`, `very_positive`.
    - **Task B – Information extraction:** given an order sentence, output JSON with `item` and `quantity`.
        
    Generate ~200 training and 60 evaluation examples (split across both tasks).
        
    **Dataset Generation Principles:**
    - Create examples that require nuanced understanding, not just keyword matching
    - For sentiment: vary intensity markers (e.g., "good" vs "excellent" vs "perfect")
    - Include subtle distinctions between adjacent classes (e.g., negative vs very_negative)
    - Ensure balanced distribution across all classes
    - Avoid overly obvious examples that rely solely on extreme language

Note: Task A will likely show refinement (moderate baseline → better), while task B may show format learning (near-zero baseline → working).
 
2. **Format each record** as:
    
    ```
    Input: "Classify sentiment into very_negative, negative, neutral, positive, or very_positive. Review: 'battery died in two days.' Label:"
    Target: "negative"
    
    ```
    
    or
    
    ```
    Input: "Extract JSON with fields item (string) and quantity (integer). Text: 'Order three blue markers for design.' JSON:"
    Target: '{"item": "blue markers", "quantity": 3}'
    
    ```
    
3. **Baseline evaluation (before fine-tuning):**
    - Load `flan-t5-small`.
    - Generate predictions on the eval set.
    - Score:
        - Task A: exact match on labels.
        - Task B: JSON validity and field-level accuracy.

4. **Fine-tuning configuration and trainer setup:**
- Use the Hugging Face `Trainer` API.
- Tokenize with `max_length=128` for inputs and `max_length=48` for targets.
- Use **CPU-only training** (`no_cuda=True`) to ensure all students run on comparable hardware.
- Configure the trainer so that the *best checkpoint* is saved and restored automatically.
- Use the correct data collator for seq2seq models:
    
    ```
    from transformers import DataCollatorForSeq2Seq
    data_collator = DataCollatorForSeq2Seq(tokenizer=tok_t5, model=model_t5)
    ```
    
- Start from the following training configuration:

      ```python
      learning_rate=5e-5             # Standard fine-tuning rate (lower than pretraining to preserve knowledge)
      num_train_epochs=1             # but it is likely that multiple epochs will be needed for format learning in Task B
      per_device_train_batch_size=8
      gradient_accumulation_steps=2  # Effective batch size: 16 (balance memory vs stability)
      weight_decay=0.01              # Light regularization to prevent overfitting
      logging_steps=25

      # Trainer best-checkpoint selection
      evaluation_strategy="epoch"
      save_strategy="epoch"
      load_best_model_at_end=True
      metric_for_best_model="eval_accuracy"
      greater_is_better=True
      no_cuda=True                  # Ensures consistent runtime across different hardware

      # You must define a compute_metrics function and pass it to Trainer.
      # It should return a dict with a key "eval_accuracy", computed as exact-match
      # accuracy between the model's *generated* text and the target labels.
      # Hint:
      # - Use `predict_with_generate=True` in TrainingArguments so `eval_pred[0]`
      #   are generated token IDs.
      # - In compute_metrics(eval_pred), decode predictions and labels with the
      #   tokenizer, then compute the fraction of examples where prediction == label.

      ```

**IMPORTANT HINTS**: 
- When defining compute_metrics, do not use the raw logits. Decode the generated predictions into text and compare them to the ground-truth targets to produce eval_accuracy.
- If the Tasks show little or no improvement after 1 epoch, this might indicate the model needs more training signal. In this case, try:
  - Increasing `learning_rate` to `1e-4` or `5e-4`
  - Extending to `num_train_epochs` to `3` or `5`


5. **Evaluate after training:**
- Reload the best checkpoint.
- Repeat the same evaluation.
- Print a small table:
     
    | Task | Metric        | Before SFT | After SFT |
    |------|---------------|------------|-----------|
    | A    | Accuracy      |            |           |
    | B    | JSON validity |            |           |
    | B    | Field match   |            |           |

6. **Save artifacts:**
    - Save the fine-tuned model in `./sft_model/`.
    - Print total training time and parameter count.

7. **Comment block at the end (8–10 lines):**
    - Describe where SFT improved or failed.
    - Explain why instruction tuning helps with task formatting and schema alignment.
    - Ground your explanation in the *pretraining → SFT → preference optimization* phases discussed in lecture.
