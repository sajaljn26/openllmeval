# Open LLM Evaluation System

A professional framework for the systematic evaluation of Retrieval-Augmented Generation (RAG) pipelines. This project provides a complete environment to ingest documents, retrieve context, generate responses using high-performance open-source LLMs, and quantify performance using industry-standard metrics.

## 📌 Overview

Evaluating LLMs often suffers from subjectivity. This system replaces qualitative "manual testing" with quantitative metrics. By leveraging **DeepEval**, the system implements an "LLM-as-a-Judge" pattern to provide a mathematical score for the quality of the RAG pipeline.

## 🛠️ Technical Stack

### Core Architecture
- **LLM Inference:** [Groq](https://groq.com/) (Llama-3 / Mixtral) for low-latency, high-throughput generation.
- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2` via HuggingFace for efficient local vectorization.
- **Vector Database:** **FAISS** (Facebook AI Similarity Search) for optimized similarity search.
- **Evaluation Framework:** **DeepEval** for calculating RAG-specific metrics.
- **Frontend:** **Streamlit** for a centralized evaluation dashboard.

### Pipeline Flow
`PDF Document` $\rightarrow$ `Text Extraction (PyMuPDF)` $\rightarrow$ `Embedding Generation` $\rightarrow$ `FAISS Indexing` $\rightarrow$ `Context Retrieval` $\rightarrow$ `Groq LLM Generation` $\rightarrow$ `Metric Scoring (DeepEval)` $\rightarrow$ `Visualization (Streamlit)`

---

## 📊 Evaluation Framework (The "Eval" Suite)

The core of this project is the transition from "vibes-based" testing to **Metric-Driven Development**. The system employs a specialized evaluation suite to pinpoint exactly where a RAG pipeline is failing.

### 1. The Metrics (KPIs)
We measure four critical dimensions to ensure the AI is both honest and useful:

| Metric | Definition | What it Detects |
| :--- | :--- | :--- |
| **Faithfulness** | Checks if the answer is derived *only* from the retrieved context. | **Hallucinations**: Stops the AI from making things up. |
| **Answer Relevancy** | Evaluates how well the answer addresses the user's specific intent. | **Avoidance**: Stops the AI from giving vague or generic answers. |
| **Context Relevancy** | Measures the proportion of retrieved chunks that are actually useful. | **Retrieval Noise**: Identifies if the Vector DB is pulling irrelevant data. |
| **Correctness** | Compares the generated answer against a ground-truth "Golden Dataset". | **Factual Errors**: Ensures the final answer is objectively true. |

### 2. Experimental Design (A/B Testing)
To optimize the system, I conducted multiple evaluation runs (Experiments) to test the impact of the **Retriever $k$ value** (the number of document chunks sent to the LLM):

- **Experiment V1 ($k=1$):** Minimal context. Used as a baseline to identify "under-retrieval" errors.
- **Experiment V2 ($k=3$):** Balanced context. Testing the optimal trade-off between precision and noise.
- **Experiment V3 ($k=5$):** Maximum context. Testing if more information leads to higher correctness or introduces "lost-in-the-middle" effects.

### 3. Failure Analysis
The system logs every case that falls below a **0.7 threshold** into a `failures.jsonl` file. This allows for a "Root Cause Analysis":
- **Low Context Relevancy $\rightarrow$ Low Faithfulness:** The problem is the **Vector Store/Embeddings**.
- **High Context Relevancy $\rightarrow$ Low Faithfulness:** The problem is the **LLM Prompt/Reasoning**.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Groq API Key ([Get one here](https://console.groq.com/))

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/Open-LLM-Evaluation-System.git
   cd Open-LLM-Evaluation-System
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables:
   Create a `.env` file in the root directory:
   ```env
   GROQ_API_KEY=your_api_key_here
   ```

### Execution
1. **Run Evaluations:**
   Generate evaluation results for multiple experiments:
   ```bash
   python run_evaluations.py
   ```
2. **Launch Dashboard:**
   Visualize the metrics and compare runs:
   ```bash
   streamlit run dashboard.py
   ```

---

## 📂 Project Structure

```text
Open_LLM_Eval_System/
├── RAG1/               # Core RAG Pipeline
│   ├── agent.py        # LLM logic and chain orchestration
│   ├── indexing.py      # Embedding and FAISS setup
│   ├── tools.py        # Retrieval tools
│   └── prompts.py      # System prompts for the agent
├── pdfs/               # Source documents for retrieval
├── single_tests/       # Unit tests for individual metrics
├── run_evaluations.py   # Main evaluation runner
├── dashboard.py        # Streamlit visualization app
└── requirements.txt    # Project dependencies
```

## ⚖️ License
Distributed under the MIT License.
