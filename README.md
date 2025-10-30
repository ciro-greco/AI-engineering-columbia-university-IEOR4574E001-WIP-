# AI Engineering - IEOR 4574E001
## Columbia University

Teaching materials and code from Columbia University's _AI Engineering_ course (2025 edition).

## 📚 Course Overview

This course provides hands-on experience with modern AI engineering practices, focusing on large language models (LLMs), their implementation, optimization, and deployment. Students will work with real models and learn practical techniques used in industry.

## 💻 Hardware Requirements

### Good News: Everything Runs Locally! ✅

All course materials are designed to be **laptop-friendly**. You do NOT need:
- ❌ Expensive GPU hardware
- ❌ Cloud computing credits
- ❌ Google Colab (optional, not required)

### Minimum Requirements
- **RAM**: 8GB (16GB recommended)
- **Storage**: 10GB free space
- **OS**: Windows, macOS, or Linux
- **Python**: 3.8 or higher

### What You'll Be Running
| Week | Content | Model Size | RAM Usage |
|------|---------|------------|-----------|
| Week 2 | Language Models, Seq2Seq | GPT-2, BERT-base | 2-4GB |
| Week 3 | Sampling, LLMOps | TinyLlama-1.1B | 3-4GB |
| Week 4+ | Various projects | Small models | 4-8GB |

All notebooks use intentionally small models (TinyLlama instead of GPT-3/4) to ensure accessibility for all students.

## 🚀 Getting Started

### Week 1: Environment Setup
1. **Set up GitHub account** for assignment submissions
2. **Install Python & Git** following the [Week 1 README](01-introduction_and_setup/README.md)
3. **Create your private repository** for assignments
4. **Test your setup** with the provided test script

### Quick Start
```bash
# Clone this repository
git clone https://github.com/ciro-greco/AI-engineering-IEOR4574E001.git
cd AI-engineering-IEOR4574E001

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install all requirements (includes all course dependencies)
pip install -r requirements.txt

# Test your setup
python 01-introduction_and_setup/test_setup.py
```

## 📁 Repository Structure

```
AI-engineering-IEOR4574E001/
├── week-1/           # Environment setup & prerequisites
├── week-2/           # Language models fundamentals
│   ├── week_2_language_models.ipynb
│   └── week2_seq2seq.ipynb
├── week-3/           # Sampling & LLMOps
│   ├── Week_3_Sampling.ipynb
│   ├── week3_LLMOPS_main_concepts.ipynb
│   └── week_3_LLMOPs_API_Playground.ipynb
├── week-4/           # (Coming soon)
└── ...
```

## What's This Repository?

**Important Note:** While these materials offer valuable insights, they can't replace the dynamic classroom experience where real learning happens through discussion, collaboration, and direct mentorship. The AI field moves fast—this course is updated annually to reflect the latest developments. Want the full experience? Consider joining the Columbia program directly!

**In Brief:** We're sharing lecture materials from Columbia's 2025 AI Engineering course—a hands-on journey into building LLM-powered applications with production-ready tools and deployment strategies.

### Why We're Sharing This

After each course completion, we release our materials to support the wider AI community. We recognize that while these static resources are valuable, they're just a starting point—nothing replaces the interactive learning environment of an actual classroom.

### Our Teaching Philosophy

The internet is already full of AI theory and mathematical proofs. What's harder to find? Real-world wisdom from practitioners who build AI systems daily. That's what we bring to the table—battle-tested insights you won't find in textbooks.

Our approach is refreshingly practical. We focus on _building things that work_ using professional-grade tools. You'll learn solid engineering practices, effective prompt design, robust evaluation methods, and production deployment patterns. Yes, we'll touch on theory when needed, but only enough to understand what we're building.

### What to Expect

Seven intense weeks of content that could occupy you for much longer. Each lesson represents countless decisions about what to include and what to skip. Every lab, every example reflects our best judgment about what matters most in AI engineering today. We can't replicate the energy of live sessions, but we trust the community will find value in the choices we've made.

## At a glance

### Main themes

The course is structured around 7 weeks: 6 weeks of lectures and hands-on labs, and 1 final demo day for students (organized in teams) to present an end-to-end AI engineering project that showcases what they learned in the course. Main topics, roughly in order of appearance:

* Introduction to AI engineering: the shift from model-centric to application-centric AI development.
* Understanding LLMs: capabilities, limitations, and the transformer revolution.
* LLM APIs and LLMOps: working with commercial and open-source models, deployment patterns.
* Prompt engineering and evaluation: systematic approaches to prompt design and testing.
* Fine-tuning: when and how to adapt models to specific domains.
* RAG and Agents: building intelligent systems with retrieval and tool use.
* Best practices: versioning, monitoring, and maintaining AI applications in production.
* Team project: building a functional AI-powered MVP from concept to deployment.

## Course Information

Title: AI engineering

Term: 7 Weeks

Hours: 18

## Description:

An applied overview of Artificial Intelligence (AI) with an emphasis on real-world industry use cases, deployment practices and cloud tool chain. The course focuses one merging paradigms of LLM-powered applications involving prompt-engineering, fine-tuning andevaluation.

Prerequisites: undergraduate-level understanding of probability, linear algebra, and Python programming.

## Course Goals:

This course will equip students with the skills necessary to:

- Design and build AI-powered applications.
- Understand AI project lifecycle following software engineering principles.
- Navigate the AI tool landscape to make informed architectural decisions.

## Course Schedule

- **Lesson 1:** *Introduction to AI engineering*
- **Lesson 2:** *Introduction to LLMs*
- **Lesson 3:** *LLMs APIs and LLMOps*
- **Lesson 4:** *Prompt engineering and Evaluation*
- **Lesson 5:** *Finetuning*
- **Lesson 6:** *Rag and Agents*
- **Lesson 7 (Final class):** *Demo Day* — live team demos & presentations (presentation length determined by final number of teams)

## Assessments & Grading

**Summary of graded components**

- **Two individual take‑home assignments — 25% each**
    - Format: take‑home; scope and deliverables provided with each assignment brief
    - Submission: via Courseworks/Gradescope (TBD) by the posted deadline
- **Team Project — 50% (total)**
    - See “Team Project (Capstone)” below for details and expectations

> There is no sit‑down midterm or final exam. Mastery is evaluated through the take‑home assignments and the team project.
> 

## Team Project (Capstone)

**Goal**

Design and build a small but functional AI application. For example, a RAG system, a co‑pilot/assistant, or similar. Choose a real problem and treat this as an MVP for a startup‑quality  idea. The domain is entirely up to you. The project will have to be submitted as a Github Repository.

**Team formation**

- Teams will be formed in class: **minimum 4, maximum 7 students** per team.

**Project selection & proposal**

- Each team will **select and scope** its project **within the first two weeks**.
- **Proposal due:** End of Week 2 (exact date/time posted in class). Suggested contents (1–2 pages): problem statement & users, MVP features, data/source plan, model(s)/APIs, evaluation plan, risk/mitigation, timeline & roles.

**Demo Day**

- Live demo + presentation. **Presentation time will depend on the total number of teams.**
- Every team member should participate in the presentation and/or live demo.

**Final deliverables (submitted before Demo Day)**

- **Working prototype** (repository or deployed app)
- **Short product brief** (≈2 pages) describing the problem, approach, system architecture, and what you learned
- **Demo artifact** (e.g., 3–5 minute screencast) in case of live‑demo issues
- **Technical appendix** (optional but encouraged): model/card, data sources, prompt strategies, evaluation metrics, and key engineering decisions

**Project grading rubric (adds up to 50% of course grade)**

- **Functionality & Reliability (30%)** — Does the MVP actually solve the stated task? Is it robust enough to demo?
- **Technical Approach & Rigor (30%)** — Sound choices of models/APIs, data handling, retrieval/grounding, prompt design, and evaluation.
- **Product Thinking & UX (20%)** — Clear user story, scoping, and an experience that makes sense for the target user.
- **Communication & Teamwork (%)** — Clear proposal, demo, and write‑up; equitable collaboration and role clarity.