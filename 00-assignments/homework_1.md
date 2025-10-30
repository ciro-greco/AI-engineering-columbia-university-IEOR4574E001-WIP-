# Homework 2

For each problem, submit a Python script (`question_1.py`, `question_2.py`, etc.). These scripts must use only standard Python or libraries listed in `requirements.txt`. The grader should be able to install the libraries and run:

```bash
python question_1.py
```

You may assume they execute the script from the folder containing this assignment.

**Also:** Clean up your code before submission. Remove extraneous commented-out code or notebook cell markers. Clear, readable code is expected.

## Problem 1: LLM Prompting & Retrieval (30%)

In this problem you will simulate a retrieval-augmented generation (RAG) setup inspired by the content in Week 1 (LLM foundations) and Week 2 (retrieval + prompt design).

Your script should:

1. Read a plain-text corpus file `data/corpus.txt` (each paragraph separated by a blank line).

2. Build a simple text index: tokenize paragraphs, compute TF-IDF vectors using `sklearn.feature_extraction.text.TfidfVectorizer`.

3. Given a query string (hard-coded in your script, e.g., "What deployment challenges should I anticipate for an LLM?"), find the top 3 paragraphs most relevant (highest cosine similarity) from the corpus.

4. Construct a prompt to a hypothetical LLM: include the retrieved paragraphs and the query, and print the full prompt to screen.

5. In commented code at the bottom: discuss which retrieved paragraphs were most/least helpful and why (e.g., coverage of topic, sentence clarity).

**Goal:** demonstrate your understanding of retrieval + prompt construction.

## Problem 2: Fine-Tuning & Versioning Workflow (70%)

In this problem you will simulate the workflow introduced in Week 2: fine-tuning (or adapt-tuning) a model, versioning it, and evaluating on a held-out set.

Your script should:

1. Read in a CSV file `data/fine_tune_data.csv` with columns: `input_prompt`, `target_response`.

2. Split into training (80%) and test (20%) sets (use sklearn's `train_test_split`, `random_state=42`).

3. Use transformers (HuggingFace) to load a small pretrained model (e.g., `distilgpt2`) and tokenizer. Fine-tune it on the training set for 1 epoch, saving the fine-tuned checkpoint in `output/checkpoint‐ft`.

4. Load the fine-tuned model from the checkpoint, generate responses on the test set (use e.g. greedy decoding, `max_length=50`).

5. Compute and print a simple accuracy metric: the fraction of cases where the generated response exactly matches the `target_response`.

6. Use `gitpython` or equivalent to simulate versioning: commit the fine-tuned model directory, print the commit hash. (You don't need to push to a remote.)

7. In commented code at the bottom: reflect on when you'd branch for controlled experiments, how you'd roll back, and how this workflow maps to production data/AI engineering.

**Goal:** tie model fine-tuning + versioning + evaluation into a coherent workflow.

## Submission Instructions

- Submit `question_1.py` and `question_2.py`.
- Ensure your `requirements.txt` includes all non-standard libraries you used (e.g., `transformers`, `gitpython`, `sklearn`).
- Include a short `README.md` noting how to install dependencies and run your scripts.