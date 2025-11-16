# AI Engineering Apps - IEOR 4574E001
## Columbia University

Teaching materials and code from Columbia University's _AI Engineering_Apps_ course (2025 edition).
Instructor: Ciro Greco 
contact: cg3631@columbia.edu

## Course Overview

An applied overview of Artificial Intelligence (AI) with an emphasis on real-world industry use cases, deployment practices and tool chain. The course focuses one merging paradigms of LLM-powered applications involving prompt-engineering, fine-tuning and evaluation.

This course provides and introduction and hands-on experience with modern AI engineering practices, focusing on large language models (LLMs), their implementation and evaluation. Students will work with real models and learn practical techniques used in industry. 

The internet is full of very good learning materials about AI and machine learning. What's ussually hard to find is real-world case studies from practitioners who build AI systems daily and that's what we hope to bring with this course.

### Main themes

The course is structured around 7 weeks: 6 weeks of lectures and hands-on labs, and 1 final demo day for students (organized in teams) to present an end-to-end AI engineering project that showcases what they learned in the course. Main topics, roughly in order of appearance:

* Introduction to AI engineering: the shift from model-centric to application-centric AI development.
* Understanding LLMs: capabilities, limitations, and the transformer revolution.
* LLM APIs and LLMOps: working with commercial and open-source models, deployment patterns.
* Prompt engineering and evaluation: systematic approaches to prompt design and testing.
* Fine-tuning: when and how to adapt models to specific domains (maybe). 
* RAG and Agents: building intelligent systems with retrieval and tool use.
* Data practices: data versioning, management and data pipelines.
* Team project: building a functional AI-powered MVP from concept to deployment.

**Important Note:** While these materials offer valuable insights, they can't replace the dynamic classroom experience where real learning happens through discussion, collaboration, and direct mentorship. The AI field moves fast, so this course is going to be updated periodically to reflect the latest developments. We can't replicate the energy of live sessions, but we hope the community will find value in the choices we've made. Want the full experience? Consider joining the Columbia program directly.


## Course Information

Title: AI Engineering Apps

Term: 7 Weeks

Hours: 18

## Requirements

Prerequisites: undergraduate-level understanding of probability, linear algebra, and Python programming.

### Good News: Everything Runs Locally! ✅

All course materials are designed to be **laptop-friendly**. You do NOT need:
- ❌ Expensive GPU hardware
- ❌ Cloud computing credits
- ❌ Google Colab (optional, not required)

All notebooks use intentionally small models (e.g. TinyLlama instead of GPT-3/4) to ensure accessibility for all students.
**NOTE** You will have to have a github account for the capstone - see [the README in the first week materials](01-introduction-and-setup%2FREADME.md).

**Week 1: Environment Setup**
1. **Set up GitHub account** for assignment submissions
2. **Install Python & Git** following the [Week 1 README](week-1/README.md)
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

# Install requirements
pip install -r requirements.txt

# Test your setup
python 01-introduction-and-setup/test_setup.py
```

## Course Schedule

| Lesson | Title | Date & Time                         |
|--------|-------|-------------------------------------|
| Lesson 1 | Introduction to AI engineering | October 31st, 3pm - 5:30pm          |
| Lesson 2 | Introduction to LLMs | Friday November 06, 3pm - 5:30pm    |
| Lesson 3 | LLMs APIs and LLMOps | Friday November 14, 3pm - 5:30pm    |
| Lesson 4 | Prompt engineering and Evaluation | Friday November 21, 3pm - 5:30pm    |
| Lesson 5 | Finetuning (TBD) | Saturday November 22, 11am - 1:30pm |
| Lesson 6 | RAG and Agents* | Friday December 5, 3pm - 5:30pm     |
| Lesson 7 | Demo Day (Final class)** | Saturday December 6, 11am - 1:30pm  |

\* *Guest speakers: Jacopo Tagliabue and Simon Gelinas*  
\** *Live team demos & presentations (presentation length determined by final number of teams)*

## Assessments & Grading

**Summary of graded components**

- **Two individual take‑home assignments — 25% each**
    - Format: take‑home; scope and deliverables provided with each assignment brief
    - Submission: via Courseworks by the posted deadline - please add your final submission also to your github account
- **Team Project — 50% (total)**
    - See “Team Project (Capstone)” below for details and expectations

> There is no sit‑down midterm or final exam. Mastery is evaluated through the take‑home assignments and the team project.


## Team Project (Capstone)

**Goal**

Design and build a small but functional AI application. For example, a RAG system, a co‑pilot/assistant, or similar. 
Choose a real problem and treat this as an MVP for a startup‑quality idea or a project that you are submitting to your product or engineering team. 
The domain is entirely up to you. The project will have to be submitted as a Github Repository.

**Team formation**

- Teams will be formed in class: **minimum 3 maximum 5** per team.

**Project selection & proposal**

- Each team will **select and scope** its project **within the first three weeks**.
- **Proposal due:** End of Week 3 (exact date/time posted in class). Suggested contents (1–2 pages): problem statement, intended users, and an initial indication of the MVP features.

**Demo Day**

- Live demo + presentation. **Presentation time will depend on the total number of teams.**
- Every team member is encouraged to participate in the presentation and/or the live demo.

**Final deliverables (submitted before Demo Day)**

- **Working prototype** (repository or deployed app with a comprehensive README).
- **Short product brief** (≈2 pages) describing the problem, approach, system architecture, and what you learned.
- **Demo video** (e.g., 3–5 minute screencast) in case of live‑demo issues.
- **Technical appendix** (optional but encouraged): model/card, data sources, prompt strategies, evaluation metrics, and key engineering decisions.

**Project grading rubric (adds up to 50% of course grade)**

- **Functionality & Reliability (30%)** — Does the MVP actually solve the stated task? Is it robust enough to demo?
- **Technical Approach & Rigor (30%)** — Sound choices of models/APIs, data handling, retrieval/grounding, prompt design, and evaluation.
- **Product Thinking & UX (20%)** — Clear user story, scoping, and an experience that makes sense for the target user.
- **Communication & Teamwork (%)** — Clear proposal, demo, and write‑up, equitable collaboration and role clarity.
- 
